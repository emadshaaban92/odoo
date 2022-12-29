/** @odoo-module **/

import { deepCopy } from "@web/core/utils/objects";
import { registry } from "@web/core/registry";
import { generateLegacyLoadViewsResult } from "@web/legacy/legacy_load_views";

/**
 * @typedef {Object} IrFilter
 * @property {[number, string] | false} user_id
 * @property {string} sort
 * @property {string} context
 * @property {string} name
 * @property {string} domain
 * @property {number} id
 * @property {boolean} is_default
 * @property {string} model_id
 * @property {[number, string] | false} action_id
 */

/**
 * @typedef {Object} ViewDescription
 * @property {string} arch
 * @property {number|false} id
 * @property {number|null} [custom_view_id]
 * @property {Object} [actionMenus] // for views other than search
 * @property {IrFilter[]} [irFilters] // for search view
 */

/**
 * @typedef {Object} LoadViewsParams
 * @property {string} resModel
 * @property {[number, string][]} views
 * @property {Object} context
 */

/**
 * @typedef {Object} LoadViewsOptions
 * @property {number|false} actionId
 * @property {boolean} loadActionMenus
 * @property {boolean} loadIrFilters
 */

/**
 * @typedef {Object} LoadFieldsOptions
 * @property {string[] | false} [fieldNames]
 * @property {string[]} [attributes]
 */

export const viewService = {
    dependencies: ["orm"],
    start(env, { orm }) {
        let cache = {};

        env.bus.addEventListener("CLEAR-CACHES", () => {
            cache = {};
            const processedArchs = registry.category("__processed_archs__");
            processedArchs.content = {};
            processedArchs.trigger("UPDATE");
        });

        /**
         * Loads fields information
         *
         * @param {string} resModel
         * @param {LoadFieldsOptions} [options]
         * @returns {Promise<object>}
         */
        async function loadFields(resModel, options = {}) {
            const key = JSON.stringify([
                "fields",
                resModel,
                options.fieldNames,
                options.attributes,
            ]);
            if (!cache[key]) {
                cache[key] = orm
                    .call(resModel, "fields_get", [options.fieldNames, options.attributes])
                    .catch((error) => {
                        delete cache[key];
                        return Promise.reject(error);
                    });
            }
            return cache[key];
        }

        /**
         *
         * @param {Element} element
         * @param {function(string, Element):void} enterModel
         * @param {function(string):void} exitModel
         */
        async function walk(element, enterModel, exitModel) {
            for (const child of element.children) {
                if (child.nodeType !== 3 /* TEXT_NODE */) {
                    const isSwitchingContext =
                        child.tagName === "field" || child.tagName === "groupby";
                    if (isSwitchingContext) {
                        await enterModel(child.getAttribute("name"), child);
                    }
                    await walk(child, enterModel, exitModel);
                    if (isSwitchingContext) {
                        exitModel(child.getAttribute("name"));
                    }
                }
            }
        }

        /**
         *
         * @param {string} resModel
         * @param {Object.<string, Object.<string, {}>>} models
         * @param {Object.<string, {id: number, arch: string}>} views
         */
        async function replaceMissingFieldsWithGhostWidget(resModel, models, views) {
            const domParser = new DOMParser();
            for (const viewType in views) {
                const view = views[viewType];
                const arch = view.arch;
                const root = domParser.parseFromString(arch, "text/xml").documentElement;

                const stack = [];
                await walk(
                    root,
                    async (fieldName, node) => {
                        const modelName =
                            stack.length > 0 ? stack[stack.length - 1].resModel : resModel;
                        const model = models[modelName];
                        const field = model[fieldName];
                        if (field) {
                            if (field.relation) {
                                stack.push({
                                    fieldName,
                                    resModel: field.relation,
                                });
                            }
                        } else {
                            const isFieldNode = node.tagName === "field";
                            const res = await orm.read("ir.ui.view", [view.id], ["xml_id"]);
                            const xmlId = res[0].xml_id;
                            console.error(
                                `field [${fieldName}] in ${viewType} view [${xmlId}](${view.id}) for model [${modelName}] is missing`
                            );
                            if (isFieldNode) {
                                node.setAttribute("widget", "ghost");
                                model[fieldName] = {
                                    name: fieldName,
                                    type: "missing",
                                    id: view.id,
                                    modelName,
                                    help: `${fieldName} is missing`,
                                    viewMode: viewType,
                                    xmlId,
                                };
                            } else {
                                // TODO: replace missing groupby by a ghost field ?
                            }
                        }
                    },
                    (fieldName) => {
                        const last = stack.length > 0 && stack[stack.length - 1];
                        if (last && last.fieldName === fieldName) {
                            stack.pop();
                        }
                    }
                );

                views[viewType].arch = root.outerHTML;
            }
        }

        /**
         * Loads various information concerning views: fields_view for each view,
         * fields of the corresponding model, and optionally the filters.
         *
         * @param {LoadViewsParams} params
         * @param {LoadViewsOptions} [options={}]
         * @returns {Promise<ViewDescriptions>}
         */
        async function loadViews(params, options = {}) {
            const loadViewsOptions = {
                action_id: options.actionId || false,
                load_filters: options.loadIrFilters || false,
                toolbar: options.loadActionMenus || false,
            };
            if (env.isSmall) {
                loadViewsOptions.mobile = true;
            }
            const { context, resModel, views } = params;
            const filteredContext = Object.fromEntries(
                Object.entries(context || {}).filter((k, v) => !String(k).startsWith("default_"))
            );
            const key = JSON.stringify([resModel, views, filteredContext, loadViewsOptions]);
            if (!cache[key]) {
                cache[key] = orm
                    .call(resModel, "get_views", [], { context, views, options: loadViewsOptions })
                    .then((result) =>
                        replaceMissingFieldsWithGhostWidget(
                            resModel,
                            result.models,
                            result.views
                        ).then(() => result)
                    )
                    .then((result) => {
                        const { models, views } = result;
                        const modelsCopy = deepCopy(models); // for legacy views
                        const viewDescriptions = {
                            __legacy__: generateLegacyLoadViewsResult(resModel, views, modelsCopy),
                            fields: models[resModel],
                            relatedModels: models,
                            views: {},
                        };
                        for (const [resModel, fields] of Object.entries(modelsCopy)) {
                            const key = JSON.stringify(["fields", resModel, undefined, undefined]);
                            cache[key] = Promise.resolve(fields);
                        }
                        for (const viewType in views) {
                            const { arch, toolbar, id, filters, custom_view_id } = views[viewType];
                            const viewDescription = { arch, id, custom_view_id };
                            if (toolbar) {
                                viewDescription.actionMenus = toolbar;
                            }
                            if (filters) {
                                viewDescription.irFilters = filters;
                            }
                            viewDescriptions.views[viewType] = viewDescription;
                        }
                        return viewDescriptions;
                    })
                    .catch((error) => {
                        delete cache[key];
                        return Promise.reject(error);
                    });
            }
            return cache[key];
        }
        return { loadViews, loadFields };
    },
};

registry.category("services").add("view", viewService);
