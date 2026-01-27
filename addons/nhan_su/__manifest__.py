# -*- coding: utf-8 -*-
{
    'name': "nhan_su",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # BƯỚC 1: Load các file chứa Action và View cơ bản trước
        # (Để action_nhan_vien được tạo ra trước)
        'views/nhan_vien.xml',
        'views/quan_ly_van_ban_views.xml',

        # BƯỚC 2: Load file Menu (Lúc này action đã có, nên menu link vào không bị lỗi)
        # (File này sẽ tạo ra menu_root)
        'views/menu.xml',  
        
        # BƯỚC 3: Load các file Menu con hoặc View phụ thuộc vào Menu Cha
        # (File này dùng menu_root nên phải để sau menu.xml)
        'views/cham_cong_view.xml', 

        'views/tinh_luong_view.xml',
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
