// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// new function
erpnext.payments.prototype.balance_amount = function(balance_amount) {
	var me = this;

	this.frm.doc.balance_amount = flt(balance_amount, precision("balance_amount"));
	this.calculate_outstanding_amount(false)
	this.show_amounts()
}

erpnext.payments.prototype.get_customer_balance = function(customer) {
	var me = this;

	frappe.call({
		method: 'pickup.pickup.custom_classes.pos.get_customer_balance',
		args: {
			'customer': customer
		},
		callback: function(r) {
//			console.log(r.message);

			var balance = flt(r.message);
			if (balance > 0)
				$(me.$body).find('#customer-balance-label').text(__("Solde (Dû)"));
			else
				$(me.$body).find('#customer-balance-label').text(__("Solde (Avoir)"));

			$(me.$body).find('#customer-balance').text(format_currency(balance, me.frm.doc.currency)).val(balance);
		}
	})
}

// override functions
erpnext.payments.prototype.show_payment_details = function(){
	var me = this;
	var multimode_payments = $(this.$body).find('.multimode-payments').empty();
	if(this.frm.doc.payments.length){
		$.each(this.frm.doc.payments, function(index, data){
			$(frappe.render_template('payment_details', {
				mode_of_payment: data.mode_of_payment,
				amount: data.amount,
				idx: data.idx,
				currency: me.frm.doc.currency,
				type: data.type
			})).appendTo(multimode_payments)

			if (data.type == 'Cash' && data.amount == me.frm.doc.paid_amount) {
				me.idx = data.idx;
				me.selected_mode = $(me.$body).find(repl("input[idx='%(idx)s']",{'idx': me.idx}));
				me.highlight_selected_row();
				me.bind_amount_change_event();
			}
		})
	}else{
		$("<p>No payment mode selected in pos profile</p>").appendTo(multimode_payments)
	}

	//Get customer balance value
	me.get_customer_balance(me.frm.doc.customer);

}

erpnext.payments.prototype.set_outstanding_amount = function(){
	this.selected_mode = $(this.$body).find(repl("input[idx='%(idx)s']",{'idx': this.idx}));
	this.highlight_selected_row()
	this.payment_val = 0.0
	if(this.frm.doc.outstanding_amount > 0 && flt(this.selected_mode.val()) == 0.0){
		//When user first time click on row
		this.payment_val = flt(this.frm.doc.outstanding_amount / this.frm.doc.conversion_rate, precision("outstanding_amount"))

		if(this.idx == 'balance_amount'){
			this.selected_mode.val(format_currency($(this.$body).find('#customer-balance').val(), this.frm.doc.currency));
		}else{
			this.selected_mode.val(format_currency(this.payment_val, this.frm.doc.currency));
			this.update_payment_amount();
		}

	}else if(flt(this.selected_mode.val()) > 0){
		//If user click on existing row which has value
		this.payment_val = flt(this.selected_mode.val());
	}
	this.selected_mode.select()
	this.bind_amount_change_event();
}
	
erpnext.payments.prototype.bind_form_control_event = function(){
	var me = this;
	$(this.$body).find('.pos-payment-row').click(function(){
		me.idx = $(this).attr("idx");
		me.set_outstanding_amount()
	})

	$(this.$body).find('.form-control').click(function(){
		me.idx = $(this).attr("idx");
		me.set_outstanding_amount();
		me.update_paid_amount(true);
	})

	$(this.$body).find('.write_off_amount').change(function(){
		me.write_off_amount(flt($(this).val()), precision("write_off_amount"));
	})

	$(this.$body).find('.change_amount').change(function(){
		me.change_amount(flt($(this).val()), precision("change_amount"));
	})

	$(this.$body).find('.balance_amount').change(function(){
		me.balance_amount(flt($(this).val()), precision("balance_amount"));
	})
}

erpnext.payments.prototype.update_paid_amount = function(update_write_off) {
	var me = this;
	if(in_list(['change_amount', 'write_off_amount', 'balance_amount'], this.idx)){
		var value = me.selected_mode.val();
		if(me.idx == 'change_amount'){
			me.change_amount(value)
		} else if(me.idx == 'write_off_amount'){
			if(flt(value) == 0 && update_write_off && me.frm.doc.outstanding_amount > 0) {
				value = flt(me.frm.doc.outstanding_amount / me.frm.doc.conversion_rate, precision(me.idx));
			}
			me.write_off_amount(value)
		} else {
			me.balance_amount(value)
		}
	}else{
		this.update_payment_amount()
	}
}

erpnext.payments.prototype.show_amounts = function(){
	var me = this;
	$(this.$body).find(".write_off_amount").val(format_currency(this.frm.doc.write_off_amount, this.frm.doc.currency));
	$(this.$body).find('.paid_amount').text(format_currency(this.frm.doc.paid_amount, this.frm.doc.currency));
	$(this.$body).find('.change_amount').val(format_currency(this.frm.doc.change_amount, this.frm.doc.currency))
	$(this.$body).find('.outstanding_amount').text(format_currency(this.frm.doc.outstanding_amount, frappe.get_doc(":Company", this.frm.doc.company).default_currency))
	$(this.$body).find(".balance_amount").val(format_currency(this.frm.doc.balance_amount, this.frm.doc.currency));
	this.update_invoice();
}