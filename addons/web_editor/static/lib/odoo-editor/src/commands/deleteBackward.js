/** @odoo-module **/
import { UNBREAKABLE_ROLLBACK_CODE, UNREMOVABLE_ROLLBACK_CODE } from '../utils/constants.js';
import {
    boundariesOut,
    childNodeIndex,
    CTGROUPS,
    CTYPES,
    DIRECTIONS,
    endPos,
    fillEmpty,
    getState,
    isBlock,
    isInPre,
    isUnremovable,
    isVisible,
    isVisibleStr,
    leftPos,
    moveNodes,
    nodeSize,
    prepareUpdate,
    setSelection,
    splitTextNode,
    isMediaElement,
    isVisibleEmpty,
} from '../utils/utils.js';

Text.prototype.oDeleteBackward = function (offset, alreadyMoved = false) {
    const parentNode = this.parentNode;
    console.warn("text oDeleteBackward", this, offset);

    if (!offset) {
        // Backspace at the beginning of a text node is not a specific case to
        // handle, let the element implementation handle it.
        HTMLElement.prototype.oDeleteBackward.call(this, offset, alreadyMoved);
        return;
    }

    // Get the size of the unicode character to remove.
    const charSize = [...this.nodeValue.slice(0, offset)].pop().length;
    // Split around the character where the backspace occurs.
    const firstSplitOffset = splitTextNode(this, offset - charSize);
    const secondSplitOffset = splitTextNode(parentNode.childNodes[firstSplitOffset], charSize);
    const middleNode = parentNode.childNodes[firstSplitOffset];

    // Do remove the character, then restore the state of the surrounding parts.
    const restore = prepareUpdate(parentNode, firstSplitOffset, parentNode, secondSplitOffset);
    const isSpace = !isVisibleStr(middleNode) && !isInPre(middleNode);
    const isZWS = middleNode.nodeValue === '\u200B';
    middleNode.remove();
    restore();

    // If the removed element was not visible content, propagate the backspace.
    if (
        isZWS ||
        isSpace &&
        getState(parentNode, firstSplitOffset, DIRECTIONS.LEFT).cType !== CTYPES.CONTENT
    ) {
        parentNode.oDeleteBackward(firstSplitOffset, alreadyMoved);
        if (isZWS) {
            fillEmpty(parentNode);
        }
        return;
    }

    fillEmpty(parentNode);
    setSelection(parentNode, firstSplitOffset);
};

