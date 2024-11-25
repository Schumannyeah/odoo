from odoo import models, api

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    @api.model
    def action_sold(self):
        # Override the action_sold method
        super_result = super(EstateProperty, self).action_sold()
        # Add print statement or debugger breakpoint to ensure it works
        print("action_sold method overridden in estate_account module")
        # Use pdb for a breakpoint (optional)
        # import pdb; pdb.set_trace()
        return super_result
