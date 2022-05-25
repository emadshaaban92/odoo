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
        if not hash_token and request.env.user.share:
            raise BadRequest()
        if hash_token and (not mailing_id or not email or not document_id):
            raise BadRequest()
        if mailing_id:
            mailing_sudo = request.env['mailing.mailing'].sudo().browse(mailing_id)
            if not mailing_sudo.exists():
                raise NotFound()
        else:
            mailing_sudo = request.env['mailing.mailing'].sudo()
        if mailing_sudo and hash_token and not consteq(mailing_sudo._generate_mailing_recipient_hash(document_id, email), hash_token):
            raise Unauthorized()
        return mailing_sudo

    def _fetch_blacklist_record(self, email):
        if not email or not tools.email_normalize(email):
            return False
        return request.env['mail.blacklist'].sudo().with_context(
            active_test=False
        ).search(
            [('email', '=', tools.email_normalize(email))]
        )

    def _fetch_contacts(self, email):
        if not email or not tools.email_normalize(email):
            return False
        return request.env['mailing.contact'].sudo().search(
            [('email_normalized', '=', tools.email_normalize(email))]
        )

    def _fetch_user_information(self, email, hash_token):
        if hash_token or request.env.user.share:
            return email, hash_token
        return request.env.user.email_normalized, None

    def _log_blacklist_action(self, blacklist_entry, mailing_id, description):
        mailing = request.env['mailing.mailing'].sudo().browse(mailing_id)
        model_display = mailing.mailing_model_id.display_name
        blacklist_entry._message_log(body=description + " ({})".format(model_display))

    # ------------------------------------------------------------
    # SUBSCRIPTION MANAGEMENT
    # ------------------------------------------------------------

    @http.route('/mailing/my', type='http', website=True, auth='user')
    def mailing_my(self):
        _email, _hash_token = self._fetch_user_information(None, None)
        if not _email:
            raise Unauthorized()

        render_values = self._prepare_mailing_subscription_values(
            request.env['mailing.mailing'], False, _email, None
        )
        render_values.update(feedback_enabled=False)
        return request.render(
            'mass_mailing.page_mailing_unsubscribe',
            render_values
        )

    @http.route('/mailing/<int:mailing_id>/unsubscribe', type='http', website=True, auth='public')
    def mailing_unsubscribe(self, mailing_id, document_id=None, email=None, hash_token=None):
        _email, _hash_token = self._fetch_user_information(email, hash_token)
        try:
            mailing_sudo = self._check_mailing_email_token(mailing_id, document_id, _email, _hash_token)
        except NotFound:
            raise Unauthorized()

        if mailing_sudo.mailing_model_real == 'mailing.contact':
            return self._mailing_unsubscribe_from_list(mailing_sudo, document_id, _email, _hash_token)
        return self._mailing_unsubscribe_from_document(mailing_sudo, document_id, _email, _hash_token)

    def _mailing_unsubscribe_from_list(self, mailing, document_id, email, hash_token):
        # Unsubscribe directly + Let the user choose their subscriptions
        mailing.contact_list_ids._update_subscription_from_email(email, opt_out=True)

        # compute name of unsubscribed list: hide non public lists
        if all(not mlist.is_public for mlist in mailing.contact_list_ids):
            lists_unsubscribed_name = _('You are no longer part of our mailing list(s).')
        elif len(mailing.contact_list_ids) == 1:
            lists_unsubscribed_name = _('You are no longer part of the %(mailing_name)s mailing list.',
                                        mailing_name=mailing.contact_list_ids.name)
        else:
            lists_unsubscribed_name = _(
                'You are no longer part of the %(mailing_names)s mailing list.',
                ', '.join(mlist.name for mlist in mailing.contact_list_ids if mlist.is_public)
            )

        return request.render(
            'mass_mailing.page_mailing_unsubscribe',
            dict(
                self._prepare_mailing_subscription_values(
                    mailing, document_id, email, hash_token
                ),
                unsubscribed_name=lists_unsubscribed_name,
            )
        )

    def _mailing_unsubscribe_from_document(self, mailing, document_id, email, hash_token):
        blacklist_rec = request.env['mail.blacklist'].sudo()._add(email)
        self._log_blacklist_action(
            blacklist_rec, mailing.id,
            _("""Requested blacklisting via unsubscribe link."""))

        return request.render(
            'mass_mailing.page_mailing_unsubscribe',
            dict(
                self._prepare_mailing_subscription_values(
                    mailing, document_id, email, hash_token
                ),
                unsubscribed_name=_('You are no longer part of our services and will not be contacted again.'),
            )
        )

    def _prepare_mailing_subscription_values(self, mailing, document_id, email, hash_token):
        """ Prepare common values used in various subscription management or
        blacklist flows done in portal. """
        bl_record = self._fetch_blacklist_record(email)
        email_normalized = tools.email_normalize(email)

        # as there may be several contacts / email -> consider any opt-in overrides
        # opt-out
        contacts = self._fetch_contacts(email)
        lists_optin = contacts.subscription_ids.filtered(
            lambda sub: not sub.opt_out
        ).list_id
        lists_optout = contacts.subscription_ids.filtered(
            lambda sub: sub.opt_out and sub.list_id not in lists_optin
        ).list_id
        lists_public = request.env['mailing.list'].sudo().search(
            [('is_public', '=', True),
             ('id', 'not in', (lists_optin + lists_optout).ids)
            ],
            limit=10,
            order='create_date DESC, id DESC',
        )

        return {
            # customer
            'document_id': document_id,
            'email': email,
            'email_valid': bool(email_normalized),
            'hash_token': hash_token,
            'mailing_id': mailing.id,
            'res_id': document_id,
            # feedback
            'feedback_enabled': True,
            'feedback_readonly': False,
            # blacklist
            'blacklist_enabled': bool(
                request.env['ir.config_parameter'].sudo().get_param(
                    'mass_mailing.show_blacklist_buttons',
                    default=True,
                )
            ),
            'blacklist_possible': bl_record is not False,
            'is_blacklisted': bl_record.active if bl_record else False,
            # mailing lists
            'contacts': contacts,
            'lists_contacts': contacts.subscription_ids.list_id,
            'lists_optin': lists_optin,
            'lists_optout': lists_optout,
            'lists_public': lists_public,
        }

    @http.route('/mail/mailing/<int:mailing_id>/unsubscribe', type='http', website=True, auth='public')
    def _mailing_unsubscribe(self, mailing_id, res_id=None, email=None, token=None, **post):
        """ Backward compatible route, for mailings sent before saas~15.4 whose
        subscription links should work for a few weeks after migration. """
        params = werkzeug.urls.url_encode(
            dict(**post, document_id=res_id, email=email, hash_token=token)
        )
        return request.redirect(f'/mailing/{mailing_id}/unsubscribe?{params}')

    @http.route('/mailing/list/update', type='json', auth='public')
    def mailing_update_list_subscription(self, mailing_id=None, document_id=None,
                                         email=None, hash_token=None,
                                         lists_optin_ids=None):
        _email, _hash_token = self._fetch_user_information(email, hash_token)
        try:
            _mailing_sudo = self._check_mailing_email_token(mailing_id, document_id, _email, _hash_token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        contacts = self._fetch_contacts(email)
        lists_optin = request.env['mailing.list'].sudo().browse(lists_optin_ids or []).exists()
        # opt-out all not chosen lists
        lists_to_optout = contacts.subscription_ids.filtered(
            lambda sub: not sub.opt_out and sub.list_id not in lists_optin
        ).list_id
        # opt-in in either already member, either public (to avoid trying to opt-in
        # in private lists)
        lists_to_optin = lists_optin.filtered(
            lambda mlist: mlist.is_public or mlist in contacts.list_ids
        )

        if lists_to_optout:
            lists_to_optout._update_subscription_from_email(email, opt_out=True)
        if lists_to_optin:
            lists_to_optin._update_subscription_from_email(email, opt_out=False)

        return True

    @http.route('/mailing/feedback', type='json', auth='public')
    def mailing_send_feedback(self, mailing_id=None, document_id=None,
                              email=None, hash_token=None,
                              feedback=None):
        _email, _hash_token = self._fetch_user_information(email, hash_token)
        try:
            mailing_sudo = self._check_mailing_email_token(mailing_id, document_id, _email, _hash_token)
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

    @http.route('/mailing/blacklist/add', type='json', auth='public')
    def mail_blacklist_add(self, mailing_id=None, document_id=None,
                           email=None, hash_token=None):
        _email, _hash_token = self._fetch_user_information(email, hash_token)
        try:
            _mailing_sudo = self._check_mailing_email_token(mailing_id, document_id, _email, _hash_token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        blacklist_rec = request.env['mail.blacklist'].sudo()._add(_email)
        self._log_blacklist_action(
            blacklist_rec, mailing_id,
            _("""Requested blacklisting via unsubscription page."""))
        return True

    @http.route('/mailing/blacklist/remove', type='json', auth='public')
    def mail_blacklist_remove(self, mailing_id=None, document_id=None,
                              email=None, hash_token=None):
        _email, _hash_token = self._fetch_user_information(email, hash_token)
        try:
            _mailing_sudo = self._check_mailing_email_token(mailing_id, document_id, _email, _hash_token)
        except BadRequest:
            return 'error'
        except (NotFound, Unauthorized):
            return 'unauthorized'

        blacklist_rec = request.env['mail.blacklist'].sudo()._remove(email)
        self._log_blacklist_action(
            blacklist_rec, mailing_id,
            _("""Requested de-blacklisting via unsubscription page."""))
        return True
