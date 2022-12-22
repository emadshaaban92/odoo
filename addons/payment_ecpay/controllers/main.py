# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hmac
import logging
import pprint

from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class EcpayController(http.Controller):
    _return_url = '/payment/ecpay/return'
    _webhook_url = '/payment/ecpay/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET'])
    def ecpay_return_from_checkout(self, **data):
        """ Process the notification data sent by ECPay after redirection.

        :param dict data: The notification data.
        """
        # Don't process the notification data as they contain no valuable information except for the
        # reference and ECPay doesn't expose an endpoint to fetch the data from the API.
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def ecpay_webhook(self, **data):
        """ Process the notification data sent by ECPay to the webhook.

        :param dict data: The notification data.
        :return: The '1|OK' string to acknowledge the notification.
        :rtype: str
        """
        _logger.info("Notification received from ECPay with data:\n%s", pprint.pformat(data))
        try:
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
                'ecpay', data
            )
            self._verify_notification_signature(data, tx_sudo)

            # Handle the notification data.
            tx_sudo._handle_notification_data('ecpay', data)
        except ValidationError: # Acknowledge the notification to avoid getting spammed.
            _logger.exception("Unable to handle the notification data; skipping to acknowledge.")

        return "1|OK"

    @staticmethod
    def _verify_notification_signature(notification_data, tx_sudo):
        """ Check that the received signature matches the expected one.

        :param dict notification_data: The notification data
        :param recordset tx_sudo: The sudoed transaction referenced by the notification data, as a
                                  `payment.transaction` record
        :return: None
        :raise: :class:`werkzeug.exceptions.Forbidden` if the signatures don't match
        """
        received_signature = notification_data.get('CheckMacValue')
        if not received_signature:
            _logger.warning("Received notification with missing signature.")
            raise Forbidden()

        # Compare the received signature with the expected signature computed from the data.
        expected_signature = tx_sudo.provider_id._ecpay_calculate_signature(
            notification_data, incoming=True
        )
        if not hmac.compare_digest(received_signature, expected_signature):
            _logger.warning("Received notification with invalid signature.")
            raise Forbidden()




