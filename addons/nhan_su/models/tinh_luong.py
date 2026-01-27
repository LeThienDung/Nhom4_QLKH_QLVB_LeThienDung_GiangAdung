# File: nhan_su/models/tinh_luong.py
from odoo import models, fields, api

class KyLuong(models.Model):
    _name = 'nhan.su.ky.luong'
    _description = 'Kỳ lương tháng'
    _rec_name = 'name'

    name = fields.Char(string='Tên kỳ lương', compute='_compute_name', store=True)
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'), ('4', 'Tháng 4'),
        ('5', 'Tháng 5'), ('6', 'Tháng 6'), ('7', 'Tháng 7'), ('8', 'Tháng 8'),
        ('9', 'Tháng 9'), ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12')
    ], string='Tháng', required=True, default='1')
    nam = fields.Integer(string='Năm', default=2026, required=True)
    
    chi_tiet_ids = fields.One2many('nhan.su.bang.luong', 'ky_luong_id', string='Danh sách lương')
    tong_tien_phai_tra = fields.Float(string='Tổng quỹ lương', compute='_compute_tong_tien')

    @api.depends('thang', 'nam')
    def _compute_name(self):
        for rec in self:
            rec.name = f"Lương tháng {rec.thang}/{rec.nam}"

    @api.depends('chi_tiet_ids.tong_luong')
    def _compute_tong_tien(self):
        for rec in self:
            rec.tong_tien_phai_tra = sum(line.tong_luong for line in rec.chi_tiet_ids)

    def tinh_luong_tat_ca(self):
        for rec in self:
            rec.chi_tiet_ids.unlink()
            tat_ca_nhan_vien = self.env['nhan_vien'].search([])
            for nv in tat_ca_nhan_vien:
                self.env['nhan.su.bang.luong'].create({
                    'ky_luong_id': rec.id,
                    'nhan_vien_id': nv.id,
                })
    
    state = fields.Selection([
    ('draft', 'Dự thảo'),
    ('confirm', 'Đã chốt'),
    ('done', 'Đã thanh toán')
    ], string='Trạng thái', default='draft')

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'  

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Bạn không thể xóa bảng lương đã chốt!")
        return super(KyLuong, self).unlink()  

class BangLuong(models.Model):
    _name = 'nhan.su.bang.luong'
    _description = 'Chi tiết lương nhân viên'

    ky_luong_id = fields.Many2one('nhan.su.ky.luong', string='Kỳ lương', ondelete='cascade')
    thang = fields.Selection(related='ky_luong_id.thang', store=True)
    nam = fields.Integer(related='ky_luong_id.nam', store=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True)
    
    so_cong_thuc_te = fields.Float(string='Số công', compute='_lay_du_lieu_cham_cong', store=True)
    tong_tien_phat = fields.Float(string='Tiền phạt', compute='_lay_du_lieu_cham_cong', store=True)
    tong_tien_ot = fields.Float(string='Tiền OT', compute='_lay_du_lieu_cham_cong', store=True)
    phu_cap = fields.Float(string='Phụ cấp')
    tong_luong = fields.Float(string='Thực lĩnh', compute='_tinh_luong_thang', store=True)

    # --- ĐẶT SQL CONSTRAINT Ở ĐÂY MỚI ĐÚNG ---
    _sql_constraints = [
        ('bang_luong_uniq', 'unique(nhan_vien_id, ky_luong_id)', 'Lỗi: Nhân viên này đã có tên trong kỳ lương này rồi!')
    ]
    # -----------------------------------------

    @api.depends('nhan_vien_id', 'ky_luong_id')
    def _lay_du_lieu_cham_cong(self):
        for rec in self:
            if not rec.nhan_vien_id or not rec.ky_luong_id:
                rec.so_cong_thuc_te = 0; rec.tong_tien_phat = 0; rec.tong_tien_ot = 0
                continue
            ds_cham_cong = self.env['nhan.su.cham.cong'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id)
            ])
            tong_gio = 0; tong_phat = 0; tong_ot = 0
            for cc in ds_cham_cong:
                if str(cc.ngay.month) == str(rec.thang) and cc.ngay.year == rec.nam:
                    tong_gio += cc.so_gio_lam
                    tong_phat += cc.tien_phat
                    tong_ot += cc.tien_ot
            rec.so_cong_thuc_te = tong_gio / 8
            rec.tong_tien_phat = tong_phat
            rec.tong_tien_ot = tong_ot

    @api.depends('so_cong_thuc_te', 'phu_cap', 'tong_tien_ot', 'tong_tien_phat')
    def _tinh_luong_thang(self):
        for rec in self:
            if rec.nhan_vien_id:
                luong_ngay = rec.nhan_vien_id.luong_co_ban / 26
                rec.tong_luong = (luong_ngay * rec.so_cong_thuc_te) + rec.phu_cap + rec.tong_tien_ot - rec.tong_tien_phat
            else:
                rec.tong_luong = 0