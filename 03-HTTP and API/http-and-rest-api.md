# HTTP + APIs for Agentic AI Applications

## Why This Layer Matters

Your mental model is correct: an agentic system is a chain of HTTP calls. Your app calls an LLM API, the LLM decides to call a tool, that tool calls another API, which might hit a database or external service. Every arrow in that chain is HTTP. If you don't understand HTTP, you're debugging a black box.

---

## HTTP Fundamentals

**HTTP (HyperText Transfer Protocol)** is the request-response protocol that powers the web. Client sends a request, server sends back a response. Stateless — each request is independent; the server doesn't remember your last request unless you explicitly pass something (like a token) that identifies you.

**HTTPS** is HTTP encrypted with TLS/SSL. Same protocol, but the data is encrypted in transit so nobody snooping the network can read your API keys or payloads. Always use HTTPS for anything involving credentials — which, in agentic systems, is almost everything.

**Request** — what the client sends. Has four parts:
1. **Method** (GET, POST, etc.) — what you want to do
2. **URL** — where you're sending it
3. **Headers** — metadata about the request
4. **Body** — the actual data (not always present)

**Response** — what the server sends back. Has:
1. **Status code** — did it work?
2. **Headers** — metadata about the response
3. **Body** — the actual data (usually JSON in modern APIs)

**Headers** are key-value pairs carrying metadata — not the main content, but context about it. Common ones you'll see constantly:
- `Content-Type: application/json` — "this body is JSON"
- `Authorization: Bearer sk-abc123...` — "here's my credential"
- `Accept: application/json` — "send me JSON back"

**Body** is the actual payload — usually a JSON object for both requests (e.g., your prompt to an LLM API) and responses (e.g., the model's reply).

**Status codes** tell you what happened, grouped by first digit:
| Range | Meaning | Examples |
|---|---|---|
| 2xx | Success | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirect | `301 Moved Permanently`, `304 Not Modified` |
| 4xx | Client error (you messed up) | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests` |
| 5xx | Server error (they messed up) | `500 Internal Server Error`, `503 Service Unavailable` |

In agentic apps, `401`/`403` usually means your API key is wrong or expired, and `429` means you're being rate-limited — both extremely common when you're calling LLM APIs in a loop.

### The Methods (verbs)

| Method | Purpose | Body? | Idempotent?* |
|---|---|---|---|
| `GET` | Retrieve data | No | Yes |
| `POST` | Create something / trigger an action | Yes | No |
| `PUT` | Replace a resource entirely | Yes | Yes |
| `PATCH` | Partially update a resource | Yes | No |
| `DELETE` | Remove a resource | Sometimes | Yes |

*Idempotent = calling it 5 times has the same effect as calling it once. `GET /user/5` five times still just returns the user. `POST /orders` five times creates 5 orders — that's why it's *not* idempotent.

**In practice**, when you call an LLM API (like Claude's `/v1/messages`), you're doing a `POST` — you're sending a body (your messages, system prompt, tools) and triggering the model to generate a response. This is the single most common call pattern you'll write in agentic systems.

---

## REST APIs

**REST** (Representational State Transfer) is a set of conventions for designing APIs around **resources** — nouns like `users`, `orders`, `messages` — manipulated with HTTP verbs. It's not a strict protocol, just a widely-adopted convention.

**Endpoint** — a specific URL you can send a request to. Example: `https://api.anthropic.com/v1/messages` is an endpoint.

**Path parameters** — part of the URL path itself, identifying a specific resource:
```
GET /users/12345
              └── this is a path parameter (the user's ID)
```

**Query parameters** — key-value pairs after a `?`, used for filtering, sorting, pagination:
```
GET /orders?status=shipped&limit=10&sort=date
            └────────────┬────────────┘
                  query parameters
```

**Request body** — the JSON payload sent with `POST`/`PUT`/`PATCH`. This is where you send structured data. For an LLM call:
```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1000,
  "messages": [
    { "role": "user", "content": "Hello" }
  ]
}
```

**JSON response** — what comes back, structured data your code parses:
```json
{
  "id": "msg_123",
  "content": [
    { "type": "text", "text": "Hi there!" }
  ]
}
```
Notice this maps directly to what's inside `anthropic_api_in_artifacts` above — `data.content` is an array of typed blocks, and you filter by `type` to extract what you need. That's REST in action: predictable structure, parsed programmatically.

---

## Authentication

This is the part that trips people up most in agentic systems, because you're often chaining multiple auth schemes together (your app → LLM API → third-party tool → that tool's own auth).

