# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, Command

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_ec_chart_template_data(self, template_code):
        return {
            'account.fiscal.position': self._get_ec_fiscal_position(template_code),
        }

    def _get_ec_template_data(self, template_code):
        return {
            'property_account_receivable_id': 'ec1102050101',
            'property_account_payable_id': 'ec210301',
            'property_account_expense_categ_id': 'ec110307',
            'property_account_income_categ_id': 'ec410201',
            'property_account_expense_id': 'ec52040201',
            'property_stock_account_input_categ_id': 'ec110307',
            'property_stock_account_output_categ_id': 'ec510102',
            'property_stock_valuation_account_id': 'ec110306',
            'code_digits': '4',
            'cash_account_code_prefix': '1101010',
            'bank_account_code_prefix': '1101020',
            'transfer_account_code_prefix': '1101030',
        }

    def _get_ec_res_company(self, template_code):
        return {
            self.env.company.get_external_id()[self.env.company.id]: {
                'account_fiscal_country_id': 'base.ec',
                'account_default_pos_receivable_account_id': 'ec1102050101',
                'income_currency_exchange_account_id': 'ec430501',
                'expense_currency_exchange_account_id': 'ec520304',
                'account_journal_early_pay_discount_loss_account_id': 'ec9993',
                'account_journal_early_pay_discount_gain_account_id': 'ec9994',
            },
        }

    def _get_ec_account_tax(self, template_code):
        tags = self._get_tag_mapper(template_code)
        return {
            'tax_vat_411': {
                'name': 'Iva 12%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 9,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_applied': '421',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat',
                        'tag_ids': tags('+421 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat',
                        'tag_ids': tags('-421 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_412': {
                'name': 'Iva 12% (activos)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '412',
                'l10n_ec_code_applied': '422',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+412 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat',
                        'tag_ids': tags('+422 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat',
                        'tag_ids': tags('-421 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_415': {
                'name': 'Iva 0%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 19,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '415',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+415 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-415 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
            },
            'tax_vat_416': {
                'name': 'Iva 0% (activos)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 20,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '416',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+414 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-414 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
            },
            'tax_vat_413': {
                'name': 'Iva 0% (sin crédito tributario)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 20,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '413',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+413 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-413 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
            },
            'tax_vat_414': {
                'name': 'Iva 0% (activos sin crédito tributario)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 20,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '414',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+414 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-414 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
            },
            'tax_vat_417': {
                'name': 'Iva 0% (exportación bienes)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 21,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '417',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+417 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_goods_exports',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-417 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_goods_exports',
                    }),
                ],
            },
            'tax_vat_418': {
                'name': 'Iva 0% (exportación servicios)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 21,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '418',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+418 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_services_exports',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-418 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_services_exports',
                    }),
                ],
            },
            'tax_vat_419': {
                'name': 'Iva 0% (no objeto/exentas)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 40,
                'amount': 0.0,
                'description': 'IVA EXENTO',
                'l10n_ec_code_base': '419',
                'tax_group_id': 'tax_group_vat_excempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+419 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-419 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_zero',
                    }),
                ],
            },
            'tax_vat_444': {
                'name': 'Iva 12% (reembolso)',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '444',
                'l10n_ec_code_applied': '454',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+412 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_other_downpayments',
                        'tag_ids': tags('+422 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_other_downpayments',
                        'tag_ids': tags('-421 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_510': {
                'name': 'Iva 12%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 9,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '510',
                'l10n_ec_code_applied': '520',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+510 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat',
                        'tag_ids': tags('+520 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-510 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat',
                        'tag_ids': tags('-520 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_511': {
                'name': 'Iva 12% (activos)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '511',
                'l10n_ec_code_applied': '521',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+511 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_assets',
                        'tag_ids': tags('+521 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-511 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_assets',
                        'tag_ids': tags('-521 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_512': {
                'name': 'Iva 12% (sin crédito tributario)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '512',
                'l10n_ec_code_applied': '522',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+512 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('+522 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-512 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'tag_ids': tags('-522 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_513': {
                'name': 'Iva 12% (importación servicios)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '513',
                'l10n_ec_code_applied': '523',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+513 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_service_imports',
                        'tag_ids': tags('+523 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-513 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_service_imports',
                        'tag_ids': tags('-523 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_514': {
                'name': 'Iva 12% (importación bienes)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '514',
                'l10n_ec_code_applied': '524',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+514 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_goods_imports',
                        'tag_ids': tags('+524 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-514 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_goods_imports',
                        'tag_ids': tags('-524 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_515': {
                'name': 'Iva 12% (importación activos)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '515',
                'l10n_ec_code_applied': '525',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+515 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_assets_imports',
                        'tag_ids': tags('+525 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-515 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_assets_imports',
                        'tag_ids': tags('-525 (Reporte 104)'),
                    }),
                ],
            },
            'tax_vat_517': {
                'name': 'Iva 0%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 20,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '517',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+517 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-517 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
            },
            'tax_vat_516': {
                'name': 'Iva 0% (importación bienes)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 20,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '516',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+516 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-516 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
            },
            'tax_vat_518': {
                'name': 'Iva 0% (rise)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 20,
                'amount': 0.0,
                'description': 'IVA 0%',
                'l10n_ec_code_base': '518',
                'tax_group_id': 'tax_group_vat0',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+518 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-518 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
            },
            'tax_vat_541': {
                'name': 'Iva 0% (no objeto de iva)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 30,
                'amount': 0.0,
                'description': 'NO OBJETO DE IVA',
                'l10n_ec_code_base': '541',
                'tax_group_id': 'tax_group_vat_not_charged',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+541 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-541 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
            },
            'tax_vat_542': {
                'name': 'Iva 0% (excento de iva)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 40,
                'amount': 0.0,
                'description': 'IVA EXENTO',
                'l10n_ec_code_base': '542',
                'tax_group_id': 'tax_group_vat_excempt',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+542 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-542 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_purchase_vat_zero',
                    }),
                ],
            },
            'tax_vat_545': {
                'name': 'Iva 12% (reembolso intermediario)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 10,
                'amount': 12.0,
                'description': 'IVA 12%',
                'l10n_ec_code_base': '545',
                'l10n_ec_code_applied': '555',
                'tax_group_id': 'tax_group_vat_12',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+545 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_other_downpayments',
                        'tag_ids': tags('+555 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-545 (Reporte 104)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_other_downpayments',
                        'tag_ids': tags('-555 (Reporte 104)'),
                    }),
                ],
            },
            'tax_withhold_profit_303': {
                'name': '303 10% honorarios profesionales y demas pagos por servicios relacionados con el titulo profesional',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -10.0,
                'description': '303',
                'l10n_ec_code_applied': '353',
                'l10n_ec_code_base': '303',
                'l10n_ec_code_ats': '303',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+303 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_10x100',
                        'tag_ids': tags('+353 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-303 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_10x100',
                        'tag_ids': tags('-353 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_304': {
                'name': '304 8% servicios predomina el intelecto no relacionados con el titulo profesional',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '304',
                'l10n_ec_code_applied': '354',
                'l10n_ec_code_base': '304',
                'l10n_ec_code_ats': '304',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-354 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_304A': {
                'name': '304a 8% comisiones y demas pagos por servicios predomina intelecto no relacionados con el titulo profesional',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '304',
                'l10n_ec_code_applied': '354',
                'l10n_ec_code_base': '304',
                'l10n_ec_code_ats': '304A',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-354 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_304B': {
                'name': '304b 8% pagos a notarios y registradores de la propiedad y mercantil por sus actividades ejercidas como tales',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '304',
                'l10n_ec_code_applied': '354',
                'l10n_ec_code_base': '304',
                'l10n_ec_code_ats': '304B',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-354 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_304C': {
                'name': '304c 8% pagos a deportistas, entrenadores, arbitros, miembros del cuerpo tecnico por sus actividades ejercidas como tales',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '304',
                'l10n_ec_code_applied': '354',
                'l10n_ec_code_base': '304',
                'l10n_ec_code_ats': '304C',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-354 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_304D': {
                'name': '304d 8% pagos a artistas por sus actividades ejercidas como tales',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '304',
                'l10n_ec_code_applied': '354',
                'l10n_ec_code_base': '304',
                'l10n_ec_code_ats': '304D',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_304E': {
                'name': '304e 8% honorarios y demas pagos por servicios de docencia',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '304',
                'l10n_ec_code_applied': '354',
                'l10n_ec_code_base': '304',
                'l10n_ec_code_ats': '304E',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+354 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-304 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-354 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_307': {
                'name': '307 2% servicios predomina mano de obra',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -2.0,
                'description': '307',
                'l10n_ec_code_applied': '357',
                'l10n_ec_code_base': '307',
                'l10n_ec_code_ats': '307',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+307 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2x100',
                        'tag_ids': tags('+357 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-307 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2x100',
                        'tag_ids': tags('-357 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_308': {
                'name': '308 10% utilizacion o aprovechamiento de la imagen o renombre',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -10.0,
                'description': '308',
                'l10n_ec_code_applied': '358',
                'l10n_ec_code_base': '308',
                'l10n_ec_code_ats': '308',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+308 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_10x100',
                        'tag_ids': tags('+358 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-308 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_10x100',
                        'tag_ids': tags('-358 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_309': {
                'name': '309 1.75% servicios prestados por medios de comunicación y agencias de publicidad',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.75,
                'description': '309',
                'l10n_ec_code_applied': '359',
                'l10n_ec_code_base': '309',
                'l10n_ec_code_ats': '309',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+309 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('+359 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-309 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_10x100',
                        'tag_ids': tags('-359 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_310': {
                'name': '310 1% servicio de transporte privado de pasajeros o transporte publico o privado de carga',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.0,
                'description': '310',
                'l10n_ec_code_applied': '360',
                'l10n_ec_code_base': '310',
                'l10n_ec_code_ats': '310',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+310 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('+360 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-310 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('-360 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_311': {
                'name': '311 2% por pagos a traves de liquidacion de compra (nivel cultural o rusticidad)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -2.0,
                'description': '311',
                'l10n_ec_code_applied': '361',
                'l10n_ec_code_base': '311',
                'l10n_ec_code_ats': '311',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+311 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2x100',
                        'tag_ids': tags('+361 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-311 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2x100',
                        'tag_ids': tags('-361 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_312': {
                'name': '312 1.75% transferencia de bienes muebles de naturaleza corporal',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.75,
                'description': '312',
                'l10n_ec_code_applied': '362',
                'l10n_ec_code_base': '312',
                'l10n_ec_code_ats': '312',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+312 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('+362 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-312 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('-362 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_312A': {
                'name': '312a 1% compra de bienes de origen agricola, avicola, pecuario, apicola, cunicula, bioacuatico, y forestal',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.0,
                'description': '312',
                'l10n_ec_code_applied': '362',
                'l10n_ec_code_base': '312',
                'l10n_ec_code_ats': '312A',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+312 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('+362 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-312 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('-362 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_314A': {
                'name': '314a 8% regalias por concepto de franquicias de acuerdo a ley de propiedad intelectual - pago a personas naturales',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '314',
                'l10n_ec_code_applied': '364',
                'l10n_ec_code_base': '314',
                'l10n_ec_code_ats': '314A',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+364 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-364 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_314B': {
                'name': '314b 8% casales, derechos de autor, marcas, patentes y similares de acuerdo a ley de propiedad intelectual – pago a personas naturales',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '314',
                'l10n_ec_code_applied': '364',
                'l10n_ec_code_base': '314',
                'l10n_ec_code_ats': '314B',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+364 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-364 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_314C': {
                'name': '314c 8% regalias por concepto de franquicias de acuerdo a ley de propiedad intelectual - pago a sociedades',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '314',
                'l10n_ec_code_applied': '364',
                'l10n_ec_code_base': '314',
                'l10n_ec_code_ats': '314C',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+364 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-364 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_314D': {
                'name': '314d 8% casales, derechos de autor, marcas, patentes y similares de acuerdo a ley de propiedad intelectual – pago a sociedades',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '314',
                'l10n_ec_code_applied': '364',
                'l10n_ec_code_base': '314',
                'l10n_ec_code_ats': '314D',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+364 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-314 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-364 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_319': {
                'name': '319 1.75% cuotas de arrendamiento mercantil (prestado por sociedades), inclusive la de opción de compra',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.75,
                'description': '319',
                'l10n_ec_code_applied': '369',
                'l10n_ec_code_base': '319',
                'l10n_ec_code_ats': '319',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+319 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('+369 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-319 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('-369 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_320': {
                'name': '320 8% por arrendamiento bienes inmuebles',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '320',
                'l10n_ec_code_applied': '370',
                'l10n_ec_code_base': '320',
                'l10n_ec_code_ats': '320',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+320 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('+370 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-320 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_8x100',
                        'tag_ids': tags('-370 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_322': {
                'name': '322 1.75% seguros y reaseguros (primas y cesiones) 1.75%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.75,
                'description': '322',
                'l10n_ec_code_applied': '372',
                'l10n_ec_code_base': '322',
                'l10n_ec_code_ats': '322',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+322 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('+372 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-322 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('-372 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_332': {
                'name': '332 0% otras compras de bienes y servicios no sujetas a retencion',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_332A': {
                'name': '332a 0% enajenacion de derechos representativos de capital y otros derechos exentos (mayo 2016)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332A',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_332B': {
                'name': '332b 0% compra de bienes inmuebles',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332B',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_332C': {
                'name': '332c 0% transporte publico de pasajeros',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332C',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_332D': {
                'name': '332d 0% pagos en el pais por transporte de pasajeros o transporte internacional de carga, a compañias nacionales o extranjeras de aviacion o maritimas',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332D',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_332G': {
                'name': '332g 0% pagos con tarjeta de credito',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332G',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_332I': {
                'name': '332i 0% pagos a través de convenios de débito (clientes ifi`s)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': 0.0,
                'description': '332',
                'l10n_ec_code_base': '332',
                'l10n_ec_code_ats': '332I',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-332 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_others',
                    }),
                ],
            },
            'tax_withhold_profit_343A': {
                'name': '343a 1% por energia electrica',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.0,
                'description': '343',
                'l10n_ec_code_applied': '393',
                'l10n_ec_code_base': '343',
                'l10n_ec_code_ats': '343A',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+343 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('+393 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-343 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('-393 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_343B': {
                'name': '343b 1% por actividades de construccion de obra material inmueble, urbanizacion, lotizacion o actividades similares',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.0,
                'description': '343',
                'l10n_ec_code_applied': '393',
                'l10n_ec_code_base': '343',
                'l10n_ec_code_ats': '343B',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+343 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('+393 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-343 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1x100',
                        'tag_ids': tags('-393 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_3440': {
                'name': '3440 2.75% otras retenciones aplicables el 2,75%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -2.0,
                'description': '3440',
                'l10n_ec_code_applied': '394',
                'l10n_ec_code_base': '3440',
                'l10n_ec_code_ats': '3440',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3440 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2_75x100',
                        'tag_ids': tags('+394 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3440 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2_75x100',
                        'tag_ids': tags('-394 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_346': {
                'name': '346 1.75% microempresas (otras retenciones aplicables a otros porcentajes)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.75,
                'description': '346',
                'l10n_ec_code_applied': '396',
                'l10n_ec_code_base': '346',
                'l10n_ec_code_ats': '346',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_1_75x100',
                        'tag_ids': tags('-346 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_347_346': {
                'name': '347-346 2% donaciones en dinero -impuesto a la donaciones',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -2.0,
                'description': '346',
                'l10n_ec_code_applied': '396',
                'l10n_ec_code_base': '346',
                'l10n_ec_code_ats': '347',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2x100',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_2x100',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_501_411': {
                'name': '501-411 22% pago al exterior - beneficios empresariales (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_ats': '501',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_501_422': {
                'name': '501-422 22% pago al exterior - beneficios empresariales (sin convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '422',
                'l10n_ec_code_applied': '472',
                'l10n_ec_code_base': '422',
                'l10n_ec_code_ats': '501',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+422 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+472 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-422 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-472 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_502_411': {
                'name': '502-411 22% pago al exterior - servicios empresariales (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_ats': '502',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_502_422': {
                'name': '502-422 22% pago al exterior - servicios empresariales (sin convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '422',
                'l10n_ec_code_applied': '472',
                'l10n_ec_code_base': '422',
                'l10n_ec_code_ats': '502',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+422 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+472 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-422 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-472 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_509_411': {
                'name': '509-411 22% pago al exterior - casales, derechos de autor, marcas, patentes y similares (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_ats': '509',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_509_422': {
                'name': '509-422 pago al exterior - casales, derechos de autor, marcas, patentes y similares (sin convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '422',
                'l10n_ec_code_base': '422',
                'l10n_ec_code_applied': '472',
                'l10n_ec_code_ats': '509',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+422 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+472 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-422 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-472 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_511_411': {
                'name': '511-411 22% pago al exterior - servicios profesionales independientes (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_ats': '511',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_512_411': {
                'name': '512-411 22% pago al exterior - servicios profesionales dependientes (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_ats': '512',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_517_411': {
                'name': '517-411 22% pago al exterior - reembolso de gastos (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_ats': '517',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_520D_411': {
                'name': '520d-411 22% pago al exterior - comisiones por exportaciones y por promocion de turismo receptivo (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '411',
                'l10n_ec_code_base': '411',
                'l10n_ec_code_applied': '461',
                'l10n_ec_code_ats': '520D',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+461 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-411 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-461 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_522A_410': {
                'name': '522a-410 22% pago al exterior - servicios tecnicos, administrativos o de consultoria y regalias con convenio de doble tributacion (con convenio de doble tributación)',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '410',
                'l10n_ec_code_base': '410',
                'l10n_ec_code_applied': '460',
                'l10n_ec_code_ats': '522A',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+410 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('+460 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-410 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ret_ir_22x100',
                        'tag_ids': tags('-460 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_1x100': {
                'name': '1% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.0,
                'description': '1%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+343 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+393 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-343 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-393 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_1_75x100': {
                'name': '1.75% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -1.75,
                'description': '1.75%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_2x100': {
                'name': '2% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -2.0,
                'description': '2%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+344 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+394 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-344 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-394 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_2_75x100': {
                'name': '2.75% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -2.75,
                'description': '2.75%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+3440 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+3940 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-3440 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-3940 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_5x100': {
                'name': '5% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -5.0,
                'description': '5%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_8x100': {
                'name': '8% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -8.0,
                'description': '8%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+345 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+395 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-345 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-395 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_10x100': {
                'name': '10% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -10.0,
                'description': '10%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_15x100': {
                'name': '15% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -15.0,
                'description': '15%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('-346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_profit_sale_22x100': {
                'name': '22% retenciones de la fuente',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 70,
                'amount': -22.0,
                'description': '22%',
                'tax_group_id': 'tax_group_withhold_income',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('+396 (Reporte 103)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                        'tag_ids': tags('+346 (Reporte 103)'),
                    }),
                    Command.create({
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_profit_withhold',
                        'tag_ids': tags('-396 (Reporte 103)'),
                    }),
                ],
            },
            'tax_withhold_vat_10': {
                'name': 'Retencion iva 10%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 50,
                'amount': -10.0,
                'description': 'RET IVA 10%',
                'l10n_ec_code_applied': '721',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_10',
                        'tag_ids': tags('+721 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_10',
                        'tag_ids': tags('-721 (Reporte 104)'),
                    }),
                ],
            },
            'tax_withhold_vat_20': {
                'name': 'Retencion iva 20%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 50,
                'amount': -20.0,
                'description': 'RET IVA 20%',
                'l10n_ec_code_applied': '723',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_20',
                        'tag_ids': tags('+723 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_20',
                        'tag_ids': tags('-723 (Reporte 104)'),
                    }),
                ],
            },
            'tax_withhold_vat_30': {
                'name': 'Retencion iva 30%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 50,
                'amount': -30.0,
                'description': 'RET IVA 30%',
                'l10n_ec_code_applied': '725',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_30',
                        'tag_ids': tags('+725 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_30',
                        'tag_ids': tags('-725 (Reporte 104)'),
                    }),
                ],
            },
            'tax_withhold_vat_50': {
                'name': 'Retencion iva 50%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 50,
                'amount': -50.0,
                'description': 'RET IVA 50%',
                'l10n_ec_code_applied': '727',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_50',
                        'tag_ids': tags('+727 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_50',
                        'tag_ids': tags('-727 (Reporte 104)'),
                    }),
                ],
            },
            'tax_withhold_vat_70': {
                'name': 'Retencion iva 70%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 50,
                'amount': -70.0,
                'description': 'RET IVA 70%',
                'l10n_ec_code_applied': '729',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_70',
                        'tag_ids': tags('+729 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_70',
                        'tag_ids': tags('-729 (Reporte 104)'),
                    }),
                ],
            },
            'tax_withhold_vat_100': {
                'name': 'Retencion iva 100%',
                'type_tax_use': 'purchase',
                'amount_type': 'percent',
                'sequence': 50,
                'amount': -100.0,
                'description': 'RET IVA 100%',
                'l10n_ec_code_applied': '731',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_100',
                        'tag_ids': tags('+731 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_vat_withhold_100',
                        'tag_ids': tags('-731 (Reporte 104)'),
                    }),
                ],
            },
            'tax_sale_withhold_vat_10': {
                'name': 'Retencion iva 10%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 60,
                'amount': -10.0,
                'description': 'RET IVA 10%',
                'l10n_ec_code_applied': '609',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('+609 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('-609 (Reporte 104)'),
                    }),
                ],
            },
            'tax_sale_withhold_vat_20': {
                'name': 'Retencion iva 20%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 60,
                'amount': -20.0,
                'description': 'RET IVA 20%',
                'l10n_ec_code_applied': '609',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('+609 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('-609 (Reporte 104)'),
                    }),
                ],
            },
            'tax_sale_withhold_vat_30': {
                'name': 'Retencion iva 30%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 60,
                'amount': -30.0,
                'description': 'RET IVA 30%',
                'l10n_ec_code_applied': '609',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('+609 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('-609 (Reporte 104)'),
                    }),
                ],
            },
            'tax_sale_withhold_vat_50': {
                'name': 'Retencion iva 50%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 60,
                'amount': -50.0,
                'description': 'RET IVA 50%',
                'l10n_ec_code_applied': '609',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('+609 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('-609 (Reporte 104)'),
                    }),
                ],
            },
            'tax_sale_withhold_vat_70': {
                'name': 'Retencion iva 70%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 60,
                'amount': -70.0,
                'description': 'RET IVA 70%',
                'l10n_ec_code_applied': '609',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('+609 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('-609 (Reporte 104)'),
                    }),
                ],
            },
            'tax_sale_withhold_vat_100': {
                'name': 'Retencion iva 100%',
                'type_tax_use': 'sale',
                'amount_type': 'percent',
                'sequence': 60,
                'amount': -100.0,
                'description': 'RET IVA 100%',
                'l10n_ec_code_applied': '609',
                'tax_group_id': 'tax_group_withhold_vat',
                'invoice_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('+609 (Reporte 104)'),
                    }),
                ],
                'refund_repartition_line_ids': [
                    Command.create({
                        'repartition_type': 'base',
                    }),
                    Command.create({
                        'factor_percent': 12,
                        'repartition_type': 'tax',
                        'account_id': 'ec_sale_vat_outstanding_withholds',
                        'tag_ids': tags('-609 (Reporte 104)'),
                    }),
                ],
            },
        }

    def _get_ec_fiscal_position(self, template_code):
        return {
            'fp_companies': {
                'name': 'Sociedades - personas juridicas',
            },
            'fp_special_taxation_companies': {
                'name': 'Contribuyentes especiales',
            },
            'fp_public_companies': {
                'name': 'Sector publico y ep',
            },
            'fp_person_obligated_accounting': {
                'name': 'Persona natural obligada a llevar contabilidad',
            },
            'fp_person_leases': {
                'name': 'Persona natural no obligada - arriendos',
            },
            'fp_person_professional': {
                'name': 'Persona natural no obligada - profesionales',
            },
            'fp_person_rustic': {
                'name': 'Persona natural no obligada - liquidaciones de compras',
            },
            'fp_person_other': {
                'name': 'Persona natural no obligadas - emite factura o nota de venta',
            },
            'fp_foreing_company_local': {
                'name': 'Empresa extranjera - venta local',
            },
            'fp_foreing_person_local': {
                'name': 'Persona extranjera - venta local',
            },
            'fp_foreing_company_exports': {
                'name': 'Empresa extranjera - exportacion',
            },
            'fp_foreing_person_exports': {
                'name': 'Persona extranjera - exportacion',
            },
            'fp_others': {
                'name': 'Otras - sin cálculo automático de retención de iva',
            },
        }
