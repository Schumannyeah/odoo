# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    name = fields.Char('Name', required=True, translate=True, default="Unknown")
    price = fields.Float('Price', digits=(16, 2))
    status = fields.Selection(
        string="Offer Status",
        selection=[
            ('accepted', "Accepted"),
            ('south', "Refused"),
            ('drafted', "Drafted")
        ],
        default='drafted',
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Supplier")
    property_id = fields.Many2one("estate.property", required=True, string="Estate Property")