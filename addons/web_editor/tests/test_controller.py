# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from base64 import b64encode
import binascii

from odoo import Command
from odoo.addons.http_routing.models.ir_http import slug
import odoo.tests
from odoo.tests.common import HttpCase
from odoo.tools import mute_logger
from odoo.tools.json import scriptsafe as json_safe

@odoo.tests.tagged('-at_install', 'post_install')
class TestController(HttpCase):
    def test_01_illustration_shape(self):
        self.authenticate('admin', 'admin')
        # SVG with all replaceable colors.
        svg = b"""
<svg viewBox="0 0 400 400">
  <rect width="300" height="300" style="fill:#3AADAA;" />
  <rect x="20" y="20" width="300" height="300" style="fill:#7C6576;" />
  <rect x="40" y="40" width="300" height="300" style="fill:#F6F6F6;" />
  <rect x="60" y="60" width="300" height="300" style="fill:#FFFFFF;" />
  <rect x="80" y="80" width="300" height="300" style="fill:#383E45;" />
</svg>
        """
        # Need to bypass security check to write image with mimetype image/svg+xml
        context = {'binary_field_real_user': self.env['res.users'].sudo().browse([1])}
        attachment = self.env['ir.attachment'].sudo().with_context(context).create({
            'name': 'test.svg',
            'mimetype': 'image/svg+xml',
            'datas': binascii.b2a_base64(svg, newline=False),
            'public': True,
            'res_model': 'ir.ui.view',
            'res_id': 0,
        })
        # Shape illustration with slug.
        url = '/web_editor/shape/illustration/%s' % slug(attachment)
        palette = 'c1=%233AADAA&c2=%237C6576&&c3=%23F6F6F6&&c4=%23FFFFFF&&c5=%23383E45'
        attachment['url'] = '%s?%s' % (url, palette)

        response = self.url_open(url)
        self.assertEqual(200, response.status_code, 'Expect response')
        self.assertEqual(svg, response.content, 'Expect unchanged SVG')

        response = self.url_open(url + '?c1=%23ABCDEF')
        self.assertEqual(200, response.status_code, 'Expect response')
        self.assertEqual(len(svg), len(response.content), 'Expect same length as original')
        self.assertTrue('ABCDEF' in str(response.content), 'Expect patched c1')
        self.assertTrue('3AADAA' not in str(response.content), 'Old c1 should not be there anymore')

        # Shape illustration without slug.
        url = '/web_editor/shape/illustration/noslug'
        attachment['url'] = url

        response = self.url_open(url)
        self.assertEqual(200, response.status_code, 'Expect response')
        self.assertEqual(svg, response.content, 'Expect unchanged SVG')

        response = self.url_open(url + '?c1=%23ABCDEF')
        self.assertEqual(200, response.status_code, 'Expect response')
        self.assertEqual(len(svg), len(response.content), 'Expect same length as original')
        self.assertTrue('ABCDEF' in str(response.content), 'Expect patched c1')
        self.assertTrue('3AADAA' not in str(response.content), 'Old c1 should not be there anymore')

    def test_02_modify_image(self):
        gif_base64 = b"R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs="
        attachment = self.env['ir.attachment'].create({
            'name': 'test.gif',
            'mimetype': 'image/gif',
            'datas': gif_base64,
            'public': True,
            'res_model': 'ir.ui.view',
            'res_id': 0,
        })

        def modify(name, expect_fail=False):
            svg = b'<svg viewBox="0 0 400 400"><!-- %s --><image url="data:image/gif;base64,%s" /></svg>' % (name.encode('ascii'), gif_base64)
            response = self.url_open('/web_editor/modify_image/%s' % attachment.id,
                headers={'Content-Type': 'application/json'},
                data=json_safe.dumps({
                    "params": {
                        "name": name,
                        "mimetype": "image/svg+xml",
                        "data": b64encode(svg).decode('ascii')
                    }
                }),
            )
            self.assertEqual(200, response.status_code, 'Expect response')
            if expect_fail:
                return json_safe.loads(response.content)
            url = json_safe.loads(response.content).get('result')
            self.assertTrue(url.endswith(name), 'Expect name in URL')
            response = self.url_open(url)
            self.assertEqual(200, response.status_code, 'Expect response')
            self.assertEqual('image/svg+xml', response.headers.get('Content-Type'), 'Expect SVG mimetype')
            self.assertEqual(svg, response.content, 'Expect unchanged SVG')

        self.authenticate('admin', 'admin')
        modify('admin.gif')

        demo_user = self.env['res.users'].search([('login', '=', 'demo')])
        demo_user.write({
            'groups_id': [
                Command.clear(),
                Command.link(self.env.ref('base.group_user').id),
            ]
        })
        self.authenticate('demo', 'demo')
        json = modify('demofail.gif', True)
        self.assertFalse(json.get('result'), 'Expect no URL when called with insufficient rights')

        demo_user.write({
            'groups_id': [
                Command.clear(),
                Command.link(self.env.ref('base.group_user').id),
                Command.link(self.env.ref('website.group_website_publisher').id),
            ]
        })
        self.authenticate('demo', 'demo')
        modify('demo.gif')

        self.authenticate('portal', 'portal')
        with mute_logger('odoo.http'):
            json = modify('portalfail.gif', True)
        self.assertEqual('odoo.exceptions.AccessError', json.get('error').get('data').get('name'), 'Expect access error')
