/** @odoo-module */

import { session } from '@web/session';
// import { _t } from "@web/core/l10n/translation"; // FIXME don't know why it does not work
const _t = str => str;

/**
 * This script, served with frontend pages, displays buttons in the top left
 * corner to provide the authenticated user an access to his odoo backend.
 * In the case of the page being viewed in the website_preview client action,
 * it will forward some events to its parent.
 */
document.addEventListener('DOMContentLoaded', () => {
    if (session.is_website_user) {
        return;
    }

    if (!window.frameElement) {
        const websiteId = document.documentElement.dataset.websiteId;
        const {pathname, search} = window.location;
        let params = new URLSearchParams(search);
        const enableEditor = params.get('enable_editor');
        params.delete('enable_editor');
        params = params.toString();
        const backendPath = `/web#action=website.website_preview&path=${encodeURIComponent(params ? `${pathname}?${params.toString()}` : pathname)}&website_id=${websiteId}`;

        const autoredirectToBackendAction = !!enableEditor;
        if (autoredirectToBackendAction) {
            document.body.innerHTML = '';
            window.location.replace(`${backendPath}${enableEditor ? '&enable_editor=1' : ''}`);
        } else {
            const frontendToBackendNavEl = document.createElement('div');
            frontendToBackendNavEl.classList.add('o_frontend_to_backend_nav');

            const backendAppsButtonEl = document.createElement('a');
            backendAppsButtonEl.href = '/web';
            backendAppsButtonEl.title = _t("Go to your Odoo Apps");
            backendAppsButtonEl.classList.add('o_frontend_to_backend_apps_btn', 'fa', 'fa-th');
            frontendToBackendNavEl.appendChild(backendAppsButtonEl);

            const backendEditButtonEl = document.createElement('a');
            backendEditButtonEl.href = backendPath;
            backendEditButtonEl.title = _t("Edit your page content");
            backendEditButtonEl.classList.add('o_frontend_to_backend_edit_btn', 'fa', 'fa-cog');
            frontendToBackendNavEl.appendChild(backendEditButtonEl);

            document.body.appendChild(frontendToBackendNavEl);
        }
    } else {
        document.addEventListener('click', (ev) => {
            const isEditorEnabled = document.body.classList.contains('editor_enable');
            const linkEl = ev.target.closest('[href]');
            if (!linkEl) {
                return;
            }

            const {href, host, target, pathname} = linkEl;
            const isNewWindow = target === '_blank';

            const backendRoutes = ['/web', '/web/session/logout'];
            const isInIframe = host === window.location.host && pathname && !backendRoutes.includes(pathname);
            if (href && !isEditorEnabled && !isNewWindow && !isInIframe) {
                window.top.location.replace(href);
            }
        });
        document.addEventListener('keydown', ev => {
            window.frameElement.dispatchEvent(new KeyboardEvent('keydown', ev));
        });
        document.addEventListener('keyup', ev => {
            window.frameElement.dispatchEvent(new KeyboardEvent('keyup', ev));
        });
        // Multiple reasons to do this:
        // - It seems like DOMContentLoaded doesn't always trigger when
        //   listened from the parent window
        // - Having an event that's fire only when the page is from Odoo avoids
        //   weird behaviours. (e.g. if we want to clear out the iframe, it might
        //   fire an DOMContentLoaded on a non odoo page)
        window.frameElement.dispatchEvent(new CustomEvent('OdooFrameContentLoaded'));
    }
});
