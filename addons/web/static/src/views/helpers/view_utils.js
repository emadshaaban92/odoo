/** @odoo-module */

import { Field } from "../../fields/field";
import { evaluateExpr } from "../../core/py_js/py";

const X2M_TYPES = ["one2many", "many2many"];
const RELATIONAL_TYPES = [...X2M_TYPES, "many2one"];
const SPECIAL_FIELDS = ["color_field"];

/**
 * @param {any} field
 * @returns {boolean}
 */
export const isRelational = (field) => field && RELATIONAL_TYPES.includes(field.type);

/**
 * @param {any} field
 * @returns {boolean}
 */
export const isX2Many = (field) => field && X2M_TYPES.includes(field.type);

function getViewModeFromNode(node, field) {
    let mode;
    if ("mode" in node.attributes) {
        mode = node.getAttribute("mode").split(",");
    } else {
        const views = Object.keys(field.views);
        if ("list" in views && !("kanban" in views)) {
            mode = ["list"];
        } else if ("kanban" in views && !("list" in views)) {
            mode = ["kanban"];
        } else {
            mode = ["kanban", "list"];
        }
    }
    return mode.map((m) => (m === "tree" ? "list" : m));
}

/**
 * @param {number | number[]} idsList
 * @returns {number[]}
 */
export const getIds = (idsList) => {
    if (Array.isArray(idsList)) {
        if (idsList.length === 2 && typeof idsList[1] === "string") {
            return [idsList[0]];
        } else {
            return idsList;
        }
    } else if (idsList) {
        return [idsList];
    } else {
        return [];
    }
};

export class FieldParser {
    /**
     * @param {any} fields
     * @param {string} viewType
     */
    constructor(fields, viewType) {
        this.fields = fields;
        this.viewType = viewType;
        this.parsedFields = Object.create(null);
        this.relations = {};
    }

    get record() {
        return {
            fields: this.fields,
            viewType: this.viewType,
        };
    }

    /**
     * @param {Element} node
     * @param {(fieldName: string) => any} [getFieldInfo=(fieldName)=>fieldName]
     * @returns {{ name: string, field: any, widget: string | false }}
     */
    addField(node, getFieldInfo) {
        const fieldName = node.getAttribute("name");
        const widget = node.getAttribute("widget");
        const field = this.fields[fieldName];
        const options = evaluateExpr(node.getAttribute("options") || "{}");
        this.parsedFields[fieldName] = getFieldInfo ? getFieldInfo(fieldName) : fieldName;
        if (isRelational(field)) {
            const relatedFields = [];
            const FieldClass = Field.getTangibleField(this.record, widget, fieldName);
            if (FieldClass.fieldsToFetch) {
                relatedFields.push(...FieldClass.fieldsToFetch);
            }
            for (const specialFieldDef of SPECIAL_FIELDS) {
                const specialFieldName = options[specialFieldDef];
                if (specialFieldName) {
                    relatedFields.push(specialFieldName);
                }
            }
            this.addRelation(field.relation, ...relatedFields);
            if (X2M_TYPES.includes(field.type) && FieldClass.useSubView) {
                field.viewMode = getViewModeFromNode(node, field);
            }
        }
        return { name: fieldName, field, widget, options };
    }

    /**
     * @param {string} relation
     * @param  {...string} fields
     */
    addRelation(relation, ...fields) {
        if (!fields.length) {
            return;
        }
        if (!(relation in this.relations)) {
            this.relations[relation] = new Set();
        }
        for (const field of fields) {
            this.relations[relation].add(field);
        }
    }

    getFields() {
        return Object.values(this.parsedFields);
    }

    getRelations() {
        const relations = {};
        for (const fieldName in this.relations) {
            relations[fieldName] = [...this.relations[fieldName]];
        }
        return relations;
    }
}
