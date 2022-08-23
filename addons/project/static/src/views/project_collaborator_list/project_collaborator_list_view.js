/** @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from '@web/views/list/list_view';
import { InviteCollaboratorsListController } from './project_collaborator_list_controller';

export const InviteCollaboratorsListView = {
    ...listView,
    Controller: InviteCollaboratorsListController,
    buttonTemplate: 'collaborators.List_view.buttons',
};

registry.category('views').add('invite_collaborators', InviteCollaboratorsListView);
