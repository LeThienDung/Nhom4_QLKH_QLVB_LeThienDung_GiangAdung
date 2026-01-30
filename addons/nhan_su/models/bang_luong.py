from odoo import models, fields, api


class BangLuong(models.Model):
    _name = 'nhan_su.bang_luong'
    _description = 'Bảng lương'

    nhan_vien_id = fields.Many2one(
        'nhan_su.nhan_vien',
        string='Nhân viên',
        required=True
    )

    thang = fields.Integer('Tháng', required=True)
    nam = fields.Integer('Năm', required=True)

    so_cong = fields.Float('Số công')
    luong_ngay = fields.Float('Lương ngày', compute='_compute_luong_ngay', store=True)
    phu_cap = fields.Float('Phụ cấp', default=0)
    thuong_phat = fields.Float('Thưởng / Phạt', default=0)
    tong_ot = fields.Float('Tổng giờ OT')

    tong_luong = fields.Float('Tổng lương', compute='_compute_tong_luong', store=True)

    @api.depends('nhan_vien_id.luong_co_ban')
    def _compute_luong_ngay(self):
        for r in self:
            r.luong_ngay = r.nhan_vien_id.luong_co_ban / 26 if r.nhan_vien_id else 0

    @api.depends('luong_ngay', 'so_cong', 'phu_cap', 'thuong_phat', 'tong_ot')
    def _compute_tong_luong(self):
        for r in self:
            r.tong_luong = (
                r.luong_ngay * r.so_cong
                + r.phu_cap
                + r.thuong_phat
                + r.tong_ot * (r.luong_ngay / 8)
            )
