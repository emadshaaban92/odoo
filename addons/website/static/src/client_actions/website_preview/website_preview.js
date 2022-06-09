/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';

const { Component, onWillStart, useEffect, useRef } = owl;

export class WebsitePreview extends Component {
    setup() {
        this.websiteService = useService('website');

        this.iframeFallbackUrl = '/website/iframefallback';

        this.iframe = useRef('iframe');
        this.iframefallback = useRef('iframefallback');

        onWillStart(async () => {
            await this.websiteService.fetchWebsites();
            this.initialUrl = `/website/force/${this.websiteId}?path=${this.path}`;
        });

        useEffect(() => {
            this.iframe.el.addEventListener('load', () => {
                // This replaces the browser url (/web#action=website...) with
                // the iframe's url (it is clearer for the user).
                this.currentUrl = this.iframe.el.contentDocument.location.href;
                history.pushState({}, this.props.action.display_name, this.currentUrl);

                // Before leaving the iframe, its content is replicated on an
                // underlying iframe, to avoid for white flashes (visible on
                // Chrome Windows/Linux).
                this.iframe.el.contentWindow.addEventListener('beforeunload', () => {
                    this.iframefallback.el.contentDocument.body.replaceWith(this.iframe.el.contentDocument.body.cloneNode(true));
                    $().getScrollingElement(this.iframefallback.el.contentDocument)[0].scrollTop = $().getScrollingElement(this.iframe.el.contentDocument)[0].scrollTop;
                });
            });
        }, () => []);
    }

    get websiteId() {
        let websiteId = this.props.action.context.params && this.props.action.context.params.website_id;
        if (!websiteId) {
            websiteId = this.websiteService.websites[0].id;
        }
        return websiteId;
    }

    get path() {
        let path = this.props.action.context.params && this.props.action.context.params.path;
        if (!path) {
            path = '/';
        }
        return path;
    }
}
WebsitePreview.template = 'website.WebsitePreview';

registry.category('actions').add('website_preview', WebsitePreview);
