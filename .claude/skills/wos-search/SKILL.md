---
name: wos-search
description: >
  Prepare Web of Science search queries. Two modes: (1) Full 5-phase research
  ideation dialogue for discovering search terms when exploring a new phenomenon,
  (2) Quick mode for direct journal filtering when search terms are already known.
  Uses ABS Academic Journal Guide 2024 for journal quality filtering. Trigger when
  the user wants to search Web of Science, prepare WoS queries, filter journals by
  ABS rating, brainstorm search terms for a research topic, needs SO= journal filter
  expressions, or wants to assemble Boolean search strings for literature retrieval.
---

# WoS Search Skill

## Purpose

Help researchers prepare Web of Science (WoS) Advanced Search queries. This skill
has two operating modes:

- **Full mode**: Multi-round dialogue to unpack a phenomenon, find analogous
  phenomena, identify theoretical lenses, synthesize search terms, and assemble a
  complete WoS query with journal filters.
- **Quick mode**: When the user already has search terms, directly filter journals
  from the ABS list and output a ready-to-paste combined query.

## Mode Detection

Determine the mode from the user's first message:

**Full mode** — The user describes a phenomenon or research interest without
ready-to-use search terms. Examples:
- "I want to research live streaming commerce"
- "Help me think through a literature search on AI agents in organizations"
- "What search terms should I use for platform ecosystems?"

**Quick mode** — The user provides explicit search terms (keywords or Boolean
expressions) and journal requirements. Examples:
- "I need WoS journals for INFO MAN, rating 4 and 4*, search terms: 'live streaming' AND 'consumer'"
- "Filter ABS journals for MKT, rating 3+, with: (AI OR artificial intelligence) AND customer behavior"
- "Give me the SO= filter for STRAT journals, 4 and 4*"

If the user's intent is ambiguous, ask one clarifying question rather than
assuming a mode.

---

## Full Mode: 5-Phase Research Ideation

Guide the user through all five phases. After each phase, briefly summarize and
confirm before proceeding. The user can skip phases or jump ahead at any time.

### Phase 1: Phenomenon Unpacking

Ask these questions, one or two at a time. Let the user respond before asking
the next. Probe deeper when an answer is vague.

1. **Core mechanism**: "What is the behavioral, organizational, or technological
   mechanism you find most interesting about this phenomenon?"
2. **Distinctiveness**: "What makes this phenomenon different from adjacent ones?
   Where would you draw the boundary?"
3. **Actors and decisions**: "Who are the key actors (individuals, organizations,
   platforms, algorithms) and what decisions or actions do they take?"
4. **Outcomes**: "What outcomes matter to you? (e.g., adoption, performance,
   well-being, market outcomes, learning, innovation)"
5. **Context and boundaries**: "Are you focused on specific industries, regions,
   time periods, or technology maturity levels?"

After the user answers, synthesize a 2-3 sentence summary of the phenomenon
definition. Ask the user to confirm before moving to Phase 2.

### Phase 2: Analogical Reasoning

Based on the confirmed phenomenon summary, propose 4-6 historically analogous
phenomena or related constructs. For each analogue, provide:
- The analogue name
- Why it is related (the shared mechanism)
- How it differs from the target phenomenon (boundary clarity)

Format example:
> **Live streaming commerce** involves real-time social influence during purchase.
> Analogues:
> 1. **TV home shopping (QVC model)** — shared: real-time product demonstration,
>    urgency creation, parasocial bond with host. Differs: one-to-many broadcast
>    vs. many-to-many interactive format.
> 2. **In-store salesperson interaction** — shared: dyadic interpersonal
>    persuasion, real-time negotiation. Differs: physical co-presence vs.
>    mediated interaction, synchronous only.

The user confirms, rejects, or adds analogues. Maintain a running list of
confirmed analogues. These feed directly into Phase 4 term generation.

### Phase 3: Theory Scouting

Based on confirmed analogues and mechanisms, suggest 5-8 theoretical lenses.
Organize by analytical level. For each theory, provide:
- Source discipline
- Core logic (1-2 sentences)
- How it maps to the target phenomenon
- 2-3 seminal references (Author, Year, Journal format)

