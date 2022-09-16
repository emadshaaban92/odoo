/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, one } from '@mail/model/model_field';

registerModel({
    name: 'EmojiSearchBarView',
    recordMethods: {
        /**
         * Handles OWL update on this EmojiSearchBarView component.
         */
        onComponentUpdate() {
            this._handleFocus();
        },
        onFocusinInput() {
            this.update({ isFocused: true });
        },
        onFocusoutInput() {
            this.update({ isFocused: false });
        },
        /**
         * @public
         */
        onInput() {
            this.update({
                currentSearch: this.inputRef.el.value,
            });
        },
        /**
         * @public
         */
        reset() {
            this.update({ currentSearch: "" });
            this.inputRef.el.value = "";
            this.update({ isDoFocus: true });
        },
        /**
         * @private
         */
        _handleFocus() {
            if (this.isDoFocus) {
                if (!this.inputRef.el) {
                    return;
                }
                this.update({ isDoFocus: false });
                this.inputRef.el.focus();
            }
        },
    },
    fields: {
        currentSearch: attr({
            default: "",
        }),
        emojiPickerView: one("EmojiPickerView", {
            identifying: true,
            inverse: "emojiSearchBarView",
        }),
        inputRef: attr(),
        isDoFocus: attr({
            default: true,
        }),
        isFocused: attr({
            default: false,
        }),
        placeholder: attr({
            compute() {
                return this.env._t("Search an emoji");
            },
            required: true,
        }),
    },
});
