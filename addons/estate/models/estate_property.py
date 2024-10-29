# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text(
        'Description', translate=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Datetime('Availability Date')
    expected_price = fields.Float('Expected Price', required=True, digits=(16, 2))
    selling_price = fields.Float('Selling Price', digits=(16, 2))
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean(string='Has Garage', default=False, help="Whether there is a garage?")
    garden = fields.Boolean(string='Has Garden', default=True, help="Whether there is a garden?")
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('east', "East"),
            ('south', "South"),
            ('west', "West"),
            ('north', "North"),
        ],
        default='South',
    )