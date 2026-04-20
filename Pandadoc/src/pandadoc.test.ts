import assert from 'node:assert/strict';

async function main() {
  const { createPandadocSigningLink } = await import('./pandadoc.ts');

  const calls: Array<{ method: string; path: string; body?: unknown }> = [];
  const client = {
    async request(method: string, path: string, body?: unknown) {
      calls.push({ method, path, body });

      if (method === 'POST' && path === '/documents') {
        return { id: 'doc_123' };
      }

      if (method === 'GET' && path === '/documents/doc_123') {
        return { status: 'document.draft' };
      }

      if (method === 'POST' && path === '/documents/doc_123/send') {
        return { ok: true };
      }

      if (method === 'POST' && path === '/documents/doc_123/session') {
        return { url: 'https://sign.pandadoc.example/session_abc' };
      }

      throw new Error(`Unexpected call ${method} ${path}`);
    },
  };

  const result = await createPandadocSigningLink(client, {
    templateUuid: 'tmpl_123',
    name: 'Acme Contract',
    recipients: [
      {
        email: 'customer@example.com',
        firstName: 'Ava',
        lastName: 'Stone',
        role: 'Signer',
      },
    ],
  });

  assert.equal(result.documentId, 'doc_123');
  assert.equal(result.signingUrl, 'https://sign.pandadoc.example/session_abc');
  assert.equal(calls[0]?.method, 'POST');
  assert.equal(calls[0]?.path, '/documents');
  assert.equal(calls[1]?.method, 'GET');
  assert.equal(calls[2]?.method, 'POST');
  assert.equal(calls[2]?.path, '/documents/doc_123/send');
  assert.equal(calls[3]?.method, 'POST');
  assert.equal(calls[3]?.path, '/documents/doc_123/session');
}

async function testMapsClientNamesToTokens() {
  const { createPandadocSigningLink } = await import('./pandadoc.ts');

  const calls: Array<{ method: string; path: string; body?: unknown }> = [];
  const client = {
    async request(method: string, path: string, body?: unknown) {
      calls.push({ method, path, body });

      if (method === 'POST' && path === '/documents') {
        return { id: 'doc_456' };
      }

      if (method === 'GET' && path === '/documents/doc_456') {
        return { status: 'document.draft' };
      }

      if (method === 'POST' && path === '/documents/doc_456/send') {
        return { ok: true };
      }

      if (method === 'POST' && path === '/documents/doc_456/session') {
        return { url: 'https://sign.pandadoc.example/session_def' };
      }

      throw new Error(`Unexpected call ${method} ${path}`);
    },
  };

  await createPandadocSigningLink(client, {
    templateUuid: 'tmpl_456',
    name: 'Acme Contract',
    recipients: [
      {
        email: 'customer@example.com',
        role: 'Signer',
      },
    ],
    clientFirstName: 'Jane',
    clientLastName: 'Doe',
  });

  const createBody = calls[0]?.body as Record<string, unknown> | undefined;
  const tokens = createBody?.tokens as Array<{ name: string; value: string }> | undefined;
  assert.deepEqual(tokens, [
    { name: 'Client.FirstName', value: 'Jane' },
    { name: 'Client.LastName', value: 'Doe' },
  ]);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

testMapsClientNamesToTokens().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
