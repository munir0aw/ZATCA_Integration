# Copyright (c) 2024, Shakir PM and contributors
# For license information, please see license.txt

import frappe

TAX_TYPES = ("Standard Rate", "Except Rate", "Zero Rate")


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = []

    append_heading("Sales Invoices and VAT", data)
    append_tax_type_rows(data, get_invoice_totals("Sales Invoice", filters))

    append_heading("Purchase Invoices and VAT", data)
    append_tax_type_rows(data, get_invoice_totals("Purchase Invoice", filters))

    return columns, data


def get_invoice_totals(doctype, filters):
    if doctype == "Sales Invoice":
        invoice_table = "tabSales Invoice"
        template_table = "tabSales Taxes and Charges Template"
    else:
        invoice_table = "tabPurchase Invoice"
        template_table = "tabPurchase Taxes and Charges Template"

    return frappe.db.sql(
        f"""
        SELECT
            stct.custom_tax_type,
            si.is_return,
            SUM(si.base_total) AS base_total,
            SUM(si.base_total_taxes_and_charges) AS base_total_taxes_and_charges,
            SUM(si.base_grand_total) AS base_grand_total
        FROM `{invoice_table}` si
        LEFT JOIN `{template_table}` stct ON stct.name = si.taxes_and_charges
        WHERE
            si.docstatus = 1
            AND si.company = %(company)s
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY stct.custom_tax_type, si.is_return
        """,
        {
            "company": filters.get("company"),
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
        },
        as_dict=True,
    )


def append_tax_type_rows(data, invoices):
    for tax_type in TAX_TYPES:
        collected = get_tax_sum(
            [
                row
                for row in invoices
                if row.get("custom_tax_type") == tax_type and not row.get("is_return")
            ]
        )
        credited = get_tax_sum(
            [
                row
                for row in invoices
                if row.get("custom_tax_type") == tax_type and row.get("is_return")
            ]
        )
        append_data(tax_type, data, collected, credited)


def get_tax_sum(rows):
    return {
        "base_total_sum": sum(row.get("base_total") or 0 for row in rows),
        "base_total_taxes_and_charges_sum": sum(
            row.get("base_total_taxes_and_charges") or 0 for row in rows
        ),
        "base_grand_total_sum": sum(row.get("base_grand_total") or 0 for row in rows),
    }


def append_data(title, data, sales_sum, crdit_sum):
    data.append(
        {
            "title": title,
            "sales_collected": sales_sum["base_total_sum"],
            "sales_credited": crdit_sum["base_total_sum"],
            "sales_total": sales_sum["base_total_sum"] + crdit_sum["base_total_sum"],
            "vat_collected": sales_sum["base_total_taxes_and_charges_sum"],
            "vat_credited": crdit_sum["base_total_taxes_and_charges_sum"],
            "vat_total": sales_sum["base_total_taxes_and_charges_sum"]
            + crdit_sum["base_total_taxes_and_charges_sum"],
        }
    )


def append_heading(title, data):
    data.append(
        {
            "title": title,
            "sales_collected": "",
            "sales_credited": "",
            "sales_total": "",
            "vat_collected": "",
            "vat_credited": "",
            "vat_total": "",
        }
    )


def get_columns():
    return [
        {"fieldname": "title", "label": ("Title"), "fieldtype": "Data", "width": 200},
        {
            "fieldname": "sales_collected",
            "label": ("Sales Collected (SAR)"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "sales_credited",
            "label": ("Sales Credited (SAR)"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "sales_total",
            "label": ("Total Sales (SAR)"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "vat_collected",
            "label": ("VAT Collected (SAR)"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "vat_credited",
            "label": ("VAT Credited (SAR)"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "vat_total",
            "label": ("Total VAT (SAR)"),
            "fieldtype": "Currency",
        },
    ]
