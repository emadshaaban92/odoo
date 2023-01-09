/** @odoo-module **/

import { ActivityMenu } from "@mail/new/activity/activity_menu";
import { DiscussClientAction } from "@mail/new/discuss/discuss_client_action";
import { messagingService } from "@mail/new/core/messaging_service";
import { ChatWindowContainer } from "@mail/new/chat/chat_window_container";
import { MessagingMenu } from "@mail/new/messaging_menu/messaging_menu";

import { registry } from "@web/core/registry";
import { rtcService } from "./new/rtc/rtc_service";
import { soundEffects } from "./new/core/sound_effects_service";
import { userSettingsService } from "./new/core/user_settings_service";
import { suggestionService } from "./new/suggestion/suggestion_service";
import { storeService } from "./new/core/store_service";
import { chatWindowService } from "./new/chat/chat_window_service";
import { threadService } from "./new/thread/thread_service";
import { messageService } from "./new/thread/message_service";
import { activityService } from "./new/activity/activity_service";
import { chatterService } from "./new/views/chatter_service";

const serviceRegistry = registry.category("services");
serviceRegistry.add("mail.store", storeService);
serviceRegistry.add("mail.activity", activityService);
serviceRegistry.add("mail.chatter", chatterService);
serviceRegistry.add("mail.chat_window", chatWindowService);
serviceRegistry.add("mail.thread", threadService);
serviceRegistry.add("mail.message", messageService);
serviceRegistry.add("mail.messaging", messagingService);
serviceRegistry.add("mail.suggestion", suggestionService);
serviceRegistry.add("mail.rtc", rtcService);
serviceRegistry.add("mail.soundEffects", soundEffects);
serviceRegistry.add("mail.userSettings", userSettingsService);

registry.category("actions").add("mail.action_discuss", DiscussClientAction);

registry
    .category("main_components")
    .add("mail.ChatWindowContainer", { Component: ChatWindowContainer });

registry.category("systray").add(
    "mail.activity_menu",
    {
        Component: ActivityMenu,
    },
    { sequence: 20 }
);
registry.category("systray").add(
    "mail.messaging_menu",
    {
        Component: MessagingMenu,
    },
    { sequence: 25 }
);
