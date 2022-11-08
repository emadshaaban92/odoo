/** @odoo-module **/

import { registry } from "@web/core/registry";
import { sprintf } from "@web/core/utils/strings";
import { useService } from "@web/core/utils/hooks";
import { useSetupAction } from "@web/webclient/actions/action_hook";
import { Layout } from "@web/search/layout";

const { Component, useState, onWillStart, markup, onRendered } = owl;


export class ProductPricelistReport extends Component {
    setup() {
        this.action = useService("action");
        this.orm = useService("orm");

        this.MAX_QTY = 5;
        const pastState = this.props.state || {};

        // Putting everything that needs to be reactive on the useState wrapper.

        // While activeIds and activeModel are not necessarily reactive we need
        // them to be keeped for the useSetupAction going back and forward on links.
        this.state = useState({
            activeIds: pastState.active_ids || this.props.action.context.active_ids,
            activeModel: pastState.active_model || this.props.action.context.active_model,
            displayPricelist: pastState.displayPricelist || false,
            html: markup(""),
            pricelists: [],
            quantities: pastState.quantities || [1, 5, 10],
            selectedPricelist: {},
        });

        onWillStart(async () => {
            this.state.pricelists = await this.getPricelists()
            this.state.selectedPricelist = pastState.selectedPricelist || this.state.pricelists[0];

            this.renderHtml();
        });

        onRendered(() => {
            this.env.config.setDisplayName(this.displayName);
        });

        /*
        When following the link of a product and coming back we need to keep the 
        precedent state:
            - if the pricelist was being showed
            - wich pricelist is selected at the moment
            - which quantities
            - the products (or product variants) for which the report was opened
            - if the active model is product.product or product.template
        */
        useSetupAction({
            getLocalState: () => {
                return {
                    active_ids: this.active_ids,
                    active_model: this.active_model,
                    displayPricelist: this.displayPricelist,
                    quantities: this.quantities,
                    selectedPricelist: this.selectedPricelist,
              };
            },
        });
    }

    get activeIds() {
        return this.state.activeIds;
    }

    get activeModel() {
        return this.state.activeModel;
    }

    get displayName() {
        return this.env._t("Pricelist Report");
    }

    get displayPricelist() {
        return this.state.displayPricelist;
    }

    get getReportParams() {
        return {
            active_model: this.activeModel || 'product.template',
            active_ids: this.state.activeIds || [],
            is_visible_title: this.displayPricelist || '',
            pricelist_id: this.selectedPricelist.id || '',
            quantities: this.quantities || [1],
        };
    }

    get html() {
        return this.state.html;
    }

    get pricelists() {
        return this.state.pricelists;
    }

    get quantities() {
        return this.state.quantities;
    }
    get selectedPricelist() {
        return this.state.selectedPricelist;
    }

    // orm calls

    getPricelists() {
        return this.orm.searchRead("product.pricelist", [], ["id", "name"]);
    }

    async renderHtml() {
        let html = await this.orm.call(
            "report.product.report_pricelist", "get_html", [], {data: this.getReportParams}
        );
        this.state.html = markup(html);
    }

    // events

    async onClickAddQty(ev) {
        if (this.quantities.length >= this.MAX_QTY) {
            let message = sprintf(
                this.env._t("At most %s quantities can be displayed simultaneously. Remove a selected quantity to add others."),
                this.MAX_QTY
            );
            await this.action.doAction({
                type: "ir.actions.client",
                tag: "display_notification",
                params: {
                    "type": "warning",
                    "message": message,
                },
            });
            return;
        }

        const qty = parseInt($("input.add-quantity-input")[0].value);
        if (qty && qty > 0) {
            // Check qty already exist.
            if (this.quantities.indexOf(qty) === -1) {
                this.state.quantities.push(qty);
                this.state.quantities = this.state.quantities.sort((a, b) => a - b);
                this.renderHtml();
            } else {
                let message = this.env._t("Quantity already present");
                await this.action.doAction({
                    type: "ir.actions.client",
                    tag: "display_notification",
                    params: {
                        "type": "info",
                        "message": `${message} (${qty}).`,
                    },
                });
            }
        } else {
            await this.action.doAction({
                type: "ir.actions.client",
                tag: "display_notification",
                params: {
                    "type": "info",
                    "message": this.env._t("Please enter a positive whole number."),
                },
            });
        }
    }

    onClickLink(ev) {
        ev.preventDefault();

        let classes = ev.target.getAttribute("class", "");
        let resModel = ev.target.getAttribute("data-model", "");
        let resId = ev.target.getAttribute("data-res-id", "");

        if (classes && classes.includes("o_action") && resModel && resId) {
            this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: resModel,
                res_id: parseInt(resId),
                views: [[false, 'form']],
                target: 'self',
            });
        }
    }

    onClickPrint() {
        this.action.doAction({
            type: 'ir.actions.report',
            report_type: 'qweb-pdf',
            report_name: 'product.report_pricelist',
            report_file: 'product.report_pricelist',
            data: this.getReportParams,
        });
    }

    async onClickRemoveQty(ev) {
        if (this.quantities.length <= 1) {
            await this.action.doAction({
                type: "ir.actions.client",
                tag: "display_notification",
                params: {
                    "type": "warning",
                    "message": this.env._t(
                        "You must leave at least one quantity."
                    ),
                },
            });
            return
        }

        const qty = parseInt(ev.srcElement.parentElement.childNodes[0].data);
        this.state.quantities = this.state.quantities.filter(q => q !== qty);
        this.renderHtml();
    }

    onSelectPricelist(ev) {
        this.state.selectedPricelist = this.pricelists.filter(pricelist => 
            pricelist.id === parseInt(ev.target.value)
        )[0];

        this.renderHtml();
    }

    onToggleDisplayPricelist() {
        this.state.displayPricelist = !this.displayPricelist;
        this.renderHtml();
    }
}

ProductPricelistReport.props = {
    action: { type: Object },
    actionId: { type: Number, optional: true },
    className: { type: String },
    state: { type: Object, optional: true },
    globalState: { type: Object, optional: true },
}
ProductPricelistReport.components = { Layout };
ProductPricelistReport.template = "product.ProductPricelistReport";
registry.category("actions").add("generate_pricelist_report", ProductPricelistReport);
