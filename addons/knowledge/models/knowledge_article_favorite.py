# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, exceptions, fields, models, _


class ArticleFavorite(models.Model):
    _name = 'knowledge.article.favorite'
    _description = 'Favorite Article'
    _order = 'sequence asc, id DESC'
    _rec_name = 'article_id'

    article_id = fields.Many2one(
        'knowledge.article', 'Article',
        index=True, required=True, ondelete='cascade')
    user_id = fields.Many2one(
        'res.users', 'User',
        index=True, required=True, ondelete='cascade')
    sequence = fields.Integer(default=0)

    _sql_constraints = [
        ('unique_favorite', 'unique(article_id, user_id)', 'User already has this article in favorites.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """ At creation, we need to set the max sequence, if not given, for each favorite to create, in order to keep
        a correct ordering as much as possible. Some sequence could be given in create values, that could lead to
        duplicated sequence per user_id. That is not an issue as they will be resequenced the next time the user reorder
        their favorites. """
        new_sequence = self.env['knowledge.article.favorite'].search([], order='sequence desc', limit=1).sequence + 1 or 0
        for vals in vals_list:
            if not vals.get('sequence'):
                vals['sequence'] = new_sequence
                new_sequence += 1
        return super(ArticleFavorite, self).create(vals_list)

    def write(self, vals):
        if ('article_id' in vals or 'user_id' in vals) and not self.env.is_admin():
            raise exceptions.AccessError(_("Can not update the article or user of a favorite."))
        return super().write(vals)
