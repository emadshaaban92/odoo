/** @odoo-module **/

import { KanbanColumnQuickCreate } from "@web/views/kanban/kanban_column_quick_create";

export class ProjectTaskKanbanColumnQuickCreate extends KanbanColumnQuickCreate {
    /**
     * @override
     *
     */
    apply(index) {
        const fold = this.props.exampleData.examples[index].folded;
        const model = this.props.exampleData.model;
        for (let i = 0 ; i < this.props.exampleData.examples[index].columns.length ; i++) {
            this.props.onValidate(this.props.exampleData.examples[index].columns[i], fold && fold[i], model);
        }
    }
}
