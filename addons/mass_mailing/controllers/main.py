# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import werkzeug
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from odoo import _, http, tools
from odoo.http import request
from odoo.tools import consteq


class MassMailController(http.Controller):

    def _check_mailing_email_token(self, mailing_id, document_id, email, hash_token):
        """ Return the mailing based on given credentials.

        :return: False if issue with credentials (missing or invalid); void
          recordset if mailing does not exist; record otherwise.
        """
        if not mailing_id or not email or not document_id or not hash_token:
            raise BadRequest()
        mailing_sudo = request.env['mailing.mailing'].sudo().browse(mailing_id)
        if not mailing_sudo.exists():
            raise NotFound()
        if not consteq(mailing_sudo._generate_mailing_recipient_hash(document_id, email), hash_token):
            raise Unauthorized()
        return mailing_sudo

    def _log_blacklist_action(self, blacklist_entry, mailing_id, description):
        mailing = request.env['mailing.mailing'].sudo().browse(mailing_id)
        model_display = mailing.mailing_model_id.display_name
        blacklist_entry._message_log(body=description + " ({})".format(model_display))

    # ------------------------------------------------------------
    # SUBSCRIPTION MANAGEMENT
    # ------------------------------------------------------------

    @http.route(['/mail/mailing/<int:mailing_id>/unsubscribe'], type='http', website=True, auth='public')
    def mailing_unsubscribe(self, mailing_id, email=None, res_id=None, token="", **post):
        try:
            mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except NotFound:
            raise Unauthorized()

        if mailing_sudo.mailing_model_real == 'mailing.contact':
            # Unsubscribe directly + Let the user choose their subscriptions
            mailing_sudo.update_opt_out(email, mailing_sudo.contact_list_ids.ids, True)

            contacts = request.env['mailing.contact'].sudo().search([('email_normalized', '=', tools.email_normalize(email))])
            subscription_list_ids = contacts.mapped('subscription_list_ids')
            # In many user are found : if user is opt_out on the list with contact_id 1 but not with contact_id 2,
            # assume that the user is not opt_out on both
            # TODO DBE Fixme : Optimise the following to get real opt_out and opt_in
            opt_out_list_ids = subscription_list_ids.filtered(lambda rel: rel.opt_out).mapped('list_id')
            opt_in_list_ids = subscription_list_ids.filtered(lambda rel: not rel.opt_out).mapped('list_id')
            opt_out_list_ids = set([list.id for list in opt_out_list_ids if list not in opt_in_list_ids])

            unique_list_ids = set([list.list_id.id for list in subscription_list_ids])
            list_ids = request.env['mailing.list'].sudo().browse(unique_list_ids)
            unsubscribed_list = ', '.join(str(list.name) for list in mailing_sudo.contact_list_ids if list.is_public)
            return request.render('mass_mailing.page_mailing_unsubscribe', {
                'contacts': contacts,
                'list_ids': list_ids,
                'opt_out_list_ids': opt_out_list_ids,
                'unsubscribed_list': unsubscribed_list,
                'email': email,
                'mailing_id': mailing_id,
                'res_id': res_id,
                'show_blacklist_button': request.env['ir.config_parameter'].sudo().get_param('mass_mailing.show_blacklist_buttons'),
            })

        opt_in_lists = request.env['mailing.contact.subscription'].sudo().search([
            ('contact_id.email_normalized', '=', email),
            ('opt_out', '=', False)
        ]).mapped('list_id')
        blacklist_rec = request.env['mail.blacklist'].sudo()._add(email)
        self._log_blacklist_action(
            blacklist_rec, mailing_id,
            _("""Requested blacklisting via unsubscribe link."""))
        return request.render('mass_mailing.page_mailing_unsubscribe_done', {
            'email': email,
            'mailing_id': mailing_id,
            'res_id': res_id,
            'list_ids': opt_in_lists,
            'show_blacklist_button': request.env['ir.config_parameter'].sudo().get_param(
                'mass_mailing.show_blacklist_buttons'),
        })

    @http.route('/mail/mailing/unsubscribe', type='json', auth='public')
    def mailing_update_list_subscription(self, mailing_id, opt_in_ids, opt_out_ids, email, res_id, token):
        try:
            mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        mailing_sudo.update_opt_out(email, opt_in_ids, False)
        mailing_sudo.update_opt_out(email, opt_out_ids, True)
        return True

    @http.route('/mailing/feedback', type='json', auth='public')
    def mailing_send_feedback(self, mailing_id, res_id, email, feedback, token):
        try:
            mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        model = request.env[mailing_sudo.mailing_model_real]
        records = model.sudo().search([('email_normalized', '=', tools.email_normalize(email))])
        for record in records:
            record.sudo().message_post(body=_("Feedback from %(email)s: %(feedback)s", email=email, feedback=feedback))
        return bool(records)

    @http.route(['/unsubscribe_from_list'], type='http', website=True, multilang=False, auth='public', sitemap=False)
    def mailing_unsubscribe_placeholder_link(self, **post):
        """Dummy route so placeholder is not prefixed by language, MUST have multilang=False"""
        raise BadRequest()

    # ------------------------------------------------------------
    # TRACKING
    # ------------------------------------------------------------

    @http.route('/mail/track/<int:mail_id>/<string:token>/blank.gif', type='http', auth='public')
    def track_mail_open(self, mail_id, token, **post):
        """ Email tracking. """
        mail = request.env['mail.mail'].sudo().browse(mail_id).exists()
        if not mail:
            raise BadRequest()
        if not consteq(token, mail._generate_mail_recipient_hash()):
            raise Unauthorized()

        request.env['mailing.trace'].sudo().set_opened(domain=[('mail_mail_id_int', 'in', [mail_id])])
        response = werkzeug.wrappers.Response()
        response.mimetype = 'image/gif'
        response.data = base64.b64decode(b'R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

        return response

    @http.route('/r/<string:code>/m/<int:mailing_trace_id>', type='http', auth="public")
    def full_url_redirect(self, code, mailing_trace_id, **post):
        # don't assume geoip is set, it is part of the website module
        # which mass_mailing doesn't depend on
        country_code = request.geoip.get('country_code')

        request.env['link.tracker.click'].sudo().add_click(
            code,
            ip=request.httprequest.remote_addr,
            country_code=country_code,
            mailing_trace_id=mailing_trace_id
        )
        return request.redirect(request.env['link.tracker'].get_url_from_code(code), code=301, local=False)

    # ------------------------------------------------------------
    # MAILING MANAGEMENT
    # ------------------------------------------------------------

    @http.route('/mailing/report/unsubscribe', type='http', website=True, auth='public')
    def mailing_report_deactivate(self, token, user_id):
        if not token or not user_id:
            raise BadRequest()
        user = request.env['res.users'].sudo().browse(int(user_id)).exists()
        if not user or not user.has_group('mass_mailing.group_mass_mailing_user') or \
           not consteq(token, request.env['mailing.mailing']._generate_mailing_report_hash(user.id)):
            raise Unauthorized()

        request.env['ir.config_parameter'].sudo().set_param('mass_mailing.mass_mailing_reports', False)
        render_vals = {}
        if user.has_group('base.group_system'):
            render_vals = {'menu_id': request.env.ref('mass_mailing.menu_mass_mailing_global_settings').id}
        return request.render('mass_mailing.mailing_report_deactivated', render_vals)

    @http.route(['/mailing/<int:mailing_id>/view'], type='http', website=True, auth='public')
    def mailing_view_in_browser(self, mailing_id, email=None, res_id=None, token=""):
        try:
            mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except NotFound:
            raise Unauthorized()
        except Unauthorized():
            if not request.env.user.has_group('mass_mailing.group_mass_mailing_user'):
                raise Unauthorized()

        res = mailing_sudo.convert_links()
        base_url = mailing_sudo.get_base_url().rstrip('/')
        urls_to_replace = [
            (base_url + '/unsubscribe_from_list', mailing_sudo._get_unsubscribe_url(email, res_id)),
            (base_url + '/view', mailing_sudo._get_view_url(email, res_id))
        ]
        for url_to_replace, new_url in urls_to_replace:
            if url_to_replace in res[mailing_id]:
                res[mailing_id] = res[mailing_id].replace(url_to_replace, new_url if new_url else '#')

        res[mailing_id] = res[mailing_id].replace(
            'class="o_snippet_view_in_browser"',
            'class="o_snippet_view_in_browser" style="display: none;"'
        )

        return request.render('mass_mailing.mailing_view', {
            'body': res[mailing_id],
        })

    # ------------------------------------------------------------
    # BLACKLIST
    # ------------------------------------------------------------

    @http.route('/mailing/blacklist/check', type='json', auth='public')
    def mail_blacklist_check(self, mailing_id, res_id, email, token):
        try:
            _mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        record = request.env['mail.blacklist'].sudo().with_context(active_test=False).search([('email', '=', tools.email_normalize(email))])
        if record['active']:
            return True
        return False

    @http.route('/mailing/blacklist/add', type='json', auth='public')
    def mail_blacklist_add(self, mailing_id, res_id, email, token):
        try:
            _mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        blacklist_rec = request.env['mail.blacklist'].sudo()._add(email)
        self._log_blacklist_action(
            blacklist_rec, mailing_id,
            _("""Requested blacklisting via unsubscription page."""))
        return True

    @http.route('/mailing/blacklist/remove', type='json', auth='public')
    def mail_blacklist_remove(self, mailing_id, res_id, email, token):
        try:
            _mailing_sudo = self._check_mailing_email_token(mailing_id, res_id, email, token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        blacklist_rec = request.env['mail.blacklist'].sudo()._remove(email)
        self._log_blacklist_action(
            blacklist_rec, mailing_id,
            _("""Requested de-blacklisting via unsubscription page."""))
        return True
