import frappe


def execute():
	if frappe.db.exists("Number Card", "NOT REPORTED INVOICES") and not frappe.db.exists(
		"Number Card", "FAILED REPORTED INVOICES"
	):
		frappe.rename_doc(
			"Number Card",
			"NOT REPORTED INVOICES",
			"FAILED REPORTED INVOICES",
			force=True,
			merge=True,
		)
