odoo.define('mail.component.ThreadPreview', function (require) {
'use strict';

const PartnerImStatusIcon = require('mail.component.PartnerImStatusIcon');
const mailUtils = require('mail.utils');

class ThreadPreview extends owl.store.ConnectedComponent {

    /**
     * @param {...any} args
     */
    constructor(...args) {
        super(...args);
        this.components = {
            PartnerImStatusIcon,
        };
        this.template = 'mail.component.ThreadPreview';
    }

    //--------------------------------------------------------------------------
    // Getter / Setter
    //--------------------------------------------------------------------------

    /**
     * @return {string}
     */
    get image() {
        if (this.props.thread.direct_partner) {
            return `/web/image/res.partner/${this.props.thread.direct_partner[0].id}/image_64`;
        }
        return `/web/image/mail.channel/${this.props.thread.id}/image_128`;
    }

    /**
     * @return {string}
     */
    get inlineLastMessageBody() {
        if (!this.props.lastMessage) {
            return '';
        }
        return mailUtils.parseAndTransform(
            this.env.store.getters.messagePrettyBody(this.props.lastMessage.localId),
            mailUtils.inline);
    }

    /**
     * @return {boolean}
     */
    get isMyselfLastMessageAuthor() {
        return (
            this.props.lastMessageAuthor &&
            this.props.lastMessageAuthor.id === this.env.session.partner_id
        ) || false;
    }

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @return {boolean}
     */
    isPartiallyVisible() {
        const elRect = this.el.getBoundingClientRect();
        if (!this.el.parentNode) {
            return false;
        }
        const parentRect = this.el.parentNode.getBoundingClientRect();
        // intersection with 20px offset
        return (
            elRect.top < parentRect.bottom + 20 &&
            parentRect.top < elRect.bottom + 20
        );
    }

    scrollIntoView() {
        this.el.scrollIntoView();
    }

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClick(ev) {
        this.trigger('o-clicked', {
            threadLocalId: this.props.threadLocalId,
        });
    }

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClickMarkAsRead(ev) {
        this.env.store.dispatch('markThreadAsSeen', this.props.threadLocalId);
    }
}

/**
 * @param {Object} state
 * @param {Object} ownProps
 * @param {string} ownProps.threadLocalId
 * @param {Object} getters
 * @return {Object}
 */
ThreadPreview.mapStoreToProps = function (state, ownProps, getters) {
    const threadLocalId = ownProps.threadLocalId;
    const thread = state.threads[threadLocalId];
    let lastMessage;
    let lastMessageAuthor;
    const { length: l, [l-1]: lastMessageLocalId } = thread.messageLocalIds;
    lastMessage = state.messages[lastMessageLocalId];
    if (lastMessage) {
        lastMessageAuthor = state.partners[lastMessage.authorLocalId];
    }
    return {
        isMobile: state.isMobile,
        lastMessage,
        lastMessageAuthor,
        thread,
        threadDirectPartner: thread.directPartnerLocalId
            ? state.partners[thread.directPartnerLocalId]
            : undefined,
        threadName: getters.threadName(threadLocalId),
    };
};

ThreadPreview.props = {
    isMobile: Boolean,
    lastMessage: {
        type: Object, // {mail.store.model.Message}
        optional: true,
    },
    lastMessageAuthor: {
        type: Object, // {mail.store.model.Partner}
        optional: true,
    },
    thread: Object, // {mail.store.model.Thread}
    threadDirectPartner: {
        type: Object, // {mail.store.model.Partner}
        optional: true,
    },
    threadLocalId: String,
    threadName: String,
};

return ThreadPreview;

});
