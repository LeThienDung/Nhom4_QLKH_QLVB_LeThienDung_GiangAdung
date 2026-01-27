# File: nhan_su/models/quan_ly_van_ban.py

from odoo import models, fields, api

# --- Model 1: Loại Văn Bản ---
class LoaiVanBan(models.Model):
    _name = 'quan_ly_van_ban.loai'
    _description = 'Danh mục loại văn bản'
    
    name = fields.Char("Tên loại văn bản", required=True)
    ma_loai = fields.Char("Mã loại", help="Ví dụ: HC, CV, ND, TB")
    mo_ta = fields.Text("Mô tả")

# --- Model 2: Văn Bản Đến ---
class VanBanDen(models.Model):
    _name = 'quan_ly_van_ban.den'
    _description = 'Quản lý văn bản đến'
    _rec_name = 'so_ky_hieu'

    so_ky_hieu = fields.Char("Số ký hiệu", required=True)
    tieu_de = fields.Char("Trích yếu/Tiêu đề", required=True)
    ngay_den = fields.Date("Ngày đến", default=fields.Date.today)
    noi_gui = fields.Char("Nơi gửi")
    
    # Quan hệ với model Loại văn bản
    loai_van_ban_id = fields.Many2one('quan_ly_van_ban.loai', string="Loại văn bản")
    
    # Quan hệ với model Nhân viên (liên kết với file nhan_vien.py)
    nguoi_tiep_nhan_id = fields.Many2one('nhan_vien', string="Người tiếp nhận")
    
    noi_dung = fields.Text("Nội dung tóm tắt")
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('done', 'Đã xử lý')
    ], string="Trạng thái", default='draft')

# --- Model 3: Văn Bản Đi ---
class VanBanDi(models.Model):
    _name = 'quan_ly_van_ban.di'
    _description = 'Quản lý văn bản đi'
    _rec_name = 'so_ky_hieu'

    so_ky_hieu = fields.Char("Số ký hiệu", required=True)
    tieu_de = fields.Char("Trích yếu/Tiêu đề", required=True)
    ngay_ban_hanh = fields.Date("Ngày ban hành", default=fields.Date.today)
    noi_nhan = fields.Char("Nơi nhận")
    
    loai_van_ban_id = fields.Many2one('quan_ly_van_ban.loai', string="Loại văn bản")
    nguoi_soan_thao_id = fields.Many2one('nhan_vien', string="Người soạn thảo")
    
    file_dinh_kem = fields.Binary("File đính kèm")