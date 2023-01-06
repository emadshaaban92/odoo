# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_dk_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_dk_fiscal_position(template_code),
        }

    def _get_dk_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'a6610',
            'property_account_payable_id': 'a8440',
            'property_account_expense_categ_id': 'a2010',
            'property_account_income_categ_id': 'a1010',
            'property_account_expense_id': 'a2010',
            'property_account_income_id': 'a1010',
            'property_stock_account_input_categ_id': 'a8450',
            'property_stock_account_output_categ_id': 'a6670',
            'property_stock_valuation_account_id': 'a6530',
            'code_digits': '4',
            'use_anglo_saxon': True,
            'cash_account_code_prefix': '681',
            'bank_account_code_prefix': '682',
            'transfer_account_code_prefix': '683',
        }

    def _get_dk_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.dk',
                'account_default_pos_receivable_account_id': 'a6611',
                'income_currency_exchange_account_id': 'a4670',
                'expense_currency_exchange_account_id': 'a4770',
                'account_journal_early_pay_discount_loss_account_id': 'a4760',
                'account_journal_early_pay_discount_gain_account_id': 'a4660',
            },
        }

    def _get_dk_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax110': {
                'sequence': 110,
                'name': 'Salgsmoms 25%, varer',
                'description': '25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8720',
                        'tag_ids': tags('+UM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8720',
                        'tag_ids': tags('-UM'),
                    }),
                ],
            },
            'tax120': {
                'sequence': 120,
                'name': 'Salgsmoms 25%, ydelser',
                'description': '25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8720',
                        'tag_ids': tags('+UM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8720',
                        'tag_ids': tags('-UM'),
                    }),
                ],
            },
            'tax210': {
                'sequence': 210,
                'name': 'EU Varesalg (Virksomheder) - momsfritaget',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+R-B-MR'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-R-B-MR'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax220': {
                'sequence': 220,
                'name': 'EU Ydelsessalg (Virksomheder) - momsfritaget',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+R-C-MR'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-R-C-MR'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax310': {
                'sequence': 310,
                'name': '3. Land Salg Vare / Ydelser',
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+R-C-UR'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-R-C-UR'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax400': {
                'sequence': 400,
                'name': 'Købsmoms 25%, varer',
                'description': '25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                ],
            },
            'tax410': {
                'sequence': 410,
                'name': 'Købsmoms 25% indeholdt, varer',
                'description': '25% indeholdt',
                'amount': 25.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                ],
            },
            'tax420': {
                'sequence': 420,
                'name': 'Købsmoms 25%, ydelser',
                'description': '25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                ],
            },
            'tax425': {
                'sequence': 420,
                'name': 'Købsmoms 25% indeholdt, ydelser',
                'description': '25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'price_include': True,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                ],
            },
            'tax430': {
                'sequence': 430,
                'name': 'Køb omvendt betalingspligt',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8725',
                        'tag_ids': tags('-UM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-UM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8725',
                        'tag_ids': tags('+KM'),
                    }),
                ],
            },
            'tax450': {
                'sequence': 450,
                'name': 'Restaurationsmoms 6,25%, købsmoms',
                'description': '6,25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 25,
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': 75,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 25,
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': 75,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax460': {
                'sequence': 450,
                'name': 'Restaurationsmoms indeholdt 6,25%, købsmoms',
                'description': '6,25%',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'price_include': True,
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 25,
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': 75,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 25,
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': 75,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax510': {
                'sequence': 510,
                'name': 'EU Varekøb',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+R-A-V'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8730',
                        'tag_ids': tags('-MVU'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-R-A-V'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8730',
                        'tag_ids': tags('+MVU'),
                    }),
                ],
            },
            'tax520': {
                'sequence': 520,
                'name': 'EU Ydelseskøb',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+R-A-Y'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8731',
                        'tag_ids': tags('-MYUOB'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-R-A-Y'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8731',
                        'tag_ids': tags('+MYUOB'),
                    }),
                ],
            },
            'tax610': {
                'sequence': 610,
                'name': '3. Land Varekøb',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+MVU'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8730',
                        'tag_ids': tags('-KM'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-MVU'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8730',
                        'tag_ids': tags('+KM'),
                    }),
                ],
            },
            'tax620': {
                'sequence': 620,
                'name': '3. Land Ydelseskøb',
                'amount': 25.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('+KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8731',
                        'tag_ids': tags('-MYUOB'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8740',
                        'tag_ids': tags('-KM'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a8731',
                        'tag_ids': tags('+MYUOB'),
                    }),
                ],
            },
            'tax710': {
                'sequence': 710,
                'name': 'Olie- og flaskegasafgift',
                'amount': 100.0,
                'amount_type': 'division',
                'price_include': True,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 92.83,
                        'repartition_type': 'tax',
                        'account_id': 'a8775',
                        'tag_ids': tags('+OFA'),
                    }),
                    Command.create({
                        'factor_percent': 7.17,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 92.83,
                        'repartition_type': 'tax',
                        'account_id': 'a8775',
                        'tag_ids': tags('-OFA'),
                    }),
                    Command.create({
                        'factor_percent': 7.17,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax720': {
                'sequence': 720,
                'name': 'Elafgift',
                'amount': 0.896,
                'amount_type': 'fixed',
                'price_include': True,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8775',
                        'tag_ids': tags('+EA'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8775',
                        'tag_ids': tags('-EA'),
                    }),
                ],
            },
            'tax730': {
                'sequence': 730,
                'name': 'Naturgas- og bygasafgift',
                'amount': 100.0,
                'amount_type': 'division',
                'price_include': True,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 92.83,
                        'repartition_type': 'tax',
                        'account_id': 'a8780',
                        'tag_ids': tags('+NOBA'),
                    }),
                    Command.create({
                        'factor_percent': 7.17,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 92.83,
                        'repartition_type': 'tax',
                        'account_id': 'a8780',
                        'tag_ids': tags('-NOBA'),
                    }),
                    Command.create({
                        'factor_percent': 7.17,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax740': {
                'sequence': 740,
                'name': 'Kulafgift',
                'amount': 100.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 92.83,
                        'repartition_type': 'tax',
                        'account_id': 'a8785',
                        'tag_ids': tags('+KA'),
                    }),
                    Command.create({
                        'factor_percent': -92.83,
                        'repartition_type': 'tax',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 92.83,
                        'repartition_type': 'tax',
                        'account_id': 'a8785',
                        'tag_ids': tags('-KA'),
                    }),
                    Command.create({
                        'factor_percent': -92.83,
                        'repartition_type': 'tax',
                    }),
                ],
            },
            'tax750': {
                'sequence': 750,
                'name': 'CO2-afgift',
                'active': False,
                'amount': 0.0,
                'amount_type': 'percent',
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8785',
                        'tag_ids': tags('+CO2A'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a4271',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8785',
                        'tag_ids': tags('-CO2A'),
                    }),
                    Command.create({
                        'factor_percent': -100,
                        'repartition_type': 'tax',
                        'account_id': 'a4271',
                    }),
                ],
            },
            'tax760': {
                'sequence': 760,
                'name': 'Vandafgift',
                'amount': 6.18,
                'amount_type': 'fixed',
                'price_include': True,
                'type_tax_use': 'purchase',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8795',
                        'tag_ids': tags('+VA'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'a8795',
                        'tag_ids': tags('-VA'),
                    }),
                ],
            },
        }

    def _get_dk_fiscal_position(self, template_code):
        return {
            'fiscal_position_template_dk_vat': {
                'name': 'Danmark (Virksomhed)',
                'auto_apply': 1,
                'vat_required': 1,
                'sequence': 10,
                'country_id': 'base.dk',
            },
            'fiscal_position_template_eu': {
                'name': 'EU lande (Privat)',
                'auto_apply': 1,
                'sequence': 11,
                'country_group_id': 'base.europe',
            },
            'fiscal_position_template_eu_taxid': {
                'name': 'EU lande (Virksomhed)',
                'auto_apply': 1,
                'vat_required': 1,
                'sequence': 12,
                'country_group_id': 'base.europe',
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax110',
                        'tax_dest_id': 'tax210',
                    }),
                    Command.create({
                        'tax_src_id': 'tax120',
                        'tax_dest_id': 'tax220',
                    }),
                    Command.create({
                        'tax_src_id': 'tax400',
                        'tax_dest_id': 'tax510',
                    }),
                    Command.create({
                        'tax_src_id': 'tax410',
                        'tax_dest_id': 'tax510',
                    }),
                    Command.create({
                        'tax_src_id': 'tax420',
                        'tax_dest_id': 'tax520',
                    }),
                    Command.create({
                        'tax_src_id': 'tax425',
                        'tax_dest_id': 'tax520',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'a1010',
                        'account_dest_id': 'a1020',
                    }),
                    Command.create({
                        'account_src_id': 'a1011',
                        'account_dest_id': 'a1021',
                    }),
                    Command.create({
                        'account_src_id': 'a2010',
                        'account_dest_id': 'a2020',
                    }),
                    Command.create({
                        'account_src_id': 'a2011',
                        'account_dest_id': 'a2021',
                    }),
                ],
            },
            'fiscal_position_template_3lande': {
                'name': '3. lande (Virksomhed / Privat)',
                'auto_apply': 1,
                'sequence': 13,
                'tax_ids': [
                    Command.create({
                        'tax_src_id': 'tax110',
                        'tax_dest_id': 'tax310',
                    }),
                    Command.create({
                        'tax_src_id': 'tax120',
                        'tax_dest_id': 'tax310',
                    }),
                    Command.create({
                        'tax_src_id': 'tax400',
                        'tax_dest_id': 'tax610',
                    }),
                    Command.create({
                        'tax_src_id': 'tax410',
                        'tax_dest_id': 'tax610',
                    }),
                    Command.create({
                        'tax_src_id': 'tax420',
                        'tax_dest_id': 'tax620',
                    }),
                    Command.create({
                        'tax_src_id': 'tax425',
                        'tax_dest_id': 'tax620',
                    }),
                ],
                'account_ids': [
                    Command.create({
                        'account_src_id': 'a1010',
                        'account_dest_id': 'a1030',
                    }),
                    Command.create({
                        'account_src_id': 'a1011',
                        'account_dest_id': 'a1031',
                    }),
                    Command.create({
                        'account_src_id': 'a2010',
                        'account_dest_id': 'a2030',
                    }),
                    Command.create({
                        'account_src_id': 'a2011',
                        'account_dest_id': 'a2031',
                    }),
                ],
            },
        }
