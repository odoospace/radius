# -*- coding: utf-8 -*-

from openerp import models, fields, api
#from pagerange import PageRange

class Partner(models.Model):
     #_name = 'product.template'
     _inherit = 'res.partner'

     radius_account_ids = fields.One2many('radius.account', 'partner_id')
     radius_product_id = fields.Many2many('product.template')
     radius_ippool_id = fields.Many2many('radius.ippool')


class Product(models.Model):
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


class IPPool(models.Model):
     _name = 'radius.ippool'

     def show_ips(self):
         pass

     name = fields.Char('Name')
     pool_type = fields.Selection([
        ('regular', 'Regular'),
        ('internal', 'Internal')
     ])
     pool_range = fields.Char('IP Range', help='Create a range (A.B.C.D-E or A.B.C.D/E)')
     ippoolgroup_id = fields.Many2one('radius.ippoolgroup')
     #partner_ids = fields.Many2many('res.partner')
     

class IPPoolGroup(models.Model):
    _name = 'radius.ippoolgroup'

    name = fields.Char('Name')
    partner_ids = fields.Many2many('res.partner')
    ippool_ids = fields.One2many('radius.ippool', 'ippoolgroup_id')


class NAS(models.Model):
    _name = 'radius.nas'

    name = fields.Char('Name')     # shortname
    ip = fields.Char('IP')         # nasname
    secret = fields.Char('Secret') # Other
    nas_type = fields.Selection([
        ('mikrotik', 'Mikrotik'),
        ('cisco', 'CISCO'),
        ('pfsense', 'PFSense'),
        ('other', 'Other')], 'NAS Type')


class Account(models.Model):
    _name = 'radius.account'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    username = fields.Char()
    password = fields.Char()
    contract_id = fields.Many2one('account.analytic.account')
    product_id = fields.Many2one('product.product')
    pool_type = fields.Selection([
        ('NAS', 'NAS'),
        ('pool', 'Pool'),
        ('static', 'Static'),
        ('dynamic', 'Dynamic')]
    )
    static_ip = fields.Char()
    ippool_id = fields.Many2one('radius.ippool')


class Task(models.Model):
    _name = 'radius.task'

    @api.model
    def sync_radius_data(self):
        """ function to sync data between Odoo and FreeRadius"""
        database = 'radius ONO'
        radius_db = self.env['base.external.dbsource'].search([('name', '=', database)])

        # test database connection
        #if not radius_db.connection_test():
        #    print "ERROR. I can't connect with %s" % database

        # remove nas
        # TODO: sync
        sql = 'delete from nas;'
        radius_db.execute(sql, nodata=True)

        # remove radcheck
        # TODO: sync
        sql = 'delete from radcheck;'
        radius_db.execute(sql, nodata=True)

        # remove radreply
        # TODO: sync
        sql = 'delete from radreply;'
        radius_db.execute(sql, nodata=True)

        # sync nas
        nas = self.env['radius.nas'].search([])
        sql_nas = "insert into nas (nasname, shortname, type, secret) values (%s, %s, %s, %s);"
        for n in nas:
            radius_db.execute(sql_nas, (n.ip, n.name, n.nas_type.lower(), n.secret), nodata=True)

        # sync accounts
        accounts = self.env['radius.account'].search([])
        sql_radcheck = "insert into radcheck (username, attribute, op, value) values (%s, %s, %s, %s);"
        sql_radreply = "insert into radreply (username, attribute, op, value) values (%s, %s, %s, %s);"
        for account in accounts:
            if account.product_id:
                product = account.product_id
                print 'bypass', product.name
            elif account.contract_id:
                product = account.contract_id.recurring_invoice_line_ids[0].product_id
                print 'contract', product.name
            else:
                # TODO: launch a warning
                continue

            # check rates
            download_rate = product.download_rate and product.download_rate.lower() or '0'
            upload_rate = product.upload_rate and product.upload_rate.lower() or '0'
            rate_limit = '%s/%s' % (upload_rate, download_rate)

            radius_db.execute(sql_radcheck, (account.username, 'password', '==', account.password), nodata=True)
            radius_db.execute(sql_radreply, (account.username, 'Mikrotik-Rate-Limit', ':=', rate_limit), nodata=True)
