# -*- coding: utf-8 -*-
from odoo import models, fields, api


class partner(models.Model):
     #_name = 'product.template'
     _inherit = 'res.partner'

     radius_account_ids = fields.One2many('radius.account', 'partner_id')
     radius_product_id = fields.Many2many('product.template')
     radius_ippoolgroup_id = fields.Many2many('radius.ippoolgroup')


class product(models.Model):
    #_name = 'product.template'
    _inherit = 'product.template'

    radius = fields.Boolean('Radius')
    download_rate = fields.Char('Download rate', help='Download rate (b,k,m,g)')
    upload_rate = fields.Char('Upload rate', help='Upload rate (b,k,m,g)')
    burst = fields.Boolean('Burst')
    burst_download_limit = fields.Char('Limit download', help='Limit burst download (b,k,m,g)')
    burst_upload_limit = fields.Char('Limit upload', help='Limit burst upload (b,k,m,g)')
    burst_download_thershold = fields.Char('Thershold download', help='Thershold burst download (b,k,m,g)')
    burst_upload_thershold  = fields.Char('Thershold upload', help='Thershold burst upload (b,k,m,g)')
    burst_download_time= fields.Char('Time download', help='Time burst download (b,k,m,g)')
    burst_upload_time = fields.Char('Time upload', help='Time burst upload (b,k,m,g)')
    radius_partner_id = fields.Many2many('res.partner')


class account_analytic_account(models.Model):
    _inherit= 'account.analytic.account'

    ippool_ip =fields.Many2one('IPPool Group', 'radius.ippoolgroup')
    