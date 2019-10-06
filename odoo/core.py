# -*- coding: utf-8 -*-

from . import util
from pprint import pprint
import xmlrpc.client
import datetime
import pandas as pd
#import pandas.io.formats.excel
#from xlsxwriter import utility as xlsutil

def get_sales_orders():

    ## get demo connection info
    info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
    url, db, username, password = \
        info['host'], info['database'], info['user'], info['password']

    ## server version (needed for next  call)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    ## get uid for subsequent authentication
    uid = common.authenticate(db, username, password, {})

    ## set up endpoint for model method calls ...
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    ## get SO's (invoiced SO's  only)
    orders = models.execute_kw(db, uid, password
        , 'sale.order', 'search_read'
        , [[['invoice_status', '=', 'to invoice']]]
        , {'fields': ['id', 'date_order', 'partner_id', 'name']})

    ## flatten JSON
    records = []
    for order in orders:

        so_id = order['id']
        so_key = order['name']
        partner_id = order['partner_id'][0]
        partner_name = order['partner_id'][1]
        order_date = order['date_order']

        ## order header (repeated across line  items)
        order_record = [so_id, so_key, partner_id, partner_name, order_date]

        ## get SO line items for this SO
        line_items = models.execute_kw(db, uid, password
            , 'sale.order.line', 'search_read'
            , [[['invoice_status', '=', 'to invoice'], ['order_id', '=', so_id]]]
            , {'fields': ['date_order', 'order_partner_id', 'price_total', 'price_subtotal',  'price_unit'
                , 'product_qty', 'price_tax', 'product_id', 'name']})

        ## flatten JSON
        for item in  line_items:

            #pprint(item)

            line_number = item['id']
            product_id = item['product_id'][0]
            product_name = item['product_id'][1]
            product_desc = item['name']
            price =  item['price_unit']
            quantity =  item['product_qty']
            tax =  item['price_tax']
            subtotal =  item['price_subtotal']
            total =  item['price_total']

            # line item
            line_item_record = [line_number, product_id, product_name, product_desc, quantity, price, subtotal, tax, total]

            ## full record
            full_record =  order_record + line_item_record
            records.append(full_record)

    return records

def export_sales_orders_2_csv():

    ## grab SO's from Odoo API
    records = get_sales_orders()

    ## store as CSV
    data_dir = "./data"
    now = datetime.datetime.now()
    csv_filename = '{}/odoo-sales-order-detail--{}.csv'.format(data_dir, now.strftime("%Y-%m-%d-%H%M%S"))
    header = 'so_id,so_key,partner_id,partner_name,order_date,line_number,product_id,product_name,product_desc,quantity,price,subtotal,tax,total'
    util.generate_csv_file(csv_filename, records, header)


def export_sales_order_2_excel():

    ## grab SO's from Odoo API
    records = get_sales_orders()
    header = 'so_id,so_key,partner_id,partner_name,order_date,line_number,product_id,product_name,product_desc,quantity,price,subtotal,tax,total'
    col_names = header.split(",")

    ## convert records to a dataframe
    df_li = pd.DataFrame(data = records, columns = col_names)

    ## aggregate orders by partner into a nw df
    df_sales_orders = df_li.groupby(['partner_name', 'so_key']).apply(lambda row: pd.Series({'quantity': sum(row['quantity']), 'total': sum(row['total'])}))

    # create list holding column display name, width, format (optional) and alignment for Excel column formatting
    column_list = [
        ['Partner Name', 30, None, 'left']
        , ['Sales Order Key', 15, None, 'left']
        , ['Total Qty', 20, '#,##0', 'right']
        , ['Total Sales', 20, '#,##0.00', 'right']
    ]

    ## rename columns
    df_sales_orders.index.names = [col[0] for col in column_list][0:2]
    df_sales_orders.columns = [col[0] for col in column_list][2:4]

    ## export to excel
    data_dir = "./data"
    now = datetime.datetime.now()
    xls_filename = '{}/odoo-sales-by-partner-report--{}.xlsx'.format(data_dir, now.strftime("%Y-%m-%d-%H%M%S"))
    util.generate_xlsx_file(xls_filename, df_sales_orders, column_list, "SALES ORDERS")


def test():

    ## from odoo demo page : https://www.odoo.com/documentation/12.0/webservices/odoo.html

    info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()

    url, db, username, password = \
        info['host'], info['database'], info['user'], info['password']

    ## retrieves version info
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    ## get uid for subsequent authentication
    uid = common.authenticate(db, username, password, {})

    ## check access rights
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    success = models.execute_kw(db, uid, password
        , 'res.partner', 'check_access_rights'
        , ['read'], {'raise_exception': False})

    ## retrieve id's (appears to retrieve PK of data model object)
    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True], ['customer', '=', True]]])

    ## cusstomer count
    cust_cnt = models.execute_kw(db, uid, password, 'res.partner', 'search_count',
        [[['is_company', '=', True], ['customer', '=', True]]])

    ##  ... all customers
    cust_cnt = models.execute_kw(db, uid, password, 'res.partner', 'search_count',
        [[['customer', '=', True]]])

    ## retrieve data
    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True], ['customer', '=', True]]],
        {'limit': 1})

    ## this is a ton of data, many fields (entire customer record)
    #[record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])
    #print(record)

    ## only get desired fields
    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True], ['customer', '=', True]]], {'limit': 12})

    records = models.execute_kw(db, uid, password,
                      'res.partner', 'read',
                      [ids], {'fields': ['name', 'website', 'sale_order_count']})

    #print(pprint(records))

    ## get so fields
    so_fields = models.execute_kw(
        db, uid, password, 'sale.order', 'fields_get',
        [], {'attributes': ['string', 'help', 'type']})



    ## sales orders
    so_ids = models.execute_kw(db, uid, password,
                            'sale.order', 'search',
                            [[['invoice_status', '=', 'to invoice']]], {'limit': 5})

    sos = models.execute_kw(db, uid, password,
                      'sale.order', 'read',
                      [so_ids], {'fields': ['date_order', 'user', 'order_line', 'partner_id']})

    pprint(sos)

    ## get so fields
    li_fields = models.execute_kw(
        db, uid, password, 'sale.order.line', 'fields_get',
        [], {'attributes': ['string', 'help', 'type']})

    #pprint(li_fields)

    li = models.execute_kw(db, uid, password
        , 'sale.order.line', 'search_read'
        , [[['invoice_status', '=', 'to invoice']]]
        , {'fields': ['date_order', 'partner_id', 'order_id', 'name', 'name_short', 'price_total', 'price_unit', 'product_qty', 'product_id']})

    pprint(li)
