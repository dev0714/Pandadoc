# PandaDoc Webhook Notes

Use this file for event-driven document and template tracking.

## Official Docs

- Webhooks overview: https://developers.pandadoc.com/reference/webhooks-overview
- Webhooks concepts: https://developers.pandadoc.com/docs/webhooks-concepts
- Listen for document status changes: https://developers.pandadoc.com/docs/listen-document-status-changes
- Document state changed webhook: https://developers.pandadoc.com/reference/handledocumentstatechanged
- Document updated webhook: https://developers.pandadoc.com/reference/handledocumentupdated
- Document deleted webhook: https://developers.pandadoc.com/reference/handledocumentdeleted
- PDF ready webhook: https://developers.pandadoc.com/reference/pdfofcompleteddocumentavailablefordownload

## Webhook Strategy

- Prefer webhooks over polling in production.
- Use polling only as a fallback or for quick prototypes.
- Treat webhook payloads as the trigger, not the final source of truth.
- Re-fetch the document when the event requires a confirmed current state.

## Important Events

- `document_state_changed`
- `document_updated`
- `document_creation_failed`
- `recipient_completed`
- `document_completed_pdf_ready`
- `document_deleted`
- `template_created`
- `template_updated`
- `template_deleted`

## Handling Rules

- Verify the HMAC signature before accepting the payload.
- Make webhook handlers idempotent.
- Store the PandaDoc document ID and your internal record ID together for deduplication.
- Reconcile the webhook event with current document details before taking irreversible action.

## Workflow Guidance

- Use `document_state_changed` to drive send, sign, complete, void, decline, and payment workflows.
- Use `document_updated` to detect edits that revert a document back to draft.
- Use `document_completed_pdf_ready` to trigger post-completion archival or download flows.

