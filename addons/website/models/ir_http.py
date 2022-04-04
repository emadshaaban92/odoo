# Part of Odoo. See LICENSE file for full copyright and licensing details.
import contextlib
import logging
from lxml import etree
import os
import unittest
import time

import pytz
import werkzeug
import werkzeug.routing
import werkzeug.utils

from functools import partial

import odoo
from odoo import api, models
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from odoo.tools.json import scriptsafe as json_scriptsafe
from odoo.osv.expression import FALSE_DOMAIN
from odoo.addons.http_routing.models import ir_http
from odoo.addons.http_routing.models.ir_http import _guess_mimetype
from odoo.addons.portal.controllers.portal import _build_url_w_params

logger = logging.getLogger(__name__)


def sitemap_qs2dom(qs, route, field='name'):
    """ Convert a query_string (can contains a path) to a domain"""
    dom = []
    if qs and qs.lower() not in route:
        needles = qs.strip('/').split('/')
        # needles will be altered and keep only element which one is not in route
        # diff(from=['shop', 'product'], to=['shop', 'product', 'product']) => to=['product']
        unittest.util.unorderable_list_difference(route.strip('/').split('/'), needles)
        if len(needles) == 1:
            dom = [(field, 'ilike', needles[0])]
        else:
            dom = FALSE_DOMAIN
    return dom


