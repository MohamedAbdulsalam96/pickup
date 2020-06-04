# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from erpnext.setup.doctype.item_group.item_group import ItemGroup, get_child_groups_for_list_in_html, get_child_groups,\
	get_parent_item_groups, adjust_qty_for_expired_items, get_item_for_list_in_html
from frappe.utils import nowdate, cint, cstr
from frappe.website.doctype.website_slideshow.website_slideshow import get_slideshow
from erpnext.shopping_cart.product_info import set_product_info_for_website

@frappe.whitelist(allow_guest=True)
def get_product_list_for_group(product_group=None, start=0, limit=10, search=None, pickup_slot=None):

	child_groups = ", ".join(['"' + frappe.db.escape(i[0]) + '"' for i in get_child_groups(product_group)])

	pickup_groups = frappe.db.sql("""select item_group from `tabPickup Slot Group` where parent = %s""",
		pickup_slot, as_dict=True)

	pickup_child_groups = ""
	for pickup_group in pickup_groups:
		if pickup_child_groups != "":
			pickup_child_groups += ", "
		pickup_child_groups += ", ".join(['"' + frappe.db.escape(i[0]) + '"' for i in get_child_groups(pickup_group.item_group)])

	# base query
	query = """select I.name, I.item_name, I.item_code, I.route, I.image, I.website_image, I.thumbnail, I.item_group,
			I.description, I.web_long_description as website_description, I.is_stock_item,
			case when (S.actual_qty - S.reserved_qty) > 0 then 1 else 0 end as in_stock, I.website_warehouse,
			I.has_batch_no
		from `tabItem` I
		left join tabBin S on I.item_code = S.item_code and I.website_warehouse = S.warehouse
		where I.show_in_website = 1
			and I.disabled = 0
			and (I.end_of_life is null or I.end_of_life='0000-00-00' or I.end_of_life > %(today)s)
			and (I.variant_of = '' or I.variant_of is null)
			and (I.item_group in ({child_groups})
			or I.name in (select parent from `tabWebsite Item Group` where item_group in ({child_groups})))
			and (I.item_group in ({pickup_child_groups})
			or I.name in (select item_code from `tabPickup Slot Item` where parent = "{pickup_slot}")
			or (not exists (select * from `tabPickup Slot Group` where parent = "{pickup_slot}")
			and not exists (select * from `tabPickup Slot Item` where parent = "{pickup_slot}")))
			""".format(child_groups=child_groups, pickup_child_groups=pickup_child_groups, pickup_slot=pickup_slot)

	# search term condition
	if search:
		query += """ and (I.web_long_description like %(search)s
				or I.item_name like %(search)s
				or I.name like %(search)s)"""
		search = "%" + cstr(search) + "%"

	query += """order by I.weightage desc, in_stock desc, I.modified desc limit %s, %s""" % (start, limit)

	data = frappe.db.sql(query, {"product_group": product_group,"search": search, "today": nowdate()}, as_dict=1)
	data = adjust_qty_for_expired_items(data)

	if cint(frappe.db.get_single_value("Shopping Cart Settings", "enabled")):
		for item in data:
			set_product_info_for_website(item)

	return [get_item_for_list_in_html(r) for r in data]

def get_context(self, context):
	context.show_search = True
	context.page_length = cint(frappe.db.get_single_value('Products Settings', 'products_per_page')) or 6
	context.search_link = '/product_search'

	start = int(frappe.form_dict.start or 0)
	if start < 0:
		start = 0
	context.update({
		"items": get_product_list_for_group(product_group=self.name, start=start, pickup_slot=frappe.form_dict.creneau,
											limit=context.page_length + 1, search=frappe.form_dict.get("search")),
		"parents": get_parent_item_groups(self.parent_item_group),
		"title": self.name,
		"products_as_list": cint(frappe.db.get_single_value('Products Settings', 'products_as_list'))
	})

	if self.slideshow:
		context.update(get_slideshow(self))

	return context

def item_group_override():
	ItemGroup.get_context = get_context
