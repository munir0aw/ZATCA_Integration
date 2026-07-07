// Fix Frappe v16 Desktop Icon quick entry save when editing from the desk.
// Boot icon data does not include `doctype`, which causes frappe.client.save to fail.
frappe.ui.form.DesktopIconQuickEntryForm = class DesktopIconQuickEntryForm extends (
    frappe.ui.form.QuickEntryForm
) {
    check_quick_entry_doc() {
        if (!this.doc) {
            this.doc = frappe.model.get_new_doc(this.doctype, null, null, true);
        } else if (!this.doc.doctype) {
            this.doc.doctype = this.doctype;
        }
    }

    update_doc() {
        this.doc.doctype = this.doctype;
        return super.update_doc();
    }
};

const ZATCA_APP_ROUTE = ["dashboard-view", "Zatca"];

function bind_zatca_desktop_navigation() {
    frappe.desktop_icons_objects?.forEach((icon_obj) => {
        if (icon_obj.icon_data?.app !== "zatca_integration" || icon_obj.icon_type !== "App") {
            return;
        }

        const $icon = $(icon_obj.icon);
        $icon.removeAttr("target");

        if (icon_obj.child_icons?.length) {
            return;
        }

        $icon.off("click.zatca_nav").on("click.zatca_nav", function (event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            frappe.set_route(...ZATCA_APP_ROUTE);
        });
    });
}

frappe.pages.on_page_load("desktop", () => {
    bind_zatca_desktop_navigation();

    const desktop_page = frappe.pages.desktop?.desktop_page;
    if (!desktop_page || desktop_page._zatca_nav_patched) {
        return;
    }

    desktop_page._zatca_nav_patched = true;
    const update = desktop_page.update.bind(desktop_page);
    desktop_page.update = function (...args) {
        const result = update(...args);
        bind_zatca_desktop_navigation();
        return result;
    };
});
