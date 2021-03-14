# -*- coding: utf-8 -*-
from odoo import models, fields, api


class covid_19(models.Model):
    _name = "covid.covid_19"

    name = fields.Char(string="Fuente", required=True)
    date = fields.Datetime(string="Fecha", required=True, dafault=fields.Datetime.now())
    country_id = fields.Many2one("res.country",string="País", required=True)
    infected = fields.Integer(string="Infectados", required=True, default=0)
    recovered = fields.Integer(string="Recuperados", required=True, default=0)
    deseaced = fields.Integer(string="Fallecidos", required=True, default=0)

    total_infected = fields.Integer(stirng="Total Infectados",
                                    compute="set_total_infected", required=True,default=0)

    total_recovered = fields.Integer(stirng="Total Recuperados",
                                     compute="set_total_recovered", required=True,default=0)

    total_deseaced = fields.Integer(stirng="Total Fallecidos",
                                    compute="set_total_deseaced", required=True,default=0)

    def set_total_infected(self):
        for data in self:
            # domain es como una clausula WHERE en sql
            # Busco los que tengan el mismo pais y una fecha inferior
            domain = [
                ('country_id', '=', data.country_id.id),
                ('date', '<', data.date)
            ]
            # Realizo la busqueda y los registros obtenidos los guardo
            records = self.search(domain)

            # Extraigo los atributos infected y los guardo en una lista
            infecteds = records.mapped('infected')

            # Sumo los infectados de los dias anteriores + el actual
            data.total_infected = sum(infecteds) + data.infected

    def set_total_recovered(self):
        for data in self:
            domain = [
                ('country_id', '=', data.country_id.id),
                ('date', '<', data.date)
            ]
            records = self.search(domain)
            recovereds = records.mapped('recovered')
            data.total_recovered = sum(recovereds) + data.recovered

    def set_total_deseaced(self):
        for data in self:
            domain = [
                ('country_id', '=', data.country_id.id),
                ('date', '<', data.date)
            ]
            records = self.search(domain)
            deseaceds = records.mapped('deseaced')
            data.total_deseaced = sum(deseaceds) + data.deseaced

    def set_porcentage_infected(self):
        total = 0
        if self.infected:
            total = (self.infected * 100) / self.total_infected
        return round(total, 2)

    def set_porcentage_recovered(self):
        total = 0
        if self.recovered:
            total = (self.recovered * 100) / self.recovered
        return round(total, 2)

    def set_porcentage_deseaced(self):
        total = 0
        if self.deseaced:
            total = (self.deseaced * 100) / self.total_deseaced
        return round(total, 2)