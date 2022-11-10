# -*- coding: utf-8 -*-
from odoo import fields, models


class LeadScoringFrequency(models.Model):
    _name = 'crm.lead.scoring.frequency'
    _description = 'Lead Scoring Frequency'

    variable = fields.Char('Variable', index=True)
    value = fields.Char('Value')
    won_count = fields.Float('Won Count', digits=(16, 1))  # Float because we add 0.1 to avoid zero Frequency issue
    lost_count = fields.Float('Lost Count', digits=(16, 1))  # Float because we add 0.1 to avoid zero Frequency issue
    team_id = fields.Many2one('crm.team', 'Sales Team', ondelete="cascade")

    def print_frequencies(self):
        frequencies = self.env['crm.lead.scoring.frequency'].search([])
        print("TEAM".rjust(15), end='')
        print("VARIABLE".rjust(15), end='')
        print("VALUE".rjust(15), end='')
        print("WON_COUNT".rjust(15), end='')
        print("LOST_COUNT".rjust(15))
        for f in frequencies:
            print(f"{f.team_id.id}".rjust(15), end='')
            print(f"{f.variable}".rjust(15), end='')
            print(f"{f.value}".rjust(15), end='')
            print(f"{f.won_count}".rjust(15), end='')
            print(f"{f.lost_count}".rjust(15))

class FrequencyField(models.Model):
    _name = 'crm.lead.scoring.frequency.field'
    _description = 'Fields that can be used for predictive lead scoring computation'

    name = fields.Char(related="field_id.field_description")
    field_id = fields.Many2one(
        'ir.model.fields', domain=[('model_id.model', '=', 'crm.lead')], required=True,
        ondelete='cascade',
    )
