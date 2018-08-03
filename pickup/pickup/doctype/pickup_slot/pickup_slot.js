// Copyright (c) 2018, Britlog and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pickup Slot', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on("Pickup Slot", "export_sales_orders", function(frm,cdt,cdn) {
    var doc = frappe.get_doc(cdt, cdn);
//    frappe.msgprint(frm.doc.name);

	//	Get sales orders
	frappe.call({
        method: "pickup.pickup.doctype.pickup_slot.pickup_slot.get_sales_orders",
        args: {
            "pickup_slot": frm.doc.name
        },
        callback: function(r) {
            //console.log(r.message);

        	var orders_no = "";
            (r.message[0] || []).forEach(function(row){
            	// Format : ["CC-00033","CC-00032"]
            	//console.log(row.name);
            	if (orders_no) {
            		orders_no += "%2C"
            	}
                orders_no += '%22' + row.name + '%22';

            });
            //console.log(orders_no);
            if (!orders_no) {
            	frappe.msgprint(__('No orders')); return;
            }

            var print_format = encodeURIComponent(r.message[1]);
            //console.log(print_format);

            var w = window.open('/api/method/frappe.utils.print_format.download_multi_pdf?doctype=Sales%20Order&name=%5B'+orders_no+'%5D&format='+print_format+'&no_letterhead=1');
        	if (!w) {
				frappe.msgprint(__('Please enable pop-ups')); return;
			}
        }
    });

});