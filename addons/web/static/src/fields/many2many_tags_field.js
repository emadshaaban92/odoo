/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { standardFieldProps } from "./standard_field_props";

import { CheckBox } from "@web/core/checkbox/checkbox";
import { ColorList } from "@web/core/colorlist/colorlist";
import { TagItem } from "@web/core/tags/tag_item";
import { AutoComplete } from "@web/core/autocomplete/autocomplete";
import { Domain } from "@web/core/domain";
import { useService } from "@web/core/utils/hooks";
import { sprintf } from "@web/core/utils/strings";
import { usePopover } from "@web/core/popover/popover_hook";

const { Component, useState } = owl;

class Many2ManyTagsFieldColorListPopover extends Component {}
Many2ManyTagsFieldColorListPopover.template = "web.Many2ManyTagsFieldColorListPopover";
Many2ManyTagsFieldColorListPopover.components = {
    CheckBox,
    ColorList,
};

export class Many2ManyTagsField extends Component {
    setup() {
        this.state = useState({
            autocompleteValue: "",
        });
        this.orm = useService("orm");
        this.previousColorsMap = {};
        this.popover = usePopover();
    }
    get tags() {
        return this.props.value.records.map((record) => ({
            id: record.id, // datapoint_X
            resId: record.resId, // X
            name: record.data.display_name,
            colorIndex: record.data[this.props.colorField],
        }));
    }
    get canOpenColorDropdown() {
        return this.handlesColor() && this.props.canEditColor;
    }
    get showM2OSelectionField() {
        return !this.props.readonly;
    }
    handlesColor() {
        return !(this.props.colorField === undefined || this.props.colorField === null);
    }
    switchTagColor(colorIndex, tag) {
        const tagRecord = this.props.value.records.find((record) => record.id === tag.id);
        tagRecord.update(this.props.colorField, colorIndex);
        tagRecord.save();
        this.closePopover();
    }
    onTagVisibilityChange(isHidden, tag) {
        const tagRecord = this.props.value.records.find((record) => record.id === tag.id);
        if (tagRecord.data[this.props.colorField] != 0) {
            this.previousColorsMap[tagRecord.resId] = tagRecord.data[this.props.colorField];
        }
        tagRecord.update(
            this.props.colorField,
            isHidden ? 0 : this.previousColorsMap[tagRecord.resId] || 1
        );
        tagRecord.save();
        this.closePopover();
    }

    closePopover() {
        this.popoverCloseFn();
        this.popoverCloseFn = null;
    }

    get sources() {
        return [this.tagsSource];
    }
    get tagsSource() {
        return {
            placeholder: this.env._t("Loading..."),
            options: this.loadTagsSource.bind(this),
        };
    }

    getDomain() {
        return Domain.and([
            this.props.domain,
            Domain.not([["id", "in", this.props.value.currentIds]]),
        ]).toList(this.props.context);
    }

    async loadTagsSource(request) {
        const records = await this.orm.call(this.props.relation, "name_search", [], {
            name: request,
            operator: "ilike",
            args: this.getDomain(),
            context: this.props.context,
        });

        const options = records.map((result) => ({
            value: result[0],
            label: result[1],
        }));

        if (
            this.props.canQuickCreate &&
            request.length &&
            !this.tagExist(
                request,
                options.map((o) => o.label)
            )
        ) {
            options.push({
                label: sprintf(this.env._t(`Create "%s"`), escape(request)),
                realLabel: request,
                classList: "o_m2o_dropdown_option o_m2o_dropdown_option_create",
                // action: this.onCreate.bind(this),
                type: "create",
            });
        }

        if (!request.length && this.props.canQuickCreate) {
            options.push({
                label: this.env._t("Start typing..."),
                classList: "o_m2o_start_typing",
                unselectable: true,
            });
        }

        if (!options.length && !this.props.canQuickCreate) {
            options.push({
                label: this.env._t("No records"),
                classList: "o_m2o_no_result",
                unselectable: true,
            });
        }

        return options;
    }

    tagExist(name, additionalTagNames) {
        return [
            ...this.props.value.records.map((r) => r.data.display_name),
            ...additionalTagNames,
        ].some((n) => n === name);
    }

    onInput({ inputValue }) {
        this.state.autocompleteValue = inputValue;
    }

    onSelect(option) {
        this.state.autocompleteValue = "";
        if (option.type === "create") {
            this.orm
                .call(this.props.relation, "name_create", [option.realLabel], {
                    context: this.props.context,
                })
                .then((data) => {
                    const ids = [...this.props.value.currentIds, data[0]];
                    this.props.value.replaceWith(ids);
                });
        } else {
            const ids = [...this.props.value.currentIds, option.value];
            this.props.value.replaceWith(ids);
        }
    }

    onDelete(tag) {
        const ids = this.props.value.currentIds.filter((id) => id !== tag.resId);
        this.props.value.replaceWith(ids);
    }

    onBadgeClick(ev, tag) {
        if (!this.canOpenColorDropdown) return;
        const isClosed = !document.querySelector(".o_tag_popover");
        if (isClosed) {
            this.currentPopoverEl = null;
        }
        if (this.popoverCloseFn) {
            this.closePopover();
        }
        if (isClosed || this.currentPopoverEl !== ev.currentTarget) {
            this.currentPopoverEl = ev.currentTarget;
            this.popoverCloseFn = this.popover.add(
                ev.currentTarget,
                this.constructor.components.Popover,
                {
                    colors: this.constructor.RECORD_COLORS,
                    tag: tag,
                    switchTagColor: this.switchTagColor.bind(this),
                    onTagVisibilityChange: this.onTagVisibilityChange.bind(this),
                }
            );
        }
    }
}

Many2ManyTagsField.components = {
    AutoComplete,
    Popover: Many2ManyTagsFieldColorListPopover,
    TagItem,
};
Many2ManyTagsField.template = "web.Many2ManyTagsField";
Many2ManyTagsField.defaultProps = {
    canEditColor: true,
    canQuickCreate: true,
};
Many2ManyTagsField.props = {
    ...standardFieldProps,
    canEditColor: { type: Boolean, optional: true },
    canQuickCreate: { type: Boolean, optional: true },
    colorField: { type: String, optional: true },
    placeholder: { type: String, optional: true },
    relation: { type: String },
    domain: { type: Domain },
    context: { type: Object },
};
Many2ManyTagsField.RECORD_COLORS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
Many2ManyTagsField.displayName = _lt("Tags");
Many2ManyTagsField.supportedTypes = ["many2many"];
Many2ManyTagsField.fieldsToFetch = {
    display_name: { name: "display_name", type: "char" },
};

Many2ManyTagsField.extractProps = (fieldName, record, attrs) => {
    const colorField = attrs.options.color_field;
    return {
        colorField: colorField,
        canEditColor:
            !attrs.options.no_edit_color && record.activeFields[fieldName].viewType !== "list",
        relation: record.activeFields[fieldName].relation,
        domain: record.getFieldDomain(fieldName),
        context: record.getFieldContext(fieldName),
        canQuickCreate: !attrs.options.no_quick_create,
    };
};

registry.category("fields").add("many2many_tags", Many2ManyTagsField);
registry.category("fields").add("form.many2many_tags", Many2ManyTagsField);
registry.category("fields").add("list.many2many_tags", Many2ManyTagsField);
