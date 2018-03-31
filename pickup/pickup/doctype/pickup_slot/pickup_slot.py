# -*- coding: utf-8 -*-
# Copyright (c) 2018, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PickupSlot(Document):

	def autoname(self):

		abbrev = frappe.get_value('Pickup Point', self.pickup_point, 'abbr')

		self.name = frappe.utils.formatdate(self.date, "EEEE dd/MM/yyyy").capitalize() + " " + \
					frappe.utils.format_datetime(frappe.utils.format_time(self.start_time), "HH:mm") + "-" + \
					frappe.utils.format_datetime(frappe.utils.format_time(self.end_time), "HH:mm") + \
					" - " + abbrev


@frappe.whitelist(allow_guest=True)
def get_items_from_sales_order(customer, pickup_slot):
	return frappe.db.sql("""
		select SOI.item_code, SOI.qty
		from `tabSales Order` SO
		inner join `tabSales Order Item` SOI on SO.name = SOI.parent
		where SO.customer = %(customer)s and SO.pickup_slot = %(pickup_slot)s
		order by SOI.idx""",
		{"customer": customer, "pickup_slot": pickup_slot}, as_dict=True)