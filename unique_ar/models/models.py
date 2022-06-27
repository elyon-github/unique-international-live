# -*- coding: utf-8 -*-

from ast import Store
import string
from xmlrpc.client import Boolean
from odoo import models, fields, api


class unique_ar(models.Model):
    _name = 'unique_ar.unique_ar'
    _description = 'unique_ar.unique_ar'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

class inherit_invoices(models.Model):
    _inherit = 'account.move'

    waybill_no = fields.Char(string="Waybill No.")
    tracking_no = fields.Char(string="Tracking No.")
    courier = fields.Char(string="Courier")

class unique_fields(models.Model):
    _inherit = 'sale.order.line'

    labor_component = fields.Integer(string="Labor Component %")
    rel_wt = fields.Float(string="Rel. Wt. %", store=True, compute="_compute_rel_wt", digits=(100,5))
    progress = fields.Integer(string="Percentage")
    is_a_project_line = fields.Boolean(string="Is a Project?", default=False)
    lot_price = fields.Float(string="Lot Price")

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'labor_component')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit
            if line.lot_price != 0:
                price = line.lot_price
            if line.labor_component != 0:
                price = price + (price * (line.labor_component / 100))
            line.update({ 'price_unit': price })
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('price_subtotal')
    def _compute_rel_wt(self):
        total = 0
        for line in self:
            total += line.price_subtotal

        for record in self:
            val = 0
            if record.price_subtotal != 0:
                val = float(record.price_subtotal) / float(total)
                
            record.update({
                'rel_wt': val
            })
    
    @api.onchange('lot_price')
    def change_unit_price(self):
        for line in self:
            price = line.lot_price
            if line.labor_component != 0:
                price = line.lot_price + (line.lot_price * (line.labor_component / 100))
            line.update({ 'price_unit': price })
    
    @api.onchange('progress')
    def change_delivered_qty(self):
        for line in self:
            percent = 0
            if line.progress != 0:
                percent = line.progress / 100
            line.update({ 'qty_delivered': percent })

