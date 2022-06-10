/** @odoo-module **/

import ListController from 'web.ListController';
import viewRegistry from 'web.view_registry';
import ListView from 'web.ListView';
import {ComponentWrapper} from 'web.OwlCompatibility';
import {PagePropertiesDialogWrapper} from '@website/components/dialog/page_properties';

const WebsitePageListController = ListController.extend({

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Used to set the new dialog (created by PagePropertiesDialogWrapper for page
     * record).
     */
    setPageManagerDialog(dialog) {
        this.pageManagerDialog = dialog;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    async _callButtonAction(attrs, record) {
        switch (attrs.name) {
            case 'action_optimize_seo':
                this._goToPage(record.data.url, record.data.website_id.res_id, {
                    enable_seo: true,
                });
                break;
            case 'action_manage_page':
                await this._addDialog(record);
                this.pageManagerDialog.open();
                break;
            case 'action_clone_page':
                await this._addDialog(record, 'clone');
                this.pageManagerDialog.open();
                break;
            case 'action_delete_page':
                await this._addDialog(record, 'delete');
                this.pageManagerDialog.open();
                break;
            case 'action_edit_page':
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'ir.ui.view',
                    res_id: record.data.view_id.res_id,
                    views: [[false, 'form']],
                });
                break;
            default:
                return this._super(...arguments);
        }
    },
    /**
     * @private
     */
    _goToPage(path, website, options = {}) {
        this.do_action('website.website_preview', {
            additional_context: {
                params: {
                    path: path,
                    website_id: website || '',
                    ...options,
                }
            },
        });
    },
    /**
     * @private
     */
    async _addDialog(record, mode = '') {
        this._pagePropertiesDialog = new ComponentWrapper(this, PagePropertiesDialogWrapper, {
            setPagePropertiesDialog: this.setPageManagerDialog.bind(this),
            currentPage: record.data.id,
            onClose: this._onCloseDialog.bind(this),
            mode: mode,
        });
        await this._pagePropertiesDialog.mount(this.el);
    },
    /**
     * Removes page properties wrapper when dialog is closed.
     *
     * @private
     */
    _onCloseDialog() {
        if (this._pagePropertiesDialog) {
            this._pagePropertiesDialog.destroy();
        }
        this._pagePropertiesDialog = undefined;
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _onOpenRecord(event) {
        const record = this.model.get(event.data.id, {raw: true});
        this._goToPage(record.data.url, record.data.website_id);
    },
});

const WebsitePageListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: WebsitePageListController,
    }),
});

viewRegistry.add('website_page_list', WebsitePageListView);

export default {
    WebsitePageListController: WebsitePageListController,
    WebsitePageListView: WebsitePageListView,
};
