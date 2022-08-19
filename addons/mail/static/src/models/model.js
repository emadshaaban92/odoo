/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr, many } from '@mail/model/model_field';
import { OnChange } from '@mail/model/model_onchange';

registerModel({
    name: 'Model',
    recordMethods: {
        _onChangeCheckConstraints() {
            switch (this.identifyingMode) {
                case 'and':
                    break;
                case 'xor':
                    if (this.identifyingFields.length === 0) {
                        throw new Error(`No identifying fields has been specified for 'xor' identifying mode on ${this}`);
                    }
                    break;
                default:
                    throw new Error(`Unsupported identifying mode "${this.identifyingMode}" on ${this}. Must be one of 'and' or 'xor'.`);
            }
            // TODO move to field itself, with identifying flag
            for (const identifyingField of this.identifyingFields) {
                if (identifyingField.type === 'relation' && identifyingField.relationType !== 'one') {
                    throw new Error(`Identifying field "${identifyingField}" has a relation of type "${identifyingField.relationType}" but identifying field is only supported for "one".`);
                }
                for (const inverseField of identifyingField.inverses) {
                    if (!inverseField.isCausal) {
                        throw new Error(`Identifying field "${identifyingField}" has an inverse "${inverseField}" not declared as "isCausal".`);
                    }
                }
            }
        },
    },
    fields: {
        identifyingFields: many('Model.Field', {
            inverse: 'modelAsIdentifyingField',
            readonly: true,
        }),
        identifyingMode: attr(),
        modelFields: many('Model.Field', {
            inverse: 'model',
            isCausal: true,
        }),
        name: attr({
            identifying: true,
        }),
        records: many('Record', {
            inverse: 'model2',
            isCausal: true,
        }),
    },
    onChanges: [
        new OnChange({
            dependencies: ['identifyingFields'],
            methodName: '_onChangeCheckConstraints',
        }),
    ],
});
