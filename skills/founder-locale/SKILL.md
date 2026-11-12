---
name: founder-locale
description: >-
  Sets the country for the founder pack. Loads a country pack (Malaysia first)
  with the local currency, languages, business registration, tax and invoicing
  rules, payroll costs, licences, trademark registry, payment methods, sales
  channels and trading calendar, re-checks the figures that change against the
  official source, and writes founder/locale.md so every other founder skill
  works with local facts instead of North American defaults. Use when the user
  says "I am in Malaysia", "localise this", "set the country", "use ringgit",
  "what are the local rules", or starts the founder pack outside the United
  States.
argument-hint: "[country name or ISO code, e.g. MY]"
---

# founder-locale

A business plan written for Toronto does not survive contact with Kuala Lumpur.
The price is in the wrong currency, the trademark check points at the wrong
registry, the payroll line is missing the statutory contributions, and the
marketing plan ignores the apps people there actually use. This skill fixes that
once, in one file, and the rest of the pack reads it.

What the user typed after `/founder-locale`: `$ARGUMENTS`

## Step 1: which country

Take it from, in this order: what the user typed, the `Country:` line in
`founder/idea.md`, or the conversation. If none of those says, ask once. A
business that sells in several countries gets one locale file per run: start
with the country where it registers and opens first.

## Step 2: load the pack

Country packs live in this skill's folder, one file per country, named by the
two-letter ISO code. Malaysia is `${CLAUDE_SKILL_DIR}/packs/MY.md`. If that path
is not expanded, use the base directory Claude Code printed for this skill.

If there is no pack for the country, do not stop. Build the locale from official
sources using `${CLAUDE_SKILL_DIR}/packs/TEMPLATE.md` as the checklist, mark the
result `Status: unreviewed`, and tell the user that nobody local has checked it
yet. Offer to turn it into a pack they can contribute.

## Step 3: re-check what changes

A pack is a map, not the territory. Every pack is dated, and rates, thresholds
and wage floors move, sometimes more than once a year. Before writing a figure
into the locale file:

1. If you can search or fetch, open the official source the pack links for that
   figure and confirm it. Official means the regulator or the government's own
   site, not a blog about it.
2. If the figure changed, use the new one, and say what changed and when.
3. If you cannot reach the source, carry the pack's figure with its "as of" date
   and mark it `unconfirmed`.

Never present a figure as current without one of those three.

## Step 4: write the locale file

Write `founder/locale.md` in the user's project, in this shape:

```markdown
# Locale: <country>

Pack: <code>, dated <pack date>. Checked on <today>. Status: <reviewed | unreviewed>.

## Basics
Currency, how prices are written, languages, how income is quoted.

## For the board and the idea
## For competitors
## For the consumer panel
## For pricing and the offer
## For the CFO
## For marketing and brand
## For operations
## For launch

## Confirm with a professional
The items a local accountant, lawyer or the authority must confirm.

## Sources
Every official link used, with the date it was checked.
```

Keep it short. Each section holds only what changes the work of that skill in
this country. Copy nothing that the business does not need: a consultancy with
no staff does not need the food handling rules.

Also add or correct the `Country:` line in `founder/idea.md`.

## Step 5: tell the user

In a few lines: the country set, the three local facts most likely to change
their plan (for example a tax registration threshold they are near, a payroll
cost they had not counted, a licence with a long lead time), and anything marked
unconfirmed. Then suggest the next skill.

## Rules

- Official sources, linked, with the date checked. No figure without a source.
- This is a checklist of what to confirm, not legal, tax or financial advice.
  Say so once.
- Do not guess a rule for a country with no pack. Say what you could not
  confirm.
- Local culture goes in as buying behaviour the user can verify (which apps,
  which paydays, which festivals move sales), never as a stereotype about a
  group of people.
- The Python tools in this pack still print `$`. Until they take a currency
  setting, tell the user to read `$` as the local currency.

## Output

`founder/locale.md`, and the `Country:` line in `founder/idea.md`. Next:
`/founder-board` on a new idea, or re-run whichever skill the locale changes
most (usually `/founder-cfo` and `/founder-ops`).

## Adding a country

Copy `packs/TEMPLATE.md` to `packs/<ISO code>.md`, fill each section from
official sources, date it, and open a pull request. A pack written by someone
who has registered and run a business in that country is worth ten written from
search results.
