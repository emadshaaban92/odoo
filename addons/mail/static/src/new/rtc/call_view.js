/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { useMessaging } from "../messaging_hook";
import { CallMainView } from "@mail/new/rtc/call_main_view";

export class CallView extends Component {
    static components = { CallMainView };
    static props = ["thread", "compact?"];
    static template = "mail.call_view";

    setup() {
        this.messaging = useMessaging();
        this.state = useState({
            isFullScreen: false,
        });
    }
    get isMinimized() {
        return false;
    }
    get hasSidebar() {
        return false;
    }
    async activateFullScreen() {
        const el = document.body;
        try {
            if (el.requestFullscreen) {
                await el.requestFullscreen();
            } else if (el.mozRequestFullScreen) {
                await el.mozRequestFullScreen();
            } else if (el.webkitRequestFullscreen) {
                await el.webkitRequestFullscreen();
            }
            this.state.isFullScreen = true;
        } catch {
            this.state.isFullScreen = false;
            // TODO
            /*
            this.messaging.notify({
                message: this.env._t("The FullScreen mode was denied by the browser"),
                type: "warning",
            });
            */
        }
    }
    async deactivateFullScreen() {
        const fullScreenElement = document.webkitFullscreenElement || document.fullscreenElement;
        if (fullScreenElement) {
            if (document.exitFullscreen) {
                await document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {
                await document.mozCancelFullScreen();
            } else if (document.webkitCancelFullScreen) {
                await document.webkitCancelFullScreen();
            }
        }
        this.isFullScreen = false;
    }
}
