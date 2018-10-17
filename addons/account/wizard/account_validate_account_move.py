from odoo import models, api, _
from odoo.exceptions import UserError


class ValidateAccountMove(models.TransientModel):
    _name = "validate.account.move"
    _description = "Validate Account Move"

    @api.multi
    def validate_move(self):
        moves = self.env['account.move'].get_active_records()
        move_to_post = self.env['account.move']
        for move in moves:
            if move.state == 'draft':
                move_to_post += move
        if not move_to_post:
            raise UserError(_('There is no journal items in draft state to post.'))
        move_to_post.post()
        return {'type': 'ir.actions.act_window_close'}
