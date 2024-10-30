# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Name', required=True, translate=True, default="Unknown")
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Datetime('Availability Date',
                                        default=lambda self: fields.Datetime.to_string(
                                            datetime.now() + relativedelta(months=3)))
    expected_price = fields.Float('Expected Price', required=True, digits=(16, 2))
    selling_price = fields.Float('Selling Price', digits=(16, 2), readonly=True)
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
        default='south',
    )
    state = fields.Selection(
        string="Status",
        required=True,
        selection=[
            ('new', "New"),
            ('received', "Received"),
            ('accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
    )
    active = fields.Boolean('Active', default=True)

    # # Add this computed field
    # formatted_date = fields.Char('Availability Date', compute='_compute_formatted_date')
    #
    # # Computed field for formatted date
    # formatted_date_availability = fields.Char(string='Formatted Availability Date', compute='_compute_formatted_date')
    #
    # @api.depends('date_availability')
    # def _compute_formatted_date(self):
    #     for record in self:
    #         if record.date_availability:
    #             record.formatted_date_availability = record.date_availability.strftime('%Y-%m-%d')
    #         else:
    #             record.formatted_date_availability = ""

    @api.model_create_multi
    def create(self, vals_list):
        # Ensure vals_list is always a list
        if not isinstance(vals_list, list):
            vals_list = [vals_list]

        # Process each record's values
        for vals in vals_list:
            # Create a copy to avoid modifying the original
            vals = vals.copy()
            # Remove protected fields
            vals.pop('date_availability', None)
            vals.pop('selling_price', None)
            vals.pop('state', None)

        # Create the records using the super method
        return super().create(vals_list)

    def write(self, vals):
        # Prevent updating date_availability and selling_price
        vals = vals.copy()
        vals.pop('date_availability', None)
        vals.pop('selling_price', None)
        vals.pop('state', None)
        return super().write(vals)

