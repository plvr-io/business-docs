# PLVR Business Portal Docs

Mintlify documentation site for the PLVR Business Portal.

## Local preview

```bash
npm i -g mint
mint dev        # http://localhost:3000
mint broken-links
```

## Structure

Navigation lives in `docs.json`. Pages are `.mdx` files grouped by portal area:
`getting-started/`, `organization/`, `events/`, `tickets/`, `promotions/`, `tap/`, `onsite/`, `other/`.

Source of truth for behavior: `plvr-io/plvr-client` → `apps/business-portal`.
