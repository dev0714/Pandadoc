---
name: pandadoc-api
description: This skill should be used when working with the PandaDoc API for API-key or OAuth integrations, document creation and management, status tracking, templates, webhooks, downloads, and related request and response handling.
---

# PandaDoc API

Build and troubleshoot PandaDoc integrations that rely on the public API, OAuth, webhooks, and document lifecycle endpoints.

## Use This Skill When

- Creating documents from templates, files, or public URLs
- Sending documents and tracking their status
- Reading document details, recipients, fields, pricing data, and metadata
- Managing templates and template-driven workflows
- Handling OAuth access tokens or API keys
- Subscribing to document and template webhooks
- Downloading completed documents or verifiable PDFs

## Stay Focused On APIs

- Prefer server-side API workflows over embedded UI guidance unless an API request depends on embedded behavior.
- Do not expand into editor embedding, signing widgets, or UI composition unless the user explicitly asks for that path.
- Treat this skill as the source of truth for document automation, not as a general PandaDoc product guide.

## Load References As Needed

- Use `references/pandadoc-api.md` for the high-level API map and default workflow rules.
- Use `references/pandadoc-auth.md` for authentication, sandbox, OAuth, API key, workspace, and member behavior.
- Use `references/pandadoc-documents.md` for create, update, send, status, download, fields, recipients, attachments, and ownership flows.
- Use `references/pandadoc-templates-content.md` for template details, content library items, content placeholders, variables, fields, and pricing data.
- Use `references/pandadoc-webhooks.md` for webhook events, payload handling, and signature verification.

## Default Integration Rules

1. Identify the auth mode first.
   - Use `Authorization: API-Key <key>` for API key auth.
   - Use OAuth 2.0 when requests must act on behalf of a user.
   - Use the sandbox key for testing and the production key for live workflows.

2. Use the correct base endpoints.
   - Public API: `https://api.pandadoc.com/public/v1`
   - OAuth token exchange: `https://api.pandadoc.com/oauth2/access_token`

3. Respect the asynchronous document lifecycle.
   - Create the document.
   - Wait until the document reaches `document.draft`.
   - Send the document.
   - Track progress with webhooks or polling.
   - Download the completed document after completion.

4. Prefer webhooks over polling in production.
   - Use polling only when webhooks are unavailable or during prototyping.
   - Treat webhook handlers as idempotent.

## Core Workflow To Apply

### 1. Choose the document source

- Use a template when the workflow is standardized.
- Use a file upload when the source is a PDF, DOCX, or RTF.
- Use a public URL when the file is hosted externally.

### 2. Build the create request carefully

- Map recipient roles exactly to the template or file structure.
- Pre-fill fields, tokens, pricing tables, images, and content placeholders only where the source supports them.
- Resolve template IDs from the app URL or by listing templates.
- Keep request bodies explicit and deterministic.

### 3. Wait for readiness

- Treat document creation as asynchronous.
- Do not send the document until the status is `document.draft`.
- If webhooks are available, wait for `document_state_changed`.
- If polling is required, poll `GET /documents/{id}` until draft is reached.

### 4. Send the document

- Send only after draft readiness is confirmed.
- Use `silent: true` only when the workflow will deliver the session another way and the recipient should not receive PandaDoc email.
- Record the send response and document ID for later tracking.

### 5. Track lifecycle changes

- Watch for `document.sent`, `document.viewed`, `document.completed`, `document.declined`, `document.voided`, `document.paid`, and approval-related states when relevant.
- Prefer `document_state_changed` for state transitions.
- Use `document_updated` for content or draft changes.
- Use `document_creation_failed` to detect failed create jobs.

### 6. Download the result

- After completion, download the document for archival or downstream processing.
- Use the protected download endpoint when a verifiable PDF is required.
- Remember that protected download works with production keys only.

## Reference The Right Endpoints

- `POST /documents` to create a document
- `GET /documents/{id}` to check basic status
- `GET /documents/{id}/details` to inspect rich document data
- `POST /documents/{id}/send` to send a document
- `PATCH /documents/{id}/status` to manually set allowed terminal states
- `GET /documents/{id}/download` or protected download for completed output
- `POST /oauth2/access_token` to exchange or refresh OAuth tokens

## Handle Templates Correctly

- Use the template UUID, not a display name, in automated flows.
- Preserve recipient order and role names where the template expects them.
- Use template creation and content placeholder behavior only when the workflow needs reusable document structure.
- Treat template changes as a contract with the downstream automation.

## Handle Webhooks Carefully

- Subscribe to the events that match the workflow, especially document state changes and completion-related events.
- Verify webhook signatures before processing payloads.
- Store the PandaDoc document ID, external record ID, and event type together so retries can be deduplicated.
- Reconcile webhook events against the current document status before taking irreversible action.

## Handle Errors Deliberately

- Treat 401 as authentication failure or expired OAuth state.
- Treat 403 as a permission or workspace scope issue.
- Treat 429 as a rate-limit issue and retry with backoff.
- Treat asynchronous processing as normal; do not assume create success means ready to send.
- Surface the raw PandaDoc response body when debugging payload issues.

## Sandbox And Production Notes

- Expect sandbox behavior to differ from production in rate limits, document naming, and generated PDF appearance.
- Prefer sandbox for development and tests.
- Mention when a workflow depends on production-only behavior, especially protected downloads.

## Preferred Output When Helping The User

- Name the exact PandaDoc endpoint.
- State the required auth type.
- List the minimum request fields.
- Explain the expected status transition.
- Call out any webhook or polling step needed next.
- When the user asks for a broader answer, expand from the relevant reference file instead of guessing.
