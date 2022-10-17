from odoo import models


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    def document_layout_save(self):
        """Save layout and onboarding step progress, return super() result"""
        res = super(BaseDocumentLayout, self).document_layout_save()
        step = self.env.ref('account.account_common_onboarding_layout_step', raise_if_not_found=False)
        if step:
            for company_id in self.company_id:
                step.with_company(company_id).action_set_just_done()
        return res
