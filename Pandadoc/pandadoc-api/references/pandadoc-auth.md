# PandaDoc Authentication And Workspace Notes

Use this file for auth, workspace, and member lookups.

## Official Docs

- API key auth: https://developers.pandadoc.com/reference/api-key-authentication-process
- OAuth auth: https://developers.pandadoc.com/reference/authentication-process
- OAuth token exchange: https://developers.pandadoc.com/reference/access-token
- Getting started: https://developers.pandadoc.com/docs/getting-started
- Organizations, workspaces, and API keys: https://developers.pandadoc.com/docs/organizations-workspaces-api-keys
- Create API key: https://developers.pandadoc.com/reference/create-api-key
- List members: https://developers.pandadoc.com/reference/list-members
- Current member details: https://developers.pandadoc.com/reference/current-member-details
- Member details: https://developers.pandadoc.com/reference/member-details
- Create member token: https://developers.pandadoc.com/reference/get-member-token

## Authentication Rules

- Use `Authorization: API-Key <key>` for API key requests.
- Use OAuth 2.0 when requests must be executed on behalf of a PandaDoc user.
- Send OAuth token exchange requests to `POST /oauth2/access_token`.
- Treat API key and OAuth flows as separate authentication paths.

## Workspace Rules

- Treat API keys as workspace-scoped unless the key belongs to an Org Admin and the action is organization-level.
- Assume the key inherits the permissions of its owner.
- Prefer using the exact workspace member or membership ID from the API, not a name.
- Remember that member details can differ from the active workspace implied by the key.

## Practical Checks

- Confirm whether the user needs sandbox or production access before building the request.
- Use sandbox keys for development and test documents.
- Expect protected or production-only actions to fail in sandbox.
- When debugging permission issues, verify workspace, owner, and role first.

