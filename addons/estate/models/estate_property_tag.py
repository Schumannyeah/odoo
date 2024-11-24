# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char('Name', required=True, translate=True, default="Unknown")
    color = fields.Integer('Color')

    _sql_constraints = [
        ('tag_name_uniq', 'unique (name)', """Only one value can be defined for each given tage name!"""),
    ]
