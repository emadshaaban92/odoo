/** @odoo-module **/

import { Component, markup, xml } from "@odoo/owl";

export class TourPointer extends Component {
    static template = xml`
        <div class="o_tooltip" t-att-class="extraClasses" t-att-style="style" t-on-mouseenter="props.onMouseEnter" t-on-mouseleave="props.onMouseLeave">
            <div class="o_tooltip_content">
                <t t-out="contentMarkup"/>
            </div>
        </div>
    `;
    static props = {
        pointerState: {
            type: Object,
            shape: {
                x: Number,
                y: Number,
                isVisible: Boolean,
                position: {
                    validate: (p) => ["top", "bottom", "left", "right"].includes(p),
                },
                content: { type: String, optional: true },
                /**
                 * "bubble": Just the pointer.
                 * "info": The pointer becomes a callout showing the [content].
                 */
                mode: {
                    validate: (m) => ["bubble", "info"].includes(m),
                },
                /**
                 * "in": the anchor is visible in the screen.
                 * "up": needs to scroll up to see the anchor.
                 * "down": needs to scroll down to see the anchor.
                 */
                viewPortState: {
                    validate: (v) => ["in", "up", "down"].includes(v),
                },
                /**
                 * Whether this component should be { display: "fixed" }.
                 */
                fixed: Boolean,
            },
        },
        onMouseEnter: Function,
        onMouseLeave: Function,
    };
    setup() {
        // If anchor is not inside the screen, the pointer should point where to scroll.
        // When mouseenter on the anchor/pointer, show the info (info mode).
        // - on mouseleave, return to bubble mode.
    }
    get extraClasses() {
        return {
            // [this.props.pointerState.mode === "bubble" ? "o_animated" : "active"]: true,
            o_animated: true, // TODO-JCB: Temporarily disable mode toggling. Remove this and uncomment line above.

            // TODO-JCB: Should be removed.
            o_tooltip_visible: this.props.pointerState.isVisible,

            [this.props.pointerState.position]: true,
            o_tooltip_fixed: this.props.pointerState.fixed,
        };
    }
    get contentMarkup() {
        return markup(this.props.pointerState.content);
    }
    get style() {
        return `top: ${this.props.pointerState.y}px; left: ${this.props.pointerState.x}px;`;
    }
}
