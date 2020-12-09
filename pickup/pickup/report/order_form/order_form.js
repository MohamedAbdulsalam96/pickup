// Copyright (c) 2016, Britlog and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Order Form"] = {
	"filters": [
        {
            "fieldname":"pickup_slot",
            "label": __("Pickup Slot"),
            "fieldtype": "Link",
            "options": "Pickup Slot",
            "reqd": 1,
            "get_query": function() {
				return {
					filters: {
						'date': [">=", frappe.datetime.get_today()]
					}
				};
			}
        },
        {
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 0,
            "get_query": function() {
				return {
					filters: {
						'disabled': ["=", 0]
					}
				};
			}
        }
	]
}
