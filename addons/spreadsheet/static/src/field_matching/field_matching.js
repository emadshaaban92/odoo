// /** @odoo-module */

// export const ObjectThatCanBeUsedWithFilters = [];


// PivotPlugin.setup = () => {
//     ObjectThatCanBeUsedWithFilters.push({
//         getObjectIds: () => this.getters.getPivotIds(),
//         getObjectName: (objectId) => this.getters.getPivotName(objectId),
//         getFieldMatching: (objectId, filterId) => this.getters.getPivotFieldMatching(objectId, filterId);
//         setFieldMatching: (objectId, filterId) => this.getters.getPivotFieldMatching(objectId, filterId);
//     })
// }

// Pour le Domain:
// GlobalFiltersCorePlugin.plugin = getters : getDomain(filterId, fieldMatching): Domain




// import GlobalFiltersCorePlugin from "@spreadsheet/global_filters/plugins/global_filters_core_plugin";
// import { Domain } from "@web/core/domain";

// /**
//  * @typedef {Object} FilterObjectMatching
//  * @property {string} chain
//  * @property {number} [offset] offset to apply to the field (for date filters)
//  * @property {Domain} domain
//  *
//  * @typedef {Object} FieldMatchingObject
//  * @property {Domain} [domain]
//  * @property {Object.<string, FilterObjectMatching>} matches
//  */

// export class FieldMatching {
//     constructor() {
//         /**
//          * @type {Object.<string, FieldMatchingObject>}
//          * @private
//          */
//         this._objects = {};
//     }

//     /**
//      * Register an object to be used with the global filters
//      *
//      * @param {string} objectId Object ID
//      */
//     register(objectId) {
//         this._objects[objectId] = {
//             matches: {},
//         };
//     }

//     /**
//      * Unregister an object
//      *
//      * @param {string} objectId
//      */
//     unregister(objectId) {
//         delete this._objects[objectId];
//     }

//     /**
//      *
//      * @param {string} objectId
//      * @returns {Domain}
//      */
//     getDomain(objectId) {
//         this._assertObject(objectId);
//         if (!this._objects[objectId].domain) {
//             this._computeDomain(objectId);
//         }
//         return this._objects[objectId].domain;
//     }

//     /**
//      *
//      * @param {string} objectId
//      * @param {string} filterId
//      * @param {FilterObjectMatching} match
//      */
//     setFieldMatching(objectId, filterId, match) {
//         this._assertObject(objectId);
//         this._objects[objectId].matches[filterId] = match;
//         this._invalidateDomain(objectId);
//     }

//     /**
//      * Ensure that the given object id is registered
//      *
//      * @param {string} objectId
//      * @private
//      */
//     _assertObject(objectId) {
//         if (!(objectId in this._objects)) {
//             throw new Error(`Unknown object: ${objectId}`);
//         }
//     }

//     /**
//      * Compute the full domain of an object, by combining the domain of all
//      * filters.
//      *
//      * @param {string} objectId
//      * @private
//      */
//     _computeDomain(objectId) {
//         this._assertObject(objectId);
//         const domains = Object.values(this._objects[objectId].matches).map((match) => match.domain);
//         this._objects[objectId].domain = Domain.combine(domains, "AND");
//     }

//     /**
//      * Invalidate the domain of an object (typically following a filter update)
//      *
//      * @param {string} objectId
//      * @private
//      */
//     _invalidateDomain(objectId) {
//         this._assertObject(objectId);
//         delete this._objects[objectId].domain;
//     }
// }

// export const fieldMatchingInstance = new FieldMatching();
