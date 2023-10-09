from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalAccount(models.Model):
    _name = 'hospital.account'
    _description = 'Hospital Account'

    name = fields.Char(string='Username', required=True, unique=True)
    password = fields.Char(string='Password', required=True)
    role = fields.Selection([
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin')
    ], string='Role', compute='_compute_role', store=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    admin_id = fields.Many2one('hospital.admin', string='Admin')

    @api.depends('patient_id', 'doctor_id', 'admin_id')
    def _compute_role(self):
        for record in self:
            if record.patient_id:
                record.role = 'patient'
            elif record.doctor_id:
                record.role = 'doctor'
            elif record.admin_id:
                record.role = 'admin'

    @api.constrains('patient_id', 'doctor_id', 'admin_id')
    def _check_role_assignment(self):
        for record in self:
            if not (record.patient_id or record.doctor_id or record.admin_id):
                raise ValidationError('An account must be linked to a patient, doctor, or admin.')

    @api.model
    def create(self, vals):
        # Kiểm tra nếu không có tài khoản nào được liên kết thì không cho tạo
        if not (vals.get('patient_id') or vals.get('doctor_id') or vals.get('admin_id')):
            raise ValidationError('An account must be linked to a patient, doctor, or admin.')
        # Kiểm tra name không được trùng lặp
        if 'name' in vals:
            existing_account = self.search([('name', '=', vals['name'])])
            if existing_account:
                raise ValidationError('Username must be unique.')
        return super(HospitalAccount, self).create(vals)

    @api.constrains('name')
    def check_name(self):
        for record in self:
            if record.name:
                existing_account = self.search([('name', '=', record.name), ('id', '!=', record.id)])
                if existing_account:
                    raise ValidationError('Username must be unique.')