Example:
> **Individual level:**
> - **Parasocial interaction theory** (Communication): Viewers form one-sided
>   relationships with media personalities. Maps to streamer-viewer bond.
>   (Horton & Wohl, 1956, Psychiatry; Rubin & Perse, 1987, JOB)
>
> **Interpersonal level:**
> - **Social presence theory** (IS): Media differ in how much they convey
>   others' presence. Maps to how streaming platforms create co-presence.
>   (Short et al., 1976; Gefen & Straub, 2004, ISR)

The user confirms, rejects, or requests alternatives. Ask which theories they
want to include as search terms.

### Phase 4: Search Term Synthesis

Produce a structured term map with these five categories:

1. **Core phenomenon terms** — the target phenomenon and its direct
   synonyms/variants (include both full terms and wildcard forms)
2. **Mechanism-level terms** — constructs from the confirmed analogues (Phase 2)
3. **Theory-level terms** — construct names and theory labels from Phase 3
4. **Context/boundary terms** — from Phase 1 boundary conditions
5. **Outcome terms** — from Phase 1 outcomes

Present as a table or nested list. The user iterates: add missing terms, remove
irrelevant ones, adjust synonyms and wildcards.

After the user approves, optionally write the term map to `search_terms_map.md`
in the working directory if the user wants to save it.

### Phase 4.5: Term Relevance Assessment

Once the term map is approved and BEFORE building the query, assess which terms
are most relevant so the query stays focused. The default behavior is to present
a tiered assessment; the user can skip it if they want all terms included.

**When to do this:** Always offer this step. The user can say "skip" to use all
terms directly.

**How to assess relevance:** For each term (or term group), assign a tier based
on how central it is to identifying the target phenomenon:

| Tier | Label | Criteria |
|---|---|---|
| ★★★ | **Core** | Terms that uniquely define the phenomenon. A paper about this phenomenon MUST include at least one of these. Without them, the search cannot find the literature. |
| ★★ | **Supporting** | Terms from confirmed analogues, central mechanisms, or primary theories. They add precision and distinguish the phenomenon from adjacent ones. Strongly recommended but not mandatory. |
| ★ | **Peripheral** | Terms that broaden the search — secondary synonyms, adjacent-theory constructs, boundary conditions, or outcomes that could also apply to other phenomena. Better suited for supplementary searches than the main query. |

**How to present the assessment:**

1. Create a compact table for each term category, annotating each group with its tier and a one-sentence rationale
2. After presenting all categories, recommend a tier threshold with reasoning
3. Show the estimated term count reduction (e.g., "Core only: 12 terms → expected ~200 results. Core + Supporting: 35 terms → expected ~500 results. All: 65 terms → expected ~1200 results.")

**Example format:**
```
## Relevance Assessment

### Core phenomenon terms
★★★ "AI fatigue", "artificial intelligence fatigue"  — the phenomenon itself
★★★ "AI tool*", "generative AI", "LLM*"               — the technological agent
★★  "ChatGPT", "Copilot"                               — specific tools; adds precision but may miss papers using generic terms

### Mechanism terms
★★★ "task switching", "cognitive load"                 — central to the phenomenon mechanism
★★  "decision fatigue", "ego depletion"                — from confirmed analogue, strongly supporting
★   "Jevons paradox"                                   — theoretical lens, better suited for supplementary search

...
```

**Let the user choose the threshold:**
- **"Core only"** — highest precision, fewest results, best for discovering the core literature
- **"Core + Supporting"** (recommended) — good balance of recall and precision
- **"All"** — most comprehensive, use when the literature base is very small

After the user chooses, proceed to Phase 5 and assemble the query using only
the selected tiers. Terms dropped from the main query should be offered as
supplementary search candidates instead.

### Phase 5: Search Query Assembly

Ask the user for:

1. **Journal scope**: Which ABS field codes and rating levels?
   - If the user is unsure, run the Python script to list available fields:
     ```bash
     python3 "$SKILL_DIR/scripts/wos_journal_filter.py" --list-fields
     ```
   - If the user says "ABS 3+" or "ABS 3 and above", interpret as ratings
     3, 4, and 4*. Confirm this interpretation.
   - The user can select multiple fields and multiple ratings.

2. **Year range** (optional): e.g., 2015-2024.

3. **Language** (optional, default: English).

4. **Document type** (optional): Article, Review, etc.

