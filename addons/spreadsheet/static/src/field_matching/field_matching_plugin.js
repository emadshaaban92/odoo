/** @odoo-module */

import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
import { Domain } from "@web/core/domain";

/**
 * @typedef {Object} FilterObjectMatching
 * @property {string} chain
 * @property {number} [offset] offset to apply to the field (for date filters)
 * @property {Domain} domain
 *
 * @typedef {Object} FieldMatchingObject
 * @property {Domain} [domain]
 * @property {Object.<string, FilterObjectMatching>} matches
 */

export class FieldMatchingPlugin extends spreadsheet.CorePlugin {
    constructor() {
        super(...arguments);
        /**
         * @type {Object.<string, FieldMatchingObject>}
         * @private
         */
        this._objects = {};
    }

    /**
     * Register an object to be used with the global filters
     *
     * @param {string} objectId Object ID
     *
     * @private
     */
    register(objectId) {
        this._objects[objectId] = {
            matches: {},
        };
    }

    /**
     * Unregister an object
     *
     * @param {string} objectId
     *
     * @private
     */
    unregister(objectId) {
        delete this._objects[objectId];
    }

    /**
     *
     * @param {string} objectId
     * @returns {Domain}
     */
    getDomain(objectId) {
        this._assertObject(objectId);
        if (!this._objects[objectId].domain) {
            this._computeDomain(objectId);
        }
        return this._objects[objectId].domain;
    }

    /**
     *
     * @param {string} objectId
     * @param {string} filterId
     * @param {FilterObjectMatching} match
     *
     * @private
     */
    setFieldMatching(objectId, filterId, match) {
        this._assertObject(objectId);
        this._objects[objectId].matches[filterId] = match;
        this._invalidateDomain(objectId);
    }

    /**
     * Ensure that the given object id is registered
     *
     * @param {string} objectId
     * @private
     */
    _assertObject(objectId) {
        if (!(objectId in this._objects)) {
            throw new Error(`Unknown object: ${objectId}`);
        }
    }

    /**
     * Compute the full domain of an object, by combining the domain of all
     * filters.
     *
     * @param {string} objectId
     * @private
     */
    _computeDomain(objectId) {
        this._assertObject(objectId);
        const domains = Object.values(this._objects[objectId].matches).map((match) => match.domain);
        this._objects[objectId].domain = Domain.combine(domains, "AND");
    }

    /**
     * Invalidate the domain of an object (typically following a filter update)
     *
     * @param {string} objectId
     * @private
     */
    _invalidateDomain(objectId) {
        this._assertObject(objectId);
        delete this._objects[objectId].domain;
    }
}

FieldMatchingPlugin.getters = ["getDomain"];

export class FieldMatching {
    constructor() {}
}

export const fieldMatchingInstance = new FieldMatching();
