/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";


export default class SlideChannelPartnerListController extends ListController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
    }

    channelEnrollInvite() {
        this._slideChannelInvite(true);
    }

    channelShareInvite() {
        this._slideChannelInvite(false);
    }

    /**
     * Method opening the wizard to invite (and enroll) new slide channel partners.
     * Reloads the model afterwards to see new (invited) attendees.
     * 
     * @private
     * @param {boolean} isEnroll If true, then the wizard will invite and enroll members, who will join
     * the course with status 'joined'. Otherwise, they will be invited only, with member_status 'invited'.
     */
    async _slideChannelInvite(isEnroll) {
        let defaultChannelId = this.model.env.searchModel._context.default_channel_id || false;
        const action = await this.orm.call(
            'slide.channel',
            'action_channel_invite',
            ["", defaultChannelId, isEnroll]
        );
        this.action.doAction(action, {
            onClose: async () => await this.model.load()
        });
    }
}
