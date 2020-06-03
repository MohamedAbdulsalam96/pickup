# -*- coding: utf-8 -*-
# Copyright (c) 2020, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from pickup.templates.pages.cart import get_pickup_slots
from frappe.contacts.doctype.address.address import get_address_display

def get_context(context):
	context.update({
		"pickup_slots": get_pickup_slots_with_address()
	})

def get_pickup_slots_with_address():
	pickup_slots = get_pickup_slots()

	for slot in pickup_slots:
		address = frappe.get_doc('Address', slot.address_name)
		slot["pickup_address"] = get_address_display(address.as_dict())

	return pickup_slots