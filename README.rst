Sample Odoo ETL Repository
===========================

This is a simple project in Python demonstrating an API call to Odoo

Execute ./demo.py to grab all sales orders line  items from the Odoo
demo DB and

(a) save to CSV (e.g. part of an ETL process to ultimately ingest into a SQL store)
(b) manipulate with pandas, then write to Excel with formatting (e.g. an external user report)

Data will be saved locally in ./data folder

The extracted Sales Orders will mirror what you see on the Odoo UI

https://demo3.odoo.com/web#action=857&model=sale.order&view_type=list&menu_id=576



