from odoo import models, Command, api, _


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @api.model
    def _get_third_party_checks_country_codes(self):
        """ Return the list of country codes for the countries where third party checks journals should be created
        when installing the COA"""
        return ["AR"]

    def _get_account_journal(self, template_code):
        journal_data = super()._get_account_journal(template_code)

        if self.env.company.country_id.code in self._get_third_party_checks_country_codes():
            journal_data["third_party_check"] = {
                'name': _('Third Party Checks'),
                'type': 'cash',
                'outbound_payment_method_line_ids': [
                    Command.create({'payment_method_id': self.env.ref('l10n_latam_check.account_payment_method_out_third_party_checks').id}),
                ],
                'inbound_payment_method_line_ids': [
                    Command.create({'payment_method_id': self.env.ref('l10n_latam_check.account_payment_method_new_third_party_checks').id}),
                    Command.create({'payment_method_id': self.env.ref('l10n_latam_check.account_payment_method_in_third_party_checks').id}),
                ],
            }
            journal_data["rejected_third_party_check"] = {
                'name': _('Rejected Third Party Checks'),
                'type': 'cash',
                'outbound_payment_method_line_ids': [
                    Command.create({'payment_method_id': self.env.ref('l10n_latam_check.account_payment_method_out_third_party_checks').id}),
                ],
                'inbound_payment_method_line_ids': [
                    Command.create({'payment_method_id': self.env.ref('l10n_latam_check.account_payment_method_new_third_party_checks').id}),
                    Command.create({'payment_method_id': self.env.ref('l10n_latam_check.account_payment_method_in_third_party_checks').id}),
                ],
            }
        return journal_data
