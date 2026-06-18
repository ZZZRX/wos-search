# Skill: research-ideation-partner

## Purpose
A multi-turn conversational skill that helps researchers brainstorm related 
concepts, identify analogous phenomena, surface relevant theoretical lenses, 
and converge on a set of search terms for systematic literature retrieval.

## Conversation Protocol

### Phase 1: Phenomenon Unpacking
- User describes the phenomenon of interest (e.g., "live streaming commerce")
- AI asks structured questions:
  - What is the core behavioral/organizational mechanism you find interesting?
  - What makes this phenomenon distinct from adjacent ones?
  - Who are the key actors and what decisions do they make?
  - What outcomes matter?

### Phase 2: Analogical Reasoning
- AI suggests historically analogous phenomena and related constructs:
  - "Live streaming commerce involves real-time social influence during 
    purchase. Earlier analogues might include: TV home shopping (QVC model), 
    video product demonstrations, salesperson-customer interaction in retail, 
    influencer marketing, real-time auctions..."
  - For each analogue, AI explains WHY it is related (shared mechanism)
  - User confirms, rejects, or adds analogues

### Phase 3: Theory Scouting
- Based on confirmed analogues and mechanisms, AI suggests theoretical lenses:
  - e.g., parasocial interaction theory, social presence theory, 
    elaboration likelihood model, signaling theory...
  - For each theory, AI provides: source discipline, core logic, 
    how it maps to the phenomenon, 2-3 seminal references

### Phase 4: Search Term Synthesis
- AI produces a structured term map:
  - Core phenomenon terms (and synonyms/variants)
  - Mechanism-level terms
  - Theory-level terms
  - Context/boundary terms
  - Outcome terms
- User iterates on this map

### Phase 5: Search Query Assembly
- User specifies:
  - Target database (Web of Science, Scopus, etc.)
  - Journal scope (ABS rank ≥ X, specific field codes, or named journals)
  - Year range
  - Language constraints
- AI outputs:
  - A ready-to-paste Boolean search string (TS= format for WoS)
  - A journal name filter (SO= format for WoS, using ABS/AJG list)
  - Suggested supplementary searches (for adjacent streams)

## Reference Files Used
- `abs_ajg_journal_list.csv`: ABS Academic Journal Guide with fields and ranks
  (user maintains this file; AI uses it to generate journal name filters)
- `project_state.md`: if available, for contextual continuity

## Output Artifacts
- `search_terms_map.md`: the structured term map from Phase 4
- `wos_query_[topic]_[date].md`: the generated search queries with metadata
  (database, scope, rationale for each term group)

## Example Output (WoS Query)

```text
# Search Query: Live Streaming Commerce — IS/Marketing Journals (ABS 3+)
# Generated: 2026-05-26
# Scope: ABS rank ≥ 3, fields: INFO MAN, MARKETING

## Main Query
TS=("live stream*" OR "livestream*" OR "live commerce" OR "real-time shopping" 
    OR "interactive commerce" OR "shoppertainment")
AND
TS=("consumer" OR "purchase" OR "buyer" OR "engagement" OR "conversion" 
    OR "trust" OR "intention")

## Journal Filter (ABS ≥ 3, INFO MAN + MARKETING)
SO=("MIS Quarterly" OR "Information Systems Research" OR "Journal of MIS" 
    OR "Journal of Marketing" OR "Journal of Marketing Research" 
    OR "Journal of Consumer Research" OR "Marketing Science" 
    OR "Journal of the Academy of Marketing Science" 
    OR "Journal of Retailing" OR "International Journal of Research in Marketing"
    OR "Journal of Interactive Marketing" OR "Electronic Commerce Research and Applications"
    OR "Information and Management" OR "Decision Support Systems" ...)

## Supplementary Search (Analogues)
TS=("video demonstration" OR "product presentation" OR "home shopping" 
    OR "teleshopping" OR "parasocial" OR "social presence")
AND TS=("purchase" OR "consumer" OR "persuasion")