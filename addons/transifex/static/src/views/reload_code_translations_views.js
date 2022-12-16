/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useReloadCodeTranslationsButton } from "@transifex/views/reload_code_translations_hook";
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";

export class TransifexCodeTranslationListController extends ListController {
    setup() {
        super.setup();
        useReloadCodeTranslationsButton();
    }
}

registry.category("views").add("transifex_code_translation_tree", {
    ...listView,
    Controller: TransifexCodeTranslationListController,
    buttonTemplate: "Transifex.CodeTranslationListView.Buttons",
});
