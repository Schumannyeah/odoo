# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import timedelta, datetime


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
    validity = fields.Integer('Facades', default=7)
    date_deadline = fields.Datetime('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline',
                                    store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # If create_date exists, compute date_deadline by adding 'validity' days
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                # Fallback if create_date is not set (shouldn't happen normally)
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                # If date_deadline is set, calculate 'validity' from create_date and date_deadline
                if record.create_date:
                    delta = record.date_deadline - record.create_date
                    record.validity = delta.days
                else:
                    # Fallback if create_date is not set, you can log or handle error
                    record.validity = 7  # Set default validity or handle according to your needs
            else:
                # If date_deadline is not set, leave validity as is
                pass