class unique_fields_header(models.Model):
    _inherit = 'sale.order'
    
    is_a_project_head = fields.Boolean(string="Is a Project?", default=False)
    waybill_no = fields.Char(string="Waybill No.")
    tracking_no = fields.Char(string="Tracking No.")
    courier = fields.Char(string="Courier")

    def _prepare_invoice(self):
        ret = super(unique_fields_header, self)._prepare_invoice()

        ret['waybill_no'] = self.waybill_no
        ret['tracking_no'] = self.tracking_no
        ret['courier'] = self.courier

        return ret

    @api.model
    def fetch_ac_values(self, so_id):
        arr = self._get_array_values(so_id)
        lines = self._process_lines(arr[1])
        # return lines
        final_arr = self._process_array(arr, lines)
        return final_arr
    
    def _get_array_values(self, so_id):
        query1 = """SELECT A1.name, A1.analytic_account_id, A1.amount_untaxed, A1.amount_tax, A1.amount_total,
            A2.id, A2.name, A2.price_total, A2.qty_invoiced, A2.progress, A2.display_type, A2.rel_wt, A2.price_unit, 
            product_uom_qty, A3.name, A2.price_subtotal, A5.type, A5.service_type 
            FROM sale_order A1 
            LEFT JOIN sale_order_line A2 ON A1.id = A2.order_id 
            LEFT JOIN uom_uom A3 ON A2.product_uom = A3.id
            LEFT JOIN product_product A4 ON A4.id = A2.product_id
            LEFT JOIN product_template A5 ON A5.id = A4.product_tmpl_id
            WHERE A1.id = {0} ORDER BY A2.id ASC"""

        query2 = """SELECT A1.name, A1.amount_untaxed, A1.amount_tax, A1.amount_total, 
            A2.id, A2.name, A2.invoice_date, A2.amount_untaxed, A2.amount_tax, A2.amount_total,
            A3.id, A3.date, A3.name, A3.quantity, A3.price_subtotal, A3.price_total, A3.display_type, A2.date
            FROM sale_order A1 
            LEFT JOIN account_move A2 ON A1.name = A2.invoice_origin AND A2.state = 'posted' 
            LEFT JOIN account_move_line A3 ON A2.id = A3.move_id AND exclude_from_invoice_tab = 'false' 
            WHERE A1.id = '{0}' ORDER BY A2.id ASC"""
        
        self._cr.execute(query1.format(so_id))
        arr1 = self._cr.fetchall()

        self._cr.execute(query2.format(so_id))
        arr2 = self._cr.fetchall()
        # return (query1.format(so_id), query2.format(so_id))
        return (arr1, arr2)
    
    # def _process_lines(self, val):
    #     unique = self._fetch_unique_val(val)

    #     return unique
    #     # return val

    def _process_lines(self, val):
        arr = []

        for arr_val in val:
            arr.append(str(arr_val[5]))
        
        toSet = set(arr)
        toList = list(toSet)
        return toList

    def _process_array(self, val, inv):
        base = val[0][1:]
        dp = val[0][1][4]
        billing = val[1]
        invoices = inv

        arr = []

        invoices.sort(reverse=True)
        seq = 0
        sub_seq = 1
        for arr_val in base:
            temp = {
                'Base':{}, 
                'Previous':{}, 
                'Current':{}, 
                'To-date':{}
            }

            base_subarr = {'seq':0, 'Desc':"", 'Amt':0, 'type':None, 'RelWt':0, 'unit':0, 'qty':0, 'priceUnit':0, 'billing_num': len(inv), 'date': "", 'DP': dp}
            previous_subarr = {'Desc':"", '%':0, 'Amt':0}
            current_subarr = {'Desc':"", '%':0, 'Amt':0}
            todate_subarr = {'Desc':"", '%':0, 'Amt':0}

            if arr_val[10] == 'line_section':
                seq += 1
                sub_seq = 1
                base_subarr['seq'] = seq
                base_subarr['Desc'] = arr_val[6]
                base_subarr['type'] = 'section'
            else:
                base_subarr['seq'] = str(seq) + "." + str(sub_seq)
                base_subarr['Desc'] = arr_val[6]
                base_subarr['Amt'] = arr_val[7]
                base_subarr['type'] = 'line'
                base_subarr['RelWt'] = round(arr_val[15]/arr_val[2], 5)
                base_subarr['unit'] = arr_val[14]
                base_subarr['qty'] = arr_val[13]
                base_subarr['priceUnit'] = arr_val[12]
                sub_seq += 1

                line_ctr = 0
                for line in invoices:
                    for det in billing:
                        storable_uom = self.compute_percent(det[13],arr_val[13],det[13],arr_val[16],arr_val[17])
                        base_subarr['date'] = det[17]

                        ### previous ###
                        if line_ctr > 0:
                            if line == det[5] and str(arr_val[6]) == str(det[12]):
                                previous_subarr['Desc'] = str(det[12])
                                # previous_subarr['%'] += float(det[13])*100
                                previous_subarr['%'] += storable_uom
                                previous_subarr['Amt'] += float(det[15])
                        ### THIS PERIOD ###
                        if line_ctr == 0:
                            if line == det[5] and str(arr_val[6]) == str(det[12]):
                                current_subarr['Desc'] = str(det[12])
                                # current_subarr['%'] += float(det[13])*100
                                current_subarr['%'] += storable_uom
                                current_subarr['Amt'] += float(det[15])
                                # current_subarr['Inv#'] = str(det[5])
                    line_ctr += 1
                total_storable = self.compute_percent(arr_val[8],arr_val[13],arr_val[8],arr_val[16],arr_val[17])

                ### TO DATE ###
                todate_subarr['Desc'] = str(arr_val[6])
                # todate_subarr['%'] += float(arr_val[8])*100
                todate_subarr['%'] += total_storable
                todate_subarr['Amt'] += round(float(arr_val[7])*float(arr_val[8]), 2)
                # todate_subarr['Inv#'] = str(det[5])
            
            temp['Base'].update(base_subarr)
            temp['Previous'].update(previous_subarr)
            temp['Current'].update(current_subarr)
            temp['To-date'].update(todate_subarr)

            arr.append(temp)
        
        return arr
    
    def compute_percent(self, default, base, div, type, service_type):
        if type != 'service':
            return round((div/base)*100, 1)
        else:
            return round(default*100, 1)
