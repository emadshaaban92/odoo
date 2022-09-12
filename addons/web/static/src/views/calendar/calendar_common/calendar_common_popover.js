/** @odoo-module **/

import { is24HourFormat } from "@web/core/l10n/dates";
import { Field } from "../../fields/field";
import { Record } from "../../record";

const { Component } = owl;

export class CalendarCommonPopover extends Component {
    setup() {
        this.time = null;
        this.timeDuration = null;
        this.date = null;
        this.dateDuration = null;

        this.computeDateTimeAndDuration();
    }

    get isEventEditable() {
        return true;
    }
    get isEventDeletable() {
        return this.props.model.canDelete;
    }

    computeDateTimeAndDuration() {
        const record = this.props.record;
        const { start, end } = record;
        const isSameDay = start.hasSame(end, "day");

        if (!record.isTimeHidden && !record.isAllDay && isSameDay) {
            const timeFormat = is24HourFormat() ? "HH:mm" : "hh:mm a";
            this.time = `${start.toFormat(timeFormat)} - ${end.toFormat(timeFormat)}`;

            const duration = end.diff(start, ["hours", "minutes"]);
            const formatParts = [];
            if (duration.hours > 0) {
                const hourString =
                    duration.hours === 1 ? this.env._t("hour") : this.env._t("hours");
                formatParts.push(`h '${hourString}'`);
            }
            if (duration.minutes > 0) {
                const minuteStr =
                    duration.minutes === 1 ? this.env._t("minute") : this.env._t("minutes");
                formatParts.push(`m '${minuteStr}'`);
            }
            this.timeDuration = duration.toFormat(formatParts.join(", "));
        }

        if (!this.props.model.isDateHidden) {
            this.date = this.getFormattedDate(start, end, record.isAllDay);

            if (record.isAllDay) {
                if (isSameDay) {
                    this.dateDuration = this.env._t("All day");
                } else {
                    const duration = end.diff(start, "days");
                    const days = Math.round(duration.days);
                    const dayString = days === 1 ? this.env._t("day") : this.env._t("days");
                    this.dateDuration = duration.toFormat(`d '${dayString}'`);
                }
            }
        }
    }
    getFormattedDate(start, end, isAllDay) {
        if (isAllDay) {
            end = end.minus({ days: 1 });
        }
        const isSameDay = start.hasSame(end, "day");
        if (!isSameDay && start.hasSame(end, "month")) {
            // Simplify date-range if an event occurs into the same month (eg. "4-5 August 2019")
            return start.toFormat("LLLL d") + "-" + end.toFormat("d, y");
        } else {
            return isSameDay
                ? start.toFormat("DDDD")
                : start.toFormat("DDD") + " - " + end.toFormat("DDD");
        }
    }

    onEditEvent() {
        this.props.editRecord(this.props.record);
        this.props.close();
    }
    onDeleteEvent() {
        this.props.deleteRecord(this.props.record);
        this.props.close();
    }
}
CalendarCommonPopover.components = {
    Field,
    Record,
};
CalendarCommonPopover.template = "web.CalendarCommonPopover";
CalendarCommonPopover.props = {
    close: Function,
    record: Object,
    model: Object,
    createRecord: Function,
    deleteRecord: Function,
    editRecord: Function,
};
