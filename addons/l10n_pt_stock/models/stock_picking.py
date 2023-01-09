from odoo import models, api, fields


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    secure_sequence_id = fields.Many2one('ir.sequence',
        help='Sequence to use to ensure the securisation of data',
        readonly=True, copy=False)


class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'hash.mixin', 'l10n_pt.mixin']

    country_code = fields.Char(related='company_id.country_id.code', depends=['company_id.country_id'])

    @api.depends('picking_type_id.code', 'picking_type_id.sequence_code', 'secure_sequence_number')
    def _compute_l10n_pt_document_number(self):
        for picking in self.filtered(lambda p: p.company_id.country_id.code == 'PT'):
            picking_type = picking.picking_type_id
            picking.l10n_pt_document_number = f'{picking_type.code} {picking_type.sequence_code}/{picking.secure_sequence_number}'

    # Override hash.mixin
    def _get_fields_used_by_hash(self):
        if self.company_id.country_id.code != 'PT':
            return super()._get_fields_used_by_hash()
        return 'date_done', 'create_date', 'secure_sequence_number'

    # Override hash.mixin
    def _get_sorting_keys(self):
        if self.company_id.country_id.code != 'PT':
            return super()._get_sorting_keys()
        return ['date_done', 'id']

    # Override hash.mixin
    def _get_secure_sequence(self):
        self.ensure_one()
        if self.company_id.country_id.code != 'PT':
            return super()._get_secure_sequence()
        self.env['hash.mixin']._create_secure_sequence(self.picking_type_id, self.company_id.id)
        return self.picking_type_id.secure_sequence_id

    # Override hash.mixin
    def _get_previous_record_domain(self):
        if self.company_id.country_id.code != 'PT':
            return super()._get_previous_record_domain()
        return [
            ('state', '=', 'done'),
            ('picking_type_id.code', '=', 'outgoing'),
            ('company_id', '=', self.company_id.id),
            ('id', '!=', self.id),
            ('secure_sequence_number', '<', self.secure_sequence_number),
            ('secure_sequence_number', '!=', 0)
        ]

    # Override hash.mixin
    @api.depends('country_code', 'picking_type_id.code', 'state', 'date_done')
    def _compute_must_hash(self):
        super()._compute_must_hash()
        for picking in self:
            picking.must_hash = picking.must_hash or (
                picking.country_code == 'PT'
                and picking.picking_type_id.code == 'outgoing'
                and picking.state == 'done'
                and picking.date_done
            )

    # Override hash.mixin
    def _create_hash_string(self, previous_hash=None):
        self.ensure_one()
        if self.company_id.country_id.code != 'PT':
            return super()._create_hash_string(previous_hash)
        return self._l10n_pt_create_hash_string(self.date_done, 0.0)
