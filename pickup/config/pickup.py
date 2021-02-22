from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Slots"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Pickup Point",
					"description": _("Pickup Points."),
				},
				{
					"type": "doctype",
					"name": "Pickup Slot",
					"description": _("Pickup Slots."),
				}
			]
		},
		{
			"label": _("Reports"),
			"icon": "fa fa-list",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Order Form"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Label Printing"
				}
			]
		},
		{
			"label": _("Setup"),
			"icon": "fa fa-cog",
			"items": [
			]
		},
	]
