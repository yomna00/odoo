from datetime import date
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'display_name'
    _inherit = ['mail.thread']

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date(string="Birth Date")
    age = fields.Integer(compute='_compute_age', store=True)
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

    email = fields.Char(string='Email', required=True)

    user_id = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True
    )

    display_name = fields.Char(compute='_compute_display_name', store=True)

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email address must be unique.')
    ]

    @api.depends('first_name', 'last_name', 'user_id')
    def _compute_display_name(self):
        for rec in self:
            user = rec.user_id.name if rec.user_id else 'Unknown'
            rec.display_name = f"{rec.first_name} {rec.last_name} ({user})"

    @api.constrains('email')
    def _check_email_validity(self):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for rec in self:
            if rec.email and not re.match(pattern, rec.email):
                raise ValidationError("Invalid email format.")

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

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0
