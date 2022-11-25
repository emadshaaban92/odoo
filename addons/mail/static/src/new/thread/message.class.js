/** @odoo-module */

export class Message {
    /**
     * @type {Number}
     */
    id;
    /**
     * @type {Array}
     */
    attachments;
    /**
     * @type {string}
     */
    body;

    /**
     * @param {Object} data
     */
    constructor(data) {
        Object.assign(this, data);
    }
}
