# -*- coding: utf-8 -*-
# Copyright (c) 2018, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime
from frappe import _
from frappe.contacts.address_and_contact import load_address_and_contact

class PickupPoint(Document):
	def on_update(self):
		create_pickup_slots()

	def onload(self):
		load_address_and_contact(self)

def create_pickup_slots():
	"""
		Automatically create pickup slots
	"""
	weekdays = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

	# Returns the dates of the given range
	daterange = lambda d1, d2: (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))

	pickup_points = frappe.db.sql("""select name, holiday_list, rolling_day_period
			from `tabPickup Point`
			where automatic_slot_creation = 1 and disabled = 0 
			""", as_dict=True)

	if pickup_points:

		slots = []
		for point in pickup_points:
			# Holiday List
			holiday_dates = frappe.get_all('Holiday', filters={'parent': point.holiday_list}, fields=['holiday_date'])

			schedule = frappe.get_all('Pickup Schedule', filters={'parent': point.name}, fields=['day','start_time','end_time'])
			for timeslot in schedule:
				dt1 = datetime.datetime.now().date()
				dt2 = dt1 + datetime.timedelta(days=point.rolling_day_period)

				for d in daterange(dt1, dt2):
					if d.weekday() == weekdays[timeslot.day]:
						# This date is the timeslot week day
						# Check if this date is not a holiday
						is_holiday = False
						for holiday_date in holiday_dates:
							if d in holiday_date.values():
								is_holiday = True
								break

						if not is_holiday:
							# Add slot in the list
							slot = {"point": point.name, "date": d, "start_time": timeslot.start_time,
									"end_time": timeslot.end_time}
							slots.append(slot)

		for slot in slots:
			if not frappe.db.get_value("Pickup Slot",
					{"pickup_point": slot["point"], "date": slot["date"], "start_time": slot["start_time"], "end_time": slot["end_time"]}):
				frappe.get_doc({
					"doctype": "Pickup Slot",
					"pickup_point": slot["point"],
					"date": slot["date"],
					"start_time": slot["start_time"],
					"end_time": slot["end_time"],
					"reference": _("Automatically created")
				}).insert(ignore_permissions=True)
