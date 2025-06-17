from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient' 

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date(string="Birth Date")
    age = fields.Integer()
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    blood_type = fields.Selection([('a', 'A'), ('b', 'B'), ('ab', 'AB'), ('o', 'O')], string="Blood Type")
    address = fields.Text()
    image = fields.Image()
    
    department_id = fields.Many2one('hms.department', string='Department')
    capacity = fields.Integer(related='department_id.capacity', readonly=True, store=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')
    pcr = fields.Boolean()
    cr_ratio = fields.Float(string='CR Ratio')
    history = fields.Html()

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined', string='State')

    @api.constrains('department_id')
    def _check_department_open(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("Cannot assign a patient to a closed department.")

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_if_pcr(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required if PCR is checked.")

    @api.onchange('department_id')
    def _onchange_department(self):
        if not self.department_id:
            self.doctor_ids = False
