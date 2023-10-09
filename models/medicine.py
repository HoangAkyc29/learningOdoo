from odoo import models, fields, api, _


class HospitalMedicine(models.Model):
    _name = 'hospital.medicine'
    _description = 'Hospital Medicine'
    _rec_name = 'medicine_name'

    medicine_name = fields.Char(string='Medicine Name', required=True)
    price = fields.Float(string='Price')
    stock = fields.Integer(string='Stock')
    description = fields.Text(string='Description')
    manufacturer_id = fields.Many2one('res.partner', string='Manufacturer')

    
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('medicine_name'):
            default['medicine_name'] = _("%s (Copy)", self.medicine_name)
        default['note'] = "Copied Record"
        return super(HospitalMedicine, self).copy(default)
    
    @api.onchange('stock')
    def _check_stock(self):
        if self.stock < 0:
            return {
                'warning': {
                    'title': 'Invalid Stock Value',
                    'message': 'Stock cannot be negative.',
                },
            }

    def unlink(self):
        for medicine in self:
            # Xóa tất cả prescription lines có chứa medicine này
            prescription_lines = self.env['appointment.prescription.lines'].search([('medicine_id', '=', medicine.id)])
            prescription_lines.unlink()
        return super(HospitalMedicine, self).unlink()
