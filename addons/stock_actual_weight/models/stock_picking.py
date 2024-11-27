from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    weight_uom_id = fields.Many2one(
        'uom.uom',
        string='Weight UoM',
        default=lambda self: self.env.ref('uom.product_uom_kgm')
    )

    total_theoretical_weight = fields.Float(
        string='Total Theoretical Weight',
        compute='_compute_total_weights',
        store=True
    )

    total_actual_weight = fields.Float(
        string='Total Actual Weight',
        compute='_compute_total_weights',
        store=True
    )

    total_weight_difference = fields.Float(
        string='Total Weight Difference',
        compute='_compute_total_weights',
        store=True
    )

    total_weight_difference_percent = fields.Float(
        string='Total Weight Difference (%)',
        compute='_compute_total_weights',
        store=True
    )

    @api.depends('move_line_ids.theoretical_weight', 'move_line_ids.actual_weight')
    def _compute_total_weights(self):
        for picking in self:
            picking.total_theoretical_weight = sum(picking.move_line_ids.mapped('theoretical_weight'))
            picking.total_actual_weight = sum(picking.move_line_ids.mapped('actual_weight'))
            picking.total_weight_difference = picking.total_actual_weight - picking.total_theoretical_weight
            if picking.total_theoretical_weight:
                picking.total_weight_difference_percent = (
                    picking.total_weight_difference / picking.total_theoretical_weight) * 100
            else:
                picking.total_weight_difference_percent = 0.0