import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache


def execute():
	"""Point the ZATCA desk icon to the Zatca dashboard route."""
	app_title = frappe.get_hooks("app_title", app_name="zatca_integration")[0]
	route = frappe.get_hooks("app_home", app_name="zatca_integration")[0]

	if not frappe.db.exists("Desktop Icon", app_title):
		return

	frappe.db.set_value(
		"Desktop Icon",
		app_title,
		{"link": route, "link_type": "External"},
		update_modified=False,
	)

	frappe.db.delete("Desktop Layout")
	clear_desktop_icons_cache()
	frappe.cache.delete_key("bootinfo")
	frappe.clear_cache()
