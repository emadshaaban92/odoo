/** @odoo-module */

import { registry } from '@web/core/registry';
import { Many2OneField } from '@web/views/fields/many2one/many2one_field';

export class ProjectPrivateTaskMany2OneField extends Many2OneField { 
    setup() {
        super.setup();
        console.log("PTSM2O");
    }

}
ProjectPrivateTaskMany2OneField.template = 'project.ProjectPrivateTaskMany2OneField';

registry.category('fields').add('project_private_task', ProjectPrivateTaskMany2OneField);
