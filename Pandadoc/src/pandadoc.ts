export interface PandadocRequestClient {
  request(method: string, path: string, body?: unknown): Promise<unknown>;
}

export interface PandadocRecipientInput {
  email: string;
  firstName?: string;
  lastName?: string;
  role?: string;
  phone?: string;
}

export interface PandadocSigningLinkInput {
  templateUuid: string;
  name: string;
  recipients: PandadocRecipientInput[];
  tokens?: Array<{ name: string; value: string }>;
  clientFirstName?: string;
  clientLastName?: string;
  fields?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  tags?: string[];
  folderUuid?: string;
  owner?: { email?: string; membership_id?: string };
  contentPlaceholders?: unknown[];
  pricingTables?: unknown[];
  tables?: unknown[];
  texts?: unknown[];
  detectTitleVariables?: boolean;
  sendSubject?: string;
  sendMessage?: string;
  silent?: boolean;
  sessionPayload?: Record<string, unknown>;
  appBaseUrl?: string;
  pollIntervalMs?: number;
  maxPollAttempts?: number;
}

export interface PandadocSigningLinkResult {
  documentId: string;
  signingUrl: string;
  session?: Record<string, unknown>;
}

export interface PandadocFetchClientOptions {
  apiKey: string;
  baseUrl?: string;
  fetchImpl?: typeof fetch;
}

export function createPandadocFetchClient({
  apiKey,
  baseUrl = 'https://api.pandadoc.com/public/v1',
  fetchImpl = fetch,
}: PandadocFetchClientOptions): PandadocRequestClient {
  return {
    async request(method: string, path: string, body?: unknown) {
      const url = new URL(path, `${baseUrl.replace(/\/$/, '')}/`);
      const headers: Record<string, string> = {
        Authorization: `API-Key ${apiKey}`,
      };

      const hasBody = body !== undefined;
      if (hasBody) {
        headers['Content-Type'] = 'application/json';
      }

      const response = await fetchImpl(url, {
        method,
        headers,
        body: hasBody ? JSON.stringify(body) : undefined,
      });

      const text = await response.text();
      const payload = text.length ? safeJsonParse(text) : undefined;

      if (!response.ok) {
        const message = typeof payload === 'object' && payload !== null
          ? JSON.stringify(payload)
          : text || response.statusText;
        throw new Error(`PandaDoc API request failed (${response.status}): ${message}`);
      }

      return payload ?? {};
    },
  };
}

export async function createPandadocSigningLink(
  client: PandadocRequestClient,
  input: PandadocSigningLinkInput,
): Promise<PandadocSigningLinkResult> {
  const createResponse = await client.request('POST', '/documents', buildCreateDocumentBody(input));
  const documentId = readId(createResponse, 'document');

  await waitForDraft(client, documentId, input.pollIntervalMs ?? 1000, input.maxPollAttempts ?? 30);

  await client.request('POST', `/documents/${documentId}/send`, {
    silent: input.silent ?? true,
    subject: input.sendSubject,
    message: input.sendMessage,
  });

  const sessionRecipient = input.recipients[0]?.email;
  if (!sessionRecipient) {
    throw new Error('PandaDoc session creation requires at least one recipient email.');
  }

  const sessionResponse = await client.request('POST', `/documents/${documentId}/session`, {
    recipient: sessionRecipient,
    ...input.sessionPayload,
  });
  const signingUrl = buildSigningUrl(sessionResponse, input.appBaseUrl);

  return {
    documentId,
    signingUrl,
    session: isRecord(sessionResponse) ? sessionResponse : undefined,
  };
}

export async function waitForDraft(
  client: PandadocRequestClient,
  documentId: string,
  pollIntervalMs = 1000,
  maxPollAttempts = 30,
): Promise<void> {
  for (let attempt = 0; attempt < maxPollAttempts; attempt++) {
    const response = await client.request('GET', `/documents/${documentId}`);
    const status = readStatus(response);

    if (status === 'document.draft') {
      return;
    }

    if (status === 'document.error') {
      throw new Error(`PandaDoc document ${documentId} failed to process.`);
    }

    if (attempt < maxPollAttempts - 1) {
      await delay(pollIntervalMs);
    }
  }

  throw new Error(`Timed out waiting for PandaDoc document ${documentId} to reach draft status.`);
}

function buildCreateDocumentBody(input: PandadocSigningLinkInput): Record<string, unknown> {
  const tokens = [
    ...(input.tokens ?? []),
    ...buildClientTokens(input.clientFirstName, input.clientLastName),
  ];

  return {
    template_uuid: input.templateUuid,
    name: input.name,
    recipients: input.recipients.map((recipient) => ({
      email: recipient.email,
      first_name: recipient.firstName,
      last_name: recipient.lastName,
      role: recipient.role,
      phone: recipient.phone,
    })),
    tokens: tokens.length ? tokens : undefined,
    fields: input.fields,
    metadata: input.metadata,
    tags: input.tags,
    folder_uuid: input.folderUuid,
    owner: input.owner,
    content_placeholders: input.contentPlaceholders,
    pricing_tables: input.pricingTables,
    tables: input.tables,
    texts: input.texts,
    detect_title_variables: input.detectTitleVariables,
  };
}

function buildClientTokens(clientFirstName?: string, clientLastName?: string): Array<{ name: string; value: string }> {
  const tokens: Array<{ name: string; value: string }> = [];

  if (clientFirstName) {
    tokens.push({ name: 'Client.FirstName', value: clientFirstName });
  }

  if (clientLastName) {
    tokens.push({ name: 'Client.LastName', value: clientLastName });
  }

  return tokens;
}

function readId(response: unknown, label: string): string {
  if (!isRecord(response)) {
    throw new Error(`PandaDoc ${label} response did not return an object.`);
  }

  const id = response.id ?? response.document_id ?? response.documentId;
  if (typeof id !== 'string' || !id) {
    throw new Error(`PandaDoc ${label} response did not include a document id.`);
  }

  return id;
}

function readStatus(response: unknown): string | undefined {
  if (!isRecord(response)) {
    return undefined;
  }

  const status = response.status ?? response.document_status;
  return typeof status === 'string' ? status : undefined;
}

function buildSigningUrl(response: unknown, appBaseUrl = 'https://app.pandadoc.com'): string {
  if (!isRecord(response)) {
    throw new Error('PandaDoc session response did not return an object.');
  }

  const sessionUrl = response.url ?? response.session_url ?? response.sessionUrl;
  if (typeof sessionUrl === 'string' && sessionUrl) {
    return sessionUrl;
  }

  const sessionId = response.id ?? response.session_id ?? response.sessionId;
  if (typeof sessionId !== 'string' || !sessionId) {
    throw new Error('PandaDoc session response did not include a signing URL.');
  }

  return `${appBaseUrl.replace(/\/$/, '')}/s/${sessionId}`;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function safeJsonParse(text: string): unknown {
  return JSON.parse(text);
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}