Then:

1. Run the Python script to get the `SO=` journal filter:
   ```bash
   python3 "$SKILL_DIR/scripts/wos_journal_filter.py" \
     --fields "INFO MAN" --fields "MKT" --ratings 4 "4*" --format so
   ```
2. Assemble the main Boolean query using `TS=` format, including ONLY terms at
   or above the relevance tier the user selected in Phase 4.5.
3. Assemble supplementary searches using:
   - Terms dropped from the main query (lower-tier terms) as separate, focused searches
   - Adjacent streams from Phase 2 analogues
   - Each supplementary search targeting one theoretical perspective for clean grouping
4. Output everything in a single formatted block.

**Output template:**
```text
# Search Query: [Topic]
# Generated: [YYYY-MM-DD]
# Database: Web of Science Core Collection
# Scope: ABS >= [rating], fields: [field codes]
# Journals matched: [N]
# Relevance tier: [Core only / Core + Supporting / All]

## Main Query
TS=([core phenomenon terms])
AND
TS=([outcome / mechanism terms])
AND
SO=([journal filter from script])

## Supplementary Search (Analogues)
TS=([analogue terms]) AND TS=([outcome terms])
AND
SO=([same journal filter])

## Journal List
[If user requests: list of all matched journal names]
```

Optionally write the output to `wos_query_[topic]_[date].md`.

---

## Quick Mode: Direct Journal Filtering

When the user provides search terms and journal requirements directly:

1. **Parse the request.** Extract:
   - The search terms (Boolean expression or keyword list)
   - ABS field code(s) requested
   - Rating level(s) requested

2. **Clarify ambiguity** with at most one question. For instance, if the user
   says "marketing journals", confirm: "I see 22 ABS field codes including MKT
   (Marketing). Is that the one you want?" Show the exact field codes — never
   guess.

3. **Interpret rating shorthand.** "3+" or "3 and above" means ratings 3, 4,
   and 4*. "Top journals" or "ABS 4" typically means 4 and 4*. Confirm with
   the user if unclear.

4. **Run the Python script:**
   ```bash
   python3 "$SKILL_DIR/scripts/wos_journal_filter.py" \
     --fields "FIELD1" --fields "FIELD2" --ratings R1 R2 --format so
   ```
   Use `$SKILL_DIR` to refer to the directory containing this SKILL.md file.
   The script lives at `$SKILL_DIR/scripts/wos_journal_filter.py`.

5. **Combine and output.** Merge the user's search terms with the `SO=` clause
   into a complete WoS query. Report the number of journals matched.

6. **Optional: list journals.** Ask if the user wants to see the list of matched
   journal names for verification.

**Quick mode output template:**
```text
# Search Query: [Topic]
# Generated: [YYYY-MM-DD]
# Scope: ABS >= [rating], fields: [field codes]
# Journals matched: [N]

TS=([user's search terms])
AND
SO=([journal filter from script])
```

---

## Python Script Reference

The helper script `wos_journal_filter.py` is located at:
`$SKILL_DIR/scripts/wos_journal_filter.py`

**Journal name cleaning:** The script automatically cleans journal titles to match
WoS source publication names:
- Strips parenthetical content (ABS disambiguators like "(JASIST)", "(UK)", etc.)
- Converts "and" to "&" for 18 journals whose official WoS title uses the ampersand
  form (e.g., Information & Management, Psychology & Marketing, R&D Management,
  Science, Technology, & Human Values)

**Before first use**, verify `openpyxl` is installed:
```bash
python3 -c "import openpyxl" 2>&1 || pip3 install openpyxl
```

**Available commands:**

```bash
# List all 22 ABS field codes with journal counts
python3 "$SKILL_DIR/scripts/wos_journal_filter.py" --list-fields

# List available rating levels
python3 "$SKILL_DIR/scripts/wos_journal_filter.py" --list-ratings

# Filter and output in various formats
python3 "$SKILL_DIR/scripts/wos_journal_filter.py" \
  --fields "INFO MAN" --ratings 4 "4*" --format so

python3 "$SKILL_DIR/scripts/wos_journal_filter.py" \
  --fields ALL --ratings 3 4 "4*" --format count

python3 "$SKILL_DIR/scripts/wos_journal_filter.py" \
  --fields "MKT" --fields "STRAT" --ratings 4 "4*" --format list

python3 "$SKILL_DIR/scripts/wos_journal_filter.py" \
  --fields "OPS&TECH" --ratings 1 2 3 4 "4*" --format csv
```

