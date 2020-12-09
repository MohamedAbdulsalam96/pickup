# -*- coding: utf-8 -*-
# Copyright (c) 2020, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):

	if not filters: filters = {}

	columns = get_columns(filters)
	data = get_items(filters.get("pickup_slot"), filters.get("customer"))

	return columns, data, [ ], [ ], [filters.get("pickup_slot")]

def get_columns(filters):
	columns = [
		_("Customer") + "::200",
		_("Code") + "::200",
		_("Quantity") + "::100",
		_("Designation") + "::300"
	]
	return columns

def get_items(pickup_slot, customer):
	items = frappe.db.sql("""
			select SO.customer_name, SOI.item_code, sum(SOI.qty) as qty, SOI.item_name
			from `tabSales Order` SO
			inner join `tabSales Order Item` SOI on SO.name = SOI.parent
			inner join `tabItem` I on SOI.item_code = I.name
			where SO.status in ('To Deliver and Bill', 'To Deliver')
				and SO.pickup_slot = %(pickup_slot)s
				and SO.customer = (case when %(customer)s != "" then %(customer)s else SO.customer end)  
			group by SO.customer_name, SOI.item_code, SOI.item_name
			order by SO.customer_name, I.special_order_item desc, SOI.item_code""",
						  {"pickup_slot": pickup_slot, "customer": customer}, as_dict=False)
	return items