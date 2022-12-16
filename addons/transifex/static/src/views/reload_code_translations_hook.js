/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";

const { useComponent } = owl;

export function useReloadCodeTranslationsButton() {
    const component = useComponent();
    const orm = useService("orm");

    component.onClickReloadCodeTranslations = async () => {
        await orm.call("transifex.code.translation", "reload", [], {});
        window.location.reload();
    };
}
