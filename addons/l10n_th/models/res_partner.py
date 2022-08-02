from odoo import models

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _l10n_th_get_company_info(self, use_code=False):
        code = self.company_registry or ""
        if use_code:
            return code or ""
        if not self.company_registry:
            return ""
        return "Headquarter" if code == "0000" else "Branch " + code
