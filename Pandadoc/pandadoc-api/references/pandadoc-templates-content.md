# PandaDoc Template And Content Notes

Use this file for templates, content library items, placeholders, variables, fields, and pricing data.

## Official Docs

- Template details: https://developers.pandadoc.com/reference/template-details
- Content library item details: https://developers.pandadoc.com/reference/content-library-item-details
- List content library items: https://developers.pandadoc.com/reference/list-content-library-items
- Create from template: https://developers.pandadoc.com/docs/create-document-from-template
- Create with content placeholders: https://developers.pandadoc.com/docs/create-with-content-placeholders-from-template
- Choosing between variables and fields: https://developers.pandadoc.com/docs/choosing-between-variables-and-fields
- Working with tables: https://developers.pandadoc.com/docs/working-with-tables
- Create document API reference: https://developers.pandadoc.com/reference/create-document
- Document details: https://developers.pandadoc.com/reference/document-details

## Template Rules

- Resolve template IDs from the PandaDoc template URL or by listing templates in the API.
- Use template details to inspect roles, fields, tokens, pricing, tags, and placeholders before building the create request.
- Treat a template as the contract for downstream document creation.

## Content Placeholders

- Use content placeholders when a template needs dynamic insertion of content library items.
- Replace every placeholder with at least one content library item.
- Keep content library items unique inside a single placeholder.
- Use content library item details to learn the item structure before populating it.

## Variables And Fields

- Use variables for one-way data injection into a template.
- Use fields when recipients need to fill or edit values.
- Avoid using a variable when the workflow must capture recipient input.
- Do not pre-fill signature fields.

## Pricing Tables

- Keep pricing tables aligned with the template configuration.
- Use the table structure expected by PandaDoc, including sections and rows.
- Enable automatic product insertion in templates when the workflow depends on it.
- Treat pricing table names as important identifiers when updating table data.

## Practical Merge Rules

- Match recipient roles exactly to the template roles.
- Keep token names, field names, and content block names consistent across systems.
- Inspect the template or content library item details endpoint when the payload shape is unclear.
- Use document details after creation to confirm the merged content matches expectations.

