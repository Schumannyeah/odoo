from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    theoretical_weight = fields.Float(
        string='Theoretical Weight',
        compute='_compute_theoretical_weight',
        store=True,
        help='Weight based on product settings'
    )
    actual_weight = fields.Float(
        string='Actual Weight',
        store=True,
        help='Actual measured weight during operation'
    )
    weight_difference = fields.Float(
        string='Weight Difference',
        compute='_compute_weight_difference',
        store=True,
        help='Difference between actual and theoretical weight'
    )
    weight_difference_percent = fields.Float(
        string='Weight Difference (%)',
        compute='_compute_weight_difference',
        store=True,
        help='Percentage difference between actual and theoretical weight'
    )
    weight_uom_id = fields.Many2one(
        'uom.uom',
        string='Weight UoM',
        related='picking_id.weight_uom_id',
        store=True
    )

    @api.depends('product_id', 'quantity', 'product_id.weight')
    def _compute_theoretical_weight(self):
        weight_uom = self.env.ref('uom.product_uom_kgm')
        for line in self:
            if line.product_id and line.quantity:
                # Get the product weight in the default unit (usually kg)
                weight = line.product_id.weight

                # If we need to convert to a different UoM
                if line.weight_uom_id and line.weight_uom_id != weight_uom:
                    weight = weight_uom._compute_quantity(
                        weight,
                        line.weight_uom_id
                    )
                line.theoretical_weight = weight * line.quantity
            else:
                line.theoretical_weight = 0.0

    @api.depends('theoretical_weight', 'actual_weight')
    def _compute_weight_difference(self):
        for line in self:
            line.weight_difference = line.actual_weight - line.theoretical_weight
            if line.theoretical_weight:
                line.weight_difference_percent = (line.weight_difference / line.theoretical_weight) * 100
            else:
                line.weight_difference_percent = 0.0