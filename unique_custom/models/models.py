# -*- coding: utf-8 -*-

from odoo import models, fields, api


class inherit_account(models.Model):
    _inherit = "account.payment"

    # ewt = fields.Float(string="EWT")

    def compute_ewt(self, id):
        payment = self.fetch_matching_id(id)
        invoice = self.fetch_inv_id(payment[0])
        ewt = self.fetch_ewt(invoice[0])
        vat = self.fetch_vat(invoice[0])

        percent = round((float(payment[1]) / float(invoice[1])),2)
        ewt_computed  = 0
        vat_computed = 0
        
        if ewt != None:
            ewt_computed = round(float(ewt) * percent,2)
        if vat != None:
            vat_computed = round(float(vat) * percent,2)

        return ewt_computed, vat_computed

    def fetch_matching_id(self, id):
        match_id = []

        query = """SELECT T2.matching_number, T0.amount 
            FROM account_payment T0
            JOIN account_move T1 ON T0.move_id = T1.id
            JOIN account_move_line T2 ON T2.move_id = T1.id AND T2.matching_number IS NOT NULL
            WHERE T0.id = '{0}'"""
        self._cr.execute(query.format(id))
        match_id = self._cr.fetchall()[0]

        return match_id

    def fetch_inv_id(self, id):
        entry_id = []

        query = """SELECT T0.id, T0.amount_total 
            FROM account_move T0
            JOIN account_move_line T1 ON T0.id = T1.move_id 
            WHERE T1.matching_number = '{0}'
            AND (T0.move_type = 'out_invoice' OR T0.move_type = 'in_invoice')"""

        self._cr.execute(query.format(id))
        entry_id = self._cr.fetchall()[0]

        return entry_id
    
    def fetch_ewt(self, id):
        ewt = []

        ewt_query = """SELECT SUM(ABS(T0.price_total)) 
            FROM account_move_line T0 
            JOIN account_tax T1 ON T0.tax_line_id = T1.id
            WHERE T0.tax_line_id IS NOT NULL AND T0.move_id = '{0}' AND T1.amount < 0"""

        self._cr.execute(ewt_query.format(id))
        ewt = self._cr.fetchall()[0]

        return ewt[0]
    
    def fetch_vat(self, id):
        vat = []

        vat_query = """SELECT SUM(ABS(T0.price_total)) 
            FROM account_move_line T0 
            JOIN account_tax T1 ON T0.tax_line_id = T1.id
            WHERE T0.tax_line_id IS NOT NULL AND T0.move_id = '{0}' AND T1.amount = 12"""

        self._cr.execute(vat_query.format(id))
        vat = self._cr.fetchall()[0]

        return vat[0]
