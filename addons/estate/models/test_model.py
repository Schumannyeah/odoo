from odoo import fields, models

class TestModel(models.Model):
    # Schumann
    # _name is crucial for ORM to create the database table instead of class
    _name = "test.model"
    _description = "Test Model"

    name = fields.Char()
