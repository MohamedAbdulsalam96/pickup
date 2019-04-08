// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

erpnext.taxes_and_totals.prototype.calculate_outstanding_amount = function(update_paid_amount) {
	// NOTE:
	// paid_amount and write_off_amount is only for POS Invoice
	// total_advance is only for non POS Invoice

	if(this.frm.doc.doctype == "Sales Invoice" && this.frm.doc.is_return){
		this.calculate_paid_amount();
	}

	if(this.frm.doc.is_return || this.frm.doc.docstatus > 0) return;

	frappe.model.round_floats_in(this.frm.doc, ["grand_total", "total_advance", "write_off_amount"]);

	if(in_list(["Sales Invoice", "Purchase Invoice"], this.frm.doc.doctype)) {
		var grand_total = this.frm.doc.rounded_total || this.frm.doc.grand_total;

		if(this.frm.doc.party_account_currency == this.frm.doc.currency) {
			var total_amount_to_pay = flt((grand_total - this.frm.doc.total_advance
				- this.frm.doc.write_off_amount + this.frm.doc.balance_amount), precision("grand_total"));
		} else {
			var total_amount_to_pay = flt(
				(flt(grand_total*this.frm.doc.conversion_rate, precision("grand_total"))
					- this.frm.doc.total_advance - this.frm.doc.base_write_off_amount)
					+ this.frm.doc.balance_amount, precision("base_grand_total")
			);
		}

		frappe.model.round_floats_in(this.frm.doc, ["paid_amount"]);
		this.set_in_company_currency(this.frm.doc, ["paid_amount"]);

		if(this.frm.refresh_field){
			this.frm.refresh_field("paid_amount");
			this.frm.refresh_field("base_paid_amount");
		}

		if(this.frm.doc.doctype == "Sales Invoice") {
			this.set_default_payment(total_amount_to_pay, update_paid_amount);
			this.calculate_paid_amount();
		}
		this.calculate_change_amount();

		var paid_amount = (this.frm.doc.party_account_currency == this.frm.doc.currency) ?
			this.frm.doc.paid_amount : this.frm.doc.base_paid_amount;

		this.frm.doc.outstanding_amount =  flt(total_amount_to_pay - flt(paid_amount) +
			flt(this.frm.doc.change_amount * this.frm.doc.conversion_rate), precision("outstanding_amount"));
	}
}

erpnext.taxes_and_totals.prototype.calculate_change_amount = function(){
	this.frm.doc.change_amount = 0.0;
	this.frm.doc.base_change_amount = 0.0;
	if(this.frm.doc.doctype == "Sales Invoice"
		&& this.frm.doc.paid_amount > (this.frm.doc.grand_total + this.frm.doc.balance_amount)
		&& !this.frm.doc.is_return) {

		var payment_types = $.map(this.frm.doc.payments, function(d) { return d.type; });
		if (in_list(payment_types, 'Cash')) {
			var grand_total = this.frm.doc.rounded_total || this.frm.doc.grand_total;
			var base_grand_total = this.frm.doc.base_rounded_total || this.frm.doc.base_grand_total;

			this.frm.doc.change_amount = flt(this.frm.doc.paid_amount - grand_total +
				this.frm.doc.write_off_amount - this.frm.doc.balance_amount, precision("change_amount"));

			this.frm.doc.base_change_amount = flt(this.frm.doc.base_paid_amount -
				base_grand_total + this.frm.doc.base_write_off_amount -	this.frm.doc.balance_amount,
				precision("base_change_amount"));
		}
	}
}

erpnext.taxes_and_totals.prototype.calculate_write_off_amount = function(){
	if(this.frm.doc.paid_amount > this.frm.doc.grand_total){
		this.frm.doc.write_off_amount = flt(this.frm.doc.grand_total - this.frm.doc.paid_amount
			+ this.frm.doc.change_amount + this.frm.doc.balance_amount, precision("write_off_amount"));

		this.frm.doc.base_write_off_amount = flt(this.frm.doc.write_off_amount * this.frm.doc.conversion_rate,
			precision("base_write_off_amount"));
	}else{
		this.frm.doc.paid_amount = 0.0;
	}
	this.calculate_outstanding_amount(false);
}

