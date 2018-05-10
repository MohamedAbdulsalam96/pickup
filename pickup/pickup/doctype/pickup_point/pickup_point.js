// Copyright (c) 2018, Britlog and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pickup Point', {
	refresh: function(frm) {

        frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Pickup Point'};

		frm.toggle_display(['address_html'], !frm.doc.__islocal);

        if(!frm.doc.__islocal) {
 			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}
	}
});
