# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DateReportWizard(models.TransientModel):
    _name = "covid_19.date.report.wizard"
    _description = "Reporte por fecha y país"

    start_date = fields.Date('Día inicial', required=True)
    end_date= fields.Date('Día final', required=True)
    country_ids = fields.Many2many(
        'res.country',
        string='Paises',
        help='Paises con los que quiera generar el reporte'
    )


    def print_report(self):
        # Instanciamos el obj donde buscaremos los datos
        Covid19 = self.env['covid.covid_19']

        domain = [
             ('date', '>', self.start_date),
             ('date', '<', self.end_date)
        ]
        if self.country_ids:
            # Si el usuario coloco el país entonces lo agrego al domain para la busqueda
            domain.append(('country_id', 'in', self.country_ids.ids))

        covidField = [
            'name',
            'date',
            'country_id',
            'infected',
            'recovered',
            'deseaced'
        ]
        # Busco los registros que coincidan con el domain y solo las campos declarados en covidField
        covidRecords = Covid19.search_read(domain, covidField)

        print("Fecha inicial: ", self.start_date)
        print("Fecha final: ", self.end_date)
        print("Pais: ", self.country_ids)

        print("Datos encontrados")
        print(covidRecords)

        datas = {
            'covidRecords': covidRecords,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        # return self.env.ref('covid_19.datesReportExternalayout').report_action(self, data=datas, config=False)
        return {
            'type': 'ir.actions.report',
            'report_name': 'covid_19.datesReportExternalayout',
            'report_type':"qweb-pdf",
            'data': datas
        }
