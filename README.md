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

## Translations

The site ships in English (root), Simplified Chinese (`zh-hans/`), Traditional Chinese (`zh-hant/`) and Japanese (`ja/`).
Each locale mirrors the English page tree and has its own navigation block under `navigation.languages` in `docs.json`.

When you add or rename an English page:

1. Add it to the English nav **and** to each locale's nav (with the locale folder prefix).
2. Create the translated `.mdx` in each locale folder. Internal links must carry the locale prefix (`/ja/tickets/concepts`); images stay at `/images/...`.
3. Run `python3 scripts/check-i18n.py` — it lists missing translations, nav entries and unprefixed links.

Portal UI labels (buttons, menus, fields) stay in English in all locales so they match what users see on screen (a translation may follow in parentheses on first mention).
