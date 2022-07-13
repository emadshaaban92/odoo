/** @odoo-module **/

import fieldRegistry from 'web.field_registry';
import { _t, _lt } from 'web.core';
import { sprintf } from "@web/core/utils/strings";
import AbstractField from 'web.AbstractField';

const DependOnWidget = AbstractField.extend({
    description: _lt("Blocked By"),
    className: 'depend-on',
    attributes: {
        'role': 'img',
    },
    supportedFieldTypes: ['integer'],

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Like integer fields, this widget always has a value, since the default
     * value is already a valid value.
     *
     * @override
     */
    isSet: function () {
        return true;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Renders an hourglass only for blocked tasks,
     * and adds a tip with the number of blocking tasks.
     *
     * @override
     * @private
     */
    _render: function () {
        if (!this.value) return;

        this.$el.empty();
        this.$el.attr('aria-label', this.string);

        const tip = sprintf(_t('Blocked by %s other task(s)'), this.value);
        this.$el.append(
            $('<span>')
            .attr('role', 'img')
            .attr('title', tip)
            .attr('aria-label', tip)
            .addClass('fa fa-hourglass-half')
        );
    },
});

fieldRegistry.add('depend_on', DependOnWidget);

export default DependOnWidget;
