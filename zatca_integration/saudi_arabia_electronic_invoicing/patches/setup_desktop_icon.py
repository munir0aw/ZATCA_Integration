import frappe


def execute():
	"""Ensure the ZATCA app desktop icon is configured for Frappe v16."""
	app_title = frappe.get_hooks("app_title", app_name="zatca_integration")[0]
	app_details = frappe.get_hooks("add_to_apps_screen", app_name="zatca_integration")
	if not app_details:
		return

	route = app_details[0].get("route")
	logo = app_details[0].get("logo")

	if frappe.db.exists("Desktop Icon", app_title):
		icon = frappe.get_doc("Desktop Icon", app_title)
	else:
		icon = frappe.new_doc("Desktop Icon")
		icon.label = app_title

	icon.update(
		{
			"icon_type": "App",
			"link_type": "External",
			"app": "zatca_integration",
			"link": route,
			"logo_url": logo,
			"icon_image": None,
			"standard": 1,
			"hidden": 0,
		}
	)
	icon.save(ignore_permissions=True)
	frappe.clear_cache()
