/** @odoo-module **/

import { useModels } from '@mail/component_hooks/use_models/use_models';
import { useShouldUpdateBasedOnProps } from '@mail/component_hooks/use_should_update_based_on_props/use_should_update_based_on_props';
import { useUpdate } from '@mail/component_hooks/use_update/use_update';
import { AutocompleteInput } from '@mail/components/autocomplete_input/autocomplete_input';
import { ChatWindowHeader } from '@mail/components/chat_window_header/chat_window_header';
import { ThreadView } from '@mail/components/thread_view/thread_view';
import { isEventHandled } from '@mail/utils/utils';

const { Component } = owl;
const { useRef } = owl.hooks;

const components = { AutocompleteInput, ChatWindowHeader, ThreadView };

export class ChatWindow extends Component {

    /**
     * @override
     */
    constructor(...args) {
        super(...args);
        useShouldUpdateBasedOnProps();
        useModels();
        useUpdate({ func: () => this._update() });
        /**
         * Reference of the header of the chat window.
         * Useful to prevent click on header from wrongly focusing the window.
         */
        this._chatWindowHeaderRef = useRef('header');
        /**
         * Reference of the autocomplete input (new_message chat window only).
         * Useful when focusing this chat window, which consists of focusing
         * this input.
         */
        this._inputRef = useRef('input');
        /**
         * Reference of thread in the chat window (chat window with thread
         * only). Useful when focusing this chat window, which consists of
         * focusing this thread. Will likely focus the composer of thread, if
         * it has one!
         */
        this._threadRef = useRef('thread');
        this._onWillHideHomeMenu = this._onWillHideHomeMenu.bind(this);
        this._onWillShowHomeMenu = this._onWillShowHomeMenu.bind(this);
        // the following are passed as props to children
        this._onAutocompleteSource = this._onAutocompleteSource.bind(this);
        this._constructor(...args);
    }

    /**
     * Allows patching constructor.
     */
    _constructor() {}

    mounted() {
        this.env.messagingBus.on('will_hide_home_menu', this, this._onWillHideHomeMenu);
        this.env.messagingBus.on('will_show_home_menu', this, this._onWillShowHomeMenu);
    }

    willUnmount() {
        this.env.messagingBus.off('will_hide_home_menu', this, this._onWillHideHomeMenu);
        this.env.messagingBus.off('will_show_home_menu', this, this._onWillShowHomeMenu);
    }

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @returns {mail.chat_window}
     */
    get chatWindow() {
        return this.env.models['mail.chat_window'].get(this.props.chatWindowLocalId);
    }

    /**
     * Get the content of placeholder for the autocomplete input of
     * 'new_message' chat window.
     *
     * @returns {string}
     */
    get newMessageFormInputPlaceholder() {
        return this.env._t("Search user...");
    }

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Apply visual position of the chat window.
     *
     * @private
     */
    _applyVisibleOffset() {
        const textDirection = this.env.messaging.locale.textDirection;
        const offsetFrom = textDirection === 'rtl' ? 'left' : 'right';
        const oppositeFrom = offsetFrom === 'right' ? 'left' : 'right';
        this.el.style[offsetFrom] = this.chatWindow.visibleOffset + 'px';
        this.el.style[oppositeFrom] = 'auto';
    }

    /**
     * Focus this chat window.
     *
     * @private
     */
    _focus() {
        this.chatWindow.update({
            isDoFocus: false,
            isFocused: true,
        });
        if (this._inputRef.comp) {
            this._inputRef.comp.focus();
        }
        if (this._threadRef.comp) {
            this._threadRef.comp.focus();
        }
    }

    /**
     * Save the scroll positions of the chat window in the store.
     * This is useful in order to remount chat windows and keep previous
     * scroll positions. This is necessary because when toggling on/off
     * home menu, the chat windows have to be remade from scratch.
     *
     * @private
     */
    _saveThreadScrollTop() {
        if (
            !this._threadRef.comp ||
            !this.chatWindow.threadViewer ||
            !this.chatWindow.threadViewer.threadView
        ) {
            return;
        }
        if (this.chatWindow.threadViewer.threadView.componentHintList.length > 0) {
            // the current scroll position is likely incorrect due to the
            // presence of hints to adjust it
            return;
        }
        this.chatWindow.threadViewer.saveThreadCacheScrollHeightAsInitial(
            this._threadRef.comp.getScrollHeight()
        );
        this.chatWindow.threadViewer.saveThreadCacheScrollPositionsAsInitial(
            this._threadRef.comp.getScrollTop()
        );
    }

