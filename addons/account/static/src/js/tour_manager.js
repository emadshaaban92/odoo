odoo.define('web_tour.account.TourManager', function (require) {
'use strict';

var ajax = require('web.ajax');
var session = require('web.session');
var TourManager = require('web_tour.TourManager');
var utils = require('web.utils');

TourManager.include({
    register: function () {
        var self = this;
        var args = Array.prototype.slice.call(arguments);
        var name = args[0];
        return this._super.apply(this, arguments).then(function () {
            var tour = self.tours[name];
            if (!self.running_tour || !tour || !tour.extra.l10n) {
                return Promise.resolve();
            }
            var current_company = false;
            var company_name = false;
            var account_fiscal_country_code = false;

            if (session.user_context.allowed_company_ids) {
                current_company = session.user_context.allowed_company_ids[0];
            } else if (session.user_companies) {
                current_company = session.user_companies.current_company;
            } else if (session.website_company_id) { // for Frontend (Website) side
                current_company = session.website_company_id;
            }
            company_name = utils.get_cookie('company_name') || false;
            if ((!current_company || session.is_website_user) && company_name) {
                tour.extra = {
                    'company_name': company_name,
                    'company_account_fiscal_country_code': utils.get_cookie('account_fiscal_country_code') || false,
                };
                return Promise.resolve();
            } else if (current_company) {
                return ajax.rpc('/web/dataset/call_kw', {
                    model: 'res.company',
                    method: 'search_read',
                    args: [[['id', '=', current_company]], ['account_fiscal_country_code', 'name']],
                    kwargs: {
                        context: session.user_context,
                    },
                }).then((records) => {
                    if (records.length) {
                        company_name = records[0].name;
                        account_fiscal_country_code = records[0].account_fiscal_country_code || false;
                    }
                    tour.extra = {
                        'company_name': company_name,
                        'company_account_fiscal_country_code': account_fiscal_country_code,
                    };
                });
            } else {
                return Promise.resolve();
            }
        });
    },
});
});
