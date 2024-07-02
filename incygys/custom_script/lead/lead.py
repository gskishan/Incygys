import frappe
from frappe import _
from erpnext.crm.doctype.opportunity.opportunity import Opportunity

@frappe.whitelist()
def create_opportunity_on_lead_status(doc, method):
    if doc.custom_lead_status == "Interested":
        try:
            opportunity = frappe.new_doc("Opportunity")
            opportunity.party_name = doc.name
            opportunity.custom_source_type = doc.custom_source_type
            opportunity.contact_email = doc.email_id
            opportunity.contact_mobile = doc.mobile_no
            opportunity.opportunity_from = "Lead"
            opportunity.company = doc.custom_sales_organization
            opportunity.custom_property_type = doc.custom_property_type
            opportunity.custom_sq_ft = doc.custom_sq_ft
            opportunity.custom_opportunity_name = doc.lead_name
            opportunity.opportunity_owner = doc.lead_owner

            opportunity.insert()
            frappe.db.commit()
            
            # Refetch the document to avoid version conflict
            doc = frappe.get_doc(doc.doctype, doc.name)
            doc.opportunity = opportunity.name
            doc.save()

            frappe.msgprint(f'Opportunity {opportunity.name} has been created for Lead {doc.name}')
        except frappe.ValidationError as e:
            frappe.throw(_("Failed to create Opportunity: {0}").format(str(e)))
        except Exception as e:
            frappe.throw(_("An unexpected error occurred: {0}").format(str(e)))
