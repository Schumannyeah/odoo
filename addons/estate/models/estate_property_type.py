# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char('Name', required=True, translate=True, default="Unknown")
    sequence = fields.Integer('Sequence', default=1)

    _sql_constraints = [
        ('type_name_uniq', 'unique (name)', """Only one value can be defined for each given type name!"""),
    ]

    # Dynamically fetch related estate properties
    property_ids = fields.One2many(
        "estate.property",
        "estate_property_type_id",
        string="Properties",
        readonly=True
    )

    # Add the field offer_ids to estate.property.type
    # which is the One2many inverse of the field defined in the previous step.
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
        readonly=True
    )

    # Computed field to count the number of offers
    offer_count = fields.Integer(
        string="Offers Count",
        compute="_compute_offer_count",
        store=True
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_all_offers_by_property_type(self):
        """Return an action that displays all offers related to this property type."""
        self.ensure_one()  # Ensure the action is triggered for a single record
        # Get the ID of the custom list view (defined in XML)
        list_view_id = self.env.ref('estate.view_estate_property_offer_list').id
        return {
            'name': 'Offers by Property Type',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list',
            'views': [(list_view_id, 'list')],  # Specify the list view
            'domain': [('id', 'in', self.offer_ids.ids)],  # Filter offers by related IDs
            'context': {
                'default_property_type_id': self.id,  # Pass current property type in context
            },
        }