import frappe


def execute():
	old_name = "NOT REPORTED INVOICES"
	new_name = "FAILED REPORTED INVOICES"

	if not frappe.db.exists("Number Card", old_name):
		return

	if frappe.db.exists("Number Card", new_name):
		frappe.delete_doc("Number Card", old_name, force=True)
		return

	frappe.rename_doc("Number Card", old_name, new_name, force=True)
