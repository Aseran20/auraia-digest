---
name: digest
description: "Generate an M&A email digest from a research file. Takes a structured markdown file (produced by /digest-research or written manually) and generates a branded MJML/HTML email with company logos, strategic context, and Outlook-ready formatting. Use when the user has a research file ready and wants to generate the email, or says 'generate the digest' or 'make the email'."
argument-hint: "[path to research markdown file]"
allowed-tools: WebFetch Read Write Bash(npx mjml *) Bash(python *) Bash(mkdir *)
---

# M&A Digest Email Generator — Auraïa Capital Advisory

You generate a professional branded email digest from a structured research file.

## Input

`$ARGUMENTS`

The user passes the path to a research markdown file (typically produced by `/digest-research`). Read it and parse the YAML frontmatter + deal sections.

If no file path is given, look for the most recent `*_research_*.md` file in the current directory.

## Step 1 — Parse the Research File

Read the file. Extract:
- **Frontmatter**: date, sector, geography, language, period, deal_count
- **Synthèse**: the overview paragraph
- **Deals**: each `## Acquéreur → Cible` section with its metadata fields and narrative

If the file doesn't match the expected format, adapt gracefully — extract what you can.

## Step 2 — Company Logos

For each deal where `acquirer_domain` is present, build a Logo.dev URL:
```
https://img.logo.dev/{acquirer_domain}?token=pk_a514bKwfQ2OAdSu_uQBOHA&size=128&format=png
```

Skip logos for unknown/small companies without a clear domain.

## Step 3 — Generate MJML

Read the reference template at `${CLAUDE_SKILL_DIR}/references/email-template.mjml` for structure and style. Adapt it to the actual deals.

### Template Design Principles

- **Light-first design** — no dark background colors (works with Outlook dark mode)
- **Bordered cards** — each section wrapped in `border="1px solid #e2e8f0" border-radius="6px"`
- **Gold highlights** — top deal and CTA use `border="2px solid #D4952A"`
- **Uniform spacing** — `6px` gap between all cards
- **Company logos** — `<mj-image>` above deal title, 28-32px, left-aligned, border-radius 4px
- **DM Sans font** — with `mso-font-alt: 'Calibri'` for Outlook fallback

### Email Structure

1. **Header card** — 2 columns: title + subtitle (left) / Auraïa logo (right). Use the dark logo variant as base64 data URI from `${CLAUDE_SKILL_DIR}/logo-dark.png`

2. **Synthèse + Recap card** — Bordered. Short paragraph from the research synthèse + "Dans ce digest :" with bullet list of all deals (one-liner each: acquirer → target (value) — sector tag)

3. **Deal cards** — One per deal, bordered. First deal gets gold border.
   Each card contains:
   - Acquirer logo (Logo.dev, 28-32px) — skip if no domain
   - "★ Opération majeure" label (first deal only)
   - Title: `Acquéreur → Cible`
   - Metadata: `{date_type} le {date} · {country} · {value_type} {value} · {sector_tag}`
   - Narrative paragraph (contexte stratégique)
   - Source link

4. **CTA card** — Gold border. "Un deal vous interpelle?" + contact button (`mailto:contact@auraia.com`)

5. **Footer** — Auraïa logo (dark variant, centered, 120px) + disclaimer + generation date

### Branding

- **Gold**: #D4952A (accents, highlights, CTAs, tags)
- **Text dark**: #111827 (titles), #1f2937 (body), #4b5563 (metadata)
- **Border**: #e2e8f0 (card borders)
- **Font**: `'DM Sans', Calibri, Arial, sans-serif`
- **Logo dark** (light bg): `${CLAUDE_SKILL_DIR}/logo-dark.png`
- **Logo clear** (dark bg): `${CLAUDE_SKILL_DIR}/logo-clear.png`
- **Tone**: Professional, sober, B2B advisory

### Sector Tag Styles

Use colored pill tags in deal metadata. Map sector tags to these CSS classes:
```
Cloud & Infra    → tag-cloud    (#dbeafe bg, #1e40af text)
Cybersécurité    → tag-cyber    (#fee2e2 bg, #991b1b text)
Data & Analytics → tag-data     (#d1fae5 bg, #065f46 text)
IT for Sustain.  → tag-green    (#fef9c3 bg, #854d0e text)
Services managés → tag-services (#ede9fe bg, #5b21b6 text)
```
For sector tags not in this list, pick the closest match or create a new class with similar light-bg/dark-text pattern.

## Step 4 — Compile

Save the MJML file, then compile:

```bash
npx mjml {output}.mjml -o {output}.html
```

Run `npx` from `${CLAUDE_SKILL_DIR}` where the `mjml` package is installed.

## Step 5 — Output

1. **Show the file paths** (MJML + HTML)
2. **Open in browser** for preview
3. **Ask** if the user wants an Outlook draft

### Outlook Draft (on demand)

```python
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)
mail.Subject = f"Digest M&A — {sector} — {geography} — {period}"
mail.HTMLBody = html_content
mail.Display()
```

### Markdown Archive (on demand)

If asked, save a markdown copy: `{date}_digest_{sector}_{geography}.md` with YAML frontmatter, deal table, narratives, and source URLs.

## Quality Checklist

- Every deal from the research file is represented in the email
- Logos load correctly (Logo.dev URLs are well-formed)
- MJML compiles without errors
- No fabricated content — everything comes from the research file
- Tags, dates, and values match the research file exactly
