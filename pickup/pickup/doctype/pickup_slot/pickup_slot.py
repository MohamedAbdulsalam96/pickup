# -*- coding: utf-8 -*-
# Copyright (c) 2018, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PickupSlot(Document):

	def autoname(self):

		abbrev = frappe.get_value('Pickup Point', self.pickup_point, 'abbr') or ''

		self.name = frappe.utils.formatdate(self.date, "EEEE dd/MM/yyyy").capitalize() + " " + \
					frappe.utils.format_datetime(frappe.utils.format_time(self.start_time), "HH:mm") + "-" + \
					frappe.utils.format_datetime(frappe.utils.format_time(self.end_time), "HH:mm") + \
					abbrev


@frappe.whitelist(allow_guest=True)
def get_items_from_sales_order(customer, pickup_slot):
	items = frappe.db.sql("""
		select SOI.item_code, sum(SOI.qty) as qty, SOI.rate, SOI.uom
		from `tabSales Order` SO
		inner join `tabSales Order Item` SOI on SO.name = SOI.parent
		where SO.status in ('To Deliver and Bill', 'To Deliver') and SO.customer = %(customer)s and SO.pickup_slot = %(pickup_slot)s
		group by SOI.item_code, SOI.rate, SOI.uom
		order by SOI.idx""",
		{"customer": customer, "pickup_slot": pickup_slot}, as_dict=True)

	# Close the order(s)
	frappe.db.sql("""
		update `tabSales Order` set status = "Closed"
		where status in ('To Deliver and Bill', 'To Deliver') and customer = %(customer)s and pickup_slot = %(pickup_slot)s
		""", {"customer": customer, "pickup_slot": pickup_slot})
	frappe.db.commit()
	
	return items

@frappe.whitelist(allow_guest=True)
def get_sales_orders(pickup_slot):
	orders = frappe.db.sql("""
		select SO.name
		from `tabSales Order` SO
		where SO.Status not in ("Cancelled","Closed") and SO.pickup_slot = %(pickup_slot)s""",
		{"pickup_slot": pickup_slot}, as_dict=True)

	default_print_format = frappe.get_value('Property Setter', 'Sales Order-default_print_format', 'value') or 'Standard'

	return [orders,default_print_format]