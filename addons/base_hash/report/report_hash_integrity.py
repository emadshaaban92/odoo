from odoo import models, _, api, fields
from odoo.tools import format_date


class ReportHashIntegrity(models.AbstractModel):
    _name = 'report.base_hash.report_hash_integrity'
    _description = 'Get hash integrity result as a PDF file.'

    @api.model
    def _check_hash_integrity(self, must_check, records, date_field):
        if not must_check:
            return {
                'status': 'not_checked',
                'msg': _('The integrity check has not been verified.'),
            }

        if not records:
            return {
                'status': 'no_record',
                'msg': _("There isn't any record flagged for data inalterability."),
            }

        records = records.sorted("secure_sequence_number")
        corrupted_record = None
        previous_hash = ''
        for record in records:
            if record.inalterable_hash != record._create_hash_string(previous_hash):
                corrupted_record = record
                break
            previous_hash = record.inalterable_hash

        if corrupted_record is not None:
            return {
                'status': 'corrupted',
                'msg': _('Corrupted data on record %s with id %s', corrupted_record.name, corrupted_record.id),
            }

        return {
            'status': 'verified',
            'msg': _('Entries are hashed from %s (%s)', records[0].name, format_date(self.env, fields.Date.to_string(records[0][date_field]))),
            'first_name': records[0]['name'],
            'first_hash': records[0]['inalterable_hash'],
            'first_date': format_date(self.env, fields.Date.to_string(records[0][date_field])),
            'last_name': records[-1]['name'],
            'last_hash': records[-1]['inalterable_hash'],
            'last_date': format_date(self.env, fields.Date.to_string(records[-1][date_field])),
        }
