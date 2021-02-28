// Copyright (c) 2021, Britlog and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Label Printing"] = {
	"filters": [
		{
            "fieldname":"item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options": "Item Group",
            "reqd": 0
        },
		{
            "fieldname":"item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0,
            "get_query": function() {
				return {
					filters: {
						'disabled': ["=", 0]
					}
				};
			}
        },
        {
            "fieldname":"item_creation_date",
            "label": "Article Créé depuis",
            "fieldtype": "Date",
            "options": "",
            "reqd": 0
        },
        {
            "fieldname":"item_price_date",
            "label": "Prix Mis à Jour depuis",
            "fieldtype": "Date",
            "options": "",
            "reqd": 0
        }
	]
}
