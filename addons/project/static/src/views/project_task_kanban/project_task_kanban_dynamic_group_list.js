/** @odoo-module */

import { KanbanDynamicGroupList } from "@web/views/kanban/kanban_model";
import { Domain } from '@web/core/domain';
import { session } from '@web/session';

export class ProjectTaskKanbanDynamicGroupList extends KanbanDynamicGroupList {
    get context() {
        const context = super.context;
        if (context.createPersonalStageGroup) {
            context.default_user_id = context.uid;
            delete context.createPersonalStageGroup;
            delete context.default_project_id;
        }
        return context;
    }

    get isGroupedByStage() {
        return !!this.groupByField && this.groupByField.name === 'stage_id';
    }

    get isGroupedByPersonalStages() {
        return !!this.groupByField && this.groupByField.name === 'personal_stage_type_ids';
    }

    async _loadGroups() {
        if (!this.isGroupedByPersonalStages) {
            return super._loadGroups(...arguments);
        }
        const previousDomain = this.domain;
        this.domain = Domain.and([[['user_ids', 'in', session.uid]], previousDomain]).toList({});
        const result = await super._loadGroups(...arguments);
        this.domain = previousDomain;
        return result;
    }

    async createGroup() {
        if (this.isGroupedByPersonalStages) {
            this.defaultContext = Object.assign({}, this.defaultContext || {}, {
                createPersonalStageGroup: true,
            });
        }

        let result;
        const model = arguments[2];
        if (model) {
            const project_domain = this.domain.find((item) => {
                return item[0] === 'display_project_id' && item[1] === '='
            });
            result = await this.model.orm.create(model, [{
                'name': arguments[0],
                'fold': arguments[1],
                'project_ids': [project_domain[2]],
            }]);
            await this.model.reloadRecords(this);
        }
        else {
            result = await super.createGroup(...arguments);
        }


        if (this.isGroupedByPersonalStages) {
            delete this.defaultContext.createPersonalStageGroup;
        }
        return result;
    }
}
