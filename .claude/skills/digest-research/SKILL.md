---
name: digest-research
description: "Research recent M&A acquisitions for a given sector and geography. Searches the web thoroughly, structures findings into a standardized markdown file that can be reviewed, edited, and fed into /digest to generate the email. Use when the user asks to find deals, research acquisitions, or as the first step of the digest workflow."
argument-hint: "[free text: sector, geography, period, language...]"
allowed-tools: WebSearch WebFetch Read Write Bash(mkdir *)
---

# M&A Deal Research — Auraïa Capital Advisory

You research recent M&A acquisitions and produce a structured markdown file ready for review and email generation.

## Input

`$ARGUMENTS`

Extract: sector, geography, time period, language. Ask if not said first.

## Research Process

This is your entire job. The value depends on finding real deals.

**Think like an M&A analyst doing competitive intelligence, not like someone running a single Google search.**

1. Search in multiple languages (French + English minimum — deals are often reported in English first)
2. Use varied queries: sector-specific terms, "acquisition", "rachat", "takeover", company names, trade press
3. Follow leads from summary articles to primary sources (press releases, regulatory filings)
4. Dig into sector-specific publications, not just general news
5. Deduplicate across sources — same deal reported by multiple outlets

For each deal found, capture ALL of the following:
- **Acquéreur** — who's buying, brief description if not well-known
- **Cible** — who's being acquired, what they do, size indicators (revenue, employees, offices)
- **Montant** — deal value if public, or "Non divulgué". Specify the nature: VE (Valeur d'Entreprise), equity value, or transaction value
- **Type de date** — "Annoncé" or "Closing" (whichever is reported)
- **Date** — the actual date
- **Pays** — where the target is based
- **Secteur tag** — specific sub-sector label (e.g. "Cloud & Infra", "Cybersécurité", "Data & Analytics")
- **Domaine acquéreur** — the acquirer's website domain (e.g. `accenture.com`, if you're unsure, check online so you don't hallucinate one) — needed for logo retrieval later
- **Contexte stratégique** — 1-3 sentences on the *why*. What does the acquirer gain? What's the market context? Consolidation trend? Geographic expansion? Tech play?
- **Source** — URL of the primary source

## Output Format

Save the file as: `{date}_research_{sector}_{geography}.md`

Use this exact structure:

```markdown
---
date: {today}
sector: {sector}
geography: {geography}
language: {language}
period: {period description}
deal_count: {number}
---

# Synthèse

{2-4 sentences on overall M&A activity and trends for this sector/geography/period. The kind of paragraph a senior partner reads to get the pulse.}

# Deals

## {Acquéreur} → {Cible}
- date_type: {Annoncé|Closing}
- date: {YYYY-MM-DD}
- country: {pays}
- value: {€XXM ou Non divulgué}
- value_type: {VE est.|Equity value|Transaction value|—}
- sector_tag: {tag}
- acquirer_domain: {domain.com}
- source: {URL}

{Contexte stratégique: 1-3 phrases}

## {Acquéreur 2} → {Cible 2}
...
```

**Important formatting rules:**
- Order deals by significance (biggest/most strategic first)
- The first deal should be the most noteworthy one (it will be highlighted in the email)
- Metadata fields use the exact names above (the email generator parses them)
- Keep sector tags short (2-3 words max)
- One source URL per deal (the best/most detailed one)

## After saving

Tell the user:
1. The file path
2. How many deals were found
3. A quick summary (e.g. "5 deals trouvés, dominés par la consolidation cloud")
4. Remind them they can review/edit the file, then run `/digest {filename}` to generate the email

## Quality checklist

- **Completeness** — Missing a major deal is the worst failure mode
- **Accuracy** — Every fact comes from a source. Never fabricate deals.
- **Dates** — Always specify if it's announcement or closing date
- **Values** — Always specify what the number represents (VE, equity, etc.)
- If nothing is found: say so honestly and suggest broadening criteria
