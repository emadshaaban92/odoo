# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2010 Savoir-faire Linux (<https://www.savoirfairelinux.com>).

from odoo import api, SUPERUSER_ID
from . import models


def load_translations(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref('l10n_ca.l10n_ca_chart_template').process_coa_translations()
