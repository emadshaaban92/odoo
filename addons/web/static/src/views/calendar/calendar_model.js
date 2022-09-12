/** @odoo-module **/

import { deserializeDateTime } from "@web/core/l10n/dates";
import { localization } from "@web/core/l10n/localization";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model } from "../model";
import { deserialize, serialize } from "./date_utils";

export class CalendarModel extends Model {
    setup(params, services) {
        /** @protected */
        this.user = services.user;

        /** @protected */
        this.keepLast = new KeepLast();

        const formViewFromConfig = (this.env.config.views || []).find((view) => view[1] === "form");
        const formViewIdFromConfig = formViewFromConfig ? formViewFromConfig[0] : false;
        this.meta = {
            ...params,
            firstDayOfWeek: localization.weekStart,
            formViewId: params.formViewId || formViewIdFromConfig,
        };

        this.data = {
            filters: {},
            filterSections: {},
            hasCreateRight: null,
            range: null,
            records: {},
            unusualDays: [],
        };
    }
    async load(params = {}) {
        Object.assign(this.meta, params);
        if (!this.meta.date) {
            this.meta.date =
                params.context && params.context.initial_date
                    ? deserializeDateTime(params.context.initial_date)
                    : luxon.DateTime.local();
        }
        const data = { ...this.data };
        await this.keepLast.add(this.updateData(data));
        this.data = data;
        this.notify();
    }

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    get date() {
        return this.meta.date;
    }
    get canCreate() {
        return this.meta.canCreate && this.data.hasCreateRight;
    }
    get canDelete() {
        return this.meta.canDelete;
    }
    get canEdit() {
        return this.meta.canEdit;
    }
    get eventLimit() {
        return this.meta.eventLimit;
    }
    get exportedState() {
        return this.meta;
    }
    get fieldMapping() {
        return this.meta.fieldMapping;
    }
    get fields() {
        return this.meta.fields;
    }
    get filterSections() {
        return Object.values(this.data.filterSections);
    }
    get firstDayOfWeek() {
        return this.meta.firstDayOfWeek;
    }
    get formViewId() {
        return this.meta.formViewId;
    }
    get hasAllDaySlot() {
        return (
            this.meta.fieldMapping.all_day ||
            this.meta.fields[this.meta.fieldMapping.date_start].type === "date"
        );
    }
    get hasEditDialog() {
        return this.meta.hasEditDialog;
    }
    get hasQuickCreate() {
        return this.meta.hasQuickCreate;
    }
    get isDateHidden() {
        return this.meta.isDateHidden;
    }
    get isTimeHidden() {
        return this.meta.isTimeHidden;
    }
    get popoverFields() {
        return this.meta.popoverFields;
    }
    get rangeEnd() {
        return this.data.range.end;
    }
    get rangeStart() {
        return this.data.range.start;
    }
    get records() {
        return this.data.records;
    }
    get resModel() {
        return this.meta.resModel;
    }
    get scale() {
        return this.meta.scale;
    }
    get scales() {
        return this.meta.scales;
    }
    get unusualDays() {
        return this.data.unusualDays;
    }

    //--------------------------------------------------------------------------

