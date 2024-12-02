from odoo import models, api, fields, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_estate_property_sold(self):
        # Override the action_sold method
        super_result = super(EstateProperty, self).action_set_estate_property_sold()

        # Create an empty account.move
        AccountMove = self.env['account.move']
        for record in self:
            if not record.buyer_id:
                raise UserError('No buyer is defined for this property.')

            move_values = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice', # Corresponds to 'Customer Invoice'
                'invoice_date': fields.Date.today(),
                'name': f"Invoice for {record.name}",
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Commission - 6% of Selling Price',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ]
            }
            invoice = AccountMove.create(move_values)

            # Add print statement to verify invoice creation
            print(f"Created invoice {invoice.id} for property {record.name}")

        return super_result