**Format options:**
| Format | Output |
|--------|--------|
| `so` | `SO=("Journal A" OR "Journal B" OR ...)` (default) |
| `ts` | `TS=("Journal A" OR "Journal B" OR ...)` |
| `list` | One journal title per line |
| `count` | Integer count of matched journals |
| `csv` | CSV with ID, Field, Title, AJG_2024 columns |

**Field code matching** is case-insensitive. `--fields "info man"` matches
`INFO MAN`. The script auto-detects the `ABS2024.xlsx` path by looking in
the project root directory.

**Character limit warning:** The script prints a warning to stderr if the
`SO=` clause exceeds 6000 characters. WoS Advanced Search has an ~8000
character limit. If warned, suggest the user split the search by rating
tier or field group.

---

## WoS Advanced Search Syntax Reference

| Element | Format | Example |
|---------|--------|---------|
| Topic (title, abstract, keywords) | `TS=(...)` | `TS=("live stream*" OR "livestream*")` |
| Title only | `TI=(...)` | `TI=("green" AND "supply chain")` |
| Journal / Source name | `SO=(...)` | `SO=("MIS Quarterly")` |
| Boolean AND | `AND` | `TS=(A) AND TS=(B)` |
| Boolean OR | `OR` | `TS=("term A" OR "term B")` |
| Wildcard (any chars) | `*` | `stream*` → stream, streaming, streamed |
| Wildcard (single char) | `?` | `wom?n` → woman, women |
| Exact phrase | `"..."` | `"live streaming commerce"` |
| Proximity | `NEAR/n` | `consumer NEAR/5 trust` |
| Parentheses for grouping | `(...)` | `(TS=(A) AND SO=(X)) OR (TS=(B) AND SO=(Y))` |
| Publication year | `PY=(...)` | `PY=(2015-2024)` |
| Language | `LA=(...)` | `LA=(English)` |
| Document type | `DT=(...)` | `DT=(Article)` |

**Tips:**
- Use wildcards liberally for morphological variants: `organi?ation*` matches
  organization, organisation, organizational, organisationally.
- Group related terms with OR within `TS=()` blocks, then combine blocks with AND.
- For interdisciplinary topics, consider running separate searches per field
  group to avoid overly broad SO= clauses.
- The default search field `TS=` covers Title, Abstract, Author Keywords, and
  Keywords Plus.

---

## Edge Cases and Guardrails

- **Unknown field codes**: If the user provides a field code that doesn't match
  any of the 22 ABS fields, the Python script returns 0 results. Always run
  `--list-fields` first if the user seems uncertain.
- **Very large journal sets**: If the user requests many fields at high ratings,
  the SO= clause may be long. Always report the journal count first. If the
  clause might exceed the WoS limit, proactively suggest splitting.
- **No matching journals**: If the script returns 0 journals, suggest relaxing
  the rating threshold or broadening the field scope.
- **The user says "top journals"**: Interpret as 4 and 4* (not just 4).
  Confirm with: "I'll include ABS 4 and 4* journals. Does that match what
  you had in mind?"
- **Full mode to quick mode transition**: If during full mode the user says
  "just give me the journal filter for X and Y", switch to quick mode
  immediately. Don't force the full dialogue.
- **Saving output**: Offer to save the query to a `.md` file. The user may
  want to keep a record or share it. Default filename:
  `wos_query_[topic_slug]_[YYYY-MM-DD].md`.
- **Skipping relevance assessment**: If the user says "skip" or "use all terms"
  during Phase 4.5, proceed directly to Phase 5 with all terms. Do not force
  the assessment.
- **Relevance assessment in quick mode**: Quick mode skips the 5-phase flow, so
  relevance assessment does not apply. However, if a quick-mode query looks
  overly broad, suggest narrowing it and offer to assess relevance.
- **WoS character limit vs. trimmed terms**: If even the trimmed query approaches
  the WoS ~8000 character limit, suggest splitting by term category (e.g.,
  phenomenon terms + mechanism terms in one query, theory terms in a
  supplementary search).
