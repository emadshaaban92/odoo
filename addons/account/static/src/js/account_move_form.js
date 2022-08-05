/** @odoo-module **/

import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormCompiler } from "@web/views/form/form_compiler";
import { FormRenderer } from "@web/views/form/form_renderer";

export class AccountMoveFormRenderer extends FormRenderer {
    async saveOnTabChange() {
        if (this.props.record.mode === "edit" && this.props.record.isDirty) {
            await this.props.record.save({
                stayInEdition: true,
            });
        }
    }
}
export class AccountMoveFormCompiler extends FormCompiler {
    compileNotebook(el, params) {
        let noteBook = super.compileNotebook(...arguments);
        if (el.hasAttribute("onPageUpdate")) {
            noteBook.setAttribute("onPageUpdate", el.getAttribute("onPageUpdate"));
        }
        return noteBook;
    }
}

const AccountMoveFormView = {
    ...formView,
    Renderer: AccountMoveFormRenderer,
    Compiler: AccountMoveFormCompiler,
};

registry.category("views").add("account_move_form", AccountMoveFormView);
