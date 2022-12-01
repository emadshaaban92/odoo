/** @odoo-module */

import { registry } from "../registry";
import { browser } from "../browser/browser";
import { routeToUrl } from "../browser/router_service";

const commandProviderRegistry = registry.category("command_provider");

commandProviderRegistry.add("debug", {
    provide: (env, options) => {
        const result = [];
        if (env.debug) {
            if (!env.debug.includes("assets")) {
                result.push({
                    action() {
                        browser.location.search = "?debug=assets";
                    },
                    category: "debug",
                    name: env._t("Activate debug mode (with assets)"),
                });
            }
            result.push({
                action() {
                    const route = env.services.router.current;
                    route.search.debug = "";
                    browser.location.href = browser.location.origin + routeToUrl(route);
                },
                category: "debug",
                name: env._t("Deactivate debug mode"),
            });
            result.push({
                action() {
                    const runTestsURL = browser.location.origin + "/web/tests?debug=assets";
                    browser.open(runTestsURL);
                },
                category: "debug",
                name: env._t("Run JS Tests"),
            });
            result.push({
                action() {
                    env.services.action.doAction("web.action_tour_manager_dummy");
                },
                category: "debug",
                name: env._t("Run Tour Manager Dummy"),
            });
            result.push({
                action() {
                    const runTestsURL = browser.location.origin + "/web/tests/mobile?debug=assets";
                    browser.open(runTestsURL);
                },
                category: "debug",
                name: env._t("Run JS Mobile Tests"),
            });
        } else {
            if (options.searchValue.toLowerCase() === "debug") {
                result.push({
                    action() {
                        browser.location.search = "?debug=assets";
                    },
                    category: "debug",
                    name: env._t("Activate debug mode (with assets)"),
                });
            }
        }
        return result;
    },
});
