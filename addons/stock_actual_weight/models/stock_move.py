from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    theoretical_weight = fields.Float(
        string='Theoretical Weight',
        compute='_compute_theoretical_weight',
        store=True,
        help='Weight based on product settings'
    )
    actual_weight = fields.Float(
        string='Actual Weight',
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

    @api.depends('product_id', 'product_uom_qty', 'product_id.weight')
    def _compute_theoretical_weight(self):
        weight_uom = self.env.ref('uom.product_uom_kgm')
        for move in self:
            if move.product_id and move.product_uom_qty:
                weight = move.product_id.weight
                if move.weight_uom_id and move.weight_uom_id != weight_uom:
                    weight = weight_uom._compute_quantity(
                        weight,
                        move.weight_uom_id
                    )
                move.theoretical_weight = weight * move.product_uom_qty
            else:
                move.theoretical_weight = 0.0

    @api.depends('theoretical_weight', 'actual_weight')
    def _compute_weight_difference(self):
        for move in self:
            move.weight_difference = move.actual_weight - move.theoretical_weight
            if move.theoretical_weight:
                move.weight_difference_percent = (move.weight_difference / move.theoretical_weight) * 100
            else:
                move.weight_difference_percent = 0.0