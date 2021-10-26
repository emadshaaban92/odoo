# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.payment.models.res_company import ODOO_PAYMENTS_DEPLOYED_COUNTRIES


ADYEN_AVAILABLE_COUNTRIES = [
    'US', 'AT', 'AU', 'BE', 'CA', 'CH', 'CZ', 'DE', 'ES', 'FI', 'FR', 'GB', 'GR', 'HR', 'IE', 'IT',
    'LT', 'LU', 'NL', 'PL', 'PT'
]


class AdyenAddressMixin(models.AbstractModel):
    _name = 'adyen.address.mixin'
    _description = "Odoo Payments Address Mixin"

    #=========== ANY FIELD BELOW THIS LINE HAS NOT BEEN CLEANED YET ===========#

    country_id = fields.Many2one(
        string="Country",
        comodel_name='res.country',
        required=True,
        domain=[
            ('code', 'in', ADYEN_AVAILABLE_COUNTRIES),
            ('code', 'in', ODOO_PAYMENTS_DEPLOYED_COUNTRIES),
        ])
    country_code = fields.Char(related='country_id.code')

    state_id = fields.Many2one(
        string="State",
        comodel_name='res.country.state',
        domain="[('country_id', '=?', country_id)]")
    state_code = fields.Char(related='state_id.code')

    city = fields.Char(string="City", required=True)
    zip = fields.Char(string="ZIP", required=True)
    street = fields.Char(string="Street", required=True)
    house_number_or_name = fields.Char(string="House Number Or Name", required=True)


class AdyenIDMixin(models.AbstractModel):
    _name = 'adyen.id.mixin'
    _description = "Odoo Payments ID Mixin"

    #=========== ANY FIELD BELOW THIS LINE HAS NOT BEEN CLEANED YET ===========#

    id_type = fields.Selection(
        string='Photo ID type',
        selection=[
            ('PASSPORT', 'Passport'),
            ('ID_CARD', 'ID Card'),
            ('DRIVING_LICENSE', 'Driving License'),
        ])
    id_front = fields.Binary(
        string='Photo ID Front', help="Allowed formats: jpg, pdf, png. Maximum allowed size: 4MB.")
    # FIXME ANVFE isn't it already stored in the attachment? is this field needed ?
    id_front_filename = fields.Char()
    id_back = fields.Binary(
        string='Photo ID Back', help="Allowed formats: jpg, pdf, png. Maximum allowed size: 4MB.")
    # FIXME ANVFE isn't it already stored in the attachment? is this field needed ?
    id_back_filename = fields.Char()

    #=== COMPUTE METHODS ===#

    #=== CONSTRAINT METHODS ===#

    #=== CRUD METHODS ===#

    #=== ACTION METHODS ===#

    #=== BUSINESS METHODS ===#

    #=========== ANY METHOD BELOW THIS LINE HAS NOT BEEN CLEANED YET ===========#

    def write(self, vals):
        res = super().write(vals)

        # Check file formats
        if vals.get('id_front'):
            self._check_file_requirements(vals.get('id_front'))
        if vals.get('id_back'):
            self._check_file_requirements(vals.get('id_back'))

        # FIXME ANVFE what is this dev logic...
        # 1) this mixin is used for adyen.account AND adyen.shareholder models
        # 2) _upload_photo_id is implemented on those models (and duplicated...), but called in the mixin -_-
        for record in self:
            if vals.get('id_front'):
                document_type = record.id_type
                if record.id_type in ['ID_CARD', 'DRIVING_LICENSE']:
                    document_type += '_FRONT'
                record._upload_photo_id(document_type, record.id_front, record.id_front_filename)
            if vals.get('id_back') and record.id_type in ['ID_CARD', 'DRIVING_LICENSE']:
                document_type = record.id_type + '_BACK'
                record._upload_photo_id(document_type, record.id_back, record.id_back_filename)
            return res

    @api.model
    def _check_file_requirements(self, content):
        content_encoded = content.encode('utf8')
        mimetype = guess_mimetype(base64.b64decode(content_encoded))
        file_size = len(content_encoded)

        # Document requirements: https://docs.adyen.com/platforms/verification-checks/photo-id-check#requirements
        if mimetype not in ['image/jpeg', 'image/png', 'application/pdf']:
            raise ValidationError(_('Allowed file formats for photo IDs are jpeg, jpg, pdf or png'))
        if file_size < (100 * 1024) or (file_size < 1024 and mimetype == 'application/pdf'):
            raise ValidationError(_('Minimum allowed size for photo ID: 1 KB for PDF, 100 KB for other formats.'))
        if file_size > (4 * 1024 * 1024):
            raise ValidationError(_('Maximum allowed size for photo ID: 4 MB.'))

    def _upload_photo_id(self, document_type, content, filename):
        # The request to be sent to Adyen will be different for Individuals,
        # Shareholders, etc. This method should be implemented by the models
        # inheriting this mixin
        raise NotImplementedError()
