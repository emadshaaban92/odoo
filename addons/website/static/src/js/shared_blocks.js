/** @odoo-module **/

import publicWidget from 'web.public.widget';

publicWidget.registry.o_shared_blocks = publicWidget.Widget.extend({
    selector: '#o_shared_blocks',
    disabledInEditableMode: false,
    events: {
        'show.bs.modal': '_onContentChanged',
        'hidden.bs.modal': '_onContentChanged',
    },
    edit_events: {
        'content_changed': '_onContentChanged',
    },

    /**
     * @override
     */
    start() {
        this._updateTargetVisibility();
        return this._super(...arguments);
    },
    /**
     * @override
     */
    destroy() {
        this.el.classList.add('d-none');
        this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @returns {boolean}
     */
    _hasVisibleChild() {
        return !!this.el.querySelector(':scope > *:not(.d-none)');
    },
    /**
     * @private
     */
    _updateTargetVisibility() {
        if (this._hasVisibleChild()) {
            this.el.classList.remove('d-none');
        } else {
            this.el.classList.add('d-none');
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onContentChanged() {
        this._updateTargetVisibility();
    },
});
