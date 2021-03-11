# -*- coding: utf-8 -*-
from odoo import models, fields, api


class covid_19(models.Model):
    _name = "covid.covid_19"

    name = fields.Char(string="Fuente", required=True)
    date = fields.Datetime(string="Fecha", required=True, dafault=fields.Datetime.now())
    countre_id = fields.Many2one("res.country", required=True)
    infected = fields.Integer(string="Infectados", required=True, default=0)
    recovered = fields.Integer(string="Recuperados", required=True, default=0)
    deseaced = fields.Integer(string="Fallecidos", required=True, default=0)

