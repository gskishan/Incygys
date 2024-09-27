import frappe
from erpnext.crm.doctype.opportunity.opportunity import Opportunity

def duplicate_check(doc, method):
    if (doc.is_new()):
        sql = """SELECT
        custom_mobiles, name,
        custom_owner_name
        FROM
        `tabLead`
        WHERE
        custom_mobiles = "{0}" """.format(doc.custom_mobiles)
        data = frappe.db.sql(sql, as_dict=True)

        email_sql = """SELECT * FROM `tabLead` WHERE custom_emails = "{0}" """.format(doc.custom_emails)
        email_data = frappe.db.sql(email_sql, as_dict=True)
        # frappe.errprint(sql)
        # frappe.errprint(email_sql)

        if data:
            frappe.errprint(data)
            frappe.throw("Duplicate mobile number {0} already linked to <b>{1}</b>".format(data[0].custom_mobiles,data[0].custom_owner_name))
        if email_data:
            frappe.errprint(email_data)
            frappe.throw(f"Duplicate email <b>{doc.custom_emails}</b> already linked to <b>{email_data[0].custom_owner_name}</b>")
