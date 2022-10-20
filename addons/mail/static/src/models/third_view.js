/** @odoo-module **/

import { clear } from '@mail/model/model_field_command';
import { attr, Model, one } from '@mail/model';

Model({
    name: 'ThirdView',
    lifecycleHooks: {
        _created() {
            console.log("ThirdView is loaded");
        },
    },
    fields: {
        /**
         * States the OWL component of this popover view.
         */
        component: attr(),
        /**
         * If set, this third view is owned by a message action view.
         */
        /*messageActionViewOwnerAsReaction: one('MessageActionView', {
            identifying: true,
            inverse: 'reactionPopoverView',
        }),*/
        /**
         * If set, this third view is owned by a composer view.
         */
        composerViewOwnerAsEmoji: one('ComposerView', {
            inverse: 'emojisThirdView',
        }),

        thirdManager: one('ThirdManager', {
            inverse: 'thirdView',
        }),

        /**
         * If set, the content of this popover view is a list of emojis.
         */
        emojiPickerView: one('EmojiPickerView', {
            compute() {
                if (this.composerViewOwnerAsEmoji) {
                    return {};
                }
                if (this.messageActionViewOwnerAsReaction) {
                    return {};
                }
                return clear();
            },
            inverse: 'thirdViewOwner',
        }),

        /**
         * Determines the record that is content of this popover view.
         */
        content: one('Record', {
            compute() {
                if (this.emojiPickerView) {
                    return this.emojiPickerView;
                }
                return clear();
            },
            //required: true,
        }),

        /**
         * Determines the class name for the component
         * that is content of this popover view.
         */
        contentClassName: attr({
            compute() {
                if (this.emojiPickerView) {
                    return 'o_ThirdView_emojiPickerView';
                }
                return clear();
            },
            default: '',
        }),

        /**
         * Determines the component name of the content.
         */
        contentComponentName: attr({
            compute() {
                if (this.emojiPickerView) {
                    return 'EmojiPickerView';
                }
                return '';
            },
            default: '',
            required: true,
        }),
    },
});
