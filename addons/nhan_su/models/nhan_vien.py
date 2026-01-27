from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class NhanVien(models.Model):
    _name = 'nhan_vien'  # Giữ nguyên tên model cũ của bạn
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten' # <--- Thêm: Để khi chọn nhân viên ở bảng chấm công nó hiện Tên chứ không hiện ID

    # Các trường cũ của bạn (Giữ nguyên)
    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")

    # Các trường CẦN THÊM để tính lương và hiển thị (Thêm mới)
    ho_ten = fields.Char(string="Họ và tên", required=True) 
    luong_co_ban = fields.Float(string="Lương cơ bản", default=5000000)

    _sql_constraints = [
        # Cấu trúc: ('tên_ràng_buộc', 'unique(tên_cột)', 'Thông báo lỗi')
        ('ma_dinh_danh_uniq', 'unique(ma_dinh_danh)', 'Lỗi: Mã định danh này đã tồn tại! Vui lòng kiểm tra lại.'),
        ('ho_ten_uniq', 'unique(ho_ten)', 'Cảnh báo: Tên nhân viên này đã có trong hệ thống!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', rec.email)
                if match == None:
                    raise ValidationError('Email không đúng định dạng! (Ví dụ đúng: ten@gmail.com)')

    @api.constrains('so_dien_thoai')
    def _check_sdt(self):
        for rec in self:
            if rec.so_dien_thoai and not rec.so_dien_thoai.isdigit():
                raise ValidationError('Số điện thoại chỉ được chứa các chữ số!')