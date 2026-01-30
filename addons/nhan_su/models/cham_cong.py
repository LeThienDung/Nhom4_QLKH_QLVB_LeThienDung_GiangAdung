from odoo import models, fields, api
from datetime import datetime


class ChamCong(models.Model):
    _name = 'nhan_su.cham_cong'
    _description = 'Chấm công nhân viên'

    nhan_vien_id = fields.Many2one(
        'nhan_su.nhan_vien',
        string='Nhân viên',
        required=True
    )

    ngay = fields.Date(
        string='Ngày',
        required=True,
        default=fields.Date.today
    )

    gio_vao = fields.Datetime('Giờ vào')
    gio_ra = fields.Datetime('Giờ ra')

    so_gio_lam = fields.Float(
        'Số giờ làm',
        compute='_compute_so_gio_lam',
        store=True
    )

    di_muon = fields.Boolean('Đi muộn', compute='_compute_di_muon', store=True)
    ve_som = fields.Boolean('Về sớm', compute='_compute_ve_som', store=True)
    ot = fields.Float('Giờ OT', compute='_compute_ot', store=True)

    @api.depends('gio_vao', 'gio_ra')
    def _compute_so_gio_lam(self):
        for r in self:
            if r.gio_vao and r.gio_ra:
                delta = r.gio_ra - r.gio_vao
                r.so_gio_lam = delta.total_seconds() / 3600
            else:
                r.so_gio_lam = 0

    @api.depends('gio_vao')
    def _compute_di_muon(self):
        for r in self:
            if r.gio_vao:
                r.di_muon = r.gio_vao.hour >= 9
            else:
                r.di_muon = False

    @api.depends('gio_ra')
    def _compute_ve_som(self):
        for r in self:
            if r.gio_ra:
                r.ve_som = r.gio_ra.hour < 17
            else:
                r.ve_som = False

    @api.depends('so_gio_lam')
    def _compute_ot(self):
        for r in self:
            r.ot = max(0, r.so_gio_lam - 8)
