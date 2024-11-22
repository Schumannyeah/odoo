# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import timedelta, datetime
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    name = fields.Char('Name', required=True, translate=True, default="Unknown")
    price = fields.Float('Price', digits=(16, 2))

    _sql_constraints = [
        ('check_offer_price_positve', 'CHECK(price > 0)',
         'The offer price must be strictly positive!')
    ]

    status = fields.Selection(
        string="Offer Status",
        selection=[
            ('drafted', "Drafted"),
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        default='drafted',
        required=True,
        index=True
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

    # Schumann important to set the constrains not only to price but also status & property_id
    # because when triggering the action_confirm it updates first the status and then the property_id
    # we need to trigger the constrain working when it does so.
    # only setting constrain to price doesn't work
    @api.constrains('price', 'status', 'property_id')
    def _check_accepted_price(self):
        for record in self:
            # If the offer is being accepted, check if its price is at least 90% of the expected price
            if record.status == 'accepted' and record.property_id:
                expected_price = record.property_id.expected_price
                # Use float_compare to safely compare the prices
                if float_compare(record.price, expected_price * 0.9, precision_digits=2) < 0:
                    raise UserError("The selling price cannot be lower than 90% of the expected price.")

    def action_confirm(self):
        # Ensure the method is being called on a single record
        self.ensure_one()

        # First check if there's already an accepted offer for this property
        existing_accepted = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
            ('id', '!=', self.id)  # Exclude current offer
        ])

        if existing_accepted:
            raise UserError("There is already an accepted offer! Multiple acceptance is not allowed!")

        # Only then check the current offer's status
        if self.status == 'refused':
            raise UserError("If you want to confirm the refused offer, please reverse it to drafted first!")

        self.write({'status': 'accepted'})

        # Update the related estate property with the current offer's price and partner
        if self.property_id:
            self.property_id.write({
                'selling_price': self.price,
                'buyer_id': self.partner_id.id
            })

        return True

    def action_cancel(self):
        for record in self:
            record.status = 'refused'

        # Check if there is still an accepted offer for the same property
        accepted_offer_exists = self.env['estate.property.offer'].search_count([
            ('property_id', '=', record.property_id.id),
            ('status', '=', 'accepted')
        ])

        # If no accepted offer exists, reset the selling_price and buyer_id of the property
        if not accepted_offer_exists and record.property_id:
            record.property_id.write({
                'selling_price': None,
                'buyer_id': None
            })

        return True


    @api.constrains('status', 'property_id')
    def _check_single_accepted_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                accepted_offers = self.env['estate.property.offer'].search([
                    ('property_id', '=', offer.property_id.id),
                    ('status', '=', 'accepted'),
                    ('id', '!=', offer.id)
                ])
                if accepted_offers:
                    raise ValidationError("Only one offer can be accepted per property!")