### API Keys
The simplest scheme. A single secret string identifying *your application* (not a specific user), usually sent as a header:
```
x-api-key: sk-ant-api03-xxxxxxxx
```
or sometimes as a query parameter (less secure, avoid when possible — query params get logged everywhere). Used for server-to-server calls where you fully trust the caller (that's you). This is how you'd authenticate to the Anthropic API directly.

### Bearer Tokens
A more general pattern — you send a token in the `Authorization` header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```
"Bearer" literally means: whoever *bears* (holds) this token gets access. No further proof needed — which is why bearer tokens must be protected like passwords. An API key is often *implemented* as a bearer token; they're closely related, but "API key" usually implies a long-lived static secret, while "bearer token" often implies something more short-lived and dynamic (like a session token or OAuth access token).

### JWT (JSON Web Token)
A specific, structured *format* for a token — not an auth method itself, but a way of packaging claims. Three base64 parts separated by dots:
```
header.payload.signature
```
- **Header**: algorithm used to sign it
- **Payload**: the actual claims — user ID, expiration time, roles, etc.
- **Signature**: cryptographic proof the token wasn't tampered with

The key property: a JWT is **self-contained**. The server can verify it's legitimate (via the signature) without a database lookup, because all the info it needs is *inside* the token. This is why JWTs are popular for stateless auth in distributed/microservice systems — no shared session store needed. You'll see JWTs issued after login flows and OAuth exchanges.

### OAuth (conceptual)
OAuth solves a different problem than API keys: **delegated authorization**. It lets your app act on a user's behalf on a *third-party service*, without ever seeing that user's password for that service.

The flow, conceptually:
1. Your app redirects the user to the third-party service (e.g., Google) to log in
2. User approves "let this app access my Google Drive"
3. Google redirects back to your app with an **authorization code**
4. Your app exchanges that code (server-side, using your app's secret) for an **access token**
5. Your app uses that access token — usually as a bearer token — to call Google's API on the user's behalf
6. Access tokens expire; a **refresh token** lets you get a new one without the user logging in again

This is exactly what's happening in the `mcp_servers` connectors you see referenced above (Gmail, Google Drive) — the user authorized access once via OAuth, and now the agent holds a token that lets it act within the scope the user granted, without ever touching the user's actual password.

**The one-line mental model for each:**
- **API key** → "this app is allowed to call me" (app-level trust)
- **Bearer token** → "whoever holds this gets in" (a delivery mechanism, key or JWT can ride inside it)
- **JWT** → "here's a signed, self-verifying packet of claims" (a token *format*)
- **OAuth** → "this user let this app act on their behalf, on a third service, without sharing their password" (a *flow* for getting a token)

---

## How This All Connects in an Agentic Loop

```
1. Your app          --POST-->  LLM API (auth: API key/bearer token)
                      <--JSON--
2. LLM decides to call a tool
3. Your app           --POST-->  Tool/API (auth: API key, or OAuth token if it's
                       <--JSON--  acting on a user's connected account)
4. Tool                --query--> Database
                        <--rows--
5. Result gets fed back into the LLM's next turn as context
6. Loop continues until the LLM has a final answer
```

Every single arrow above is an HTTP request-response pair, with its own status code, headers, and auth scheme. Once this clicks, agentic system debugging becomes mostly: "which hop in this chain returned a 4xx or 5xx, and why?"