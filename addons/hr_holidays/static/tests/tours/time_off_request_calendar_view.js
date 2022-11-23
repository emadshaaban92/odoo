odoo.define('hr_holidays.tour_time_off_request_calendar_view', function (require) {
'use strict';

var tour = require('web_tour.tour');

tour.register('time_off_request_calendar_view', {
    test: true,
    url: '/web',
},
[
    tour.stepUtils.showAppsMenuItem(),
    {
        content: "Open Time Off app",
        trigger: '.o_app[data-menu-xmlid="hr_holidays.menu_hr_holidays_root"]',
    },
    {
        content: "Click on Friday 8th of January",
        trigger: '.fc-day[data-date="2022-11-01"]',
        run: () => {
            const el = document.querySelector('.fc-day-top[data-date="2022-11-01"]').firstChild;
            const fromPosition = el.getBoundingClientRect();
            fromPosition.x += el.offsetWidth / 2;
            fromPosition.y += el.offsetHeight / 2;

            el.dispatchEvent(new MouseEvent("mousedown", {
                bubbles: true,
                which: 1,
                button: 0,
                clientX: fromPosition.x,
                clientY: fromPosition.y}));
            el.dispatchEvent(new MouseEvent("mouseup", {
                bubbles: true,
                which: 1,
                button: 0,
                clientX: fromPosition.x,
                clientY: fromPosition.y }));
        }
    },
    {
        content: "Save the leave",
        trigger: '.btn:contains("Save")',
        run: 'click',
    }
]);
});
