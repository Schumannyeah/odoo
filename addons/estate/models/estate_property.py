# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import timedelta


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
    living_area = fields.Float('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean(string='Has Garage', default=False, help="Whether there is a garage?")
    garden = fields.Boolean(string='Has Garden', default=True, help="Whether there is a garden?")
    garden_area = fields.Float('Garden Area')
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
    is_recent = fields.Boolean(compute='_compute_is_recent', search='_search_is_recent')
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    estate_property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many(
        string="Property Tags", comodel_name='estate.property.tag', relation='estate_property_tag_estate_property_rel'
    )
    offer_price_ids = fields.One2many('estate.property.offer', 'property_id', 'Offer Price', depends_context=('company',))
    # offer_status_ids = fields.One2many('estate.property.offer', 'property_id', 'Offer Status', depends_context=('company',))
    # offer_partner_ids = fields.One2many('estate.property.offer', 'property_id', 'Offer Supplier', depends_context=('company',))
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float('Best Offer Price', compute='_compute_best_price', store=True)

    def _compute_is_recent(self):
        for record in self:
            record.is_recent = fields.Datetime.from_string(record.create_date) >= fields.Datetime.now() - timedelta(hours=2)

    def _search_is_recent(self, operator, value):
        if operator == '=' and value:
            return [('create_date', '>=', fields.Datetime.now() - timedelta(hours=7))]
        return []

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_price_ids.price')
    def _compute_best_price(self):
        for record in self:
            # If there are offers related to the property, get the highest price
            if record.offer_price_ids:
                best_offer = max(record.offer_price_ids, key=lambda offer: offer.price)
                record.best_price = best_offer.price
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = False

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

