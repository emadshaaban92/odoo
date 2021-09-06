odoo.define('point_of_sale.ProductsWidgetControlPanel', function(require) {
    'use strict';

    const { useRef } = owl.hooks;
    const { debounce } = owl.utils;
    const { identifyError } = require('point_of_sale.utils');
    const { ConnectionLostError, ConnectionAbortedError } = require('@web/core/network/rpc_service');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');

    class ProductsWidgetControlPanel extends PosComponent {
        constructor() {
            super(...arguments);
            this.searchWordInput = useRef('search-word-input');
            this.updateSearch = debounce(this.updateSearch, 100);
        }
        mounted() {
            posbus.on('search-product-from-info-popup', this, this.searchProductFromInfo)
        }
        willUnmount() {
            posbus.off('search-product-from-info-popup', this);
        }

        clearSearch() {
            this.searchWordInput.el.value = '';
            this.trigger('clear-search');
        }
        updateSearch(event) {
            this.trigger('update-search', event.target.value);
            if (event.key === 'Enter') {
                // We are passing the searchWordInput ref so that when necessary,
                // it can be modified by the parent.
                this.trigger('try-add-product', { searchWordInput: this.searchWordInput });
            }
        }
        searchProductFromInfo(productName) {
            this.searchWordInput.el.value = productName;
            this.trigger('switch-category', 0);
            this.trigger('update-search', productName);
        }
        async loadProductFromDB() {
            if(!this.searchWordInput.el.value) {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t(''),
                    body: this.env._t("Please first, write a product name within the search bar to look for it in the back-office database !"),
                });
                return;
            }

            try {
                let ProductIds = await this.rpc({
                    model: 'product.product',
                    method: 'search',
                    args: [[['name', 'ilike', this.searchWordInput.el.value + "%"]]],
                    context: this.env.session.user_context,
                });
                if(!ProductIds.length) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t(''),
                        body: this.env._t("No product found"),
                    });
                } else {
                    await this.env.pos._addProducts(ProductIds);
                }
                this.trigger('update-product-list');
            } catch (error) {
                const identifiedError = identifyError(error)
                if (identifiedError instanceof ConnectionLostError || identifiedError instanceof ConnectionAbortedError) {
                    return this.showPopup('OfflineErrorPopup', {
                        title: this.env._t('Network Error'),
                        body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
                    });
                } else {
                    throw error;
                }
            }
        }
    }
    ProductsWidgetControlPanel.template = 'ProductsWidgetControlPanel';

    Registries.Component.add(ProductsWidgetControlPanel);

    return ProductsWidgetControlPanel;
});
