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

    # for inline views
    property_ids = fields.One2many("estate_property_type_line", "property_id")

class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Estate Property Type Line"
    _order = "id"

    property_id = fields.Many2one("estate.property.type", string="Property Id", required=True, ondelete='cascade')
    name = fields.Char("Name", required=True, translate=True)
    expected_price = fields.Float('Expected Price', required=True, digits=(16, 2))
    state = fields.Char()