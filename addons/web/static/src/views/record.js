/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { useModel } from "@web/views/model";
import { RelationalModel } from "@web/views/relational_model";
import { getFieldClassFromRegistry } from "@web/views/fields/field";
import { Component, xml, onWillStart, onWillUpdateProps } from "@odoo/owl";

const defaultActiveField = { attrs: {}, options: {}, domain: "[]", string: "" };

class _Record extends Component {
    setup() {
        this.model = useModel(RelationalModel, {
            resId: this.props.info.resId,
            resModel: this.props.info.resModel,
            fields: this.props.fields,
            viewMode: "form",
            rootType: "record",
            activeFields: this.getActiveFields(),
            mode: this.props.info.mode === "edit" ? "edit" : undefined,
            initialValues: this.props.info.initialValues,
        });
        onWillUpdateProps(async (nextProps) => {
            await this.model.load({
                resId: nextProps.info.resId,
                mode: nextProps.info.mode,
            });
        });

        if (this.props.info.onRecordChanged) {
            const load = this.model.load;
            this.model.load = async (...args) => {
                const res = await load.call(this.model, ...args);
                const root = this.model.root;
                root.onChanges = async () => {
                    const changes = root.getChanges();
                    this.props.info.onRecordChanged(root, changes);
                };
                return res;
            };
        }
    }

    getActiveFields() {
        if (this.props.info.activeFields) {
            const activeFields = {};
            for (const [fName, fInfo] of Object.entries(this.props.info.activeFields)) {
                activeFields[fName] = { ...defaultActiveField, ...fInfo };

                if (this.props.fields[fName].type.includes("2many")) {
                    const Component = getFieldClassFromRegistry(
                        this.props.fields[fName].type,
                        fInfo.widget,
                        "form"
                    );
                    if (Component.fieldsToFetch) {
                        activeFields[fName].fieldsToFetch = { ...Component.fieldsToFetch };
                    }
                }
            }
            return activeFields;
        }
        return Object.fromEntries(
            this.props.info.fieldNames.map((f) => [f, { ...defaultActiveField }])
        );
    }

    getFieldProps(fName) {
        const activeField = this.model.root.activeFields[fName];
        const field = this.props.fields[fName];
        const props = {
            name: fName,
            type: activeField.widget || field.type,
            record: this.model.root,
        };

        if (field.type.includes("2many")) {
            props.fieldInfo = activeField;
            props.relation = field.relation;
        }

        return props;
    }
}
_Record.template = xml`<t t-slot="default" record="model.root" getFieldProps.bind="getFieldProps"/>`;

export class Record extends Component {
    setup() {
        if (this.props.fields) {
            this.fields = this.props.fields;
        } else {
            const orm = useService("orm");
            onWillStart(async () => {
                this.fields = await orm.call(
                    this.props.resModel,
                    "fields_get",
                    [this.props.fieldNames],
                    {}
                );
            });
        }
    }
}
Record.template = xml`<_Record fields="fields" slots="props.slots" info="props" />`;
Record.components = { _Record };
Record.props = [
    "slots",
    "resModel",
    "fieldNames?",
    "activeFields?",
    "fields?",
    "resId?",
    "mode?",
    "initialValues?",
    "onRecordChanged?",
];
