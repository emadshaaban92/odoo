/** @odoo-module */

import { registry } from "@web/core/registry";
import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";

import IrMenuPlugin from "./ir_ui_menu_plugin";

import {
    isMarkdownIrMenuIdUrl,
    isIrMenuXmlUrl,
    isMarkdownViewUrl,
    parseIrMenuXmlUrl,
    parseViewLink,
    parseIrMenuIdLink,
} from "./odoo_menu_link_cell";
import { _t } from "@web/core/l10n/translation";
import { sprintf } from "@web/core/utils/strings";

const { urlRegistry, corePluginRegistry } = spreadsheet.registries;
const { EvaluationError } = spreadsheet;

corePluginRegistry.add("ir_ui_menu_plugin", IrMenuPlugin);

class BadOdooLinkError extends EvaluationError {
    constructor(menuId) {
        super(
            _t("#LINK"),
            sprintf(_t("Menu %s not found. You may not have the required access rights."), menuId)
        );
    }
}

export const spreadsheetLinkMenuCellService = {
    dependencies: ["menu"],
    start(env) {
        function _getIrMenuByXmlId(xmlId) {
            const menu = env.services.menu.getAll().find((menu) => menu.xmlid === xmlId);
            if (!menu) {
                throw new BadOdooLinkError(xmlId);
            }
            return menu;
        }

        urlRegistry
            .add("OdooMenuIdLink", {
                sequence: 65,
                match: isMarkdownIrMenuIdUrl,
                createLink(url, label) {
                    const menuId = parseIrMenuIdLink(url);
                    const menu = env.services.menu.getMenu(menuId);
                    if (!menu) {
                        throw new BadOdooLinkError(menuId);
                    }
                    return {
                        url,
                        label,
                        isExternal: false,
                        isUrlEditable: false,
                    };
                },
                urlRepresentation(url) {
                    const menuId = parseIrMenuIdLink(url);
                    return env.services.menu.getMenu(menuId).name;
                },
                open(url) {
                    const menuId = parseIrMenuIdLink(url);
                    const menu = env.services.menu.getMenu(menuId);
                    env.services.action.doAction(menu.actionID);
                },
                // createCell: (id, content, properties, sheetId, getters) => {
                //     const { url } = parseMarkdownLink(content);
                //     const menuId = parseIrMenuIdLink(url);
                //     const menuName = env.services.menu.getMenu(menuId).name;
                //     return new OdooMenuLinkCell(id, content, menuId, menuName, properties);
                // },
            })
            .add("OdooMenuXmlLink", {
                sequence: 66,
                match: isIrMenuXmlUrl,
                createLink(url, label) {
                    const xmlId = parseIrMenuXmlUrl(url);
                    _getIrMenuByXmlId(xmlId);
                    return {
                        url,
                        label,
                        isExternal: false,
                        isUrlEditable: false,
                    };
                },
                urlRepresentation(url) {
                    const xmlId = parseIrMenuXmlUrl(url);
                    const menuId = _getIrMenuByXmlId(xmlId).id;
                    return env.services.menu.getMenu(menuId).name;
                },
                open(url) {
                    const xmlId = parseIrMenuXmlUrl(url);
                    const menuId = _getIrMenuByXmlId(xmlId).id;
                    const menu = env.services.menu.getMenu(menuId);
                    env.services.action.doAction(menu.actionID);
                },
                // createCell: (id, content, properties, sheetId, getters) => {
                //     const { url } = parseMarkdownLink(content);
                //     const xmlId = parseIrMenuXmlLink(url);
                //     const menuId = _getIrMenuByXmlId(xmlId).id;
                //     const menuName = _getIrMenuByXmlId(xmlId).name;
                //     return new OdooMenuLinkCell(id, content, menuId, menuName, properties);
                // },
            })
            .add("OdooViewLink", {
                sequence: 67,
                match: isMarkdownViewUrl,
                createLink(url, label) {
                    return {
                        url,
                        label: label,
                        isExternal: false,
                        isUrlEditable: false,
                    };
                },
                urlRepresentation(url) {
                    const actionDescription = parseViewLink(url);
                    return actionDescription.name;
                },
                open(url) {
                    const { viewType, action, name } = parseViewLink(url);
                    env.services.action.doAction(
                        {
                            type: "ir.actions.act_window",
                            name: name,
                            res_model: action.modelName,
                            views: action.views,
                            target: "current",
                            domain: action.domain,
                            context: action.context,
                        },
                        { viewType }
                    );
                },
                // createCell: (id, content, properties, sheetId, getters) => {
                //     const { url } = parseMarkdownLink(content);
                //     const actionDescription = parseViewLink(url);
                //     return new OdooViewLinkCell(id, content, actionDescription, properties);
                // },
            });

        return true;
    },
};

registry.category("services").add("spreadsheetLinkMenuCell", spreadsheetLinkMenuCellService);
