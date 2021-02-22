# Copyright (c) 2021, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.setup.doctype.item_group.item_group import get_child_groups

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns(filters)
	data = get_items(filters.get("item_group"), filters.get("item_code"),
					 filters.get("item_creation_date"), filters.get("item_price_date"))

	return columns, data

def get_columns(filters):
	columns = [
		_("Item Code") + "::100",
		_("Item Name") + "::250",
		_("Price Sales UOM") + "::100",
		_("Price Stock UOM") + "::100",
		_("Stock UOM") + "::100"
	]

	return columns

def get_items(item_group, item_code, item_creation_date, item_price_date):

	if item_group:
		child_groups = ", ".join(['"' + frappe.db.escape(i[0]) + '"' for i in get_child_groups(item_group)])
	else:
		child_groups = ", ".join(['"' + frappe.db.escape(i[0]) + '"' for i in get_child_groups(_("Produits"))])

	items = frappe.db.sql("""
			select I.item_code, I.item_name, 
				round(IP.price_list_rate * ifnull(C.conversion_factor,1),2) as price_sales_uom, 
				IP.price_list_rate as price_stock_uom, I.stock_uom
			from `tabItem` I
			inner join `tabItem Price` IP on I.item_code = IP.item_code and IP.price_list = %(price_list)s
			left join `tabUOM Conversion Detail` C on I.name = C.parent and I.sales_uom = C.uom  
			where I.disabled = 0 and I.print_label = 1
			and I.item_code = (case when %(item_code)s != "" then %(item_code)s else I.item_code end) 
			and I.item_group in ({child_groups}) 
			and I.creation >= (case when %(item_creation_date)s != "" then %(item_creation_date)s else "19000101" end)
			and IP.modified >= (case when %(item_price_date)s != "" then %(item_price_date)s else "19000101" end)
			order by I.item_code""".format(child_groups=child_groups),
				{"item_code": item_code, "item_creation_date": item_creation_date, "item_price_date": item_price_date,
				 "price_list": frappe.db.get_single_value("Selling Settings", "selling_price_list")}, as_dict=False)

	return items