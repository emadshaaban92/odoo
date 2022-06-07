# -*- coding: utf-8 -*-
{
    'name': 'Live Chat',
    'version': '1.0',
    'sequence': 210,
    'summary': 'Chat with your website visitors',
    'category': 'Website/Live Chat',
    'website': 'https://www.odoo.com/app/live-chat',
    'description':
        """
Live Chat Support
==========================

Allow to drop instant messaging widgets on any web page that will communicate
with the current server and dispatch visitors request amongst several live
chat operators.
Help your customers with this chat, and analyse their feedback.

        """,
    'data': [
        "security/im_livechat_channel_security.xml",
        "security/ir.model.access.csv",
        "data/mail_shortcode_data.xml",
        "data/mail_data.xml",
        "data/im_livechat_channel_data.xml",
        "data/im_livechat_chatbot_data.xml",
        'data/digest_data.xml',
        'views/chatbot_script_answer_views.xml',
        'views/chatbot_script_step_views.xml',
        'views/chatbot_script_views.xml',
        "views/rating_views.xml",
        "views/mail_channel_views.xml",
        "views/im_livechat_channel_views.xml",
        "views/im_livechat_channel_templates.xml",
        "views/im_livechat_chatbot_templates.xml",
        "views/res_users_views.xml",
        "views/digest_views.xml",
        "report/im_livechat_report_channel_views.xml",
        "report/im_livechat_report_operator_views.xml"
    ],
    'demo': [
        "data/im_livechat_channel_demo.xml",
        'data/mail_shortcode_demo.xml',
    ],
    'depends': ["mail", "rating", "digest", "utm"],
    'installable': True,
    'application': True,
    'assets': {
        'mail.assets_discuss_public': [
            'im_livechat/static/src/components/*/*',
            'im_livechat/static/src/models/*.js',
        ],
        'web.assets_backend': [
            'im_livechat/static/src/js/im_livechat_channel_form_view.js',
            'im_livechat/static/src/js/im_livechat_channel_form_controller.js',
            'im_livechat/static/src/js/im_livechat_chatbot_form_view.js',
            'im_livechat/static/src/js/im_livechat_chatbot_form_controller.js',
            'im_livechat/static/src/js/im_livechat_chatbot_step_form_view_dialog.js',
            'im_livechat/static/src/js/chatbot_script_answers_m2m_tags.js',
            'im_livechat/static/src/js/chatbot_script_step_o2m.js',
            'im_livechat/static/src/components/*/*.js',
            'im_livechat/static/src/models/*.js',
            'im_livechat/static/src/scss/im_livechat_history.scss',
            'im_livechat/static/src/scss/im_livechat_form.scss',
        ],
        'web.tests_assets': [
            'im_livechat/static/tests/helpers/*.js',
        ],
        'web.qunit_suite_tests': [
            'im_livechat/static/tests/qunit_suite_tests/components/**/*.js',
            'im_livechat/static/src/legacy/public_livechat_constants.js',
            'im_livechat/static/src/legacy/public_livechat_history_tracking.js',
            'im_livechat/static/src/legacy/models/*',
            'im_livechat/static/src/legacy/widgets/*',
            'im_livechat/static/src/legacy/widgets/*/*',
            'im_livechat/static/src/legacy/public_livechat_chatbot.js',
            'im_livechat/static/src/legacy/website_livechat_message_chatbot.js',
        ],
        'web.assets_tests': [
            'im_livechat/static/tests/tours/**/*',
        ],
        'web.assets_qweb': [
            'im_livechat/static/src/components/*/*.xml',
        ],
        # Bundle of External Librairies of the Livechat (Odoo + required modules)
        'im_livechat.external_lib': [
            # Momentjs
            'web/static/lib/moment/moment.js',
            'web/static/lib/luxon/luxon.js',
            # Odoo minimal lib
            'web/static/lib/underscore/underscore.js',
            'web/static/lib/underscore.string/lib/underscore.string.js',
            # jQuery
            'web/static/lib/jquery/jquery.js',
            'web/static/lib/jquery.ui/jquery-ui.js',
            'web/static/lib/jquery/jquery.browser.js',
            'web/static/lib/jquery.ba-bbq/jquery.ba-bbq.js',
            # Qweb2 lib
            'web/static/lib/qweb/qweb2.js',
            # Odoo JS Framework
            'web/static/lib/owl/owl.js',
            'web/static/src/owl2_compatibility/*.js',
            'web/static/src/legacy/js/promise_extension.js',
            'web/static/src/boot.js',
            'web/static/src/legacy/legacy_component.js',
            'web/static/src/core/assets.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/browser/feature_detection.js',
            'web/static/src/core/dialog/dialog.js',
            'web/static/src/core/errors/error_dialogs.js',
            'web/static/src/core/effects/**/*.js',
            'web/static/src/core/hotkeys/hotkey_service.js',
            'web/static/src/core/hotkeys/hotkey_hook.js',
            'web/static/src/core/l10n/dates.js',
            'web/static/src/core/l10n/localization.js',
            'web/static/src/core/l10n/localization_service.js',
            'web/static/src/core/l10n/translation.js',
            'web/static/src/core/main_components_container.js',
            'web/static/src/core/network/rpc_service.js',
            'web/static/src/core/notifications/notification.js',
            'web/static/src/core/notifications/notification_container.js',
            'web/static/src/core/notifications/notification_service.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/transition.js',
            'web/static/src/core/ui/block_ui.js',
            'web/static/src/core/ui/ui_service.js',
            'web/static/src/core/user_service.js',
            'web/static/src/core/utils/components.js',
            'web/static/src/core/utils/functions.js',
            'web/static/src/core/utils/hooks.js',
            'web/static/src/core/utils/strings.js',
            'web/static/src/core/utils/timing.js',
            'web/static/src/core/utils/ui.js',
            'web/static/src/env.js',
            'web/static/src/legacy/utils.js',
            'web/static/src/legacy/js/owl_compatibility.js',
            'web/static/src/legacy/js/libs/download.js',
            'web/static/src/legacy/js/libs/content-disposition.js',
            'web/static/src/legacy/js/libs/pdfjs.js',
            'web/static/src/legacy/js/services/config.js',
            'web/static/src/legacy/js/core/abstract_service.js',
            'web/static/src/legacy/js/core/class.js',
            'web/static/src/legacy/js/core/collections.js',
            'web/static/src/legacy/js/core/translation.js',
            'web/static/src/legacy/js/core/ajax.js',
            'im_livechat/static/src/js/ajax_external.js',
            'web/static/src/legacy/js/core/time.js',
            'web/static/src/legacy/js/core/mixins.js',
            'web/static/src/legacy/js/core/service_mixins.js',
            'web/static/src/legacy/js/core/rpc.js',
            'web/static/src/legacy/js/core/widget.js',
            'web/static/src/legacy/js/core/registry.js',
            'web/static/src/session.js',
            'web/static/src/legacy/js/core/session.js',
            'web/static/src/legacy/js/core/concurrency.js',
            'web/static/src/legacy/js/core/cookie_utils.js',
            'web/static/src/legacy/js/core/utils.js',
            'web/static/src/legacy/js/core/dom.js',
            'web/static/src/legacy/js/core/qweb.js',
            'web/static/src/legacy/js/core/bus.js',
            'web/static/src/legacy/js/services/core.js',
            'web/static/src/legacy/js/core/local_storage.js',
            'web/static/src/legacy/js/core/ram_storage.js',
            'web/static/src/legacy/js/core/abstract_storage_service.js',
            'web/static/src/legacy/js/common_env.js',
            'web/static/src/legacy/js/public/lazyloader.js',
            'web/static/src/legacy/js/public/public_env.js',
            'web/static/src/legacy/js/public/public_root.js',
            'web/static/src/legacy/js/public/public_root_instance.js',
            'web/static/src/legacy/js/public/public_widget.js',
            'web/static/src/legacy/js/services/ajax_service.js',
            'web/static/src/legacy/js/services/local_storage_service.js',
            # Bus, Mail, Livechat
            'bus/static/src/js/longpolling_bus.js',
            'bus/static/src/js/crosstab_bus.js',
            'bus/static/src/js/services/bus_service.js',
            'mail/static/src/js/utils.js',
            'im_livechat/static/src/legacy/public_livechat_constants.js',
            'im_livechat/static/src/legacy/public_livechat_history_tracking.js',
            'im_livechat/static/src/legacy/models/*',
            'im_livechat/static/src/legacy/widgets/*',
            'im_livechat/static/src/legacy/widgets/*/*',
            'im_livechat/static/src/legacy/public_livechat_chatbot.js',
            'im_livechat/static/src/legacy/website_livechat_message_chatbot.js',

            ('include', 'web._assets_helpers'),

            'web/static/lib/bootstrap/scss/_variables.scss',
            'im_livechat/static/src/scss/im_livechat_bootstrap.scss',
            'im_livechat/static/src/legacy/public_livechat.scss',
            'im_livechat/static/src/legacy/public_livechat_chatbot.scss',


            'web/static/src/core/utils/*.scss',

            'mail/static/src/utils/*.js',
            'mail/static/src/js/emojis.js',
            'mail/static/src/component_hooks/*.js',
            'mail/static/src/model/*.js',
            'mail/static/src/models/*.js',
            'im_livechat/static/src/models/*.js',
            'mail/static/src/services/messaging_service.js',
            # Framework JS
            'bus/static/src/js/*.js',
            'bus/static/src/js/services/bus_service.js',
            'bus/static/src/js/services/legacy/legacy_bus_service.js',
            'web/static/lib/luxon/luxon.js',
            'web/static/src/core/**/*',
            # FIXME: debug menu currently depends on webclient, once it doesn't we don't need to remove the contents of the debug folder
            ('remove', 'web/static/src/core/debug/**/*'),
            'web/static/src/env.js',
            'web/static/src/legacy/js/core/dialog.js',
            'web/static/src/legacy/js/core/owl_dialog.js',
            'web/static/src/legacy/js/core/misc.js',
            # 'web/static/src/legacy/js/env.js',
            'web/static/src/legacy/js/fields/field_utils.js',

            'im_livechat/static/src/public/*.js',
            'im_livechat/static/src/services/*.js',
        ]
    },
    'license': 'LGPL-3',
}
