# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from frappe.utils import flt
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals

def calculate_change_amount(self):
	self.doc.change_amount = 0.0
	self.doc.base_change_amount = 0.0

	if self.doc.doctype == "Sales Invoice" \
			and self.doc.paid_amount > (self.doc.grand_total + self.doc.balance_amount) and not self.doc.is_return \
			and any([d.type == "Cash" for d in self.doc.payments]):
		grand_total = self.doc.rounded_total or self.doc.grand_total
		base_grand_total = self.doc.base_rounded_total or self.doc.base_grand_total

		self.doc.change_amount = flt(self.doc.paid_amount - grand_total +
									 self.doc.write_off_amount
									 - self.doc.balance_amount, self.doc.precision("change_amount"))

		self.doc.base_change_amount = flt(self.doc.base_paid_amount - base_grand_total +
										  self.doc.base_write_off_amount
										  - self.doc.balance_amount, self.doc.precision("base_change_amount"))

def calculate_write_off_amount(self):
	if flt(self.doc.change_amount) > 0:
		self.doc.write_off_amount = flt(self.doc.grand_total - self.doc.paid_amount
										+ self.doc.change_amount
										+ self.doc.balance_amount, self.doc.precision("write_off_amount"))
		self.doc.base_write_off_amount = flt(self.doc.write_off_amount * self.doc.conversion_rate,
											 self.doc.precision("base_write_off_amount"))

def taxes_and_totals_override(doctype, event_name):
	calculate_taxes_and_totals.calculate_change_amount = calculate_change_amount
	calculate_taxes_and_totals.calculate_write_off_amount = calculate_write_off_amount