    /**
     * @private
     */
    _update() {
        if (!this.chatWindow) {
            // chat window is being deleted
            return;
        }
        if (this.chatWindow.isDoFocus) {
            this._focus();
        }
        this._applyVisibleOffset();
    }

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Called when typing in the autocomplete input of the 'new_message' chat
     * window.
     *
     * @private
     * @param {Object} req
     * @param {string} req.term
     * @param {function} res
     */
    _onAutocompleteSource(req, res) {
        this.env.models['mail.partner'].imSearch({
            callback: (partners) => {
                const suggestions = partners.map(partner => {
                    return {
                        id: partner.id,
                        value: partner.nameOrDisplayName,
                        label: partner.nameOrDisplayName,
                    };
                });
                res(_.sortBy(suggestions, 'label'));
            },
            keyword: _.escape(req.term),
            limit: 10,
        });
    }

    /**
     * Called when clicking on header of chat window. Usually folds the chat
     * window.
     *
     * @private
     * @param {CustomEvent} ev
     */
    _onClickedHeader(ev) {
        ev.stopPropagation();
        if (this.env.messaging.device.isMobile) {
            return;
        }
        if (this.chatWindow.isFolded) {
            this.chatWindow.unfold();
            this.chatWindow.focus();
        } else {
            this._saveThreadScrollTop();
            this.chatWindow.fold();
        }
    }

    /**
     * Called when an element in the thread becomes focused.
     *
     * @private
     * @param {FocusEvent} ev
     */
    _onFocusinThread(ev) {
        ev.stopPropagation();
        if (!this.chatWindow) {
            // prevent crash on destroy
            return;
        }
        this.chatWindow.update({ isFocused: true });
    }

    /**
     * Focus out the chat window.
     *
     * @private
     */
    _onFocusout() {
        if (!this.chatWindow) {
            // ignore focus out due to record being deleted
            return;
        }
        this.chatWindow.update({ isFocused: false });
    }

    /**
     * @private
     * @param {KeyboardEvent} ev
     */
    _onKeydown(ev) {
        if (!this.chatWindow) {
            // prevent crash during delete
            return;
        }
        switch (ev.key) {
            case 'Tab':
                ev.preventDefault();
                if (ev.shiftKey) {
                    this.chatWindow.focusPreviousVisibleUnfoldedChatWindow();
                } else {
                    this.chatWindow.focusNextVisibleUnfoldedChatWindow();
                }
                break;
            case 'Escape':
                if (isEventHandled(ev, 'ComposerTextInput.closeSuggestions')) {
                    break;
                }
                if (isEventHandled(ev, 'Composer.closeEmojisPopover')) {
                    break;
                }
                ev.preventDefault();
                this.chatWindow.focusNextVisibleUnfoldedChatWindow();
                this.chatWindow.close();
                break;
        }
    }

    /**
     * Save the scroll positions of the chat window in the store.
     * This is useful in order to remount chat windows and keep previous
     * scroll positions. This is necessary because when toggling on/off
     * home menu, the chat windows have to be remade from scratch.
     *
     * @private
     */
    async _onWillHideHomeMenu() {
        this._saveThreadScrollTop();
    }

    /**
     * Save the scroll positions of the chat window in the store.
     * This is useful in order to remount chat windows and keep previous
     * scroll positions. This is necessary because when toggling on/off
     * home menu, the chat windows have to be remade from scratch.
     *
     * @private
     */
    async _onWillShowHomeMenu() {
        this._saveThreadScrollTop();
    }

}

Object.assign(ChatWindow, {
    components,
    defaultProps: {
        hasCloseAsBackButton: false,
        isExpandable: false,
        isFullscreen: false,
    },
    props: {
        chatWindowLocalId: String,
        hasCloseAsBackButton: Boolean,
        isExpandable: Boolean,
        isFullscreen: Boolean,
    },
    template: 'mail.ChatWindow',
});