    async createFilter(fieldName, filterValue) {
        const info = this.meta.filtersInfo[fieldName];
        if (info && info.writeFieldName && info.writeResModel) {
            const data = {
                user_id: this.user.userId,
                [info.writeFieldName]: filterValue,
            };
            if (info.filterFieldName) {
                data[info.filterFieldName] = true;
            }
            await this.orm.create(info.writeResModel, [data]);
            await this.load();
        }
    }
    async createRecord(record) {
        const rawRecord = this.buildRawRecord(record);
        const context = this.makeContextDefaults(record);
        await this.orm.create(this.meta.resModel, [rawRecord], { context });
        await this.load();
    }
    async unlinkFilter(fieldName, recordId) {
        const info = this.meta.filtersInfo[fieldName];
        if (info && info.writeResModel) {
            await this.orm.unlink(info.writeResModel, [recordId]);
            await this.load();
        }
    }
    async unlinkRecord(recordId) {
        await this.orm.unlink(this.meta.resModel, [recordId]);
        await this.load();
    }
    async updateFilters(fieldName, filters) {
        const section = this.data.filterSections[fieldName];
        if (section) {
            for (const value in filters) {
                const active = filters[value];
                const filter = section.filters.find((filter) => filter.value == value);
                if (filter) {
                    filter.active = active;
                    const info = this.meta.filtersInfo[fieldName];
                    if (
                        filter.recordId &&
                        info &&
                        info.writeFieldName &&
                        info.writeResModel &&
                        info.filterFieldName
                    ) {
                        const data = {
                            [info.filterFieldName]: active,
                        };
                        await this.orm.write(info.writeResModel, [filter.recordId], data);
                    }
                }
            }
        }
        await this.load();
    }
    async updateRecord(record, options = {}) {
        const rawRecord = this.buildRawRecord(record, options);
        delete rawRecord.name; // name is immutable.
        await this.orm.write(this.meta.resModel, [record.id], rawRecord, {
            context: { from_ui: true },
        });
        await this.load();
    }

    //--------------------------------------------------------------------------

    buildRawRecord(partialRecord, options = {}) {
        const data = {};
        data[this.meta.fieldMapping.create_name_field || "name"] = partialRecord.title;

        let start = partialRecord.start;
        let end = partialRecord.end;

        if (!end || !end.isValid) {
            // Set end date if not existing
            if (partialRecord.isAllDay) {
                end = start;
            } else {
                // in week mode or day mode, convert allday event to event
                end = start.plus({ hours: 2 });
            }
        } else if (partialRecord.isAllDay) {
            end = end.minus({ days: 1 });
        }

        const isDateEvent = this.fields[this.meta.fieldMapping.date_start].type === "date";
        // An "all day" event without the "all_day" option is not considered
        // as a 24h day. It's just a part of the day (by default: 7h-19h).
        if (partialRecord.isAllDay) {
            if (!this.hasAllDaySlot && !isDateEvent && !partialRecord.id) {
                // default hours in the user's timezone
                start = start.set({ hours: 7 });
                end = end.set({ hours: 19 });
            }
        }

        if (this.meta.fieldMapping.all_day) {
            data[this.meta.fieldMapping.all_day] = partialRecord.isAllDay;
        }

        data[this.meta.fieldMapping.date_start] = serialize(
            start,
            partialRecord.isAllDay && this.hasAllDaySlot
                ? "date"
                : this.fields[this.meta.fieldMapping.date_start].type
        );
        if (this.meta.fieldMapping.date_stop) {
            data[this.meta.fieldMapping.date_stop] = serialize(
                end,
                partialRecord.isAllDay && this.hasAllDaySlot
                    ? "date"
                    : this.fields[this.meta.fieldMapping.date_start].type
            );
        }

        if (this.meta.fieldMapping.date_delay) {
            if (this.meta.scale !== "month" || !options.moved) {
                data[this.meta.fieldMapping.date_delay] = end.diff(start, "hours").hours;
            }
        }
        return data;
    }
    makeContextDefaults(record) {
        const { fieldMapping, scale } = this.meta;

        const rawRecord = this.buildRawRecord(record);
        if (["month", "year"].includes(scale)) {
            rawRecord[fieldMapping.all_day || "allday"] = true;
        }

        const context = { ...this.meta.context };
        const fieldNames = [
            fieldMapping.create_name_field || "name",
            fieldMapping.date_start,
            fieldMapping.date_stop,
            fieldMapping.date_delay,
            fieldMapping.all_day || "allday",
        ];
        for (const fieldName of fieldNames) {
            // fieldName could be in rawRecord but not defined
            if (rawRecord[fieldName] !== undefined) {
                context[`default_${fieldName}`] = rawRecord[fieldName];
            }
        }

        return context;
    }

