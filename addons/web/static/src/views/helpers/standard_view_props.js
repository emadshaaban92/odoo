/** @odoo-module **/

// TODO: add this in info props description

// breadcrumbs: { type: Array, optional: true },
// __getLocalState__: { type: CallbackRecorder, optional: true },
// __getContext__: { type: CallbackRecorder, optional: true },
// display: { type: Object, optional: true },
// displayName: { type: String, optional: true },
// noContentHelp: { type: String, optional: true },
// searchViewId: { type: [Number, false], optional: true },
// viewId: { type: [Number, false], optional: true },
// views: { type: Array, element: Array, optional: true },
// viewSwitcherEntries: { type: Array, optional: true },

export const standardViewProps = {
    info: {
        type: Object,
    },
    resModel: String,
    arch: { type: String },
    comparison: { validate: () => true }, // fix problem with validation with type: [Object, null]
    // Issue OWL: https://github.com/odoo/owl/issues/910
    context: { type: Object },
    domain: { type: Array },
    fields: { type: Object, elements: Object },
    relatedModels: { type: Object, elements: Object, optional: true },
    groupBy: { type: Array, elements: String },
    limit: { type: Number, optional: true },
    orderBy: { type: Array, elements: String },
    useSampleModel: { type: Boolean },
    state: { type: Object, optional: true },
    globalState: { type: Object, optional: true },
    resId: { type: [Number, Boolean], optional: true },
    resIds: { type: Array, optional: true },
    bannerRoute: { type: String, optional: true },
    className: { type: String, optional: true },
    searchMenuTypes: { type: Array, elements: String },
    selectRecord: { type: Function, optional: true },
    createRecord: { type: Function, optional: true },
    noBreadcrumbs: { type: Boolean, optional: true },
};
