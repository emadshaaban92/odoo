/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { registry } from "@web/core/registry";
import { FloatFactorField } from "@web/views/fields/float_factor/float_factor_field";
import { FloatToggleField } from "@web/views/fields/float_toggle/float_toggle_field";
import { FloatTimeField } from "@web/views/fields/float_time/float_time_field";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const { Component } = owl;


export class TimesheetUOM extends Component {

    setup() {
        this.timesheetUOMService = useService("new_timesheet_uom");
        this.companyService = useService("company");
    }

    get timesheetComponent() {
        return this.timesheetUOMService.timesheetComponent;
    }

    get timesheetComponentProps() {
        return this.timesheetUOMService.getTimesheetComponentProps(this.props);
    }

}

TimesheetUOM.props = {
    ...standardFieldProps,
};

TimesheetUOM.template = "hr_timesheet.TimesheetUOM";

TimesheetUOM.components = { FloatFactorField, FloatToggleField, FloatTimeField };

registry.category("fields").add("timesheet_uom", TimesheetUOM);
