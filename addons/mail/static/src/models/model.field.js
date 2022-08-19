/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, many, one } from '@mail/model/model_field';
import { clear } from '@mail/model/model_field_command';
import { OnChange } from '@mail/model/model_onchange';

registerModel({
    name: 'Model.Field',
    recordMethods: {
        _computeModelAsIdentifyingField() {
            return this.identifying ? this.model : clear();
        },
        _onChangeCheckConstraints() {
            if (!(['attribute', 'relation'].includes(this.type))) {
                throw new Error(`${this} has unsupported type ${this.type}.`);
            }
            if (this.compute && this.related) {
                throw new Error(`${this} cannot be a related and compute field at the same time.`);
            }
            if (this.type === 'relation') {
                if (!this.relationType) {
                    throw new Error(`${this} must define a relation type in "relationType".`);
                }
                if (!(['many', 'one'].includes(this.relationType))) {
                    throw new Error(`${this} has invalid relation type "${this.relationType}".`);
                }
                if (this.inverses.length === 0) {
                    throw new Error(`${this} must define an inverse relation in "inverse".`);
                }
            }
        },
    },
    fields: {
        compute: attr(),
        default: attr(),
        identifying: attr({
            default: false,
        }),
        // many because of generic Record fields...
        inverses: many('Model.Field', {
            inverse: 'inverses',
        }),
        isCausal: attr({
            default: false,
        }),
        model: one('Model', {
            identifying: true,
            inverse: 'modelFields',
        }),
        modelAsIdentifyingField: one('Model', {
            compute: '_computeModelAsIdentifyingField',
            inverse: 'identifyingFields',
        }),
        name: attr({
            identifying: true,
        }),
        readonly: attr({
            default: false,
        }),
        related: attr(),
        relationType: attr(),
        required: attr({
            default: false,
        }),
        sort: attr({

        }),
        type: attr({
            required: true,
        }),
    },
    onChanges: [
        new OnChange({
            dependencies: ['compute', 'related', 'relationType', 'type'],
            methodName: '_onChangeCheckConstraints',
        }),
    ],
});
