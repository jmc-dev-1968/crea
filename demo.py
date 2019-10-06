
from odoo import export_sales_order_2_excel, export_sales_orders_2_csv

## execute odoo API call (grab sales order details), save to CSV
export_sales_orders_2_csv()

## execute odoo API call (grab sales order details), use pandas to aggregate data and writee to Excel workbook
export_sales_order_2_excel()

