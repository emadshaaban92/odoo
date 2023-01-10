from odoo import fields, models


class NewModule(models.Model):
    _inherit = 'pos.config'

    country_code = fields.Char(related="company_id.country_id.code")

    l10n_eg_pos_serial = fields.Char("POS Serial")
    l10n_eg_pos_version = fields.Char("POS Version")
    l10n_eg_pos_model_framework = fields.Char("POS Model Framework")
    l10n_eg_pos_pre_shared_key = fields.Char("POS Pre-Shared Key")

    l10n_eg_pos_client_identifier = fields.Char('POS Client ID', groups="base.group_erp_manager")
    l10n_eg_pos_client_secret = fields.Char('POS Secret', groups="base.group_erp_manager")
    l10n_eg_pos_production_env = fields.Boolean('POS In Production Environment')
    l10n_eg_pos_receipt_threshold = fields.Float(
        'Receipt Threshold',
        default=50000,
        help="Threshold at which you are required to give the VAT number of the customer.")

    l10n_eg_pos_branch_id = fields.Many2one('res.partner', string='Branch', copy=False,
                                        help="Address of the subdivision of the company.  You can just put the "
                                             "company partner if this is used for the main branch.")
    l10n_eg_pos_activity_type_id = fields.Many2one('l10n_eg_edi.activity.type', 'ETA Activity Code', copy=False,
                                               help='This is the activity type of the branch according to Egyptian Tax Authority')
    l10n_eg_pos_branch_identifier = fields.Char('ETA Branch ID', copy=False,
                                            help="This number can be found on the taxpayer profile on the eInvoicing portal. ")