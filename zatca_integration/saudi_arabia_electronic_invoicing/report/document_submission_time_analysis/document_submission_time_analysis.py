# Copyright (c) 2025, Shakir PM and contributors
# For license information, please see license.txt

import frappe


# Report Script (Python)
def execute(filters=None):
    result = frappe.db.sql(
        """
	SELECT
		MIN(`zatca_elapsed_time`) as min_time,
		MAX(`zatca_elapsed_time`) as max_time,
		AVG(`zatca_elapsed_time`) as avg_time
	FROM `tabZatca Transactions`
	WHERE `zatca_elapsed_time` IS NOT NULL
	""",
        as_dict=True,
    )

    row = result[0] if result else {}

    data = [
        ["Min Time", row.get("min_time") or 0],
        ["Max Time", row.get("max_time") or 0],
        ["Avg Time", round(row["avg_time"], 2) if row.get("avg_time") is not None else 0],
    ]

    columns = ["Metric", "Value"]
    return columns, data
