/** @odoo-module */

import { registry } from "@web/core/registry";

const { Component } = owl;

class LogFieldWidget extends Component {
}
LogFieldWidget.template = "exception_tracker.LogFieldWidget"

registry.category("fields").add("log", LogFieldWidget);

