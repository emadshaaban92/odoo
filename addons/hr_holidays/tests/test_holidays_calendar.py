# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from freezegun import freeze_time

from odoo.addons.base.tests.common import HttpCase
from odoo.tests.common import tagged
from odoo.tests.common import users

from odoo.addons.hr_holidays.tests.common import TestHrHolidaysCommon

@tagged('post_install', '-at_install')
class TestHolidaysCalendar(HttpCase, TestHrHolidaysCommon):

    @freeze_time("2022-11-01")
    @users('admin')
    def test_hours_time_off_request_calendar_view(self):
        """
        Testing the flow of clicking on a day, save the leave request directly
        and verify that the start/end time are correctly set
        """
        self.env.user.tz = 'UTC'
        calendar = self.env.user.employee_id.resource_calendar_id.attendance_ids
        tuesday_expected_start = calendar[2].hour_from
        tuesday_expected_end = calendar[3].hour_to

        self.start_tour('/', 'time_off_request_calendar_view', login='admin')

        last_leave = self.env['hr.leave'].search([('employee_id.id', '=', self.env.user.employee_id.id)]).sorted(lambda leave: leave.create_date)[-1]
        self.assertEqual(last_leave.date_from.weekday(), 1, "It should be Tuesday")
        self.assertEqual(last_leave.date_from.hour, tuesday_expected_start, "Wrong start of the day")
        self.assertEqual(last_leave.date_to.hour, tuesday_expected_end, "Wrong end of the day")
