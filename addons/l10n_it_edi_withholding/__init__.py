# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models
from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


def _l10n_it_edi_add_accounts(env, company):
    account_codes = ['1611', '2603']
    for account_code in account_codes:
        template_vals = []
        if not env['account.account'].search([('code', '=', account_code)]):
            account_template = env.ref(f'l10n_it_edi_withholding.{account_code}')
            vals = company.chart_template_id._get_account_vals(company, account_template, account_code, {})
            template_vals.append((account_template, vals))
        company.chart_template_id._create_records_with_xmlid('account.account', template_vals, company)
    _logger.info("Created withholding accounts")


def _l10n_it_edi_withholding_add_taxes(env, company):
    # Create the new taxes on existing company
    existing_taxes = no_tax = env['account.tax']
    templates = env['account.tax.template']
    for xml_id in (
        '20awi', '20vwi',
        '20awc', '20vwc',
        '23awo', '23vwo',
        '4vcp', '4acp',
        '4vinps', '4ainps'
    ):
        templates |= env.ref(f"l10n_it_edi_withholding.{xml_id}")
        tax = env.ref(f"l10n_it_edi_withholding.{company.id}_{xml_id}", raise_if_not_found=False) or no_tax
        existing_taxes |= tax
    if not existing_taxes:
        templates._generate_tax(company)
        _logger.info("Created withholding taxes")

    # Increase the sequence number of the old taxes multiplying it by 10 and adding 21
    # so that the withholding can have sequence=10 and the pension fund sequence=20
    offset = 21
    all_taxes = env['account.tax'].search([('company_id', '=', company.id)])
    for tax in all_taxes.filtered(lambda x: (x.sequence <= 20 and not x.l10n_it_pension_fund_type and not x.l10n_it_withholding_type)):
        if not tax.l10n_it_withholding_type and not tax.l10n_it_pension_fund_type:
            tax.sequence += offset
    _logger.info("Increased sequence number of old taxes by %s", offset)


def _l10n_it_edi_withholding_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    chart_template = env.ref('l10n_it.l10n_it_chart_template_generic', raise_if_not_found=False)
    if chart_template:
        for company in env['res.company'].search([('chart_template_id', '=', chart_template.id)]):
            _logger.info("Company %s that already has the Italian localization installed, updating...", company.name)
            _l10n_it_edi_withholding_add_taxes(env, company)
            _l10n_it_edi_add_accounts(env, company)
