/** @odoo-module **/

import { Component, onMounted, xml } from "@odoo/owl";

export class TourPointer extends Component {
    static template = xml`
        <div t-if="props.pointerState.isVisible" class="o_web_tour">
            <div class="o_web_tour_pointer" t-att-class="props.pointerState.position" t-att-style="style">
                <div class="o_web_tour_pointer_text" t-esc="props.pointerState.text"/>
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
                text: { type: String, optional: true },
            },
        },
        setSizeGetter: { type: Function },
    };
    setup() {
        // TODO-JCB: size should be dynamically computed from this component's element size.
        this.size = { width: 20, height: 20 };
        onMounted(() => {
            this.props.setSizeGetter(() => this.size);
        });
    }
    get style() {
        return `top: ${this.props.pointerState.y}px; left: ${this.props.pointerState.x}px;`;
    }
}
