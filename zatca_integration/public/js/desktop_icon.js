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