def get_request_website():
    """ Return the website set on `request` if called in a frontend context
    (website=True on route).
    This method can typically be used to check if we are in the frontend.

    This method is easy to mock during python tests to simulate frontend
    context, rather than mocking every method accessing request.website.

    Don't import directly the method or it won't be mocked during tests, do:
    ```
    from odoo.addons.website.models import ir_http
    my_var = ir_http.get_request_website()
    ```
    """
    return request and getattr(request, 'website', False) or False


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def routing_map(cls, key=None):
        key = key or (request and request.website_routing)
        return super(Http, cls).routing_map(key=key)

    @classmethod
    def clear_caches(cls):
        super()._clear_routing_map()
        return super().clear_caches()

    @classmethod
    def _slug_matching(cls, adapter, endpoint, **kw):
        for arg in kw:
            if isinstance(kw[arg], models.BaseModel):
                kw[arg] = kw[arg].with_context(slug_matching=True)
        qs = request.httprequest.query_string.decode('utf-8')
        return adapter.build(endpoint, kw) + (qs and '?%s' % qs or '')

    @classmethod
    def _generate_routing_rules(cls, modules, converters):
        website_id = request.website_routing
        logger.debug("_generate_routing_rules for website: %s", website_id)
        domain = [('redirect_type', 'in', ('308', '404')), '|', ('website_id', '=', False), ('website_id', '=', website_id)]

        rewrites = dict([(x.url_from, x) for x in request.env['website.rewrite'].sudo().search(domain)])
        cls._rewrite_len[website_id] = len(rewrites)

        for url, endpoint in super()._generate_routing_rules(modules, converters):
            if url in rewrites:
                rewrite = rewrites[url]
                url_to = rewrite.url_to
                if rewrite.redirect_type == '308':
                    logger.debug('Add rule %s for %s' % (url_to, website_id))
                    yield url_to, endpoint  # yield new url

                    if url != url_to:
                        logger.debug('Redirect from %s to %s for website %s' % (url, url_to, website_id))
                        _slug_matching = partial(cls._slug_matching, endpoint=endpoint)
                        endpoint.routing['redirect_to'] = _slug_matching
                        yield url, endpoint  # yield original redirected to new url
                elif rewrite.redirect_type == '404':
                    logger.debug('Return 404 for %s for website %s' % (url, website_id))
                    continue
            else:
                yield url, endpoint

    @classmethod
    def _get_converters(cls):
        """ Get the converters list for custom url pattern werkzeug need to
            match Rule. This override adds the website ones.
        """
        return dict(
            super()._get_converters(),
            model=ModelConverter,
        )

    @classmethod
    def _auth_method_public(cls):
        """ If no user logged, set the public user of current website, or default
            public user as request uid.
        """
        if not request.session.uid:
            website = request.env(user=SUPERUSER_ID)['website'].get_current_website()  # sudo
            if website:
                request.update_env(user=website._get_cached('user_id'))

        if not request.uid:
            super()._auth_method_public()

    @classmethod
    def _register_website_track(cls, response):
        if getattr(response, 'status_code', 0) != 200:
            return False

        template = False
        if hasattr(response, '_cached_page'):
            website_page, template = response._cached_page, response._cached_template
        elif hasattr(response, 'qcontext'):  # classic response
            main_object = response.qcontext.get('main_object')
            website_page = getattr(main_object, '_name', False) == 'website.page' and main_object
            template = response.qcontext.get('response_template')

        view = template and request.env['website'].get_template(template)
        if view and view.track:
            request.env['website.visitor']._handle_webpage_dispatch(response, website_page)

        return False

    @classmethod
    def _match(cls, path):
        if not hasattr(request, 'website_routing'):
            website = request.env['website'].get_current_website()
            request.website_routing = website.id

        return super()._match(path)

    @classmethod
    def _pre_dispatch(cls, rule, arguments):
        super()._pre_dispatch(rule, arguments)

        for record in arguments.values():
            if isinstance(record, models.BaseModel) and hasattr(record, 'can_access_from_current_website'):
                try:
                    if not record.can_access_from_current_website():
                        raise werkzeug.exceptions.NotFound()
                except AccessError:
                    # record.website_id might not be readable as
                    # unpublished `event.event` due to ir.rule, return
                    # 403 instead of using `sudo()` for perfs as this is
                    # low level.
                    raise werkzeug.exceptions.Forbidden()

    @classmethod
    def _get_web_editor_context(cls):
        ctx = super()._get_web_editor_context()
        if request.is_frontend_multilang and request.lang == cls._get_default_lang():
            ctx['edit_translations'] = False
        return ctx

    @classmethod
    def _frontend_pre_dispatch(cls):
        super()._frontend_pre_dispatch()

        if not request.context.get('tz'):
            with contextlib.suppress(pytz.UnknownTimeZoneError):
                tz = request.geoip.get('time_zone', '')
                request.update_context(tz=pytz.timezone(tz).zone)

        website = request.env['website'].get_current_website()
        user = request.env.user

        # This is mainly to avoid access errors in website controllers
        # where there is no context (eg: /shop), and it's not going to
        # propagate to the global context of the tab. If the company of
        # the website is not in the allowed companies of the user, set
        # the main company of the user.
        website_company_id = website._get_cached('company_id')
        if user.id == website._get_cached('user_id'):
            # avoid a read on res_company_user_rel in case of public user
            allowed_company_ids = [website_company_id]
        elif website_company_id in user.company_ids.ids:
            allowed_company_ids = [website_company_id]
        else:
            allowed_company_ids = user.company_id.ids

        request.update_context(
            allowed_company_ids=allowed_company_ids,
            website_id=website.id,
            **cls._get_web_editor_context(),
        )

        request.website = website.with_context(request.context)

    @classmethod
    def _dispatch(cls, endpoint):
        response = super()._dispatch(endpoint)
        cls._register_website_track(response)
        return response

    @classmethod
    def _get_frontend_langs(cls):
        # _get_frontend_langs() is used by @http_routing:IrHttp._match
        # where is_frontend is not yet set and when no backend endpoint
        # matched. We have to assume we are going to match a frontend
        # route, hence the default True. Elsewhere, request.is_frontend
        # is set.
        if getattr(request, 'is_frontend', True):
            website_id = request.env.get('website_id', request.website_routing)
            res_lang = request.env['res.lang'].with_context(website_id=website_id)
            return [code for code, *_ in res_lang.get_available()]
        else:
            return super()._get_frontend_langs()

    @classmethod
    def _get_default_lang(cls):
        if getattr(request, 'is_frontend', True):
            website = request.env['website'].sudo().get_current_website()
            return request.env['res.lang'].browse([website._get_cached('default_lang_id')])
        return super()._get_default_lang()

    @classmethod
    def _get_translation_frontend_modules_name(cls):
        mods = super()._get_translation_frontend_modules_name()
        installed = request.registry._init_modules.union(odoo.conf.server_wide_modules)
        return mods + [mod for mod in installed if mod.startswith('website')]

    @classmethod
    def _serve_page(cls):
        req_page = request.httprequest.path
        page_domain = [('url', '=', req_page)] + request.website.website_domain()

        published_domain = page_domain
        # specific page first
        page = request.env['website.page'].sudo().search(published_domain, order='website_id asc', limit=1)

        # redirect withtout trailing /
        if not page and req_page != "/" and req_page.endswith("/"):
            # mimick `_postprocess_args()` redirect
            path = request.httprequest.path[:-1]
            if request.lang != cls._get_default_lang():
                path = '/' + request.lang.url_code + path
            if request.httprequest.query_string:
                path += '?' + request.httprequest.query_string.decode('utf-8')
            return request.redirect(path, code=301)

        if page:
            # prefetch all menus (it will prefetch website.page too)
            menu_pages_ids = request.website._get_menu_page_ids()
            page.browse([page.id] + menu_pages_ids).mapped('view_id.name')
            request.website.menu_id

        if page and (request.website.is_publisher() or page.is_visible):
            need_to_cache = False
            cache_key = page._get_cache_key(request)
            if (
                page.cache_time  # cache > 0
                and request.httprequest.method == "GET"
                and request.env.user._is_public()    # only cache for unlogged user
                and 'nocache' not in request.httprequest.args  # allow bypass cache / debug
                and not request.session.debug
                and len(cache_key) and cache_key[-1] is not None  # nocache via expr
            ):
                need_to_cache = True
                try:
                    r = page._get_cache_response(cache_key)
                    if r['time'] + page.cache_time > time.time():
                        response = odoo.http.Response(r['content'], mimetype=r['contenttype'])
                        response._cached_template = r['template']
                        response._cached_page = page
                        return response
                except KeyError:
                    pass

            _, ext = os.path.splitext(req_page)
            response = request.render(page.view_id.id, {
                'deletable': True,
                'main_object': page,
            }, mimetype=_guess_mimetype(ext))

            if need_to_cache and response.status_code == 200:
                r = response.render()
                page._set_cache_response(cache_key, {
                    'content': r,
                    'contenttype': response.headers['Content-Type'],
                    'time': time.time(),
                    'template': getattr(response, 'qcontext', {}).get('response_template')
                })
            return response
        return False

    @classmethod
    def _serve_redirect(cls):
        req_page = request.httprequest.path
        domain = [
            ('redirect_type', 'in', ('301', '302')),
            # trailing / could have been removed by server_page
            '|', ('url_from', '=', req_page.rstrip('/')), ('url_from', '=', req_page + '/')
        ]
        domain += request.website.website_domain()
        return request.env['website.rewrite'].sudo().search(domain, limit=1)

    @classmethod
    def _serve_fallback(cls):
        # serve attachment before
        parent = super()._serve_fallback()
        if parent:  # attachment
            return parent

        # minimal setup to serve frontend pages
        if not request.uid:
            cls._auth_method_public()
        cls._frontend_pre_dispatch()
        cls._handle_debug()
        request.params = request.get_http_params()

        website_page = cls._serve_page()
        if website_page:
            website_page.flatten()
            cls._register_website_track(website_page)
            cls._post_dispatch(website_page)
            return website_page

        redirect = cls._serve_redirect()
        if redirect:
            return request.redirect(
                _build_url_w_params(redirect.url_to, request.params),
                code=redirect.redirect_type,
                local=False)  # safe because only designers can specify redirects

    @classmethod
    def _get_exception_code_values(cls, exception):
        code, values = super()._get_exception_code_values(exception)
        if isinstance(exception, werkzeug.exceptions.NotFound) and request.website.is_publisher():
            code = 'page_404'
            values['path'] = request.httprequest.path[1:]
        if isinstance(exception, werkzeug.exceptions.Forbidden) and \
           exception.description == "website_visibility_password_required":
            code = 'protected_403'
            values['path'] = request.httprequest.path
        return (code, values)

    @classmethod
    def _get_values_500_error(cls, env, values, exception):
        View = env["ir.ui.view"]
        values = super()._get_values_500_error(env, values, exception)
        if 'qweb_exception' in values:
            try:
                # exception.name might be int, string
                exception_template = int(exception.name)
            except ValueError:
                exception_template = exception.name
            view = View._view_obj(exception_template)
            if exception.html and exception.html in view.arch:
                values['view'] = view
            else:
                # There might be 2 cases where the exception code can't be found
                # in the view, either the error is in a child view or the code
                # contains branding (<div t-att-data="request.browse('ok')"/>).
                et = view.with_context(inherit_branding=False)._get_combined_arch()
                node = et.xpath(exception.path) if exception.path else et
                line = node is not None and etree.tostring(node[0], encoding='unicode')
                if line:
                    values['view'] = View._views_get(exception_template).filtered(
                        lambda v: line in v.arch
                    )
                    values['view'] = values['view'] and values['view'][0]
        # Needed to show reset template on translated pages (`_prepare_environment` will set it for main lang)
        values['editable'] = request.uid and request.website.is_publisher()
        return values

    @classmethod
    def _get_error_html(cls, env, code, values):
        if code in ('page_404', 'protected_403'):
            return code.split('_')[1], env['ir.ui.view']._render_template('website.%s' % code, values)
        return super()._get_error_html(env, code, values)

    def binary_content(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       unique=False, filename=None, filename_field='name', download=False,
                       mimetype=None, default_mimetype='application/octet-stream',
                       access_token=None):
        obj = None
        if xmlid:
            obj = self._xmlid_to_obj(self.env, xmlid)
        elif id and model in self.env:
            obj = self.env[model].browse(int(id))
        if obj and 'website_published' in obj._fields:
            try:
                if obj.sudo().website_published:
                    self = self.sudo()
            except MissingError:
                pass
        return super(Http, self).binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype,
            default_mimetype=default_mimetype, access_token=access_token)

    @classmethod
    def _xmlid_to_obj(cls, env, xmlid):
        website_id = env['website'].get_current_website()
        if website_id and website_id.theme_id:
            domain = [('key', '=', xmlid), ('website_id', '=', website_id.id)]
            Attachment = env['ir.attachment']
            if request.env.user.share:
                domain.append(('public', '=', True))
                Attachment = Attachment.sudo()
            obj = Attachment.search(domain)
            if obj:
                return obj[0]

        return super()._xmlid_to_obj(env, xmlid)

    @api.model
    def get_frontend_session_info(self):
        session_info = super(Http, self).get_frontend_session_info()
        geoip_country_code = request.geoip.get('country_code')
        geoip_phone_code = request.env['res.country']._phone_code_for(geoip_country_code) if geoip_country_code else None
        session_info.update({
            'is_website_user': request.env.user.id == request.website.user_id.id,
            'geoip_country_code': geoip_country_code,
            'geoip_phone_code': geoip_phone_code,
            'has_cookies_bar': request.website.cookies_bar,
        })
        if request.env.user.has_group('website.group_website_publisher'):
            session_info.update({
                'website_id': request.website.id,
                'website_company_id': request.website._get_cached('company_id'),
            })
        return session_info

    @classmethod
    def _is_allowed_cookie(cls, cookie_type, cookie_name="undefined"):
        result = super()._is_allowed_cookie(cookie_type, cookie_name)

        if cookie_type not in ["required", "optional"]:
            logger.warning("Cookie %s of type %s is unknown.", cookie_name, cookie_type)
            cookie_type = 'required'

        if cookie_type == 'required':
            return result

        # If user has not rejected optional cookies, they are accepted by default
        accepted_cookie_types = json_scriptsafe.loads(request.httprequest.cookies.get('accepted_cookie_types', '{"required": true, "optional": true}'))

        if cookie_type in accepted_cookie_types:
            return accepted_cookie_types[cookie_type] and result

        logger.warning("Cookie %s of type %s not found in consents.", cookie_name, cookie_type)
        return result


class ModelConverter(ir_http.ModelConverter):

    def to_url(self, value):
        if value.env.context.get('slug_matching'):
            return value.env.context.get('_converter_value', str(value.id))
        return super().to_url(value)

    def generate(self, env, args, dom=None):
        Model = env[self.model]
        # Allow to current_website_id directly in route domain
        args['current_website_id'] = env['website'].get_current_website().id
        domain = safe_eval(self.domain, args)
        if dom:
            domain += dom
        for record in Model.search(domain):
            # return record so URL will be the real endpoint URL as the record will go through `slug()`
            # the same way as endpoint URL is retrieved during dispatch (301 redirect), see `to_url()` from ModelConverter
            yield record
