import logging
import marshal
import os
import reprlib

from ctypes import Structure, c_bool, c_int32, c_int64, c_ssize_t
from multiprocessing import Lock, RawValue, RawArray
from multiprocessing.shared_memory import SharedMemory
from time import time, time_ns


_logger = logging.getLogger(__name__)


class LockIdentify:
    """
    Lock where the pid process is save into a Shared Value after that the process acquires the lock.
    It is to be able to release the lock from a other Process (parent process) when the process
    is killed (the Lock is not release automatically in that case).
    """
    def __init__(self) -> None:
        self._lock = Lock()
        self._pid = RawValue(c_int64, -1)  # Shared Value to save the pid of the current process using Lock
        self._last_exit = RawValue(c_int64, time_ns())  # Last usage of the lock (timestamp)

    def __enter__(self):
        # TODO: Maybe we should make the pid a lazy property + hook before fork
        pid = os.getpid() # Make the call before to minimize the Critical Spot

        # CRITICAL SPOT: if the process is killed after the acquire
        # but before set the pid, the _lock is locked without knowing
        # which one take it, then the PreforkServer cannot release it.
        # See `force_release_if_mandatory` where there is a partial solution to this
        self._lock.acquire()
        self._pid.value = pid

    def __exit__(self, exc_type, exc_val, exc_tb):
        # CRITICAL SPOT: if the process is killed after reset the pid
        # but before release, the _lock is locked without knowing
        # which one take it, then the PreforkServer cannot release it.
        # See `force_release_if_mandatory` where there is a partial solution to this
        self._last_exit.value = time_ns()
        self._pid.value = -1
        try:
            self._lock.release()
        except ValueError:
            # One a worst case of the worst case, if we have a ValueError ("release" a already released lock), it seems
            # that none other process has used the lock between (or it already finished)
            _logger.error("One process has release the lock when it was used.")
            raise Exception("One process has release the lock when it was used.")

    def force_release_if_mandatory(self, pid: int):
        """Release the lock if it is locked by the killed process with `pid`

        :param int pid: pid of a killed (mandatory) process
        """
        # TODO: it still not a complete safe solution (IMO, there isn't any a complete solution)
        have_lock = self._lock.acquire(block=False)
        # Read _pid outside locking section seems "wrong", but we only use it to compare equality,
        # then the change to get a bad value and take the wrong decision is very "small" (or "inexistant", not sure)
        if not have_lock and self._pid.value == pid:
            _logger.info("Force the release of SM lock for pid=%s", pid)
            self._pid.value = -1
            self._lock.release()
        elif not have_lock and self._pid.value == -1:
            old_last_exit = self._last_exit.value
            # After 50 msec, if we cannot still acquire and the _last_exit didn't change
            # We consider into the first worst case, one process take the lock without write
            # his pid (or after clean it). Then we let the process 50 msec to set or reset
            # the `self._pid` after/before acquire/release) after that we consider the process dead
            # (which can be False with the CPU high and the process didn't get a round trip on it => TODO: what can we do ? )
            have_lock = self._lock.acquire(timeout=0.05)
            if not have_lock and old_last_exit == self._last_exit.value and self._pid.value == -1:
                _logger.warning("Force the release of SM lock but there wasn't pid attach to the lock")
                self._lock.release()
            elif have_lock:
                self._lock.release()
        elif have_lock:
            self._lock.release()

class _Entry(Structure):
    """
    Hash LRU Table entry structure
    """
    _fields_ = [
        ("hash", c_ssize_t),
        ("prev", c_int32),
        ("next", c_int32),
    ]

    def __str__(self) -> str:
        return f"hash={self.hash}, prev={self.prev}, next={self.next}"
    __repr__ = __str__

class _DataIndex(Structure):
    _fields_ = [
        ("position", c_int64),
        ("size", c_int64),  # TODO: maybe `end` instead, to avoid useless concat
    ]

    def __str__(self) -> str:
        return f"position={self.position}, size={self.size}"
    __repr__ = __str__

