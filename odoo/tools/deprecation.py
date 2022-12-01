import logging
import sys
import warnings

import odoo


logger = logging.getLogger(__name__)


SIMPLE_MSG = "since odoo {since} and is scheduled for removal in odoo {until}"
MOVED_MSG = f"{{old_name}} is deprecated {SIMPLE_MSG}, please use {{new_name}} instead"
USELESS_MSG = f"{{name}} does nothing {SIMPLE_MSG}"


def warn_useless(name, *, since, until, stacklevel=1, warn_only_once=True):
    """
    Warn that a method or a parameter has become useless useless. In
    case the current odoo version is earlier than ``until``, it raises
    an exception instead.

    The ``name`` argument is free text and is injected in the following
    sentence:

        {name} does nothing since...

    :param str name: the thing that has become useless
    :param tuple since: the version since the thing is useless, usually
        the current (MAJOR, MINOR) odoo version but it can also be a
        past version in case the thing had become useless without
        deprecation warning long ago.
    :param tuple | None until: the optional version when it is expected
        to remove the useless thing, usually the second next stable
        major version: ``(MAJOR + 1 + int(bool(MINOR)), 0)``
    :param int stacklevel: how many stacks should we go up to find the
        function that use the deprecated ``name``, , 0 for the function
        where ``warn_useless`` is used, 1 (defaut) for the above
        function.
    :warn_only_once: whether to use ``logging.warn`` (logs everytime) or
        ``warnings.warn`` (log a single time, default).
    """
    return warn(
        USELESS_MSG.format(name=name),
        since=since, until=until, stacklevel=stacklevel + 1, warn_only_once=warn_only_once
    )


def warn_moved(old_name, new_name, *, since, until, stacklevel=1, warn_only_once=True):
    """
    Warn that a method or a function has been moved elsewhere. In case
    the current odoo version is earlier than ``until``, it raises an
    exception instead.

    The ``old_name`` and ``new_name`` arguments are free text and are
    injected in the following sentence:

        {old_name} is deprecated since ..., please use {new_name} instead

    :param str old_name: the thing that is now a deprecated alias
    :param str new_name: the newer, prefered thing 
    :param tuple since: the version since the thing moved, usually the
        current (MAJOR, MINOR) odoo version but it can also be a past
        version in case the thing had become useless without deprecation
        warning long ago.
    :param tuple | None until: the optional version when it is expected
        to remove the deprecated alias, usually the second next stable
        major version: ``(MAJOR + 1 + int(bool(MINOR)), 0)``
    :param int stacklevel: how many stacks should we go up to find the
        function that use the deprecated ``old_name``, 0 for the
        function where ``warn_moved`` is used, 1 (defaut) for the above
        function.
    :warn_only_once: whether to use ``logging.warn`` (logs everytime) or
        ``warnings.warn`` (log a single time, default).
    """
    return warn(
        MOVED_MSG.format(old_name=old_name, new_name=new_name),
        since=since, until=until, stacklevel=stacklevel + 1, warn_only_once=warn_only_once
    )


def warn(message=SIMPLE_MSG, *, since, until, stacklevel=1, warn_only_once=True):
    """
    Warn that this thing is something deprecated. In case the current
    odoo version is earlier than ``until``, it raises an exception
    instead.

    :param str message: free text to use as deprecation message
    :param tuple since: the version since it is deprecated, usually the
        current (MAJOR, MINOR) odoo version but it can also be a past
        version in case the thing had become useless without deprecation
        warning long ago.
    :param tuple | None until: the optional version when it is expected
        to remove this deprecated thing, usually the second next stable
        major version: ``(MAJOR + 1 + int(bool(MINOR)), 0)``
    :param int stacklevel: how many stacks should we go up to find the
        function that use this deprecated thing, 0 for the function
        where ``warn`` is used, 1 (defaut) for the above function.
    :warn_only_once: whether to use ``logging.warn`` (logs everytime) or
        ``warnings.warn`` (log a single time, default).
    """
    if until and odoo.release.version_info[:2] >= until:
        raise RuntimeError(f"this thing was scheduled for removal in {until[0]}.{until[1]}")

    msg = message.format(since=f'{since[0]}.{since[1]}', until=f'{until[0]}.{until[1]}')
    if warn_only_once:
        warnings.warn(msg, DeprecationWarning, stacklevel=stacklevel + 2)
    elif sys.version_info >= (3.8):
        logger.warning(msg, stack_info=True, stacklevel=stacklevel + 2)
    else:
        logger.warning(msg, stack_info=True)
