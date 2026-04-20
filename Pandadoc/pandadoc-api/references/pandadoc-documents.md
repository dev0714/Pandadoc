# PandaDoc Document API Notes

Use this file for document lifecycle, recipient, field, attachment, and ownership operations.

## Official Docs

- Create document: https://developers.pandadoc.com/reference/create-document
- Create document from upload: https://developers.pandadoc.com/reference/create-document-from-upload
- Create document section: https://developers.pandadoc.com/reference/create-document-section
- Create document section from upload: https://developers.pandadoc.com/reference/create-document-section-from-upload
- List documents: https://developers.pandadoc.com/reference/list-documents
- Document details: https://developers.pandadoc.com/reference/document-details
- Update document: https://developers.pandadoc.com/reference/update-document
- Delete document: https://developers.pandadoc.com/reference/delete-document
- Bulk delete documents: https://developers.pandadoc.com/reference/bulkdeletedocuments
- Send document: https://developers.pandadoc.com/reference/send-document
- Download protected document: https://developers.pandadoc.com/reference/download-protected-document
- Document status change: https://developers.pandadoc.com/reference/change-document-status-manually
- Update document ownership: https://developers.pandadoc.com/reference/change-document-ownership
- Update document settings: https://developers.pandadoc.com/reference/update-document-settings
- List document fields: https://developers.pandadoc.com/reference/list-document-fields
- Create document fields: https://developers.pandadoc.com/reference/create-document-fields
- Update document recipient: https://developers.pandadoc.com/reference/update-recipient
- Delete document recipient: https://developers.pandadoc.com/reference/delete-recipient
- Delete document attachment: https://developers.pandadoc.com/reference/delete-attachment
- Delete document section: https://developers.pandadoc.com/reference/delete-section
- Delete linked object: https://developers.pandadoc.com/reference/delete-linked-object

## Document Lifecycle

1. Create the document from a template, file upload, or public URL.
2. Wait for asynchronous processing to finish.
3. Confirm the document reaches `document.draft`.
4. Update draft-only content when needed.
5. Send the document.
6. Track state changes until completion, decline, void, or payment completion.
7. Download the final output after completion.

## Create Document Rules

- Use `template_uuid` for template-based creation.
- Use `multipart/form-data` for file uploads.
- Use `url` for public file creation where supported.
- Keep recipient roles aligned with the template or file tags.
- Use fields, tokens, tags, metadata, pricing tables, and content placeholders only where the source supports them.

## Draft-Only Behaviors

- Treat `document.draft` as the only safe state for most content updates.
- Use update document only when the document is still editable.
- Use recipient and field updates carefully after send, since changes can affect contacts and access.

## Recipient And Field Rules

- Use recipient IDs from document details for later edits or removals.
- Treat signer and CC permissions differently.
- Do not pre-fill signature fields.
- Use document fields to collect recipient input.
- Use variables to push one-way data into templates.

## Ownership And Organization

- Use member IDs when transferring ownership.
- Use owner fields when creating documents on another member's behalf.
- Confirm the caller has permission before attempting ownership or recipient changes.

## File And Attachment Rules

- Treat uploaded source files as not stored for reuse in PandaDoc account storage.
- Expect only one file per create request.
- Remove attachments and sections through their dedicated endpoints when needed.

## Download And Finalization

- Use the protected download endpoint for verifiable PDFs.
- Note that protected download requires a production key.
- Use the status-change endpoint only for supported terminal states.

