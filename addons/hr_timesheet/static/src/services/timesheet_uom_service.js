/** @odoo-module */

import { session } from "@web/session";
import { registry } from "@web/core/registry";
import { formatFloatTime, formatFloatFactor, formatFloat } from "@web/views/fields/formatters";
import { FloatFactorField } from "@web/views/fields/float_factor/float_factor_field";


export const timesheetUOMService = {
    dependencies: ["company"],
    start(env, { company }) {
        return  {
            get _timesheetUOMId() {
                return company.currentCompany.timesheet_uom_id;
            },
            get _timesheetWidget() {
                let timesheet_widget = "float_factor";
                if (this._timesheetUOMId in session.uom_ids) {
                    timesheet_widget = session.uom_ids[this._timesheetUOMId].timesheet_widget;
                }
                return timesheet_widget;
            },
            get timesheetComponent() {
                return registry.category("fields").get(this._timesheetWidget, FloatFactorField);
            },
            getTimesheetComponentProps(props) {
                const factorDependantComponents = ["float_toggle", "float_factor"];
                return factorDependantComponents.includes(this._timesheetWidget) ? this._getFactorCompanyDependentProps(props) : props;
            },
            _getFactorCompanyDependentProps(props) {
                const factor = company.currentCompany.timesheet_uom_factor || props.factor;
                return { ...props, factor };
            },
            get formatter(){
                if (this._timesheetWidget === "float_time") {
                    return formatFloatTime
                }
                const factor = company.currentCompany.timesheet_uom_factor || 1;
                if (this._timesheetWidget === "float_toggle") {
                    return (value, options = {}) => formatFloat(value * factor, options);
                }
                if (this._timesheetWidget === "float_factor") {
                    return (value, options = {}) => formatFloatFactor(value, Object.assign({ factor }, options));
                }
            }
        }
    }
};

registry.category("services").add("timesheetUOM", timesheetUOMService);