    //--------------------------------------------------------------------------
    // Protected
    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    async updateData(data) {
        if (data.hasCreateRight === null) {
            data.hasCreateRight = await this.orm.call(this.meta.resModel, "check_access_rights", [
                "create",
                false,
            ]);
        }
        data.range = this.computeRange();
        if (this.meta.showUnusualDays) {
            data.unusualDays = await this.loadUnusualDays(data);
        }

        const { sections, dynamicFiltersInfo } = await this.loadFilters(data);

        // Load records and dynamic filters only with fresh filters
        data.filterSections = sections;
        data.records = await this.loadRecords(data);
        const dynamicSections = await this.loadDynamicFilters(data, dynamicFiltersInfo);

        // Apply newly computed filter sections
        Object.assign(data.filterSections, dynamicSections);

        // Remove records that don't match dynamic filters
        for (const [recordId, record] of Object.entries(data.records)) {
            for (const [fieldName, filterInfo] of Object.entries(dynamicSections)) {
                for (const filter of filterInfo.filters) {
                    const rawValue = record.rawRecord[fieldName];
                    const value = Array.isArray(rawValue) ? rawValue[0] : rawValue;
                    if (filter.value === value && !filter.active) {
                        delete data.records[recordId];
                    }
                }
            }
        }
    }

    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    computeRange() {
        const { scale, date, firstDayOfWeek } = this.meta;
        let start = date;
        let end = date;

        if (scale !== "week") {
            // startOf("week") does not depend on locale and will always give the
            // "Monday" of the week...
            start = start.startOf(scale);
            end = end.endOf(scale);
        }

        if (["week", "month"].includes(scale)) {
            const weekday = start.weekday < firstDayOfWeek ? firstDayOfWeek - 7 : firstDayOfWeek;
            start = start.set({ weekday });
            end = start.plus({ weeks: scale === "week" ? 1 : 6, days: -1 });
        }

        start = start.startOf("day");
        end = end.endOf("day");

        return { start, end };
    }

    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    computeDomain(data) {
        return [
            ...this.meta.domain,
            ...this.computeRangeDomain(data),
            ...this.computeFiltersDomain(data),
        ];
    }
    /**
     * @protected
     */
    computeFiltersDomain(data) {
        // List authorized values for every field
        // fields with an active "all" filter are skipped
        const authorizedValues = {};
        const avoidValues = {};

        for (const [fieldName, filterSection] of Object.entries(data.filterSections)) {
            // Skip "all" filters because they do not affect the domain
            const filterAll = filterSection.filters.find((f) => f.type === "all");
            if (!(filterAll && filterAll.active)) {
                const filterSectionInfo = this.meta.filtersInfo[fieldName];

                // Loop over subfilters to complete authorizedValues
                for (const filter of filterSection.filters) {
                    if (filterSectionInfo.writeResModel) {
                        if (!authorizedValues[fieldName]) {
                            authorizedValues[fieldName] = [];
                        }
                        if (filter.active) {
                            authorizedValues[fieldName].push(filter.value);
                        }
                    } else {
                        if (!filter.active) {
                            if (!avoidValues[fieldName]) {
                                avoidValues[fieldName] = [];
                            }
                            avoidValues[fieldName].push(filter.value);
                        }
                    }
                }
            }
        }

        // Compute the domain
        const domain = [];
        for (const field in authorizedValues) {
            domain.push([field, "in", authorizedValues[field]]);
        }
        for (const field in avoidValues) {
            if (avoidValues[field].length > 0) {
                domain.push([field, "not in", avoidValues[field]]);
            }
        }
        return domain;
    }
    /**
     * @protected
     */
    computeRangeDomain(data) {
        const { fieldMapping } = this.meta;
        const formattedEnd = serialize(data.range.end, "datetime");
        const formattedStart = serialize(data.range.start, "datetime");

        const domain = [[fieldMapping.date_start, "<=", formattedEnd]];
        if (fieldMapping.date_stop) {
            domain.push([fieldMapping.date_stop, ">=", formattedStart]);
        } else if (!fieldMapping.date_delay) {
            domain.push([fieldMapping.date_start, ">=", formattedStart]);
        }
        return domain;
    }

    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    fetchUnusualDays(data) {
        return this.orm.call(this.meta.resModel, "get_unusual_days", [
            serialize(data.range.start, "datetime"),
            serialize(data.range.end, "datetime"),
        ]);
    }
    /**
     * @protected
     */
    async loadUnusualDays(data) {
        const unusualDays = await this.fetchUnusualDays(data);
        return Object.entries(unusualDays)
            .filter((entry) => entry[1])
            .map((entry) => entry[0]);
    }

    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    fetchRecords(data) {
        const { fieldNames, resModel } = this.meta;
        return this.orm.searchRead(resModel, this.computeDomain(data), fieldNames);
    }
    /**
     * @protected
     */
    async loadRecords(data) {
        const rawRecords = await this.fetchRecords(data);
        const records = {};
        for (const rawRecord of rawRecords) {
            records[rawRecord.id] = this.normalizeRecord(rawRecord);
        }
        return records;
    }
    /**
     * @protected
     * @param {Record<string, any>} rawRecord
     */
    normalizeRecord(rawRecord) {
        const { fields, fieldMapping, filtersInfo, isTimeHidden, scale } = this.meta;

        const startType = fields[fieldMapping.date_start].type;
        let start = deserialize(rawRecord[fieldMapping.date_start], startType);

        let end = start;
        let endType = startType;
        if (fieldMapping.date_stop) {
            endType = fields[fieldMapping.date_stop].type;
            end = deserialize(rawRecord[fieldMapping.date_stop], endType);
        }

        const duration = rawRecord[fieldMapping.date_delay] || 1;

        const isAllDay =
            startType === "date" ||
            (fieldMapping.all_day && rawRecord[fieldMapping.all_day]) ||
            false;

        if (isAllDay) {
            start = start.startOf("day");
            end = end.startOf("day");
        }
        if (!fieldMapping.date_stop && duration) {
            end = start.plus({ hours: duration });
        }
        if (isAllDay && ["week", "month"].includes(scale)) {
            // TODO: a test in year view ?
            end = end.plus({ days: 1 });
        }

        const showTime =
            !(fieldMapping.all_day && rawRecord[fieldMapping.all_day]) &&
            scale === "month" &&
            startType !== "date" &&
            start.day === end.day;

        let colorValue = rawRecord[fieldMapping.color];
        let colorIndex = Array.isArray(colorValue) ? colorValue[0] : colorValue;
        const filterInfo = Object.values(filtersInfo).find((info) => info.colorFieldName);
        if (filterInfo && filterInfo.colorFieldName) {
            colorValue = rawRecord[filterInfo.colorFieldName];
            colorIndex = Array.isArray(colorValue) ? colorValue[0] : colorValue;
        }

        const title = rawRecord[fieldMapping.create_name_field || "display_name"];

        return {
            id: rawRecord.id,
            title,
            isAllDay,
            start,
            startType,
            end,
            endType,
            duration,
            colorIndex,
            isHatched: rawRecord["is_hatched"] || false,
            isStriked: rawRecord["is_striked"] || false,
            isTimeHidden: isTimeHidden || !showTime,
            rawRecord,
        };
    }

    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    loadFilterColor(filterInfo, fieldName, rawRecord, color) {
        const { fields, fieldMapping } = this.meta;
        const field = fields[fieldName];
        const colorField = fields[fieldMapping.color];
        const relatedField = `${fieldName}.${filterInfo.colorFieldName}`;
        let rawValue = null;
        if (
            !!colorField &&
            (field.relation === colorField.relation || colorField.related === relatedField)
        ) {
            if (rawRecord[fieldName]) {
                // The color field is a related field of the current field.
                rawValue = color ? color[fieldMapping.color] : rawRecord[fieldName][0];
            } else {
                // Re use the color of the record
                rawValue = rawRecord[fieldMapping.color];
            }
        } else {
            rawValue = rawRecord[fieldName];
        }
        const value = Array.isArray(rawValue) ? rawValue[0] : rawValue;
        return value || null;
    }
    /**
     * @protected
     */
    fetchFilters(resModel, fieldNames) {
        return this.orm.searchRead(resModel, [["user_id", "=", this.user.userId]], fieldNames);
    }
    /**
     * @protected
     */
    async loadFilters(data) {
        const previousSections = data.filterSections;
        const sections = {};
        const dynamicFiltersInfo = {};
        for (const [fieldName, filterInfo] of Object.entries(this.meta.filtersInfo)) {
            const previousSection = previousSections[fieldName];
            if (filterInfo.writeResModel) {
                sections[fieldName] = await this.loadFilterSection(
                    fieldName,
                    filterInfo,
                    previousSection
                );
            } else {
                dynamicFiltersInfo[fieldName] = { filterInfo, previousSection };
            }
        }
        return { sections, dynamicFiltersInfo };
    }
    /**
     * @protected
     */
    async loadFilterSection(fieldName, filterInfo, previousSection) {
        const fields = [filterInfo.writeFieldName, filterInfo.filterFieldName].filter(Boolean);

        // TO DISCUSS: should we fetch all the filters each time we load ?
        const rawRecords = await this.fetchFilters(filterInfo.writeResModel, fields);
        const previousFilters = previousSection ? previousSection.filters : [];
        const filters = rawRecords.map((r) => {
            const previousRecordFilter = previousFilters.find(
                (f) => f.type === "record" && f.recordId === r.id
            );
            return this.makeFilterRecord(
                filterInfo,
                previousRecordFilter,
                r,
                filterInfo.writeFieldName,
                filterInfo.filterFieldName
            );
        });

        const field = this.meta.fields[fieldName];
        const isUserOrPartner = ["res.users", "res.partner"].includes(field.relation);
        if (isUserOrPartner) {
            const previousUserFilter = previousFilters.find((f) => f.type === "user");
            filters.push(
                this.makeFilterUser(filterInfo, previousUserFilter, fieldName, rawRecords)
            );
        }
        const previousAllFilter = previousFilters.find((f) => f.type === "all");
        filters.push(this.makeFilterAll(previousAllFilter, isUserOrPartner));

        return {
            label: filterInfo.label,
            fieldName,
            filters,
            avatar: {
                field: filterInfo.avatarFieldName,
                model: filterInfo.resModel,
            },
            hasAvatar: !!filterInfo.avatarFieldName,
            write: {
                field: filterInfo.writeFieldName,
                model: filterInfo.writeResModel,
            },
            canCollapse: filters.length > 2,
            canAddFilter: !!filterInfo.writeResModel,
        };
    }
    /**
     * @protected
     */
    async loadDynamicFilters(data, filtersInfo) {
        const fieldNames = Object.keys(filtersInfo);
        if (this.meta.fieldMapping.color) {
            fieldNames.push(this.meta.fieldMapping.color);
        }

        const sections = {};
        for (const [fieldName, { filterInfo, previousSection }] of Object.entries(filtersInfo)) {
            sections[fieldName] = await this.loadDynamicFilterSection(
                data,
                fieldName,
                filterInfo,
                previousSection
            );
        }

        return sections;
    }
    /**
     * @protected
     */
    async loadDynamicFilterSection(data, fieldName, filterInfo, previousSection) {
        const { fields, fieldMapping } = this.meta;
        const field = fields[fieldName];
        const previousFilters = previousSection ? previousSection.filters : [];

        const treatedValues = new Map();
        const relatedIds = new Set();

        for (const record of Object.values(data.records)) {
            if (record.rawRecord[fieldName]) {
                relatedIds.add(record.rawRecord[fieldName][0]);
            }

            const rawValues = ["many2many", "one2many"].includes(field.type)
                ? record.rawRecord[fieldName]
                : [record.rawRecord[fieldName]];

            for (const rawValue of rawValues) {
                const value = Array.isArray(rawValue) ? rawValue[0] : rawValue;
                if (!treatedValues.has(value)) {
                    treatedValues.set(value, { record, rawValue });
                }
            }
        }

        // TODO: refactor this and merge in with loadFilterColor
        //       in order to simplify makeFilterDynamic
        const rawColors =
            filterInfo.colorFieldName && relatedIds.size
                ? await this.orm.searchRead(
                      fields[fieldName].relation,
                      [["id", "in", Array.from(relatedIds)]],
                      [fieldMapping.color]
                  )
                : [];

        const filters = Array.from(treatedValues).map(([value, { record, rawValue }]) => {
            const color = rawColors.find((r) => r.id === value);
            const previousDynamicFilter = previousFilters.find(
                (f) => f.type === "dynamic" && f.value === value
            );
            return this.makeFilterDynamic(
                filterInfo,
                previousDynamicFilter,
                rawValue,
                fieldName,
                record,
                color
            );
        });

        return {
            label: filterInfo.label,
            fieldName,
            filters,
            avatar: {
                field: filterInfo.avatarFieldName,
                model: filterInfo.resModel,
            },
            hasAvatar: !!filterInfo.avatarFieldName,
            write: {
                field: filterInfo.writeFieldName,
                model: filterInfo.writeResModel,
            },
            canCollapse: filters.length > 2,
            canAddFilter: !!filterInfo.writeResModel,
        };
    }
    /**
     * @protected
     */
    makeFilterDynamic(filterInfo, previousFilter, rawValue, fieldName, record, color) {
        const field = this.meta.fields[fieldName];
        const formatter = registry.category("formatters").get(field.type);
        const value = Array.isArray(rawValue) ? rawValue[0] : rawValue;
        return {
            type: "dynamic",
            recordId: null,
            value,
            label: formatter(rawValue) || _t("Undefined"),
            active: previousFilter ? previousFilter.active : true,
            canRemove: false,
            colorIndex: this.loadFilterColor(filterInfo, fieldName, record.rawRecord, color),
            hasAvatar: !!value,
        };
    }
    /**
     * @protected
     */
    makeFilterRecord(filterInfo, previousFilter, record, fieldName, filterFieldName) {
        const raw = record[fieldName];
        const value = Array.isArray(raw) ? raw[0] : raw;
        const field = this.meta.fields[fieldName];
        const isX2Many = ["many2many", "one2many"].includes(field.type);
        const formatter = registry.category("formatters").get(isX2Many ? "many2one" : field.type);
        let active = false;
        if (previousFilter) {
            active = previousFilter.active;
        } else if (filterFieldName) {
            active = record[filterFieldName];
        }
        return {
            type: "record",
            recordId: record.id,
            value,
            label: formatter(raw),
            active,
            canRemove: true,
            colorIndex: this.loadFilterColor(filterInfo, fieldName, record),
            hasAvatar: !!value,
        };
    }
    /**
     * @protected
     */
    makeFilterUser(filterInfo, previousFilter, fieldName, rawRecords) {
        const field = this.meta.fields[fieldName];
        const userFieldName = field.relation === "res.partner" ? "partnerId" : "userId";
        const value = this.user[userFieldName];
        return {
            type: "user",
            recordId: null,
            value,
            label: this.user.name,
            active: previousFilter ? previousFilter.active : true,
            canRemove: false,
            colorIndex: this.loadFilterColor(
                filterInfo,
                fieldName,
                rawRecords.find((r) => r.id === value) || {}
            ),
            hasAvatar: !!value,
        };
    }
    /**
     * @protected
     */
    makeFilterAll(previousAllFilter, isUserOrPartner) {
        return {
            type: "all",
            recordId: null,
            value: "all",
            label: isUserOrPartner
                ? this.env._t("Everybody's calendars")
                : this.env._t("Everything"),
            active: previousAllFilter ? previousAllFilter.active : false,
            canRemove: false,
            colorIndex: null,
            hasAvatar: false,
        };
    }
}
CalendarModel.services = ["user"];
