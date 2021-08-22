odoo.define('website_livechat/static/tests/helpers/mock_models.js', function (require) {
'use strict';

const { MockModels } = require('@mail/../tests/helpers/mock_models');
const { patch } = require('web.utils');

patch(MockModels, 'website_livechat/static/tests/helpers/mock_models.js', {

    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------

    /**
     * @override
     */
    generateServerData() {
        const data = this._super(...arguments);
        Object.assign(data.models, {
            'website.visitor': {
                fields: {
                    country_id: { string: "Country", type: 'many2one', relation: 'res.country' },
                    display_name: { string: "Display name", type: 'string' },
                    // Represent the browsing history of the visitor as a string.
                    // To ease testing this allows tests to set it directly instead
                    // of implementing the computation made on server.
                    // This should normally not be a field.
                    history: { string: "History", type: 'string' },
                    is_connected: { string: "Is connected", type: 'boolean' },
                    lang_name: { string: "Language name", type: 'string' },
                    partner_id: { string: "partner", type: "many2one", relation: 'res.partner' },
                    website_name: { string: "Website name", type: 'string' },
                },
                records: [],
            },
        });
        Object.assign(data.models['mail.channel'].fields, {
            livechat_visitor_id: { string: "Visitor", type: 'many2one', relation: 'website.visitor' },
        });
        return data;
    },

});

});
