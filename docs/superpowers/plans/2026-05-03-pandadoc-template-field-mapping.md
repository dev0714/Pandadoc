# PandaDoc Template Field Mapping Plan

## Objective
Add PandaDoc template field mappings to the super-admin PandaDoc settings flow so each manually created PandaDoc template can declare which sales-screen fields it needs from the branch sale forms.

## Context
The PandaDoc template library already exists in super-admin settings and the service mapping dropdown already points at that library. The next step is to let each template carry its own linked-field configuration, based on the branch and branch-admin sales-screen inputs.

## Tasks

### 1. Extend the PandaDoc settings data model
Update the PandaDoc settings types and normalization helpers so each template library item can store a list of linked fields.

Files:
- `lib/pandadoc-settings.ts`
- `tests/pandadoc-settings.test.mjs`

Requirements:
- add a `linked_fields` array to PandaDoc template library entries
- each linked field should support:
  - `label`
  - `source_key`
  - `required`
  - optional `pandadoc_field_name`
- keep existing template library fields working:
  - template name
  - PandaDoc template ID
  - active/inactive
  - notes
- preserve backward compatibility with older saved settings rows

Validation:
- reject linked fields without a `source_key`
- preserve blank or missing `linked_fields` as an empty array

### 2. Add linked-field editing UI to PandaDoc template library
Update the super-admin PandaDoc settings section so admins can add, edit, and remove linked fields on each template record.

Files:
- `app/dashboard/super-admin/settings/pandadoc-section.tsx`

Requirements:
- add a linked-fields editor under the PandaDoc Template Library form
- allow adding multiple field rows per template
- each row should capture:
  - display label
  - source key
  - required toggle
  - optional PandaDoc field name
- show the saved linked fields when editing a template
- keep the existing template creation flow intact

### 3. Add sales-screen field presets for branch and branch-admin
Define the allowed source keys from the branch sales forms so admins can select from a consistent list instead of typing arbitrary field names.

Files:
- `app/dashboard/super-admin/settings/pandadoc-section.tsx`
- optionally `lib/pandadoc-settings.ts` if the field list is shared

Sales-screen source keys to support:
- `first_name`
- `last_name`
- `client_full_name`
- `id_number`
- `phone`
- `email`
- `gender`
- `province`
- `service_name`
- `service_code`
- `branch_name`
- `nupay_reference`

Requirements:
- use a dropdown or select for `source_key` where practical
- allow the admin to choose common sales fields quickly
- make it obvious which fields are contact fields versus service context fields

### 4. Surface linked-field readiness in the service mapping section
Show template-linked-field status in the service mapping UI so super-admins can tell whether a PandaDoc template is ready to be used.

Files:
- `app/dashboard/super-admin/settings/pandadoc-section.tsx`

Requirements:
- show how many linked fields are defined for the selected template
- warn if a template has no linked fields
- keep the service code and NuPay settings dropdown behavior unchanged

### 5. Wire the PandaDoc send flow to pass sales-screen field values
Prepare the PandaDoc send route to use the selected template’s linked field definitions when building the PandaDoc payload.

Files:
- `lib/pandadoc-send-route.ts`
- `lib/pandadoc-service-template-resolver.ts`
- `app/api/pandadoc/send/route.ts`
- `tests/pandadoc-send-route.test.mjs`

Requirements:
- resolve the mapped PandaDoc template as before
- load linked fields from the PandaDoc template library
- pass branch sales values into the PandaDoc payload using the configured mappings
- keep the sale capture flow unchanged if PandaDoc fails

### 6. Add tests for the new linked-field behavior
Cover normalization, UI payload shape, and send-route field resolution.

Files:
- `tests/pandadoc-settings.test.mjs`
- `tests/pandadoc-send-route.test.mjs`
- any new focused test file if needed

Requirements:
- verify linked fields round-trip through settings normalization
- verify invalid linked fields are rejected
- verify the send route receives the mapped field definitions

## Verification
Run:
- `npm run build`
- the relevant PandaDoc unit tests

## Notes
- The branch sale flow already contains the source values the templates need, so this work is mostly a configuration and payload-mapping change.
- The template library should remain manually managed by super-admin users.

