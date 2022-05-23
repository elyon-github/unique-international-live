# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import calendar
import psycopg2
import xlwt


class bir_module(models.Model):
    _name = 'bir_module.print_history'
    _description = 'bir_module.print_history'

    form_type = fields.Char(string='BIR Form Type')
    print_date = fields.Char()

class print_history_line(models.Model):
    _name = 'bir_module.print_history_line'
    _description = 'bir_module.print_history_line'

    print_id = fields.Many2one('bir_module.print_history')
    move_id = fields.Many2one('account.move')
    scope = fields.Char()
    form_type = fields.Char(string='BIR Form Type')

class atc_setup(models.Model):
    _name = 'bir_module.atc_setup'
    _description = 'bir_module.atc_setup'

    name = fields.Char(required=True)
    tax_id = fields.Many2one('account.tax', required=True)
    description = fields.Char()
    scope = fields.Selection([('sales', 'Sales'), ('purchase', 'Purchases')], required=True)
    remarks = fields.Char()

class bir_add_partner_field(models.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

    service_provider = fields.Many2one('res.partner', string="Service Provider")

class bir_reports(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    test_field = fields.Char()

    @api.model
    def test(self):
        pass

    def x_2307_forms(self, args):
        return self.env.ref('bir_module.2307_report_action_id_multi').report_action(self,data={'name':'BIR Form 2550M', 'month': args['month'], 'id': args['id'], 'trigger': args['trigger']})

    def x_get_2307_data(self, kwargs):
        data = []
        transactional = self._2307_query(kwargs)
        # landed_cost = self._2307_landed_cost_query(kwargs)

        data.append(transactional)
        # data.append(landed_cost)

        return data

    def _2307_query(self, args):
        query = """ SELECT Abs(T1.price_total)*(Abs(T3.amount)/100), T1.price_total, T5.name, T5.vat, T4.name, T3.name,
            T0.id, T0.move_type {2} 
            FROM account_move T0 
            JOIN account_move_line T1 ON T0.id = T1.move_id AND (T1.is_landed_costs_line = 'false' OR T1.is_landed_costs_line IS NULL) 
            JOIN account_move_line_account_tax_rel T2 ON T1.id = T2.account_move_line_id 
            JOIN account_tax T3 ON T2.account_tax_id = T3.id 
            JOIN bir_module_atc_setup T4 ON T3.id = T4.tax_id 
            JOIN res_partner T5 ON T0.partner_id = T5.id 
            LEFT JOIN bir_module_print_history_line T6 ON T6.move_id = T0.id AND T6.form_type = '2307' 
            WHERE T0.company_id = {0} AND T0.move_type = 'in_invoice' {1}"""

        end_parameter = self._2307_params(trans = args[1], id = args[0])

        self._cr.execute(query.format(self.env.company.id, end_parameter[0], end_parameter[1]))
        val = self._cr.fetchall()

        if args[2] == 'print':
            self.record_bir_form_print(val, '2307')

        return val

    def _2307_params(self, **kwargs):
        param = ""
        field = ""
        # group = ""
        
        if kwargs['trans'] == "transactional":
            param = " AND T0.id = " + str(kwargs['id'])
        else:
            parameter = kwargs['id'][1].replace("-", " ").split()
            span = self.check_quarter_2307(int(parameter[1]))

            param = " AND T0.partner_id = " + kwargs['id'][0] + " AND T6.id IS NULL AND "
            param += self.sawt_map_params(span, parameter[0])

            field = ", T0.invoice_date, T6.id "
            # group = ", T0.invoice_date"

        return [param, field]

    def process_2307_quarterly(self, data):
        cont = []
        temp_out = ()
        final = []

        for val in data:
            cont.append(val[4])

            temp_in = set(cont)
            temp_out = tuple(temp_in)
        
        for atc in temp_out:
            dict = {'desc': '', 'code': '', 'm1': 0, 'm2': 0, 'm3':0, 'taxed': 0, 'm_total': 0}

            for dat in data:
                if atc == dat[4]:
                    month_num = self.get_bir_month_num(dat[8])

                    if month_num == '1':
                        dict['m1'] += dat[1]
                    elif month_num == '2':
                        dict['m2'] += dat[1]
                    elif month_num == '3':
                        dict['m3'] += dat[1]
                    
                    dict['taxed'] += dat[0]
                    dict['m_total'] += dat[1]
                    dict['desc'] = dat[5]
                    dict['code'] = dat[4]
            final.append(dict)

        return final

    def process_2307_transactional(self, data):
        cont = []
        temp_out = ()
        final = []

        for val in data[0]:
            cont.append(val[4])

            temp_in = set(cont)
            temp_out = tuple(temp_in)
        
        for atc in temp_out:
            dict = {'desc': '', 'code': '', 'm1': 0, 'm2': 0, 'm3':0, 'taxed': 0, 'm_total': 0}

            for dat in data[0]:
                if atc == dat[4]:
                    month_num = self.get_bir_month_num(data[1])

                    if month_num == '1':
                        dict['m1'] += dat[1]
                    elif month_num == '2':
                        dict['m2'] += dat[1]
                    elif month_num == '3':
                        dict['m3'] += dat[1]
                    
                    dict['taxed'] += dat[0]
                    dict['m_total'] += dat[1]
                    dict['desc'] = dat[5]
                    dict['code'] = dat[4]
            final.append(dict)

        return final

    # def x_process_landed_cost_many(self, data):
    #     base_set = []
    #     new_val = []
    #     for x in data:
    #         base_set.append(x[2])

    #     for set_val in set(base_set):
    #         new_val.append([set_val, []])

    #     for dict_val in new_val:
    #         for base in data:
    #             if dict_val[0] == base[2]:
    #                 dict_val[1].append(base)
    #                 dict_val.append([base[3], base[4], base[5], base[6]])

    #     return new_val

    def x_2550_forms(self, args):
        param = args[0].replace("-", " ").split()
        #                   AR or AP    TAX total per line  line total      tax Name    tax Amount       ven/cust name  industry    has landed cost?
        #                   0           1               2                   3           4           5           6       7       8       9
        query = """ SELECT T0.move_type, T1.price_total, T1.tax_base_amount, T3.name, T3.amount, T3.tax_scope, T4.name, T5.name, T0.id, T0.move_type, T2.id
            FROM account_move T0 
            JOIN account_move_line T1 ON T0.id = T1.move_id AND T1.exclude_from_invoice_tab = 'true' 
            LEFT JOIN bir_module_print_history_line T2 ON T2.move_id = T0.id AND T2.form_type = '2550' 
            JOIN account_tax T3 ON T3.id = T1.tax_line_id AND T3.amount >= 0 
            JOIN res_partner T4 ON T4.id = T0.partner_id 
            LEFT JOIN res_partner_industry T5 ON T5.id = T4.industry_id 
            LEFT JOIN stock_landed_cost T6 ON T0.id = T6.vendor_bill_id 
            LEFT JOIN bir_module_print_history T7 ON T7.id = T2.print_id
            WHERE T0.company_id = {0} AND {1}"""

        quarter = {'month': param[1], 'year': param[0], 'trans': 'month'}
        if args[1] == '2550Q':
            quarter = {'month': self.x_2550_qrtrs(param), 'year': param[0], 'trans': 'qrtr'}

        end_param = self.x_2550_param(quarter)

        self._cr.execute(query.format(self.env.company.id, end_param))
        val = self._cr.fetchall()

        # return self.x_2550_process_data(val)
        if args[2] == 'print':
            self.record_bir_form_print(val, '2550')

        processed = self.x_2550_process_data(val)
        return processed

    def x_2550_process_data(self, data):
        sales = {'12A': 0, '12B': 0, '13A': 0, '13B': 0, '14': 0, '15': 0, '16A': 0, '16B': 0}
        purchase = {'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'P1': 0, 'P2': 0}

        for val in data:
            flag = False
            if val[0] == 'out_invoice':
                if str(val[7]) == 'Government':
                    sales['13A'] += abs(float(val[2]))
                    sales['13B'] += abs(float(val[1]))
                    flag = True
                elif int(val[4]) == 12:
                    sales['12A'] += abs(float(val[2]))
                    sales['12B'] += abs(float(val[1]))
                    flag = True
                elif int(val[4]) == 0:
                    sales['14'] += abs(float(val[2]))
                elif 'excempt' in str(val[3]).lower():
                    sales['15'] += abs(float(val[2]))
                else:
                    pass

                if flag == True:
                    sales['16A'] += abs(float(val[2]))
                    sales['16B'] += abs(float(val[1]))
                else:
                    sales['16A'] += abs(float(val[2]))
            else:
                if int(val[4]) == 12 and str(val[5]) == 'consu':
                    purchase['E'] += abs(float(val[2]))
                    purchase['F'] += abs(float(val[1]))
                    flag = True
                elif int(val[4]) == 12 and str(val[5]) == 'consu':
                    purchase['G'] += abs(float(val[2]))
                    purchase['H'] += abs(float(val[1]))
                    flag = True
                elif int(val[4]) == 12 and str(val[5]) == 'service':
                    purchase['I'] += abs(float(val[2]))
                    purchase['J'] += abs(float(val[1]))
                    flag = True
                elif int(val[4]) == 12 and str(val[5]) == 'service':
                    purchase['K'] += abs(float(val[2]))
                    purchase['L'] += abs(float(val[1]))
                    flag = True
                elif int(val[4]) == 0:
                    purchase['M'] += abs(float(val[2]))
                else:
                    pass

                if flag == True:
                    purchase['P1'] += abs(float(val[2]))
                    purchase['P2'] += abs(float(val[1]))
                else:
                    purchase['P1'] += abs(float(val[2]))

        value = [sales, purchase, self.env.company.id]

        return value


    def x_2550_print_action(self, args):
        if args['trans'] == '2550M':
            return self.env.ref('bir_module.bir_form_2550M').report_action(self,data={'name':'BIR Form 2550M', 'month': args['month'], 'trans': args['trans'], 'trigger': args['trigger']})
        else:
            return self.env.ref('bir_module.bir_form_2550Q').report_action(self,data={'name':'BIR Form 2550Q', 'month': args['month'], 'trans': args['trans'], 'trigger': args['trigger']})

    def x_2550_param(self, data):
        query = ""

        if(data['trans']) == 'month':
            init = "{0} = EXTRACT(MONTH FROM T0.date) AND {1} = EXTRACT(YEAR FROM T0.date)"
            query = init.format(data['month'], data['year'])
        else:
            init = "EXTRACT(MONTH FROM T0.date) >= {0} AND EXTRACT(MONTH FROM T0.date) <= {1} AND EXTRACT(YEAR FROM T0.date) = {2} AND T2.id IS NULL"
            query = init.format(data['month'][0], data['month'][1], data['year'])

        return query
    

##############################################################################################################################################################################
################################################################ SAWT AND MAP ################################################################################################
##############################################################################################################################################################################

    def SAWT_report(self, month):
        param = month.replace("-", " ").split()

        query = """ SELECT SUM(Abs(T1.price_total)), SUM(Abs(T1.tax_base_amount)), T5.vat, MAX(T5.name), T4.name, MAX(Abs(T3.amount)) 
            FROM account_move T0 
            JOIN account_move_line T1 ON T0.id = T1.move_id AND T1.exclude_from_invoice_tab = 'true' 
            JOIN account_tax T3 ON T3.id = T1.tax_line_id 
            JOIN bir_module_atc_setup T4 ON T3.id = T4.tax_id 
            JOIN res_partner T5 ON T5.id = T0.partner_id AND T5.vat IS NOT NULL
            WHERE T0.company_id = {0} AND T0.move_type = 'out_invoice' AND {1} GROUP BY T5.vat, T4.name, T3.amount"""

        quarter_iden = self.check_quarter(int(param[1]))
        end_parameter = self.sawt_map_params(quarter_iden, int(param[0]))

        self._cr.execute(query.format(self.env.company.id, end_parameter))
        val = self._cr.fetchall()

        return val

    def MAP_report(self, month):
        param = month.replace("-", " ").split()

        # return self.env.company.id
        query = """ SELECT SUM(Abs(T1.price_total)), SUM(Abs(T1.tax_base_amount)), T5.vat, MAX(T5.name), T4.name, MAX(Abs(T3.amount)) 
            FROM account_move T0 
            JOIN account_move_line T1 ON T0.id = T1.move_id AND T1.exclude_from_invoice_tab = 'true' 
            JOIN account_tax T3 ON T3.id = T1.tax_line_id 
            JOIN bir_module_atc_setup T4 ON T3.id = T4.tax_id 
            JOIN res_partner T5 ON T5.id = T0.partner_id AND T5.vat IS NOT NULL
            WHERE T0.company_id = {0} AND T0.move_type = 'in_invoice' AND {1} GROUP BY T5.vat, T4.name, T3.amount"""

        quarter_iden = self.check_quarter(int(param[1]))
        end_parameter = self.sawt_map_params(quarter_iden, int(param[0]))

        self._cr.execute(query.format(self.env.company.id, end_parameter))
        val = self._cr.fetchall()

        return val

    def sawt_map_params(self, param, year):
        append = ""
        if param[0] == "monthly":
            append = "EXTRACT(MONTH FROM T0.date) = " + str(param[1]) + " AND EXTRACT(YEAR FROM T0.date) = " + str(year)
        else:
            append = "EXTRACT(MONTH FROM T0.date) >= " + str(param[0]) + "  AND EXTRACT(MONTH FROM T0.date) <= " + str(param[1]) + " AND EXTRACT(YEAR FROM T0.date) = " + str(year)
        return append

    def export_sawt_map(self, month, report):
        try:
            ### Data Preparation ###
            data = []
            title = ""
            fname = ""
            if report == 'sawt':
                data = self.SAWT_report(month) # Fetch data 
                title = "SUMMARY ALPHALIST OF WITHHOLDING TAXES"
                fname = "SAWT report.xls"
            else:
                data = self.MAP_report(month) # Fetch data 
                title = "Monthly Alphalist of Payees"
                fname = "MAP report.xls"

            param = month.replace("-", " ").split()
            scope_init = self.check_quarter(int(param[1])) # Get Month or Quarter
            scope = ""
            if len(scope_init) == 2:
                scope = self.get_string_month(int(param[1]))
            else:
                scope = scope_init[2]

             # self.env.company.vat
            wb = xlwt.Workbook()
            sheet = wb.add_sheet('SAWT report')

            sheet.write(0, 0, "BIR Form 1702")
            sheet.write(1, 0, title)
            sheet.write(2, 0, "FOR THE MONTH/S OF " + str(scope) + ", " + str(param[0]))
            sheet.write(4, 0, "TIN: " + str(self.env.company.vat))
            sheet.write(5, 0, "Payee's Name: " + str(self.env.company.name))

            sheet.write(7, 0, "Seq Number")
            sheet.write(8, 0, "(1)")
            sheet.write(7, 1, "Taxpayer Identification Number")
            sheet.write(8, 1, "(2)")
            sheet.write(7, 2, "Corporation (Registered Name)")
            sheet.write(8, 2, "(3)")
            sheet.write(7, 3, "ATC Code")
            sheet.write(8, 3, "(4)")
            sheet.write(7, 4, "Amount of Income Payment")
            sheet.write(8, 4, "(5)")
            sheet.write(7, 5, "Tax Rate")
            sheet.write(8, 5, "(6)")
            sheet.write(7, 6, "Amount of Tax Withheld")
            sheet.write(8, 6, "(7)")

            ctr = 9
            seq = 1
            for val in data:
                sheet.write(ctr, 0, seq)
                sheet.write(ctr, 1, val[2])
                sheet.write(ctr, 2, val[3])
                sheet.write(ctr, 3, val[4])
                sheet.write(ctr, 4, val[1])
                sheet.write(ctr, 5, val[5])
                sheet.write(ctr, 6, val[0])

                ctr += 1
                seq += 1

            wb.save("C:/Users/asus/Downloads/" + fname)
        except Exception as ex:
            return str(ex)

##############################################################################################################################################################################
################################################################ SLS AND SLP #################################################################################################
##############################################################################################################################################################################

    def SLS_SLP_report(self, month, trans):
        param = month.replace("-", " ").split()

        quarter_iden = self.check_quarter(int(param[1]))
        end_parameter = self.sawt_map_params(quarter_iden, int(param[0]))

        contacts = self.get_contacts(quarter_iden, end_parameter, trans)
        numbers = self.get_numbers(quarter_iden, end_parameter, trans)

        vals = self.get_sls_slp_values(contacts, numbers)

        return vals

    def get_contacts(self, quarter_iden, end_parameter, trans):
        query = """ SELECT DISTINCT(T1.vat), T1.name
            FROM account_move T0 
            JOIN res_partner T1 ON T1.id = T0.partner_id 
            WHERE T0.company_id = {0} AND T0.state = 'posted' AND T0.move_type = '{1}' AND {2} """

        self._cr.execute(query.format(self.env.company.id, trans, end_parameter))
        val = self._cr.fetchall()

        return val

    def get_numbers(self, quarter_iden, end_parameter, trans):

        query = """ SELECT
            T4.vat as vat_name, T4.name as company_name, T0.name, T3.amount, T5.name, T3.tax_scope,
            CASE WHEN Abs(T3.amount) = 12 THEN Abs(price_subtotal) ELSE 0 END as VAT, 
            CASE WHEN LOWER(T5.name) LIKE '%zero%' THEN Abs(price_subtotal) ELSE 0 END as Zero_Rated, 
            CASE WHEN LOWER(T5.name) LIKE '%exempt%' THEN Abs(price_subtotal) ELSE 0 END as Exempt 
            FROM account_move T0 
            JOIN account_move_line T1 ON T0.id = T1.move_id 
            JOIN account_move_line_account_tax_rel T2 ON T1.id = T2.account_move_line_id 
            JOIN account_tax T3 ON T3.id = T2.account_tax_id AND T3.amount >= 0 
            JOIN res_partner T4 ON T4.id = T0.partner_id 
            LEFT JOIN account_tax_group T5 ON T5.id = T3.tax_group_id 
            WHERE T0.company_id = {0} AND T0.state = 'posted' AND T0.move_type = '{1}' AND {2} """

        self._cr.execute(query.format(self.env.company.id, trans, end_parameter))
        val = self._cr.fetchall()

        return val

    def get_sls_slp_values(self, bp, data):
        vals = []

        for x in bp:
            vals.append({'vat': x[0], 'name': x[1], 
                'gross_sales_po': 0,
                'exempt': 0,
                'zero_rated': 0,
                'taxable': 0,
                'po_services': 0,
                'po_capital_goods': 0,
                'po_other': 0,
                'tax': 0,
                'gross_tax': 0,
                })

        for y in vals:
            for z in data:
                if str(y['vat']) == str(z[0]):
                    tax = float(z[6]) * (float(z[3]) / 100)

                    y['gross_sales_po'] += float(z[6])
                    y['exempt'] += float(z[7])
                    y['zero_rated'] += float(z[8])
                    y['taxable'] += float(z[6])
                    y['po_other'] += float(z[6])
                    y['tax'] += round(tax, 2)
                    y['gross_tax'] += round(float(z[6]) + tax, 2)

        return vals


##############################################################################################################################################################################
################################################################ 1601e  ######################################################################################################
##############################################################################################################################################################################

    def x_1601e_print_action(self, month):
        company_id = self.env.company.id
        return self.env.ref('bir_module.1601e_report_action_id').report_action(self,data={'name':'BIR Form 1601e', 'month': month, 'company_id:': company_id})

    def x_1601e_data(self, month):
        param = month.replace("-", " ").split()

        query = """ SELECT SUM(Abs(T1.price_total)), SUM(Abs(T1.tax_base_amount)), T4.name, T4.description, MAX(Abs(T3.amount)) 
            FROM account_move T0 
            JOIN account_move_line T1 ON T0.id = T1.move_id AND T1.exclude_from_invoice_tab = 'true' 
            JOIN account_tax T3 ON T3.id = T1.tax_line_id 
            JOIN bir_module_atc_setup T4 ON T3.id = T4.tax_id 
            WHERE T0.company_id = {0} AND T0.move_type = 'out_invoice' AND EXTRACT(MONTH FROM T0.date) = {1} AND EXTRACT(YEAR FROM T0.date) = {2} GROUP BY T4.name, T4.description"""

        self._cr.execute(query.format(self.env.company.id, param[1], param[0]))
        val = self._cr.fetchall()

        return val


##############################################################################################################################################################################
################################################################ GENERAL FUNCTIONS  ##########################################################################################
##############################################################################################################################################################################

    def check_quarter(self, month):
        iden = ["monthly", month]
        if month == 3:
            iden = [1, 3, "January - March"]
        elif month == 6:
            iden = [4, 6, "April - June"]
        elif month == 9:
            iden = [7, 9, "July - September"]
        elif month == 12:
            iden = [10, 12, "October - December"]
        
        return iden
    
    def check_quarter_2307(self, month):
        iden = ["monthly", month]
        if month <= 3 and month >= 1:
            iden = [1, 3, "January - March"]
        elif month <= 6 and month >= 4:
            iden = [4, 6, "April - June"]
        elif month <= 9 and month >= 5:
            iden = [7, 9, "July - September"]
        elif month <= 12 and month >= 10:
            iden = [10, 12, "October - December"]
        
        return iden

    def get_string_month(self, num):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        return months[num-1]

    def x_2550_qrtrs(self, param):
        month = int(param[1])
        quarter = []
        if month >= 1 and month <= 3:
            quarter = [1, 3, "January", "March", 1]
        elif month >= 4 and month <= 6:
            quarter = [4, 6, "April", "June", 2]
        elif month >= 7 and month <= 9:
            quarter = [7, 9, "July", "September", 3]
        else:
            quarter = [10, 12, "October", "December", 4]

        return quarter

    def fetch_BP(self):
        query = """ SELECT id, name FROM res_partner WHERE is_company = 'true' AND vat IS NOT NULL """

        self._cr.execute(query)
        val = self._cr.fetchall()

        return val

    def get_bir_quarter(self, value):
        quarter = 0
        month = int(value.month)

        if month == 4 or month == 1 or month == 7 or month == 10: quarter = 1
        elif month == 2 or month == 5 or month == 8 or month == 11: quarter = 2
        else: quarter = 3

        return str(quarter)

    def get_bir_month_num(self, value):
        quarter = 0
        month = self.splice_month(str(value))

        if int(month[1]) == 4 or int(month[1]) == 1 or int(month[1]) == 7 or int(month[1]) == 10: quarter = 1
        elif int(month[1]) == 2 or int(month[1]) == 5 or int(month[1]) == 8 or int(month[1]) == 11: quarter = 2
        else: quarter = 1

        return str(quarter)

    def splice_month(self, month):
        return month.replace("-", " ").split()

    def get_marker_quarter(self, month):
        return self.x_2550_qrtrs(self.splice_month(month))

    def fetch_period_dates(self, value):
        vals = self.splice_month(value)

        month = self.x_2550_qrtrs(vals)

        range1 = calendar.monthrange(int(vals[0]), int(month[0]))
        range2 = calendar.monthrange(int(vals[0]), int(month[1]))

        month1 = str(month[0])
        month2 = str(month[1])

        if int(month[0]) < 10:
            month1 = "0" + month1

        if int(month[1]) < 10:
            month2 = "0" + month2

        return [str(vals[0][2:]), month1, month2, str(range1[1]), str(range2[1]), str(vals[0]), str(vals[1])]
    
    def fetch_month_coverage(self, value):
        year = value.strftime("%Y")
        month = value.strftime("%m")

        range = calendar.monthrange(int(year), int(month))

        return {'month': str(month), 'year': str(year), 'date': str(range[1])}

    def x_format_vat(self, vat):
        val = ""
        if vat != False:
            val = vat[:3] + "-" + vat[3:6] + "-" + vat[6:]

        return str(val)

    def x_slice_vat(self, vat):
        val = []
        if vat != False:
            val = [vat[:3], vat[3:6], vat[6:], '000']

        return val

    def x_fetch_company_id(self):
        return self.env.company.id

    def record_bir_form_print(self, arr, process):
        data = self.process_array(arr, process)
        
        header_query = ""
        header_query = "INSERT INTO bir_module_print_history (form_type, create_uid, print_date, create_date) VALUES('{0}','{1}', '{2}', current_timestamp) RETURNING id"

        if len(data) > 0:
            self._cr.execute(header_query.format(data[0][1],data[0][2],data[0][3]))
            print_id = self._cr.fetchone()[0]

        for val in data:
            base_query = "INSERT INTO bir_module_print_history_line (print_id, move_id, scope, form_type, create_uid, create_date) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', current_timestamp)"

            self._cr.execute(base_query.format(print_id, val[0], val[4], val[1], val[2]))

    def process_array(self, arr, process):
        data = []
        curr_datetime = datetime.today().strftime("%d/%m/%Y")
        if process == '2550':
            for val in arr:
                data.append([val[8],'2550', self._uid, curr_datetime, val[9]])
        elif process == '2307':
            for val in arr:
                data.append([val[6], '2307', self._uid, curr_datetime, val[7]])

        return data