HTMLElement.prototype.oDeleteBackward = function (offset, alreadyMoved = false, maxSizeNodeToMove = null) {
    console.warn("html oDeleteBackward", this, this.outerHTML, offset);
    console.log('>>', document.querySelector('.odoo-editor-editable').innerHTML + '');
    const contentIsZWS = this.textContent === '\u200B';
    let moveDest;
    if (offset) {
        const leftNode = this.childNodes[offset - 1];
        if (isUnremovable(leftNode)) {
            throw UNREMOVABLE_ROLLBACK_CODE;
        }
        if (
            isMediaElement(leftNode) ||
            (leftNode.getAttribute &&
                typeof leftNode.getAttribute('contenteditable') === 'string' &&
                leftNode.getAttribute('contenteditable').toLowerCase() === 'false')
        ) {
            leftNode.remove();
            return;
        }
        if (leftNode.getAttribute && leftNode.getAttribute('contenteditable') === 'false') {
            leftNode.remove();
            return;
        }
        if (!isBlock(leftNode) || isVisibleEmpty(leftNode)) {
            /**
             * Backspace just after an inline node, convert to backspace at the
             * end of that inline node.
             *
             * E.g. <p>abc<i>def</i>[]</p> + BACKSPACE
             * <=>  <p>abc<i>def[]</i></p> + BACKSPACE
             */
            leftNode.oDeleteBackward(nodeSize(leftNode), alreadyMoved);
            return;
        }

        /**
         * Backspace just after an block node, we have to move any inline
         * content after it, up to the next block. If the cursor is between
         * two blocks, this is a theoretical case: just do nothing.
         *
         * E.g. <p>abc</p>[]de<i>f</i><p>ghi</p> + BACKSPACE
         * <=>  <p>abcde<i>f</i></p><p>ghi</p>
         */
        alreadyMoved = true;
        moveDest = endPos(leftNode);
    } else {
        if (isUnremovable(this)) {
            throw UNREMOVABLE_ROLLBACK_CODE;
        }
        const parentEl = this.parentNode;

        if (!isBlock(this) || isVisibleEmpty(this)) {
            // console.log('----', document.querySelector('.odoo-editor-editable').innerHTML);
            /**
             * Backspace at the beginning of an inline node, nothing has to be
             * done: propagate the backspace. If the node was empty, we remove
             * it before.
             *
             * E.g. <p>abc<b></b><i>[]def</i></p> + BACKSPACE
             * <=>  <p>abc<b>[]</b><i>def</i></p> + BACKSPACE
             * <=>  <p>abc[]<i>def</i></p> + BACKSPACE
             */
            const parentOffset = childNodeIndex(this);

            if (!nodeSize(this) || contentIsZWS) {
                const visible = isVisible(this) && !contentIsZWS;
                const restore = prepareUpdate(...boundariesOut(this));
                this.remove();
                restore();

                fillEmpty(parentEl);

                if (visible) {
                    // TODO this handle BR/IMG/etc removals../ to see if we
                    // prefer to have a dedicated handler for every possible
                    // HTML element or if we let this generic code handle it.
                    setSelection(parentEl, parentOffset);
                    return;
                }
            }
            // console.log('----', document.querySelector('.odoo-editor-editable').innerHTML);
            parentEl.oDeleteBackward(parentOffset, alreadyMoved);
            return;
        }

        /**
         * Backspace at the beginning of a block node, we have to move the
         * inline content at its beginning outside of the element and propagate
         * to the left block if any.
         *
         * E.g. (prev == block)
         *      <p>abc</p><div>[]def<p>ghi</p></div> + BACKSPACE
         * <=>  <p>abc</p>[]def<div><p>ghi</p></div> + BACKSPACE
         *
         * E.g. (prev != block)
         *      abc<div>[]def<p>ghi</p></div> + BACKSPACE
         * <=>  abc[]def<div><p>ghi</p></div>
         */
        moveDest = leftPos(this);
    }

    // console.log('*** 2', document.querySelector('.odoo-editor-editable').innerHTML + '');
    let node = this.childNodes[offset];
    let firstBlockIndex = offset;
    // console.log('maxSizeNodeToMove', maxSizeNodeToMove);
    // console.log('node + maxSizeNodeToMove ', offset + maxSizeNodeToMove);
    // console.log('firstBlockIndex', firstBlockIndex);
    // console.log('cond', node + maxSizeNodeToMove > firstBlockIndex);
    // console.log('this ', this.outerHTML);
    // console.log('this is block', isBlock(this));
    while (
        node &&
        !isBlock(node) &&
        (
            maxSizeNodeToMove === null ||
            offset + maxSizeNodeToMove > firstBlockIndex
        )) {
        // console.log('=====> while from ', firstBlockIndex, 'to', firstBlockIndex + 1);
        node = node.nextSibling;
        firstBlockIndex++;
    }
    let [cursorNode, cursorOffset] = moveNodes(...moveDest, this, offset, firstBlockIndex);
    setSelection(cursorNode, cursorOffset);
    // console.log('*** 3', document.querySelector('.odoo-editor-editable').innerHTML + '');

    // Propagate if this is still a block on the left of where the nodes were
    // moved.
    if (
        cursorNode.nodeType === Node.TEXT_NODE &&
        (cursorOffset === 0 || cursorOffset === cursorNode.length)
    ) {
        cursorOffset = childNodeIndex(cursorNode) + (cursorOffset === 0 ? 0 : 1);
        cursorNode = cursorNode.parentNode;
    }
    console.log('*** 4', document.querySelector('.odoo-editor-editable').innerHTML + '');
    if (cursorNode.nodeType !== Node.TEXT_NODE) {
        const { cType } = getState(cursorNode, cursorOffset, DIRECTIONS.LEFT);
        console.log('get state', cType);
        console.log('alreadyMoved', alreadyMoved);
        if (cType & CTGROUPS.BLOCK && (!alreadyMoved || cType === CTYPES.BLOCK_OUTSIDE)) {
            console.log('propagate');
            cursorNode.oDeleteBackward(cursorOffset, alreadyMoved, firstBlockIndex - offset);
        } else if (!alreadyMoved) {
            const cursorNodeRightNode = cursorNode.childNodes[cursorOffset] ? cursorNode.childNodes[cursorOffset].nextSibling : undefined;
            if (cursorNodeRightNode && Node.TEXT_NODE === cursorNodeRightNode.nodeType) {
                console.log('\n\nadd BR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
                console.log('cursorNode', cursorNode.outerHTML);
                console.log('cursorNode child nodes', cursorNode.childNodes);
                console.log('cursorNode child nodes', cursorNode.childNodes[cursorOffset]);
                console.log('CursorNodeRightNode', cursorNodeRightNode);
                moveDest[0].insertBefore(document.createElement('br'), cursorNodeRightNode);
            }
        }
    }
};

HTMLLIElement.prototype.oDeleteBackward = function (offset, alreadyMoved = false) {
    if (offset > 0 || this.previousElementSibling) {
        // If backspace inside li content or if the li is not the first one,
        // it behaves just like in a normal element.
        HTMLElement.prototype.oDeleteBackward.call(this, offset, alreadyMoved);
        return;
    }
    this.oShiftTab(offset);
};

HTMLBRElement.prototype.oDeleteBackward = function (offset, alreadyMoved = false) {
    const parentOffset = childNodeIndex(this);
    const rightState = getState(this.parentElement, parentOffset + 1, DIRECTIONS.RIGHT).cType;
    if (rightState & CTYPES.BLOCK_INSIDE) {
        this.parentElement.oDeleteBackward(parentOffset, alreadyMoved);
    } else {
        HTMLElement.prototype.oDeleteBackward.call(this, offset, alreadyMoved);
    }
};
