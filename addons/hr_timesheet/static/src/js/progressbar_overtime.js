/** @odoo-module **/

import field_registry from 'web.field_registry';
import { FieldProgressBar } from 'web.basic_fields';

const FieldProgressBarOvertime = FieldProgressBar.extend({

    /**
     * @override
     */
    _render_value(v) {
        this._super.apply(this, arguments);
        if (this.value > this.max_value) {
            this.$('.o_progressbar_complete').removeClass('bg-primary');
            this.$('.o_progressbar_complete').addClass('bg-danger');
        } else {
            this.$('.o_progressbar_complete').removeClass('bg-danger');
            this.$('.o_progressbar_complete').addClass('bg-primary');
        }
    },

});

field_registry.add('progressbar_overtime', FieldProgressBarOvertime);

export default FieldProgressBarOvertime;
