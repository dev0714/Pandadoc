# Service Email Templates Mapping (Manager-Admin) Design

Date: 2026-04-22

## Goal

Allow manager-admin users to assign exactly one default email template per canonical service code. Template content remains managed by the existing super-admin email template editor. This task only adds the mapping UI and API for persisting mappings; sending emails is explicitly out of scope (Task 4).

## Non-Goals

- No client-side “send email” action.
- No server-side “send email” route.
- No changes to the super-admin email template editor UI.

## Canonical Services Source

The settings UI lists services from the application’s canonical `SERVICE_LABELS` model in `lib/client-store.ts`. The service codes are:

- S1A, S1B, S2, S3, S4, S5, S6, S7, DOS

No separate database source is used for service labels.

## Data Model

Uses the table added in Task 1:

- `service_email_templates`
  - `service_code` (text, unique)
  - `template_id` (uuid FK to `email_templates.id`)
  - `updated_by` (uuid FK to `users.id`, nullable)
  - `updated_at` (timestamptz)

Service codes are normalized to uppercase for both lookup and save.

## API

### `GET /api/service-email-templates`

Purpose: return the active email templates for the picker plus current service-to-template mappings.

Auth:
- Requires an authenticated session.
- Must allow manager-admin capable roles (same family of roles used elsewhere for manager dashboard APIs).

Server-side:
- Uses the existing Supabase admin client pattern (`createAdminClient()`).

Queries:
- `email_templates`: load all `active = true` templates for the picker (fields: `id`, `name`, `subject`; order by `name`).
- `service_email_templates`: load mappings and join template metadata (`name`, `subject`).

Response (example):

```json
{
  "templates": [
    { "id": "uuid", "name": "[MANDATE] Default", "subject": "..." }
  ],
  "mappings": [
    {
      "service_code": "S1B",
      "template_id": "uuid",
      "template_name": "[MANDATE] Default",
      "template_subject": "..."
    }
  ]
}
```

### `PUT /api/service-email-templates/[serviceCode]` (and `POST` alias)

Purpose: upsert a single mapping for a single service.

Normalization:
- `serviceCode` path param is normalized via `trim().toUpperCase()` and is the source of truth.

Body:
- `{ "template_id": "uuid" }`

Behavior:
- Upserts into `service_email_templates` using `onConflict: 'service_code'`.
- Sets `updated_at` to now.
- Sets `updated_by` to the session user id when available.

## UI

File: `app/dashboard/manager-admin/settings/page.tsx`

Add a new tab/section titled `Service Email Templates` within the existing tabbed settings page:

- Loads services from `SERVICE_LABELS`.
- Uses SWR to load data from `GET /api/service-email-templates`.
- Renders one row per service:
  - service code and label
  - current mapped template (name and subject) or “Not configured”
  - a single-select dropdown listing active templates
  - per-row Save button to persist selection
- After saving, revalidate SWR so a page reload shows the saved selection.

Edge case:
- If an existing mapping points to an inactive template, the UI still displays the current mapping, but the picker list contains only active templates. The user can replace with an active template.

## Manual Verification

- Open `/dashboard/manager-admin/settings`, go to `Service Email Templates`.
- Change a mapping, click Save, confirm it persists.
- Reload the page and confirm the selected template is shown again for that service.

