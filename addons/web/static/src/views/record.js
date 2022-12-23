/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { useModel } from "@web/views/model";
import { RelationalModel } from "@web/views/relational_model";
import { Component, xml, onWillStart, onWillUpdateProps } from "@odoo/owl";

class _Record extends Component {
    setup() {
        const fieldNames = this.props.info.fieldNames || Object.keys(this.props.info.initialValues);
        const activeFields =
            this.props.info.activeFields ||
            Object.fromEntries(
                fieldNames.map((f) => [f, { attrs: {}, options: {}, domain: "[]" }])
            );

        const resId = this.props.info.resId || this.props.info.initialValues?.id;
        this.model = useModel(RelationalModel, {
            resId,
            resModel: this.props.info.resModel,
            fields: this.props.fields,
            viewMode: "form",
            rootType: "record",
            activeFields,
            mode: this.props.info.mode === "edit" ? "edit" : undefined,
            initialValues: this.props.info.initialValues,
        });
        onWillUpdateProps(async (nextProps) => {
            await this.model.load({
                resId: nextProps.info.resId ?? resId,
                mode: nextProps.info.mode,
            });
        });
    }
}
_Record.template = xml`<t t-slot="default" record="model.root"/>`;

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
];
