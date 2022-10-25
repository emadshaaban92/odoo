/** @odoo-module **/

export class RecordInfo {

    constructor({ record }) {
        this.record = record;
        /**
         * Listeners that are bound to this record, to be notified of
         * change in dependencies of compute, related and "on change".
         */
        this.listeners = [];
        /**
         * Map between listeners that are observing this record and array of
         * information about how the record is observed.
         */
        this.listenersOnRecord = new Map();
        /**
         * Map between fields and a Map between listeners that are observing
         * the field and array of information about how the field is observed.
         */
        this.listenersOnField = new Map();
    }

}
