import frappe

WORKSPACE_NAME = "ZATCA Integrations"
MODULE_NAME = "Saudi Arabia Electronic Invoicing"


def sync_zatca_desk():
    """Ensure ZATCA workspace and v16 desktop icons are available on the desk."""
    if not frappe.db.exists("Workspace", WORKSPACE_NAME):
        import_workspace_fixture()

    if frappe.db.exists("Workspace", WORKSPACE_NAME):
        frappe.db.set_value(
            "Workspace",
            WORKSPACE_NAME,
            {
                "module": MODULE_NAME,
                "app": "zatca_integration",
                "public": 1,
                "is_hidden": 0,
                "type": "Workspace",
            },
            update_modified=False,
        )


def import_workspace_fixture():
    import os

    from frappe.modules.import_file import import_file_by_path

    fixture_path = os.path.join(
        frappe.get_app_path("zatca_integration"),
        "fixtures",
        "workspace.json",
    )
    if os.path.exists(fixture_path):
        import_file_by_path(fixture_path, force=True, ignore_version=True)

    from frappe.utils.install import auto_generate_icons_and_sidebar

    auto_generate_icons_and_sidebar()
    frappe.clear_cache()
