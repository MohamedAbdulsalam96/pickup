// Copyright (c) 2018, Britlog and contributors
// For license information, please see license.txt

erpnext.pos.PointOfSale = erpnext.pos.PointOfSale.extend({

	make_customer: function (wrapper) {
		this._super(wrapper);
		this.list_customers_btn = this.page.wrapper.find('.list-customers-btn');
		this.list_customers_btn.after($('<button class="btn btn-default get-orders-btn" style="margin-left: 12px"><i class="octicon octicon-gift"></i></button>'));
		this.get_customer_orders();
	},

	get_customer_orders: function (wrapper) {
		var me = this;
		this.get_orders_btn = this.page.wrapper.find('.get-orders-btn');

		this.page.wrapper.on('click', '.get-orders-btn', function(wrapper) {
			me.customer_validate();

			frappe.call({
				method: 'pickup.pickup.doctype.pickup_slot.pickup_slot.get_items_from_sales_order',
				args: {
					'customer': me.frm.doc.customer,
					'pickup_slot': me.pos_profile_data.pickup_slot
				},
				callback: function(r) {
					//console.log(r.message);

					(r.message || []).forEach(function(row){
						me.items = me.get_items(row.item_code)
						me.add_to_cart();
						if (row.qty != 1) {
							me.update_qty(row.item_code, row.qty);
						}
					})
				}
			})
		})
	},
})