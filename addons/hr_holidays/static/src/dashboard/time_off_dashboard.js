/* @odoo-module */

import { TimeOffCard } from './time_off_card';
import { useBus, useService } from "@web/core/utils/hooks";
import { DatePicker } from "@web/core/datepicker/datepicker";

const { Component, useState, onWillStart } = owl;

export class TimeOffDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            date: luxon.DateTime.now(),
            holidays: [],
            is_today: true,
        });
        useBus(this.env.timeOffBus, 'update_dashboard', async () => {
            await this.loadDashboardData()
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData(date=false) {
        const context = {};
        if (this.props && this.props.employeeId !== null) {
            context['employee_id'] = this.props.employeeId;
        }
        if(date){
            this.state.date = date;
            this.state.is_today = date.startOf('day').ts == luxon.DateTime.now().startOf('day').ts;
        }
        this.state.holidays = await this.orm.call(
            'hr.leave.type',
            'get_allocation_data_request',
            [
                this.state.date,
            ],
            {
                context: context
            }
        );
    }
}

TimeOffDashboard.components = { TimeOffCard, DatePicker };
TimeOffDashboard.template = 'hr_holidays.TimeOffDashboard';
TimeOffDashboard.props = ['employeeId'];
