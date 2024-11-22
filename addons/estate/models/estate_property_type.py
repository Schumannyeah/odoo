# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char('Name', required=True, translate=True, default="Unknown")

    _sql_constraints = [
        ('type_name_uniq', 'unique (name)', """Only one value can be defined for each given type name!"""),
    ]
