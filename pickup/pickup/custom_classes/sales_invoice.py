# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.accounts.utils import get_account_currency

def make_pos_bank_entry(self):

	if self.is_pos:
		for payment_mode in self.payments:
			if payment_mode.amount:
				# POS, make journal entries
				je = frappe.new_doc("Journal Entry")
				je.posting_date = self.posting_date
				je.voucher_type = 'Bank Entry'
				je.company = self.company
				je.cheque_no = self.name
				je.cheque_date = self.posting_date

				je.append("accounts", {
					"account": self.debit_to,
					"credit_in_account_currency": payment_mode.base_amount \
						if self.party_account_currency == self.company_currency \
						else payment_mode.amount,
					"party_type": "Customer",
					"party": self.customer,
					"is_advance": "No"
				})

				payment_mode_account_currency = get_account_currency(payment_mode.account)
				je.append("accounts", {
					"account": payment_mode.account,
					"debit_in_account_currency": payment_mode.base_amount \
						if payment_mode_account_currency == self.company_currency \
						else payment_mode.amount,
					"account_currency": payment_mode_account_currency
				})

				je.flags.ignore_permissions = True
				je.submit()


def get_gl_entries(self, warehouse_account=None):
	from erpnext.accounts.general_ledger import merge_similar_entries

	gl_entries = []

	self.make_customer_gl_entry(gl_entries)

	self.make_tax_gl_entries(gl_entries)

	self.make_item_gl_entries(gl_entries)

	# merge gl entries before adding pos entries
	gl_entries = merge_similar_entries(gl_entries)

	if self.balance_amount > 0:
		make_pos_bank_entry(self)
	else:
		self.make_pos_gl_entries(gl_entries)

	self.make_gle_for_change_amount(gl_entries)

	self.make_write_off_gl_entry(gl_entries)
	self.make_gle_for_rounding_adjustment(gl_entries)

	return gl_entries


def sales_invoice_override(doctype, event_name):
	SalesInvoice.get_gl_entries = get_gl_entries
