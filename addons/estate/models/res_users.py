from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # One2many field referencing estate.property
    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",  # Inverse field in estate.property
        string="Assigned Properties",
        # domain="[('state', 'not in', ['cancelled'])]"
    )
