import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import clear_desktop_icons_cache


def execute():
	"""Refresh desk icon/logo after assets were updated."""
	app_title = frappe.get_hooks("app_title", app_name="zatca_integration")[0]
	app_details = frappe.get_hooks("add_to_apps_screen", app_name="zatca_integration")
	if not app_details:
		return

	logo = app_details[0].get("logo")
	route = app_details[0].get("route")

	if not frappe.db.exists("Desktop Icon", app_title):
		return

	frappe.db.set_value(
		"Desktop Icon",
		app_title,
		{
			"icon_type": "App",
			"link_type": "External",
			"app": "zatca_integration",
			"link": route,
			"logo_url": logo,
			"icon_image": None,
			"standard": 1,
			"hidden": 0,
			"bg_color": "gray",
		},
		update_modified=False,
	)

	frappe.db.delete("Desktop Layout")
	clear_desktop_icons_cache()
	frappe.cache.delete_key("bootinfo")
	frappe.clear_cache()
