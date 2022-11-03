from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.tools.sql import constraint_definition, drop_constraint


class EtaThumbDrive(models.Model):
    _inherit = 'l10n_eg_edi.thumb.drive'

    name = fields.Char()
    active = fields.Boolean(default=True)

    def _auto_init(self):
        res = super()._auto_init()
        table = 'l10n_eg_edi_thumb_drive'
        constraint_name = '%s_%s' % (table, 'user_drive_uniq')
        current_definition = constraint_definition(self.env.cr, table, constraint_name)
        if current_definition:
            drop_constraint(self.env.cr, table, constraint_name)
        return res

    @api.constrains('active', 'user_id', 'company_id')
    def _constrains_active_thumb(self):
        for drive in self:
            if self.search_count([('company_id', '=', drive.company_id.id), ('user_id', '=', drive.user_id.id)]) > 1:
                raise ValidationError(_('You can only have one drive active at a time per user and per company'))
