/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { cleanTerm } from "@mail/new/utils/format";
import { Component, xml } from "@odoo/owl";
import { Thread } from "./core/thread_model";

const commandSetupRegistry = registry.category("command_setup");
const commandProviderRegistry = registry.category("command_provider");

// -----------------------------------------------------------------------------
// add @ namespace + provider
// -----------------------------------------------------------------------------
commandSetupRegistry.add("@", {
    debounceDelay: 200,
    emptyMessage: _lt("No user found"),
    name: _lt("users"),
    placeholder: _lt("Search for a user..."),
});

class DialogCommand extends Component {}
DialogCommand.template = xml`
    <div class="o_command_default d-flex align-items-center justify-content-between px-4 py-2 cursor-pointer">
        <t t-slot="name"/>
        <span t-if="props.email" t-out="props.email"/>
    </div>
`;

commandProviderRegistry.add("mail.partner", {
    namespace: "@",
    async provide(env, options) {
        /** @type {import("@mail/new/core/messaging").Messaging} */
        const messaging = env.services["mail.messaging"];
        const results = await messaging.searchPartners(options.searchValue);
        return results.map(function (partner) {
            return {
                Component: DialogCommand,
                action() {
                    messaging.openChat({ partnerId: partner.id });
                },
                name: partner.nameOrDisplayName,
                props: { email: partner.email },
            };
        });
    },
});

// -----------------------------------------------------------------------------
// add # namespace + provider
// -----------------------------------------------------------------------------

commandSetupRegistry.add("#", {
    debounceDelay: 200,
    emptyMessage: _lt("No channel found"),
    name: _lt("channels"),
    placeholder: _lt("Search for a channel..."),
});

commandProviderRegistry.add("mail.channel", {
    namespace: "#",
    async provide(env, options) {
        /** @type {import("@mail/new/core/messaging").Messaging} */
        const messaging = env.services["mail.messaging"];
        const domain = [
            ["channel_type", "=", "channel"],
            ["name", "ilike", cleanTerm(options.searchValue)],
        ];
        const channelsData = await messaging.orm.searchRead(
            "mail.channel",
            domain,
            ["channel_type", "name"],
            { limit: 10 }
        );
        return channelsData.map((data) => ({
            async action() {
                await messaging.joinChannel(data.id, data.name);
                messaging.openDiscussion(
                    Thread.createLocalId({ model: "mail.channel", id: data.id })
                );
            },
            // todo: handle displayname in a way (seems like "group" channels
            // do not have a name
            name: data.name,
        }));
    },
});
