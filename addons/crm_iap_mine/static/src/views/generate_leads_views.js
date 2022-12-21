/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useGenerateLeadsButton } from "@crm_iap_mine/views/generate_leads_hook";
import { crmKanbanView } from "@crm/views/crm_kanban/crm_kanban_view";

patch(crmKanbanView.Controller.prototype, "crm_iap_lead_mining_request_kanban", {
    setup() {
        this._super(...arguments);
        this.useLeadGeneration = !this.props.context.no_crm_lead_generation;
        if (this.useLeadGeneration) {
            useGenerateLeadsButton();
        }
    },
});
crmKanbanView.buttonTemplate = "LeadMiningRequestKanbanView.buttons";
