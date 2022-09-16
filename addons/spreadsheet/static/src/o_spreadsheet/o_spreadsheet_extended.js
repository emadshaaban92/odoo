/** @odoo-module */

const spreadsheet = o_spreadsheet;
export const initCallbackRegistry = new spreadsheet.Registry();

import { _t } from "@web/core/l10n/translation";
o_spreadsheet.setTranslationMethod(_t);

// export * from spreadsheet ?
export default spreadsheet;
