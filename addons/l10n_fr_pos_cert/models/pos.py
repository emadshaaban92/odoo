# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.exceptions import UserError


class pos_config(models.Model):
    _inherit = 'pos.config'

    def open_ui(self):
        for config in self:
            if not config.company_id.country_id:
                raise UserError(_("You have to set a country in your company setting."))
            if config.company_id._is_accounting_unalterable():
                if config.current_session_id:
                    config.current_session_id._check_session_timing()
        return super(pos_config, self).open_ui()


class pos_session(models.Model):
    _inherit = 'pos.session'

    def _check_session_timing(self):
        self.ensure_one()
        return True

    def open_frontend_cb(self):
        sessions_to_check = self.filtered(lambda s: s.config_id.company_id._is_accounting_unalterable())
        sessions_to_check.filtered(lambda s: s.state == 'opening_control').start_at = fields.Datetime.now()
        for session in sessions_to_check:
            session._check_session_timing()
        return super(pos_session, self).open_frontend_cb()


class pos_order(models.Model):
    _name = 'pos.order'
    _inherit = ['pos.order', 'hash.mixin']

    # Override hash.mixin
    @api.depends('state')
    def _compute_must_hash(self):
        super()._compute_must_hash()
        for order in self:
            order.must_hash = order.must_hash or (
                order.company_id._is_accounting_unalterable()
                and order.state in ['paid', 'done', 'invoiced']
                and order.date_order
            )

    # Override hash.mixin
    def _get_sorting_keys(self):
        if self.company_id.country_id.code != 'FR':
            return super()._get_sorting_keys()
        return ['date_order', 'id']

    # Override hash.mixin
    def _get_secure_sequence(self):
        self.ensure_one()
        if self.company_id.country_id.code != 'FR':
            return super()._get_secure_sequence()
        self.env['hash.mixin']._create_secure_sequence(self.company_id, self.company_id.id, "l10n_fr_pos_cert_sequence_id")
        return self.company_id.l10n_fr_pos_cert_sequence_id

    # Override hash.mixin
    def _get_inalterable_fields(self):
        if self.company_id.country_id.code != 'FR':
            return super()._get_inalterable_fields()
        return 'date_order', 'user_id', 'lines', 'payment_ids', 'pricelist_id', 'partner_id', \
               'session_id', 'pos_reference', 'sale_journal', 'fiscal_position_id'

    # Override hash.mixin
    def _get_previous_record_domain(self):
        self.ensure_one()
        if self.company_id.country_id.code != 'FR':
            return super()._get_previous_record_domain()
        return [
            ('state', 'in', ['paid', 'done', 'invoiced']),
            ('company_id', '=', self.company_id.id),
            ('secure_sequence_number', '!=', 0),
            ('secure_sequence_number', '=', int(self.secure_sequence_number) - 1)
        ]

    # Override hash.mixin
    def _get_dict_fields_values_to_hash(self, lines=()):
        if self.company_id.country_id.code != 'FR':
            return super()._get_dict_fields_values_to_hash()
        return super()._get_dict_fields_values_to_hash(self.lines)

    @api.ondelete(at_uninstall=True)
    def _unlink_except_pos_so(self):
        for order in self:
            if order.company_id._is_accounting_unalterable():
                raise UserError(_("According to French law, you cannot delete a point of sale order."))

    def _export_for_ui(self, order):
        res = super()._export_for_ui(order)
        res['inalterable_hash'] = order.inalterable_hash
        return res


class PosOrderLine(models.Model):
    _name = 'pos.order.line'
    _inherit = ['pos.order.line', 'sub.hash.mixin']

    # Override sub.hash.mixin
    def _get_hash_parent(self):
        self.ensure_one()
        if self.company_id.country_id.code != 'FR':
            return super()._get_hash_parent()
        return self.order_id

    # Override sub.hash.mixin
    def _get_inalterable_fields(self):
        if self.company_id.country_id.code != 'FR':
            return super()._get_inalterable_fields()
        return 'notice', 'product_id', 'qty', 'price_unit', 'discount', 'tax_ids', 'tax_ids_after_fiscal_position'
