# -*- coding: utf-8 -*-

import ast
import csv
import logging
from collections import defaultdict

from odoo import SUPERUSER_ID, Command, _, api, models
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG
from odoo.tools import file_open

_logger = logging.getLogger(__name__)

TEMPLATE_MODELS = (
    'res.company',
    'account.account',
    'account.tax.group',
    'account.tax',
    'account.journal',
    'account.group',
    'account.reconcile.model',
)


def preserve_existing_tags_on_taxes(cr, registry, module):
    '''
        This is a utility function used to preserve existing previous tags during upgrade of the module.
    '''
    env = api.Environment(cr, SUPERUSER_ID, {})
    xml_records = env['ir.model.data'].search([('model', '=', 'account.account.tag'), ('module', 'like', module)])
    if xml_records:
        cr.execute("update ir_model_data set noupdate = 't' where id in %s", [tuple(xml_records.ids)])

class AccountChartTemplate(models.AbstractModel):
    _name = "account.chart.template"
    _description = "Account Chart Template"

    def get_default_chart_template_code(self):
        return 'generic_coa'

    def get_chart_template_mapping(self):
        def templ(code, name=None, country='', modules=None, parent=None):
            country_code = country or code.split('_')[0] if country is not None else None
            country = country_code and self.ref(f"base.{country_code}", raise_if_not_found=False)
            country_name = "%s %s" % ("".join(chr(int(f"1f1{ord(c)+165:02x}", base=16)) for c in country.code), f" {country.name}") if country else ''
            return (code, {
                'name': country_name and (f"{country_name} - {name}" if name else country_name) or name,
                'country_id': country and country.id,
                'country_code': country and country.code,
                'modules': modules or [f"l10n_{code.split('_')[0]}"],
                'parent': parent,
            })

        return dict([
            # TODO translability of names?
            templ('generic_coa', name='Generic Chart Template', country=None, modules=['account']),
            templ('ae'),
            templ('ar_base', 'Monotributista / Base'),
            templ('ar_ex', 'Exentos', parent='ar_base'),
            templ('ar_ri', 'Responsables Inscriptos', parent='ar_ex'),
            templ('at'),
            templ('au'),
            templ('be'),
            templ('bg'),
            templ('bo'),
            templ('br'),
            templ('ca'),
            templ('ch'),
            templ('cl'),
            templ('cn'),
            templ('co'),
            templ('cr'),
            templ('cz'),
            templ('de_skr03', 'SKR03', modules=['l10n_de', 'l10n_de_skr03']),
            templ('de_skr04', 'SKR04', modules=['l10n_de', 'l10n_de_skr04']),
            templ('dk'),
            templ('do'),
            templ('dz'),
            templ('ec'),
            templ('eg'),
            templ('es_assec', 'entidades sin ánimo de lucro', parent='es_common'),
            templ('es_common', 'común'),
            templ('es_full', 'completo', parent='es_common'),
            templ('es_pymes', 'PYMEs', parent='es_common'),
            templ('et'),
            templ('fi'),
            templ('fr'),
            templ('gr'),
            templ('gt'),
            templ('hk'),
            templ('hn'),
            templ('hr'),
            templ('hu'),
            templ('id'),
            templ('ie'),
            templ('il'),
            templ('in'),
            templ('it'),
            templ('jp'),
            templ('ke'),
            templ('kz'),
            templ('lt'),
            templ('lu'),
            templ('ma'),
            templ('mn'),
            templ('mx'),
            templ('my'),
            templ('nl'),
            templ('no'),
            templ('nz'),
            templ('pa'),
            templ('pe'),
            templ('ph'),
            templ('pk'),
            templ('pl'),
            templ('pt'),
            templ('ro'),
            templ('rs'),
            templ('sa'),
            templ('se', 'Minimalist'),
            templ('se_k2', 'Complete K2', parent='se'),
            templ('se_k3', 'Complete K3', parent='se_k2'),
            templ('sg'),
            templ('si'),
            templ('sk'),
            templ('syscohada', 'SYSCOHADA', country=None),
            templ('th'),
            templ('tr'),
            templ('tw'),
            templ('ua_ias', 'МСФЗ'),
            templ('ua_psbo', 'ПСБО'),
            templ('uk'),
            templ('uy'),
            templ('ve'),
            templ('vn'),
            templ('za'),
        ])

    def _select_chart_template(self, company=False):
        company = company or self.env.company
        chart_template_mapping = self.get_chart_template_mapping()
        result = [(key, template['name']) for key, template in chart_template_mapping.items()]
        if company:
            proposed = self._guess_chart_template(company)
            result.sort(key=lambda sel: (sel[0] != proposed))
        return result

    def _guess_chart_template(self, company=False):
        # TODO: also fix account/populate/res_company.py then
        company = company or self.env.company
        country = company.country_id
        default_chart_template = self.get_default_chart_template_code()
        if not company.country_id:
            return default_chart_template
        # Python 3.7 dicts preserve the order, so it will take the first entry that matches the country code
        return next((x for x in self._get_template_codes_for_country(country.code)), default_chart_template)

    def _get_template_codes_for_country(self, country_code):
        chart_templates = self.get_chart_template_mapping()
        return [key for key, template in chart_templates.items() if template['country_code'] == country_code]

    def _get_tag_mapper(self, template_code):
        tags = {x.name: x.id for x in self.env['account.account.tag'].search([
            ('applicability', '=', 'taxes'),
            ('country_id', '=', self.get_chart_template_mapping()[template_code]['country_id']),
        ])}
        return lambda *args: [tags[x] for x in args]

    def try_loading(self, template_code, company, install_demo=True):
        """ Checks if the chart template can be loaded then proceeds installing it.

        :param template_code (str): code of the chart template to be loaded.
        :param company (Model<res.company>): the company we try to load the chart template on.
            If not provided, it is retrieved from the context.
        :param install_demo (bool): whether or not we should load demo data right after loading the
            chart template.
        """
        if not company:
            company = self.env.company
        if isinstance(company, int):
            company = self.env['res.company'].browse([company])

        template_code = template_code or company and self._guess_chart_template(company)

        return self._load(template_code, company, install_demo)

    def _load(self, template_code, company, install_demo):
        """ Installs this chart of accounts for the current company.
        This function is overridden in modules like point_of_sales.

        :param template_code (str): code of the chart template to be loaded.
        :param company (Model<res.company>): the company we try to load the chart template on.
            If not provided, it is retrieved from the context.
        :param install_demo (bool): whether or not we should load demo data right after loading the
            chart template.
        """
        # Ensure that the context is the correct one, even if not called by try_loading
        self = self.with_context(default_company_id=company.id, allowed_company_ids=[company.id], tracking_disable=True, loading_coa=True)

        module_names = self.get_chart_template_mapping()[template_code].get('modules', [])
        module_ids = self.env['ir.module.module'].search([('name', 'in', module_names), ('state', '=', 'uninstalled')])
        if module_ids:
            module_ids.sudo().button_immediate_install()
            self.env.reset()

        # TODO use id instead of xml_id
        xml_id = company.get_metadata()[0]['xmlid']
        if not xml_id:
            self.env['ir.model.data']._update_xmlids([{
                'xml_id': f"base.company_{company.id}",
                'record': company
            }])

        template_data = self._get_data(template_code, 'template_data', get_root=True)
        data = self._get_data(template_code, "chart_template_data", get_root=True)

        reload_template = template_code == company.chart_template
        if reload_template:
            for model_name, records in data.items():
                _fields = self.env[model_name]._fields
                for xml_id, values in records.items():
                    x2manyfields = [
                        fname
                        for fname in values
                        if fname in _fields and _fields[fname].type in ('one2many', 'many2many') and isinstance(values[fname], (list, tuple))
                    ]
                    if x2manyfields:
                        rec = self.ref(xml_id, raise_if_not_found=False)
                        if rec:
                            for fname in x2manyfields:
                                for i, (line, vals) in enumerate(zip(rec[fname], values[fname])):
                                    values[fname][i] = Command.update(line.id, vals[2])
        else:
            for model in ('account.move',) + TEMPLATE_MODELS[::-1]:
                if model != 'res.company':
                    self.env[model].sudo().search([('company_id', '=', company.id)]).with_context({MODULE_UNINSTALL_FLAG: True}).unlink()


        company.chart_template = template_code
        data = self._pre_load_data(template_code, company, template_data, data)
        self._load_data(data)
        self._post_load_data(template_code, company, template_data)

        # Install the demo data when the first localization is instanciated on the company
        if install_demo and self.ref('base.module_account').demo and not reload_template:
            try:
                with self.env.cr.savepoint():
                    self._load_data(self._get_demo_data(company))
                    self._post_load_demo_data(company)
            except Exception:
                # Do not rollback installation of CoA if demo data failed
                _logger.exception('Error while loading accounting demo data')

    def _load_template_data(self, template_code, company, template_data, country_id):
        # Apply template data to the company
        filter_properties = lambda key: (
            (not key.startswith("property_") or key.startswith("property_stock_") or key == "additional_properties")
            and key in company._fields
        )
        # Set the currency to the fiscal country's currency
        vals = {key: val for key, val in template_data.items() if filter_properties(key)}
        vals['currency_id'] = country_id.currency_id.id
        if not company.country_id:
            vals['country_id'] = country_id.id

        # This write method is important because it's overridden and has additional triggers
        # e.g it activates the currency
        company.write(vals)

    def _pre_load_data(self, template_code, company, template_data, data):
        """
            Some of the data needs special pre_process before being fed to the database.
            e.g. the account codes' width must be standardized to the code_digits applied.
            The fiscal country code must be put in place before taxes are generated.
        """
        xml_id = company.get_external_id()[company.id]
        if 'account_fiscal_country_id' in data['res.company'][xml_id]:
            fiscal_country = self.ref(data['res.company'][xml_id]['account_fiscal_country_id'])
        else:
            fiscal_country = company.account_fiscal_country_id
        for model in ('account.fiscal.position', 'account.reconcile.model'):
            if model in data:
                data[model] = data.pop(model)
        self._load_template_data(template_code, company, template_data, fiscal_country)

        # Normalize the code_digits of the accounts
        code_digits = int(template_data.get('code_digits', 6))
        for key, account_data in data.get('account.account', {}).items():
            data['account.account'][key]['code'] = f'{account_data["code"]:<0{code_digits}}'

        return data

    def ref(self, xmlid, raise_if_not_found=True):
        return self.env.ref(f"account.{self.env.company.id}_{xmlid}" if xmlid and '.' not in xmlid else xmlid, raise_if_not_found)

    def _load_data(self, data):
        # TODO document and check naming

        def deref(values, model):
            fields = ((model._fields[k], k, v) for k, v in values.items() if k in model._fields)
            for field, field_idx, value in fields:
                if not value:
                    values[field_idx] = False
                elif isinstance(value, str) and (
                    field.type == 'many2one'
                    or (field.type in ('integer', 'many2one_reference') and not value.isdigit())
                ):
                    values[field_idx] = self.ref(value).id
                elif field.type in ('one2many', 'many2many') and isinstance(value[0], (list, tuple)):
                    for i, (command, _id, *last_part) in enumerate(value):
                        if last_part:
                            last_part = last_part[0]
                        # (0, 0, {'test': 'account.ref_name'}) -> Command.Create({'test': 13})
                        if command in (Command.CREATE, Command.UPDATE):
                            deref(last_part, self.env[field.comodel_name])
                        # (6, 0, ['account.ref_name']) -> Command.Set([13])
                        if command == Command.SET:
                            for subvalue_idx, subvalue in enumerate(last_part):
                                if isinstance(subvalue, str):
                                    last_part[subvalue_idx] = self.ref(subvalue).id
                        if command == Command.LINK and isinstance(_id, str):
                            value[i] = Command.link(self.ref(_id).id)
                elif field.type in ('one2many', 'many2many') and isinstance(value, str):
                    values[field_idx] = [Command.set([
                        self.ref(v).id
                        for v in value.split(',')
                        if v
                    ])]
            return values

        def defer(all_data):
            created_models = set()
            while all_data:
                (model, data), *all_data = all_data
                to_delay = defaultdict(dict)
                for xml_id, vals in data.items():
                    to_be_removed = []
                    for field_name in vals:
                        field = self.env[model]._fields.get(field_name, None)
                        if (field and
                            field.relational and
                            field.comodel_name not in created_models and
                            (field.comodel_name in dict(all_data) or field.comodel_name == model)
                        ):
                            to_be_removed.append(field_name)
                            to_delay[xml_id][field_name] = vals.get(field_name)
                    for field_name in to_be_removed:
                        del vals[field_name]
                if any(to_delay.values()):
                    all_data.append((model, to_delay))
                yield model, data
                created_models.add(model)

        for model, data in defer(list(data.items())):
            _logger.debug("Loading model %s ...", model)
            translate_vals = []
            create_vals = []

            for xml_id, record in data.items():
                xml_id = f"{('account.' + str(self.env.company.id) + '_') if '.' not in xml_id else ''}{xml_id}"
                if any('@' in key for key in record):
                    translate_vals.append({
                        translate.split('@')[1]: value
                        for translate, value in record.items()
                        if '@' in translate and value
                    })
                    translate_vals[-1]['en_US'] = record['name']
                    for key in list(record):
                        if '@' in key:
                            del record[key]
                create_vals.append({
                    'xml_id': xml_id,
                    'values': deref(record, self.env[model]),
                    'noupdate': True,
                })

            _logger.debug('Loading records for model %s...', model)
            created = self.env[model].sudo()._load_records(create_vals)
            if translate_vals:
                # Update the translations in batch for all languages
                self.env.cache.update_raw(created, created._fields['name'], translate_vals, dirty=True)
            _logger.debug('Loaded records for model %s', model)

    def _load_csv(self, template_code, model):
        Model = self.env[model]
        model_fields = Model._fields

        template = self.get_chart_template_mapping().get(template_code)
        module = template['modules'][-1]

        res = {}
        for suffix in self._get_parent_suffix(template_code)[::-1] or ['']:
            try:
                with file_open(f"{module}/data/template/{model}{f'-{suffix}' if suffix else ''}.csv", 'r') as csv_file:
                    res.update({
                        row['id']: {
                            key: (
                                value if '@' in key
                                else (value and ast.literal_eval(value) or False) if model_fields[key].type in ('boolean', 'int', 'float')
                                else value
                            )
                            for key, value in ((key.replace('/id', ''), value) for key, value in row.items())
                            if key != 'id'
                        }
                        for row in csv.DictReader(csv_file)
                    })
            except FileNotFoundError:
                _logger.debug("No file %s found for template '%s'", model, module)
        return res

    def _get_parent_suffix(self, code):
        parents = []
        template_mapping = self.get_chart_template_mapping()
        while self.get_chart_template_mapping().get(code):
            parents.append(code)
            code = template_mapping.get(code).get('parent')
        return parents

    def _is_templated(self, template_code, model):
        func = template_code and self._get_data_func(template_code, model)
        return func and func.__name__ != f"_get_{model.replace('.', '_')}"

    def _get_data(self, template_code, model, get_root=False):
        assert model in self.env or 'template_data' in model
        funcs = [
            getattr(self, func_name)
            for func_name in (
                f"_get{'_' + suffix if suffix else ''}_{model.replace('.', '_')}"
                for suffix in self._get_parent_suffix(template_code)
            )
            if hasattr(self, func_name)
        ]
        if not funcs or get_root:
            funcs += [getattr(self, f"_get_{model.replace('.', '_')}")]
        return {
            k: v
            for func in funcs
            for k, v in func(template_code).items()
        }

    def _post_load_data(self, template_code, company, template_data):
        company = (company or self.env.company)
        additional_properties = template_data.pop('additional_properties', {})

        self._setup_utility_bank_accounts(template_code, company, template_data)

        # Unaffected earnings account on the company (if not present yet)
        company.get_unaffected_earnings_account()

        # Set newly created Cash difference and Suspense accounts to the Cash and Bank journals
        for kind, journal in [(kind, self.ref(kind)) for kind in ('bank', 'cash')]:
            journal.suspense_account_id = journal.suspense_account_id or company.account_journal_suspense_account_id
            journal.profit_account_id = journal.profit_account_id or company.default_cash_difference_income_account_id
            journal.loss_account_id = journal.loss_account_id or company.default_cash_difference_expense_account_id

        # Set newly created journals as defaults for the company
        if not company.tax_cash_basis_journal_id:
            company.tax_cash_basis_journal_id = self.ref('caba')
        if not company.currency_exchange_journal_id:
            company.currency_exchange_journal_id = self.ref('exch')

        # Setup default Income/Expense Accounts on Sale/Purchase journals
        self.ref("sale").default_account_id = self.ref(template_data.get('property_account_income_categ_id'))
        self.ref("purchase").default_account_id = self.ref(template_data.get('property_account_expense_categ_id'))

        # Set default Purchase and Sale taxes on the company
        if not company.account_sale_tax_id:
            company.account_sale_tax_id = self.env['account.tax'].search([
                ('type_tax_use', 'in', ('sale', 'all')), ('company_id', '=', company.id)], limit=1).id
        if not company.account_purchase_tax_id:
            company.account_purchase_tax_id = self.env['account.tax'].search([
                ('type_tax_use', 'in', ('purchase', 'all')), ('company_id', '=', company.id)], limit=1).id

        for field, model in {
            **additional_properties,
            'property_account_receivable_id': 'res.partner',
            'property_account_payable_id': 'res.partner',
            'property_account_expense_categ_id': 'product.category',
            'property_account_income_categ_id': 'product.category',
            'property_account_expense_id': 'product.template',
            'property_account_income_id': 'product.template',
            'property_tax_payable_account_id': 'account.tax.group',
            'property_tax_receivable_account_id': 'account.tax.group',
            'property_advance_tax_payment_account_id': 'account.tax.group',
            'property_stock_journal': 'product.category',
            'property_stock_account_input_categ_id': 'product.category',
            'property_stock_account_output_categ_id': 'product.category',
            'property_stock_valuation_account_id': 'product.category',
        }.items():
            value = template_data.get(field)
            if value and field in self.env[model]._fields:
                self.env['ir.property']._set_default(field, model, self.ref(value).id, company=company)

    def _get_chart_template_data(self, template_code):
        company = self.env.company
        data = {}
        try:
            for model in TEMPLATE_MODELS:
                data[model] = self._get_data(template_code, model)
        except Exception as e:
            message = f"Error in data from model {model} for template '{template_code}' and company '{company.name}' ({company.id})"
            raise RuntimeError(message) from e
        return data


    def _setup_utility_bank_accounts(self, template_code, company, template_data):
        """
            Define basic bank accounts for the company.
            - Suspense Account
            - Outstanding Receipts/Payments Accounts
            - Cash Difference Gain/Loss Accounts
            - Liquidity Transfer Account
        """
        # Create utility bank_accounts
        bank_prefix = template_data.get('bank_account_code_prefix', '')
        cash_prefix = template_data.get('cash_account_code_prefix', '')   # TODO unused ?
        code_digits = int(template_data.get('code_digits', 6))
        accounts_data = {
            'account_journal_suspense_account_id': {
                'name': _("Bank Suspense Account"),
                'prefix': bank_prefix,
                'account_type': 'asset_current',
            },
            'account_journal_payment_debit_account_id': {
                'name': _("Outstanding Receipts"),
                'prefix': bank_prefix,
                'account_type': 'asset_current',
                'reconcile': True,
            },
            'account_journal_payment_credit_account_id': {
                'name': _("Outstanding Payments"),
                'prefix': bank_prefix,
                'account_type': 'asset_current',
                'reconcile': True,
            },
            'account_journal_early_pay_discount_loss_account_id': {
                'name': _("Cash Discount Loss"),
                'code': '999998',
                'account_type': 'expense',
            },
            'account_journal_early_pay_discount_gain_account_id': {
                'name': _("Cash Discount Gain"),
                'code': '999997',
                'account_type': 'income_other',
            },
            'default_cash_difference_income_account_id': {
                'name': _("Cash Difference Gain"),
                'prefix': '999',
                'account_type': 'expense',
                'tag_ids': [(6, 0, self.ref('account.account_tag_investing').ids)],
            },
            'default_cash_difference_expense_account_id': {
                'name': _("Cash Difference Loss"),
                'prefix': '999',
                'account_type': 'expense',
                'tag_ids': [(6, 0, self.ref('account.account_tag_investing').ids)],
            },
        }

        # Transfer account: if the chart_template has no parent, create the single company.transfer_account_id
        if not self.get_chart_template_mapping()[template_code].get('parent_id'):
            accounts_data['transfer_account_id'] = {
                'name': _("Liquidity Transfer"),
                'prefix': company.transfer_account_code_prefix,
                'account_type': 'asset_current',
                'reconcile': True,
            }

        # Create needed company's bank accounts described above
        for company_attr_name, account_data in accounts_data.items():
            if not company[company_attr_name]:
                if 'code' not in account_data:
                    account_data['code'] = self.env['account.account']._search_new_account_code(company, code_digits, account_data.pop('prefix'))
                xml_id = account_data.pop('xml_id', None)
                account_id = self.env['account.account'].create(account_data)
                if xml_id:
                    self.env['ir.model.data']._update_xmlids([{'xml_id': xml_id, 'record': account_id}])
                company[company_attr_name] = account_id

    # --------------------------------------------------------------------------------

    def _get_template_data(self, template_code):
        return {}

    def _get_account_account(self, template_code):
        return self._load_csv(template_code, 'account.account')

    def _get_account_group(self, template_code):
        return self._load_csv(template_code, 'account.group')

    def _get_account_tax_group(self, template_code):
        return {
            **self._load_csv(template_code, 'account.tax.group'),
            'tax_group_taxes': {
                'name': _("Taxes"),
                'sequence': 0,
            }
        }

    def _get_account_journal(self, template_code):
        return {
            "sale": {
                'name': _('Customer Invoices'),
                'type': 'sale',
                'code': _('INV'),
                'show_on_dashboard': True,
                'color': 11,
                'sequence': 5,
            },
            "purchase": {
                'name': _('Vendor Bills'),
                'type': 'purchase',
                'code': _('BILL'),
                'show_on_dashboard': True,
                'color': 11,
                'sequence': 6,
            },
            "general": {
                'name': _('Miscellaneous Operations'),
                'type': 'general',
                'code': _('MISC'),
                'show_on_dashboard': True,
                'sequence': 7,
            },
            "exch": {
                'name': _('Exchange Difference'),
                'type': 'general',
                'code': _('EXCH'),
                'show_on_dashboard': False,
                'sequence': 9,
            },
            "caba": {
                'name': _('Cash Basis Taxes'),
                'type': 'general',
                'code': _('CABA'),
                'show_on_dashboard': False,
                'sequence': 10,
            },
            "bank": {
                'name': _('Bank'),
                'type': 'bank',
                'show_on_dashboard': True,
                'sequence': 11
            },
            "cash": {
                'name': _('Cash'),
                'type': 'cash',
                'show_on_dashboard': True,
                'sequence': 12
            },
        }

    def _get_account_reconcile_model(self, template_code):
        return {
            "reconcile_perfect_match": {
                "name": _('Invoices/Bills Perfect Match'),
                "sequence": 1,
                "rule_type": 'invoice_matching',
                "auto_reconcile": True,
                "match_nature": 'both',
                "match_same_currency": True,
                "allow_payment_tolerance": True,
                "payment_tolerance_type": 'percentage',
                "payment_tolerance_param": 0,
                "match_partner": True,
            },
            "reconcile_partial_underpaid": {
                "name": _('Invoices/Bills Partial Match if Underpaid'),
                "sequence": 2,
                "rule_type": 'invoice_matching',
                "auto_reconcile": False,
                "match_nature": 'both',
                "match_same_currency": True,
                "allow_payment_tolerance": False,
                "match_partner": True,
            }
        }
