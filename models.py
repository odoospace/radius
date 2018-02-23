# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ippool(models.Model):
    _name = 'radius.ippool'

    def show_ips(self):
        pass

    name = fields.Char('Name')
    pool_type = fields.Selection([
      ('regular', 'Regular'),
      ('internal', 'Internal')
    ])
    pool_range = fields.Char('IP Range', help='Create range (A.B.C.D-E or A.B.C.D/E)')
    ippoolgroup_id = fields.Many2one('radius.ippoolgroup')
    priority = fields.Integer('Priority')
    #partner_ids = fields.Many2many('res.partner')
     

class ippool_group(models.Model):
    _name = 'radius.ippool.group'

    name = fields.Char('Name')
    partner_ids = fields.Many2many('res.partner')
    ippool_ids = fields.One2many('radius.ippool', 'ippoolgroup_id')


class nas(models.Model):
    _name = 'radius.nas'

    name = fields.Char('Name')     # shortname
    ip = fields.Char('IP')         # nasname
    secret = fields.Char('Secret') # Other
    nas_type = fields.Selection([
        ('mikrotik', 'Mikrotik'),
        ('cisco', 'CISCO'),
        ('pfsense', 'PFSense'),
        ('other', 'Other')], 'NAS Type')


class account(models.Model):
    _name = 'radius.account'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    username = fields.Char()
    password = fields.Char()
    contract_id = fields.Many2one('account.analytic.account')
    product_id = fields.Many2one('product.product')
    pool_type = fields.Selection([
        ('NAS', 'NAS'),
        ('poolgroup', 'Pool Group'),
        ('static', 'Static'),
        ('dynamic', 'Dynamic')]
    )
    static_ip = fields.Char()
    ippoolgroup_id = fields.Many2one('radius.ippool')


class task(models.Model):
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
