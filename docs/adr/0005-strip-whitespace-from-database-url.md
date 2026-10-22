# ADR-0005: Strip whitespace from `DATABASE_URL` before connecting

- Status: proposed
- Date: 2026-10-22
- Deciders: yiming Liu

## Context

`DATABASE_URL` reaches the server by being copied out of Neon's dashboard
and pasted into Render's environment variables (ADR-0003). A copy-paste
can pick up an invisible trailing newline or space, and a terminal or
`.env` file can add one too. The server used to pass the value to
`psycopg.connect()` unchanged, so that stray character became part of the
connection string: usually tacked onto the last query parameter (for
example `sslmode=require\n`). Then the connection fails with an error
about a setting that looks correct on screen. It is a hard bug to see,
because the bad character is invisible in the place where you would
check.

## Decision

Read the variable as
`os.environ.get("DATABASE_URL", "").strip()`: remove leading and trailing
whitespace once, at startup, before anything else uses the value.

## The roads not taken, and why

**Leave it alone and document the pitfall.** The value only goes wrong
in a way you can't see, and a line in the README does not help someone
who is staring at a correct-looking URL in Render's dashboard. Since a
connection string never legitimately starts or ends with whitespace,
removing it costs nothing.

**Reject the value loudly if it has surrounding whitespace.** This is
more honest about the mistake, but it turns a harmless paste artifact
into a failed deploy for no benefit. Once the whitespace is stripped,
the value is exactly what you meant to paste.

**Validate or parse the whole URL** (scheme, host, required params).
Correctness belongs to libpq, which already reports a malformed URL
clearly. The only failure it reports badly is the invisible one, so
that is the only one we handle.

## Consequences

- Only the two ends are stripped. Whitespace *inside* the URL is left
  alone and still fails, which is what we want, because it signals a
  real mistake.
- An empty or whitespace-only value is now treated like a missing one:
  `db()` gives the setup pointer (ADR-0003) instead of a confusing libpq
  error.
- `render.yaml` is unchanged. The fix is in the code that *reads* the
  secret, not in how the secret is delivered.
