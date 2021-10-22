# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    def _get_es_common_account_tax(self, template_code):
        taxes = super()._get_es_common_account_tax(template_code)
        taxes['account_tax_template_s_iva21b'].update({
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_iva21s'].update({
            'l10n_es_type': 'sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_s_iva21isp'].update({
            'l10n_es_type': 'sujeto_isp',
        })
        taxes['account_tax_template_p_iva21_bc'].update({
            'name': "21% IVA soportado (bienes corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva21_sc'].update({
            'name': "21% IVA soportado (servicios corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_p_iva21_sp_in'].update({
            'name': "IVA 21% Adquisición de servicios intracomunitarios",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_p_iva21_ic_bc'].update({
            'name': "IVA 21% Adquisición Intracomunitaria. Bienes corrientes",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva21_ic_bi'].update({
            'name': "IVA 21% Adquisición Intracomunitaria. Bienes de inversión",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva21_ibc'].update({
            'name': "IVA 21% Importaciones bienes corrientes",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva21_ibi'].update({
            'name': "IVA 21% Importaciones bienes de inversión",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_irpf21td'].update({
            'name': "Retenciones IRPF (Trabajadores) dinerarios",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_iva4_sp_ex'].update({
            'name': "IVA 4% Adquisición de servicios extracomunitarios",
            'l10n_es_type': 'sujeto_isp',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_sp_ex'].update({
            'name': "IVA 10% Adquisición de servicios extracomunitarios",
            'l10n_es_type': 'sujeto_isp',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva21_sp_ex'].update({
            'name': "IVA 21% Adquisición de servicios extracomunitarios",
            'l10n_es_type': 'sujeto_isp',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_p_iva4_ic_bc'].update({
            'name': "IVA 4% Adquisición Intracomunitario. Bienes corrientes",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva4_ic_bi'].update({
            'name': "IVA 4% Adquisición Intracomunitario. Bienes de inversión",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_ic_bc'].update({
            'name': "IVA 10% Adquisición Intracomunitario. Bienes corrientes",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_ic_bi'].update({
            'name': "IVA 10% Adquisición Intracomunitario. Bienes de inversión",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_iva0_sp_i'].update({
            'name': "IVA 0% Prestación de servicios intracomunitario",
            'l10n_es_type': 'no_sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_s_iva_ns'].update({
            'name': "No sujeto Repercutido (Servicios)",
            'l10n_es_type': 'no_sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_s_iva_ns_b'].update({
            'name': "No sujeto Repercutido (Bienes)",
            'l10n_es_type': 'no_sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_iva_e'].update({
            'name': "IVA 0% Prestación de servicios extracomunitaria",
            'l10n_es_type': 'no_sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_p_iva4_ibc'].update({
            'name': "IVA 4% Importaciones bienes corrientes",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva4_ibi'].update({
            'name': "IVA 4% Importaciones bienes de inversión",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_ibc'].update({
            'name': "IVA 10% Importaciones bienes corrientes",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_ibi'].update({
            'name': "IVA 10% Importaciones bienes de inversión",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva4_bi'].update({
            'name': "4% IVA Soportado (bienes de inversión)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
            'l10n_es_bien_inversion': True,
        })
        taxes['account_tax_template_p_iva4_sc'].update({
            'name': "4% IVA soportado (servicios corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_bi'].update({
            'name': "10% IVA Soportado (bienes de inversión)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
            'l10n_es_bien_inversion': True,
        })
        taxes['account_tax_template_p_iva21_bi'].update({
            'name': "21% IVA Soportado (bienes de inversión)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
            'l10n_es_bien_inversion': True,
        })
        taxes['account_tax_template_p_iva10_bc'].update({
            'name': "10% IVA soportado (bienes corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva4_bc'].update({
            'name': "4% IVA soportado (bienes corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva10_sc'].update({
            'name': "10% IVA soportado (servicios corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_iva0'].update({
            'name': "IVA Exento Repercutido Sujeto",
            'l10n_es_type': 'exento',
            'l10n_es_exempt_reason': 'E1',
        })
        taxes['account_tax_template_s_iva0_ns'].update({
            'name': "IVA Exento Repercutido No Sujeto",
            'l10n_es_type': 'ignore',
        })
        taxes['account_tax_template_s_req05'].update({
            'name': "0.50% Recargo Equivalencia Ventas",
            'l10n_es_type': 'recargo',
        })
        taxes['account_tax_template_s_iva4b'].update({
            'name': "IVA 4% (Bienes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_iva10b'].update({
            'name': "IVA 10% (Bienes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva0_nd'].update({
            'name': "21% IVA Soportado no deducible",
            'l10n_es_type': 'no_deducible',
        })
        taxes['account_tax_template_p_iva10_nd'].update({
            'name': "10% IVA Soportado no deducible",
            'l10n_es_type': 'no_deducible',
        })
        taxes['account_tax_template_p_iva4_nd'].update({
            'name': "4% IVA Soportado no deducible",
            'l10n_es_type': 'no_deducible',
        })
        taxes['account_tax_template_s_iva4s'].update({
            'name': "IVA 4% (Servicios)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_s_iva10s'].update({
            'name': "IVA 10% (Servicios)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_s_req014'].update({
            'name': "1.4% Recargo Equivalencia Ventas",
            'l10n_es_type': 'recargo',
        })
        taxes['account_tax_template_s_req52'].update({
            'name': "5.2% Recargo Equivalencia Ventas",
            'l10n_es_type': 'recargo',
        })
        taxes['account_tax_template_p_iva0_bc'].update({
            'name': "IVA Soportado exento (operaciones corrientes)",
            'l10n_es_type': 'sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_iva0_ns'].update({
            'name': "IVA Soportado no sujeto (Servicios)",
            'l10n_es_type': 'no_sujeto',
            'tax_scope': 'service',
        })
        taxes['account_tax_template_p_iva0_ns_b'].update({
            'name': "IVA Soportado no sujeto (Bienes)",
            'l10n_es_type': 'no_sujeto',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_irpf9'].update({
            'name': "Retenciones a cuenta IRPF 9%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf18'].update({
            'name': "Retenciones a cuenta IRPF 18%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf19'].update({
            'name': "Retenciones a cuenta IRPF 19%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf19a'].update({
            'name': "Retenciones a cuenta 19% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf195a'].update({
            'name': "Retenciones a cuenta 19,5% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf19'].update({
            'name': "Retenciones IRPF 19%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf20a'].update({
            'name': "Retenciones 20% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf18'].update({
            'name': "Retenciones IRPF 18%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf19a'].update({
            'name': "Retenciones 19% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf195a'].update({
            'name': "Retenciones 19,5% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf7'].update({
            'name': "Retenciones IRPF 7%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf9'].update({
            'name': "Retenciones IRPF 9%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf24'].update({
            'name': "Retenciones IRPF 14%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf20'].update({
            'name': "Retenciones a cuenta IRPF 20%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf20a'].update({
            'name': "Retenciones a cuenta 20% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf24'].update({
            'name': "Retenciones a cuenta IRPF 24%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_iva12_agr'].update({
            'name': "12% IVA Soportado régimen agricultura",
            'l10n_es_type': 'sujeto_agricultura',
        })
        taxes['account_tax_template_p_iva105_gan'].update({
            'name': "10,5% IVA Soportado régimen ganadero o pesca",
        })
        taxes['account_tax_template_s_iva0_e'].update({
            'name': "IVA 0% Exportaciones",
            'l10n_es_type': 'exento',
            # E2 for exportation
            'l10n_es_exempt_reason': 'E2',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_s_iva0_ic'].update({
            'name': "IVA 0% Entregas Intracomunitarias exentas",
            'l10n_es_type': 'exento',
            # E5  for intra-community
            'l10n_es_exempt_reason': 'E5',
            'tax_scope': 'consu',
        })
        taxes['account_tax_template_p_req014'].update({
            'name': "1.4% Recargo Equivalencia Compras",
            'l10n_es_type': 'recargo',
        })
        taxes['account_tax_template_p_req05'].update({
            'name': "0.50% Recargo Equivalencia Compras",
            'l10n_es_type': 'recargo',
        })
        taxes['account_tax_template_p_req52'].update({
            'name': "5.2% Recargo Equivalencia Compras",
            'l10n_es_type': 'recargo',
        })
        taxes['account_tax_template_s_irpf1'].update({
            'name': "Retenciones a cuenta IRPF 1%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf2'].update({
            'name': "Retenciones a cuenta IRPF 2%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf21'].update({
            'name': "Retenciones a cuenta IRPF 21%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf21a'].update({
            'name': "Retenciones a cuenta 21% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf7'].update({
            'name': "Retenciones a cuenta IRPF 7%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_irpf15'].update({
            'name': "Retenciones a cuenta IRPF 15%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf1'].update({
            'name': "Retenciones IRPF 1%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf15'].update({
            'name': "Retenciones IRPF 15%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf21t'].update({
            'name': "Retenciones IRPF (Trabajadores)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_iva10_sp_in'].update({
            'name': "IVA 10% Adquisición de servicios intracomunitarios",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_iva4_sp_in'].update({
            'name': "IVA 4% Adquisición de servicios intracomunitarios",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf21te'].update({
            'name': "Retenciones IRPF (Trabajadores) en especie",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf20'].update({
            'name': "Retenciones IRPF 20%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf21a'].update({
            'name': "Retenciones 21% (Arrendamientos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf21p'].update({
            'name': "Retenciones IRPF 21%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_irpf2'].update({
            'name': "Retenciones IRPF 2%",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_s_iva0_isp'].update({
            'name': "IVA 0% Venta con Inversión del Sujeto Pasivo",
            'l10n_es_type': 'sujeto_isp',
        })
        taxes['account_tax_template_p_iva4_isp'].update({
            'name': "IVA 4% Compra con Inversión del Sujeto Pasivo Nacional",
            'l10n_es_type': 'sujeto_isp',
        })
        taxes['account_tax_template_p_iva10_isp'].update({
            'name': "IVA 10% Compra con Inversión del Sujeto Pasivo Nacional",
            'l10n_es_type': 'sujeto_isp',
        })
        taxes['account_tax_template_p_iva21_isp'].update({
            'name': "IVA 21% Compra con Inversión del Sujeto Pasivo Nacional",
            'l10n_es_type': 'sujeto_isp',
        })
        taxes['account_tax_template_p_rp19'].update({
            'name': "Retenciones 19% (préstamos)",
            'l10n_es_type': 'retencion',
        })
        taxes['account_tax_template_p_rrD19'].update({
            'name': "Retenciones 19% (reparto de dividendos)",
            'l10n_es_type': 'retencion',
        })
        return taxes
