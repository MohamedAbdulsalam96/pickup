# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

import frappe
from frappe.utils import cint
from frappe.contacts.doctype.address.address import get_address_display
from erpnext.shopping_cart.cart import _get_cart_quotation

def get_context(context):
	context.update({
		"pickup_slots": get_pickup_slots(),
		"shipping_addresses": get_pickup_addresses()
	})

def get_pickup_slots():
	return frappe.db.sql("""
			select PS.name, PS.pickup_point, DL.parent AS address_name, 
				IFNULL(PS.practical_information,'') AS practical_information
			from `tabPickup Slot` PS
			inner join `tabPickup Point` PP on PS.pickup_point = PP.name
			inner join `tabDynamic Link` DL on PP.name = DL.link_name and DL.link_doctype = 'Pickup Point'
			where PS.show_in_website = 1
				and DATE_ADD(NOW(), INTERVAL PP.preparation_time HOUR) < TIMESTAMP(PS.date,PS.start_time)
			order by PS.date ASC, PS.start_time ASC""",as_dict=True)

def get_pickup_addresses(doctype=None, txt=None, filters=None, limit_start=0, limit_page_length=20,
	party=None):

	address_names = frappe.db.get_all('Dynamic Link', fields=('parent'),
		filters=dict(parenttype='Address', link_doctype='Pickup Point'))

	out = []

	for a in address_names:
		address = frappe.get_doc('Address', a.parent)
		address.display = get_address_display(address.as_dict())
		out.append(address)

	return out

@frappe.whitelist(allow_guest=True)
def set_pickup_slot(slot_name, cart_count):

	# delete actual quotation because items depend on slot
	if int(cart_count) > 0:
		quotation = _get_cart_quotation()
		quotation.delete()
		frappe.local.cookie_manager.set_cookie("cart_count", 0)

	# set cookie for website
	if cint(frappe.db.get_singles_value("Shopping Cart Settings", "enabled")):
		if hasattr(frappe.local, "cookie_manager"):
			frappe.local.cookie_manager.set_cookie("pickup_slot", slot_name)

	return True

def clear_pickup_slot():
	frappe.local.cookie_manager.delete_cookie("pickup_slot")

@frappe.whitelist()
def update_quotation_pickup_slot(slot_name, address_name):

	quotation = _get_cart_quotation()

	if address_name:
		# update pickup slot
		quotation.pickup_slot = slot_name

		# update pickup address
		address_display = get_address_display(frappe.get_doc("Address", address_name).as_dict())
		quotation.shipping_address_name = address_name
		quotation.shipping_address = address_display
	else:
		quotation.pickup_slot = ""
		quotation.shipping_address_name = ""
		quotation.shipping_address = ""

	# save
	quotation.flags.ignore_permissions = True
	quotation.save()

	return True