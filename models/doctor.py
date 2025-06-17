from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'
    _rec_name = 'name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary(string="Image")

    name = fields.Char(string="Name", compute='_compute_name', store=True)

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.name = f"{rec.first_name} {rec.last_name}"
            else:
                rec.name = rec.first_name or rec.last_name or "Unknown"
