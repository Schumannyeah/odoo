from odoo import models, fields, api
from datetime import datetime


class ManufacturingOrderGantt(models.Model):
    _inherit = 'mrp.production'

    # Add additional fields for Gantt view
    progress_percentage = fields.Float(
        string='Progress',
        compute='_compute_progress_percentage',
        store=True,
        help='Progress percentage of the manufacturing order'
    )

    planned_start_date = fields.Datetime(
        string='Planned Start Date',
        required=True,
        default=fields.Datetime.now,
        help='Planned start date for the manufacturing order'
    )

    planned_end_date = fields.Datetime(
        string='Planned End Date',
        required=True,
        compute='_compute_planned_end_date',
        store=True,
        help='Planned end date for the manufacturing order'
    )

    @api.depends('workorder_ids.state', 'workorder_ids.duration_expected', 'workorder_ids.duration')
    def _compute_progress_percentage(self):
        for order in self:
            if not order.workorder_ids:
                order.progress_percentage = 0.0
                continue

            total_duration = sum(wo.duration_expected for wo in order.workorder_ids)
            completed_duration = sum(wo.duration for wo in order.workorder_ids if wo.state == 'done')

            if total_duration:
                order.progress_percentage = (completed_duration / total_duration) * 100
            else:
                order.progress_percentage = 0.0

    @api.depends('planned_start_date', 'workorder_ids.duration_expected')
    def _compute_planned_end_date(self):
        for order in self:
            if order.planned_start_date:
                total_duration = sum(wo.duration_expected for wo in order.workorder_ids)
                # Convert duration from seconds to days and add to start date
                duration_days = total_duration / (24 * 60 * 60)
                order.planned_end_date = fields.Datetime.add(
                    order.planned_start_date,
                    days=int(duration_days),
                    seconds=int((duration_days % 1) * 24 * 60 * 60)
                )
            else:
                order.planned_end_date = False


# Views definition
class ManufacturingOrderGanttView(models.Model):
    _inherit = 'mrp.production'

    def init(self):
        # Ensure proper indexing for better performance
        self._cr.execute("""
            CREATE INDEX IF NOT EXISTS mrp_production_date_index 
            ON mrp_production (planned_start_date, planned_end_date)
        """)