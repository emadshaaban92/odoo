/** @odoo-module **/
import { insert, many, Patch } from '@mail/model';

// ensure load order
import '@mail/models/message';

Patch({
    name: 'Message',
    fields: {
        failureTitle: {
            compute() {
                return this.failureTraces.length > 0 ? this.env._t('Failed Mass Mailing') : this._super();
            },
        },
        failureTraces: many('MailingTrace', {
            compute() {
                return this.traces.filter(trace => trace.isFailure);
            },
        }),
        hasStatusNotification: {
            compute() {
                return this._super() || this.traces.length > 0;
            },
        },
        isSuccess: {
            compute() {
                return this._super() && this.failureTraces.length === 0;
            },
        },
        traces: many('MailingTrace'),
    },
    modelMethods: {
        /**
         *  @override
         */
        convertData(data) {
            const data2 = this._super(data);
            if ('traces' in data) {
                data2.traces = insert(data.traces);
            }
            return data2;
        },
    },
    recordMethods: {
        /**
        * Opens the mailing the message originated from
        */
        openMailingView() {
            return this.messaging.openDocument({ id: this.failureTraces[0].mailing_id, model: 'mailing.mailing' });
        },
    },
});