class SharedMemoryLRU:

    # byte size allocate for each entry for data (key, value). A data entry can still take more space
    # but this value should match as most as possible the average size of data entry to avoid
    # losing too much memory (if too high) or losing too much number entries (if too low)
    AVG_SIZE_OF_DATA = 4000
    USABLE_FRACTION = 2 / 3 # USABLE_FRACTION is the maximum sm lru load (same than python dict)

    def __init__(self, size: int):
        """ Init a Shared Memory which acts as a dict with a lru.

        :param int size: number of entry in the hash table should be > 2
        """
        byte_size = size * self.AVG_SIZE_OF_DATA
        _logger.debug("Create Shared Memory of %d bytes", byte_size)

        # The lock to ensure that only one process access to critical section in the time
        self._lock = LockIdentify()
        # The Raw Shared Memory, will contain only data (key, value)
        self._sm = SharedMemory(size=byte_size, create=True)

        self._size = size

        # We cannot take more that 10 % of memory with one data (TODO ?)
        self._max_size_one_data = byte_size // 10
        # `self._max_length` should be always < than size.
        # bigger it is, more there are hash conflict, and then slow down the `_lookup` but decrease the memory cost
        self._max_length = int(size * self.USABLE_FRACTION)

        # Allow to know if the Shared Memory is corrupted (`_check_consistence`)
        self._consistent = RawValue(c_bool, True)
        # root, length, free_len (see property below)
        self._head = RawArray(c_int32, [-1, 0, 1])
        # Hash and the linked list information for each entry index
        self._entry_table = RawArray(_Entry, [(0, -1, -1)] * size)
        # Position info of data for each entry index
        self._data_idx = RawArray(_DataIndex, [(-1, -1)] * size)
        # Position info of free memory blocks
        self._data_free = RawArray(_DataIndex, [(-1, -1)] * size)
        # Number of free memory block (max == size)
        self._data_free[0] = (0, self._sm.size)
        # Buffer of shared memory for data (key/value)
        self._data = self._sm.buf

    _root = property(lambda self: self._head[0], lambda self, x: self._head.__setitem__(0, x))
    _length = property(lambda self: self._head[1], lambda self, x: self._head.__setitem__(1, x))
    _free_len = property(lambda self: self._head[2], lambda self, x: self._head.__setitem__(2, x))

    def hook_process_killed(self, pid):
        self._lock.force_release_if_mandatory(pid)

    def _check_consistence(self):
        """ Check that the last change of the SharedMemory was consistent

        ! Need lock !
        """
        if not self._consistent.value:
            _logger.info("Shared Memory not consistent, clean it")
            self._head[:] = [-1, 0, 1]
            self._entry_table[:] = [(0, -1, -1)] * self._size
            self._data_idx[:] = [(-1, -1)] * self._size
            self._data_free[0] = (0, self._sm.size)
            self._consistent.value = True

    def _defrag(self):
        """
        Defragment the `self._data`, it will result only one block of free fragment.
        The `self._entry_table` should be already update to avoid defragment

        O(log(n) * n), n is `self._max_length` (due to `sorted`)

        ! Need lock !
        """
        _logger.debug("Defragment the shared memory, nb fragment = %d", self._free_len)
        s = time()
        # Filtered out unused index and sorted by position to ensure that the defragmentation won't override any data
        current_position = 0
        used_indices = filter(lambda i: self._entry_table[i].prev != -1 and self._data_idx[i].position != -1, range(self._size))
        sorted_indexes = sorted(used_indices, key=lambda i: self._data_idx[i].position)
        for i in sorted_indexes:
            data_entry = self._data_idx[i]
            self._data[current_position:current_position + data_entry.size] = self._data[data_entry.position:data_entry.position + data_entry.size]
            data_entry.position = current_position
            current_position += data_entry.size
        self._data_free[0] = (current_position, self._sm.size - current_position)
        self._free_len = 1
        _logger.debug("Defragment the shared memory in %.4f ms, remaining free space : %s", (time() - s), self._data_free[0])

    def _malloc(self, data):
        """
        Reserved a free slot of shared memory for the root entry,
        insert data into and keep track of this spot.
        If there isn't enough memory, pop min(10% of entry, enough for this data) and _defrag

        ! Need lock !

        :param bytes data: (key, value) marshalled
        """
        size = len(data)
        nb_free_byte = 0
        for i in range(self._free_len):
            data_free_entry = self._data_free[i]
            if data_free_entry.size >= size:
                break
            nb_free_byte += data_free_entry.size
        else:
            if nb_free_byte < size:
                # If nb_free_byte isn't enough,
                # We pop existing data until we have enough memory
                for i in range(self._length):
                    if nb_free_byte >= size and i > self._length // 10:
                        # At minimum remove 10% of the memory to avoid to many defrag when memory is the bottleneck
                        break
                    nb_free_byte += self._lru_pop()
                else:
                    raise MemoryError("Your max_size_one_data is > size_byte, it shouldn't happen")
                _logger.debug("Pop %s items to be handle to add the new item", i + 1)

            self._defrag()
            data_free_entry = self._data_free[0]

        mem_pos = data_free_entry.position
        self._data[mem_pos:(mem_pos + size)] = data
        # We restrict _malloc for the root entry only,
        # because a index can already change because of the lru_pop before
        self._data_idx[self._root] = (mem_pos, size)
        data_free_entry.size -= size
        data_free_entry.position += size

    def _free(self, index: int):
        """
        It is the opposite of _malloc. Free the memory used by entry at `index`
        Also, it launch sometime the _defrag if:
            - No more entry to register free position entry
            - The first free slot is too _small (heuristic: _small = AVG_SIZE_OF_DATA)

        ! Need lock !

        :param int index: entry index of the data to free
        """
        last = self._free_len
        self._data_free[last] = self._data_idx[index]
        free_size = self._data_free[last].size
        new_free_len = last + 1
        self._data_idx[index] = (-1, -1)
        # If the first free slot is too _small (heuristic: _small = AVG_SIZE_OF_DATA) and there are lot of fragment to retrieve:
        # -> We should _defrag to get a efficient _malloc
        # Also _defrag directly if there isn't any place in self._data_free
        if (self._data_free[0].size < self.AVG_SIZE_OF_DATA and new_free_len > self._size // 10) or new_free_len >= self._size:
            # It will result that self._free_len == 1
            self._defrag()
        else:
            self._free_len = new_free_len

        return free_size  # Return the size freed

    def _lru_pop(self):
        """
        Remove the last entry/data used (approximately for now,
        because doesn't update lru if not acquire write lock)

        ! Need lock !
        """
        if self._root == -1:
            raise Exception(f"Try to pop from empty lru ({self._length})")
        prev_index = self._entry_table[self._root].prev
        return self._del_index(prev_index, self._entry_table[prev_index])

    def _del_index(self, index: int, entry: _Entry):
        """
        Remove the entry at `index` and data linked to.
        It compacts the hash table to ensure the correctness
        of the _lookup (linear probing)

        ! Need lock !

        :param int index: index of entry to delete
        :param _Entry index: entry to delete
        """
        if entry.prev == entry.next == index:  # If am the only one
            self._root = -1
        else:
            self._entry_table[entry.next].prev = entry.prev
            self._entry_table[entry.prev].next = entry.next
            if self._root == index:
                self._root = entry.next

        self._entry_table[index] = (0, -1, -1)
        self._length -= 1
        free_size = self._free(index)

        # Delete the keys that are between this element, and the next free spot, having
        # an index lower or equal to the position we delete (conflicts handling).
        def move_index(old_index, new_index):
            old_entry = self._entry_table[old_index]
            hash_i, prev_i, next_i = old_entry.hash, old_entry.prev, old_entry.next
            if self._entry_table[old_index].next == old_index:  # if it is the only one item
                prev_i = next_i = new_index
            self._entry_table[prev_i].next = self._entry_table[next_i].prev = new_index
            self._entry_table[new_index] = (hash_i, prev_i, next_i)
            self._entry_table[old_index] = (0, -1, -1)
            self._data_idx[new_index] = self._data_idx[old_index]
            self._data_idx[old_index] = (-1, -1)
            if self._root == old_index:
                self._root = new_index

        index_empty = index
        for i in range(index + 1, index + self._size):
            i_mask = i % self._size  # from index -> self._size -> 0 -> index - 1
            i_entry = self._entry_table[i_mask]
            if i_entry.prev == -1:
                break
            hash_mask = i_entry.hash % self._size

            distance_i = i_mask - hash_mask if i_mask >= hash_mask else self._size - hash_mask + i_mask
            # distance error of i,
            # - if 0 then he is a the correct location don't move
            # - if < than distance_new = not suitable location
            # else compress
            if distance_i == 0:
                continue
            distance_new = index_empty - hash_mask if index_empty >= hash_mask else self._size - hash_mask + index_empty
            if distance_new < distance_i:
                move_index(i_mask, index_empty)
                index_empty = i_mask
        else:
            raise MemoryError("The hashtable seems full, it doesn't make any sense")

        return free_size

    def _data_get(self, index: int):
        """
        Get (key, value) of entry at `index`.

        ! Need lock !
        """
        data_id = self._data_idx[index]
        # Load the value (not the key) outside the lock should be a good idea (for multi-processing performance).
        # But because it increase the complexity of data structure (need to have the key length)
        # and we are force to copy the bytes outside the lock (or it can change between the release and the marshall.loads)
        # it isn't more efficient and increase the complexity of the code (need maybe more test) :/
        return marshal.loads(self._data[data_id.position:data_id.position + data_id.size])

    def _lookup(self, key, hash_: int) -> tuple:
        """
        Return the first (index, entry, value) corresponding to (key, hash).
        If a entry is found, the value is set else it is None.

        ! Need lock !
         """
        for i in range(self._size):
            index = (hash_ + i) % self._size
            entry = self._entry_table[index]
            if entry.prev == -1:
                return index, entry, None
            if entry.hash == hash_:
                key_full, val = self._data_get(index)
                if key_full == key:  # Hash conflict is rare, then it is ok to load to much some time.
                    return index, entry, val
        raise MemoryError("Hash table full, doesn't make any sense, LRU is broken")

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        """ Get a value from the key

        :param key: hashable key
        :raises KeyError: If the key doesn't exist
        :return: The value unmarshalled
        """
        hash_ = hash(key)
        with self._lock:
            self._check_consistence()
            index, entry, val = self._lookup(key, hash_)
            if val is None:
                raise KeyError(f"{key} doesn't not exist")

            self._consistent.value = False
            if self._root != index:
                # Pop me from my previous location
                self._entry_table[entry.prev].next = entry.next
                self._entry_table[entry.next].prev = entry.prev
                # Put me in front
                entry.next = self._root
                entry.prev = self._entry_table[self._root].prev
                self._entry_table[self._entry_table[self._root].prev].next = index
                self._entry_table[self._root].prev = index
                self._root = index
            self._consistent.value = True
        return val

    def __setitem__(self, key, value):
        hash_ = hash(key)
        data = marshal.dumps((key, value))
        if len(data) > self._max_size_one_data:
            raise MemoryError(f"Too big object ({len(data)}) to put in the Shared Memory (max {self._max_size_one_data} bytes by entry)")

        with self._lock:
            self._check_consistence()
            index, entry, val = self._lookup(key, hash_)
            self._consistent.value = False
            if self._root == index:  # If I am already the root, just update the hash
                self._entry_table[index].hash = hash_
            else:
                if val is not None:  # Remove previous spot if exist
                    self._entry_table[entry.prev].next = entry.next
                    self._entry_table[entry.next].prev = entry.prev
                if self._root == -1:  # First item set
                    self._entry_table[index] = (hash_, index, index)
                else:
                    old_root_i = self._root
                    self._entry_table[index] = (hash_, self._entry_table[old_root_i].prev, old_root_i)
                    self._entry_table[self._entry_table[old_root_i].prev].next = index
                    self._entry_table[old_root_i].prev = index
                self._root = index

            if val is None:
                self._length += 1
            else:
                self._free(index)
            self._malloc(data)  # Malloc use root entry to find index

            if self._length > self._max_length:
                self._lru_pop()  # Make it after to avoid modifying index
            self._consistent.value = True

    # --------- Close methods

    def close(self):
        _logger.debug("Close shared memory")
        self._sm.close()

    def unlink(self):
        _logger.debug("Delete shared memory")
        self.close()
        del self._head, self._entry_table, self._data_idx, self._data_free, self._data, self._lock
        self._sm.unlink()
        del self

    # --------------------- TESTING methods ---------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlink()

    def __len__(self):
        with self._lock:
            return self._length

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        return True

    def __delitem__(self, key):
        hash_ = hash(key)
        with self._lock:
            self._check_consistence()
            index, entry, val = self._lookup(key, hash_)
            if val is None:
                raise KeyError(f"{key} doesn't not exist, cannot delete it")
            self._del_index(index, entry)

    # --------------------- DEBUGGING Methods --------------

    def __iter__(self):
        """ Only use for debugging"""
        # with self._lock:
        if self._root == -1:
            return
        node_index = self._root
        for _ in range(self._length + 1):
            yield self._data_get(node_index)
            node_index = self._entry_table[node_index].next
            if node_index == self._root:
                break
        else:
            raise MemoryError(f"Infinite loop detected in the Linked list, {self._root=}:\n" + "\n".join(str(i) + ": " + str(e) for i, e in enumerate(self._entry_table)))

    def __repr__(self) -> str:
        """ Only use for debugging"""
        result = []
        # with self._lock:
        if self._root == -1:
            return f'hashtable size: {self._size}, len: {str(self._length)}\n' + '\n'.join(result) + '\n' + "\n".join(str(e) for e in self._data_free[:self._free_len])
        node_index = self._root
        for _ in range(self._length + 1):
            hash_key, nxt = self._entry_table[node_index].hash, self._entry_table[node_index].next
            try:
                data = self._data_get(node_index)
            except (ValueError, EOFError):
                data = ("<unable to read>", "<unable to read>")
            result.append(f'key: {data[0]}, hash % size: {hash_key % self._size}, index: {node_index}, {self._entry_table[node_index]}, data_pos={self._data_idx[node_index].position} - data_size={self._data_idx[node_index].size}: {reprlib.repr(data[1])}')
            node_index = nxt
            if node_index == self._root:
                return f'hashtable size: {self._size}, len: {str(self._length)}, {self._root=}\n' + \
                    '\n'.join(result) + \
                    f'\nFree spots {self._free_len}:\n' + \
                    "\n".join(str(e) for e in self._data_free[:self._free_len])
        raise MemoryError(f"Infinite loop detected in the Linked list, {self._root=}:\n" + "\n".join(str(i) + ": " + str(e) for i, e in enumerate(self._entry_table)))
