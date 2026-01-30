from odoo import models, fields


class DanhSachChungChiBangCap(models.Model):
    _name = 'nhan_su.danh_sach_chung_chi_bang_cap'
    _description = 'Bảng danh sách chứng chỉ bằng cấp'

    chung_chi_bang_cap_id = fields.Many2one(
        'nhan_su.chung_chi_bang_cap',
        string='Chứng chỉ bằng cấp',
        required=True
    )

    nhan_vien_id = fields.Many2one(
        'nhan_su.nhan_vien',
        string='Nhân viên',
        required=True,
        ondelete='cascade'
    )

    ghi_chu = fields.Char('Ghi chú')

    ma_dinh_danh = fields.Char(
        string='Mã định danh',
        related='nhan_vien_id.ma_dinh_danh',
        store=True,
        readonly=True
    )

    tuoi = fields.Integer(
        string='Tuổi',
        related='nhan_vien_id.tuoi',
        store=True,
        readonly=True
    )
