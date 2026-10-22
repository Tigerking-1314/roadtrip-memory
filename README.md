# roadtrip-memory

**A memory for the places worth stopping again.** Built on
[`your-first-memory`](https://github.com/jlumbroso/your-first-memory):
the diner with the pie, the overlook at sunset, the motel you'd book
again. You tell your model about them on the road, and they're still
there when the conversation ends.

One table (`favorites`: `place`, `reason`, `created_at`). Two tools:

- `save_favorite(place, reason)` saves a place and why it was worth it.
- `list_favorites()` lists every favorite, oldest first.

A database that outlives the server, the deploy, and the chat window.

- **Setup**: follow [COURSE-STEPS.md](COURSE-STEPS.md), which was written
  for the original quotes version. The Neon and Render steps are the same.
  To test, ask *"Save the Blue Moon Diner as a favorite: best pie on
  Route 66"* and then, in a new conversation, *"What are my road-trip
  favorites?"*
- **Every design choice, with the road not taken**: [docs/adr/](docs/adr/).
  ADR-0001 to 0004 come from the template (0004 still describes the quotes
  schema it replaced). ADR-0005 explains why `DATABASE_URL` is stripped
  of stray whitespace before connecting.
- **Stack**: FastMCP (`mcp[cli] >=1.2,<2`, pinned in render.yaml) +
  `psycopg` + [Neon](https://neon.tech) free-tier Postgres + Render
  free-tier compute. The secret (`DATABASE_URL`) lives only in the
  environment (ADR-0003).

*Derived from your-first-memory, CAM · CIS 7000-008 · Penn · Fall 2026.
See [NOTICE](NOTICE).*
