# PandaDoc API Reference Notes

Use this as the entry point for the full PandaDoc API skill.

## Read In This Order

1. `references/pandadoc-auth.md`
2. `references/pandadoc-documents.md`
3. `references/pandadoc-templates-content.md`
4. `references/pandadoc-webhooks.md`

## Core Official Pages

- API overview: https://developers.pandadoc.com/reference/about
- Getting started: https://developers.pandadoc.com/docs/getting-started
- Full API reference: https://developers.pandadoc.com/reference
- Document lifecycle: https://developers.pandadoc.com/docs/automate-document-workflows
- Create and send first document: https://developers.pandadoc.com/docs/create-and-send-document-fundamentals
- Create document overview: https://developers.pandadoc.com/docs/create-document

## Universal API Rules

- Use the public API host `https://api.pandadoc.com/public/v1` for REST requests.
- Use `Authorization: API-Key <key>` unless the workflow explicitly requires OAuth.
- Treat document creation as asynchronous.
- Use webhooks first for production workflows.
- Expand into the topic-specific reference files when a request needs more detail.

## Common Troubleshooting Questions

- Is the request using the right auth type for the workspace?
- Is the document still `document.uploaded` and waiting to become `document.draft`?
- Are the template roles, recipient roles, and field names aligned?
- Is the workflow expecting a production-only endpoint or behavior?
- Would a webhook remove the need for polling?
