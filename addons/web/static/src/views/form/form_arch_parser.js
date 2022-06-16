/** @odoo-module **/

import { XMLParser } from "@web/core/utils/xml";
import { Field } from "@web/fields/field";
import { archParseBoolean, getActiveActions } from "@web/views/helpers/utils";
import { Widget } from "../widgets/widget";

export class FormArchParser extends XMLParser {
    parse(arch, models, modelName) {
        const xmlDoc = this.parseXML(arch);
        const jsClass = xmlDoc.getAttribute("js_class");
        const disableAutofocus = archParseBoolean(xmlDoc.getAttribute("disable_autofocus") || "");
        const activeActions = getActiveActions(xmlDoc);
        const fieldNodes = {};
        const fieldNextIds = {};
        let autofocusFieldId = null;
        const activeFields = {};
        this.visitXML(xmlDoc, (node) => {
            if (node.tagName === "field") {
                const fieldInfo = Field.parseFieldNode(node, models, modelName, "form", jsClass);
                let fieldId = fieldInfo.name;
                if (fieldInfo.name in fieldNextIds) {
                    fieldId = `${fieldInfo.name}_${fieldNextIds[fieldInfo.name]++}`;
                } else {
                    fieldNextIds[fieldInfo.name] = 1;
                }
                fieldNodes[fieldId] = fieldInfo;
                node.setAttribute("field_id", fieldId);
                if (archParseBoolean(node.getAttribute("default_focus") || "")) {
                    autofocusFieldId = fieldId;
                }
                return false;
            } else if (node.tagName === "div" && node.classList.contains("oe_chatter")) {
                // remove this when chatter fields are declared as attributes on the root node
                return false;
            } else if (node.tagName === "widget") {
                const widgetInfo = Widget.parseWidgetNode(node);
                for (const [name, field] of Object.entries(widgetInfo.fieldDependencies)) {
                    activeFields[name] = {
                        name,
                        type: field.type,
                    };
                }
            }
        });
        // TODO: generate activeFields for the model based on fieldNodes (merge duplicated fields)
        for (const fieldNode of Object.values(fieldNodes)) {
            activeFields[fieldNode.name] = fieldNode;
            // const { onChange, modifiers } = fieldNode;
            // let readonly = modifiers.readonly || [];
            // let required = modifiers.required || [];
            // if (activeFields[fieldNode.name]) {
            //     activeFields[fieldNode.name].readonly = Domain.combine([activeFields[fieldNode.name].readonly, readonly], "|");
            //     activeFields[fieldNode.name].required = Domain.combine([activeFields[fieldNode.name].required, required], "|");
            //     activeFields[fieldNode.name].onChange = activeFields[fieldNode.name].onChange || onChange;
            // } else {
            //     activeFields[fieldNode.name] = { readonly, required, onChange };
            // }
        }
        return {
            arch,
            activeActions,
            activeFields,
            autofocusFieldId,
            disableAutofocus,
            fieldNodes,
            xmlDoc,
            __rawArch: arch,
        };
    }
}
