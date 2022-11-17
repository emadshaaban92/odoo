/** @odoo-module **/

/**
 * @param {number} value
 * @param {number} comparisonValue
 * @returns {number}
 */
export function computeVariation(value, comparisonValue) {
    if (isNaN(value) || isNaN(comparisonValue)) {
        return NaN;
    }
    if (comparisonValue === 0) {
        if (value === 0) {
            return 0;
        } else if (value > 0) {
            return 1;
        } else {
            return -1;
        }
    }
    return (value - comparisonValue) / Math.abs(comparisonValue);
}

/**
 * Returns value clamped to the inclusive range of min and max.
 *
 * @param {number} num
 * @param {number} min
 * @param {number} max
 * @returns {number}
 */
export function clamp(num, min, max) {
    return Math.max(Math.min(num, max), min);
}

/**
 * @param {number} a
 * @param {number} b
 * @returns {number} greatest common divisor of a and b
 */
export function greatestCommonDivisor(a, b) {
    if (b === 0) {
        return a;
    }
    if (a < b) {
        return greatestCommonDivisor(b, a);
    }
    return greatestCommonDivisor(b, a % b);
}
