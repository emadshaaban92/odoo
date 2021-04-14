/** @odoo-module **/

import { AddMilestone, OpenMilestone } from '@project/js/components/project_utils';
const { useState } = owl.hooks;

export default class ProjectRightPanel extends owl.Component {
    constructor() {
        super(...arguments);
        this.context = this.props.action.context;
        this.domain = this.props.action.domain;
        this.project_id = this.context.active_id;
        this.state = useState({
            data: {
                tasks_analysis: {
                    data: []
                },
                milestones: {
                    data: []
                }
            }
        });
    }

    async willStart() {
        await super.willStart(...arguments);
        await this._loadQwebContext();
    }

    async willUpdateProps() {
        await super.willUpdateProps(...arguments);
        await this._loadQwebContext();
    }

    async _loadQwebContext() {
        const data = await this.rpc({
            model: 'project.project',
            method: 'get_panel_data',
            args: [this.project_id],
        });
        this.state.data = data;
        return data;
    }

    async onProjectActionClick(event) {
        if (event.currentTarget.dataset.type === "action") {
            const action = event.currentTarget.dataset.action;
            const additionalContext = JSON.parse(event.currentTarget.dataset.additional_context);
            this._doAction(action, {
                additional_context: additionalContext
            });
        } else {
            const action = await this.rpc({
                model: 'project.project',
                method: event.currentTarget.dataset.action,
                args: [this.project_id]
            });
            this._doAction(action);
        }
    }

    _doAction(action, options) {
        this.trigger('do-action', {
            action,
            options
        });
    }
}

ProjectRightPanel.template = "project.ProjectRightPanel";
ProjectRightPanel.components = {AddMilestone, OpenMilestone};
