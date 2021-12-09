/** @odoo-module **/

const { Component } = owl;

export class Notification extends Component {
    shouldUpdate() {
        return false;
    }

    get className() {
        let className;
        switch (this.props.type) {
            case "danger":
                className = "bg-danger";
                break;
            case "warning":
                className = "bg-warning";
                break;
            case "success":
                className = "bg-success";
                break;
            case "info":
                className = "bg-info";
                break;
        }
        return className ? `${className} ${this.props.className}` : this.props.className;
    }
}

Notification.template = "web.NotificationWowl";
Notification.props = {
    message: {
        validate: (m) => {
            return (
                typeof m === "string" || (typeof m === "object" && typeof m.toString === "function")
            );
        },
    },
    title: { type: [String, Boolean, { toString: Function }], optional: true },
    type: {
        type: String,
        optional: true,
        validate: (t) => ["warning", "danger", "success", "info"].includes(t),
    },
    className: { type: String, optional: true },
    buttons: {
        type: Array,
        element: {
            type: Object,
            shape: {
                name: { type: String },
                icon: { type: String, optional: true },
                primary: { type: Boolean, optional: true },
                onClick: Function,
            },
        },
    },
    close: { type: Function },
};
Notification.defaultProps = {
    buttons: [],
    className: "",
    type: "warning",
};
