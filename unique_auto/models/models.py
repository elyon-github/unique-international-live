# # -*- coding: utf-8 -*-

from odoo import models, fields, api


class unique_auto(models.Model):
    pass

class inhetit_stock_picking(models.Model):
    _inherit = "stock.picking"

    sales_team_id = fields.Many2one('crm.team', string="Sales Team")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    sales_person_id = fields.Many2one('res.users', string="Salesperson")

class inherit_invoice(models.Model):
    _inherit = 'account.move'

    dr_only = fields.Boolean(string="DR Only", readonly=True)

class inherit_sales(models.Model):
    _inherit = "sale.order"

    dr_only = fields.Boolean(string="DR Only")

    def action_confirm(self):
        res = super(inherit_sales, self).action_confirm()
        for do_pick in self.picking_ids:
            do_pick.write({
                'sales_team_id': self.team_id,
                'analytic_account_id': self.analytic_account_id,
                'sales_person_id': self.user_id
                })
        return res
    
    def _prepare_invoice(self):
        ret = super(inherit_sales, self)._prepare_invoice()

        ret['dr_only'] = self.x_studio_dr_only

        return ret
    
    def migrate_custom_data(self):
        picking = self.select_picking_values()
        bills = self.select_invoice_values()
        update_stock_picking = ""
        update_bills = ""
        
        for pick in picking:
            analytic = pick[3]
            if analytic == None:
                analytic = "NULL"

            stock_picking_temp = """UPDATE stock_picking
                SET sales_team_id={0}, analytic_account_id={1}, sales_person_id={2} 
                WHERE sale_id={3};"""

            update_stock_picking += stock_picking_temp.format(pick[1], analytic, pick[2], pick[0])
        self._cr.execute(update_stock_picking)

        for inv in bills:
            stat = inv[0]
            if inv[0] == None:
                stat = False

            billsQ_temp = """UPDATE account_move 
                SET dr_only={0}
                WHERE id={1};"""
            
            update_bills += billsQ_temp.format(stat, inv[1])
        self._cr.execute(update_bills)
        
        
    def select_picking_values(self):
        select_ids = """SELECT id, team_id, user_id, analytic_account_id, x_studio_dr_only FROM sale_order"""

        self._cr.execute(select_ids)
        val = self._cr.fetchall()

        return val
    
    def select_invoice_values(self):
        sales_ids = """SELECT T3.x_studio_dr_only, T4.id 
            FROM sale_order_line_invoice_rel T0 
            JOIN sale_order_line T1 ON T1.id = T0.order_line_id 
            JOIN account_move_line T2 ON T2.id = T0.invoice_line_id 
            JOIN sale_order T3 ON T1.order_id = T3.id 
            JOIN account_move T4 ON T2.move_id = T4.id"""
        
        self._cr.execute(sales_ids)
        val = self._cr.fetchall()

        return val

