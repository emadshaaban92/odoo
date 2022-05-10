# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.http import request

class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def l10n_uk_try_loading(self, company=False, install_demo=True):
        """ Ordinarily, the try_loading function is called when the module is installed. This causes a problem when
        installing l10n_xi, which depends on l10n_uk but has it's own CoA, as the UK try_loading function will occur
        first. To solve this, we load the CoA based on the country code of the company.
        """

        if not self == self.env.ref('l10n_uk.l10n_uk'):
            return super().try_loading(company, install_demo)
        else:
            # Determine whether the country of the company is Northern Ireland
            if not company:
                if request and hasattr(request, 'allowed_company_ids'):
                    company = self.env['res.company'].browse(request.allowed_company_ids[0])
                else:
                    company = self.env.company

        uk_fiscal_country = company.account_fiscal_country_id.code == 'uk' or company.account_fiscal_country_id.code == 'xi'
        use_northern_ireland_coa = uk_fiscal_country and company.country_id.code == 'xi'

        if not company.chart_template_id and not self.existing_accounting(company):
            # The NI CoA is in l10n_uk, we want to load it if the country is Northern Ireland
            if use_northern_ireland_coa:
                template = self.env.ref('l10n_xi.l10n_xi_account_chart')
                template.with_context(default_company_id=company.id)._load(15.0, 15.0, company)
            else:
                self.with_context(default_company_id=company.id)._load(15.0, 15.0, company)

            # Install the demo data when the first localization is instanciated on the company
            if install_demo and self.env.ref('base.module_account').demo:
                self.with_context(
                    default_company_id=company.id,
                    allowed_company_ids=[company.id],
                )._create_demo_data()

        else:
            return super().try_loading(company, install_demo)
