odoo.define('point_of_sale.main', function(require) {
    'use strict';

    const env = require('web.env');
    const Chrome = require('point_of_sale.Chrome');
    const Registry = require('point_of_sale.ComponentsRegistry');
    const { configureGui } = require('point_of_sale.Gui');

    owl.config.mode = env.isDebug() ? 'dev' : 'prod';
    owl.Component.env = env;

    async function startPosApp(webClient) {
        Registry.freeze();
        await env.session.is_bound;
        env.qweb.addTemplates(env.session.owlTemplates);
        await owl.utils.whenReady();
        await webClient.setElement(document.body);
        await webClient.start();
        const chrome = new (Registry.get(Chrome))(null, { webClient });
        await chrome.mount(document.querySelector('.o_action_manager'));
        await chrome.start();
        configureGui({ component: chrome });
    }

    return { startPosApp };
});
