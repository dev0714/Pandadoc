# PandaDoc Template Field Mapping Design

## Goal
The PandaDoc template library in super-admin settings must support field mappings so each manually created PandaDoc template can declare which sales-screen fields it expects to receive when a document is generated.

This keeps the template configuration aligned with the actual branch sales form, rather than relying on a generic or guessed list of placeholders.

## Scope
This design applies to:
- `app/dashboard/branch/page.tsx`
- `app/dashboard/branch-admin/page.tsx`
- `app/dashboard/super-admin/settings/pandadoc-section.tsx`
- `lib/pandadoc-settings.ts`
- PandaDoc send flow configuration

It does not change the sale capture flow.

## Required Sales-Screen Fields
The PandaDoc template library should support mappings for the following sales-screen contact fields.

### Core Contact Fields
- `client_first_name` from `first_name`
- `client_last_name` from `last_name`
- `client_full_name` from `first_name + last_name`
- `client_id_number` from `id_number`
- `client_phone` from `phone`
- `client_email` from `email`
- `client_gender` from `gender`
- `client_province` from `province`

### Supporting Sale Context Fields
- `service_name` from the selected service name
- `service_code` from the selected service code
- `branch_name` from the active branch name
- `nupay_reference` from the current NuPay reference

## Template Library Requirements
Each PandaDoc template record in the super-admin library must support:
- template name
- PandaDoc template ID
- active/inactive flag
- notes
- linked field definitions

### Linked Field Definition
Each linked field should store:
- `label`
- `source_key`
- `required`
- optional `pandadoc_field_name` if the PandaDoc field name differs from the source key

## Example Template Metadata
Example template configuration:

```json
{
  "template_name": "S1A - Court Route Agreement",
  "pandadoc_template_id": "1234567890",
  "active": true,
  "notes": "Used for S1A court-route sign-up",
  "linked_fields": [
    { "label": "Client First Name", "source_key": "first_name", "required": true },
    { "label": "Client Last Name", "source_key": "last_name", "required": true },
    { "label": "Client ID Number", "source_key": "id_number", "required": true },
    { "label": "Client Phone", "source_key": "phone", "required": true },
    { "label": "Client Email", "source_key": "email", "required": true },
    { "label": "Service Name", "source_key": "service_name", "required": true },
    { "label": "Service Code", "source_key": "service_code", "required": true },
    { "label": "Branch Name", "source_key": "branch_name", "required": true },
    { "label": "NuPay Reference", "source_key": "nupay_reference", "required": false }
  ]
}
```

## UI Requirements
### Template Library
The PandaDoc Template Library should allow admins to:
- create template records manually
- store the PandaDoc template ID
- define linked fields for the template
- mark linked fields as required or optional
- edit or remove linked fields later

### Service Mapping
The service mapping section should continue to:
- select service code
- select NuPay settings ID
- select a PandaDoc template from the template library

The mapping UI should also show:
- whether the chosen template has linked fields configured
- how many linked fields are required

## Validation Rules
- A template cannot be saved without a template name and PandaDoc template ID.
- A linked field cannot be saved without a `source_key`.
- A template should not be considered ready for branch use unless it has at least one linked field.
- If a template is mapped to a service, the UI should warn when required linked fields are missing.

## Runtime Behavior
When `Send PandaDoc` is clicked from the branch sale screens:
- the app resolves the service-to-template mapping
- the app loads the linked field definitions from the PandaDoc template library
- the app populates the PandaDoc payload with values from the branch sales form
- the client and logged-in user still receive the PandaDoc notification email
- the sale flow remains unchanged if PandaDoc fails

## Acceptance Criteria
- The PandaDoc template library can store field mappings tied to sales-screen inputs.
- The branch sales screens can use the saved mappings when generating PandaDoc documents.
- The super-admin UI makes it obvious which fields a template expects.
- Sale capture continues to work even if PandaDoc is not configured or fails.

