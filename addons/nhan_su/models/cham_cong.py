# File: nhan_su/models/cham_cong.py
from odoo import models, fields, api
from datetime import timedelta

class ChamCong(models.Model):
    _name = 'nhan.su.cham.cong'
    _description = 'Quản lý chấm công'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True)
    ngay = fields.Date(string='Ngày chấm công', default=fields.Date.today)
    
    # Giờ vào/ra (Sử dụng Float cho đơn giản: ví dụ 8.5 là 8h30, 17.0 là 17h00)
    gio_vao = fields.Float(string='Giờ vào', default=8.0) 
    gio_ra = fields.Float(string='Giờ ra', default=17.0)
    
    # Các trường tính toán
    so_gio_lam = fields.Float(string='Số giờ làm', compute='_tinh_cong', store=True)
    tien_phat = fields.Float(string='Tiền phạt', compute='_tinh_cong', store=True)
    tien_ot = fields.Float(string='Tiền OT', compute='_tinh_cong', store=True)
    ghi_chu = fields.Text(string='Ghi chú')

    _sql_constraints = [
        ('cham_cong_uniq', 'unique(nhan_vien_id, ngay)', 'Lỗi: Nhân viên này đã được chấm công ngày hôm nay rồi!')
    ]

    @api.depends('gio_vao', 'gio_ra')
    def _tinh_cong(self):
        for rec in self:
            # 1. Tính tổng giờ làm
            if rec.gio_ra > rec.gio_vao:
                rec.so_gio_lam = rec.gio_ra - rec.gio_vao
            else:
                rec.so_gio_lam = 0.0

            # 2. Xử lý Logic Phạt (Nếu làm dưới 8 tiếng)
            # Giả sử quy định phạt 50k/giờ thiếu
            if rec.so_gio_lam < 8.0:
                so_gio_thieu = 8.0 - rec.so_gio_lam
                rec.tien_phat = so_gio_thieu * 50000 
            else:
                rec.tien_phat = 0.0

            # 3. Xử lý Logic OT (Nếu làm > 8 tiếng + 0.5 tiếng nghỉ = 8.5)
            # Giả sử tăng ca tính 100k/giờ
            if rec.so_gio_lam >= 8.5: 
                so_gio_ot = rec.so_gio_lam - 8.0 # Trừ 8 tiếng hành chính
                rec.tien_ot = so_gio_ot * 100000
            else:
                rec.tien_ot = 0.0

    @api.depends('ngay', 'gio_vao', 'gio_ra')
    def _tinh_cong(self):
        for rec in self:
            # Logic cũ tính giờ làm
            if rec.gio_ra > rec.gio_vao:
                rec.so_gio_lam = rec.gio_ra - rec.gio_vao
            else:
                rec.so_gio_lam = 0.0

            # --- LOGIC MỚI: XỬ LÝ CHỦ NHẬT ---
            # weekday(): 0 là thứ 2, ..., 6 là Chủ nhật
            is_sunday = rec.ngay.weekday() == 6 

            if is_sunday:
                # Nếu là chủ nhật: Không làm thì không phạt, làm thì tính full OT
                rec.tien_phat = 0.0
                rec.tien_ot = rec.so_gio_lam * 100000 * 2 # Nhân đôi đơn giá OT
            else:
                # Nếu là ngày thường: Chạy logic cũ (Phạt nếu thiếu, OT nếu thừa)
                if rec.so_gio_lam < 8.0:
                    rec.tien_phat = (8.0 - rec.so_gio_lam) * 50000
                    rec.tien_ot = 0
                elif rec.so_gio_lam >= 8.5:
                    rec.tien_ot = (rec.so_gio_lam - 8.0) * 100000
                    rec.tien_phat = 0
                else:
                    rec.tien_phat = 0
                    rec.tien_ot = 0