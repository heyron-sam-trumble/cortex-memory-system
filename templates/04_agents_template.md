# 04_agents_template.md — AGENTS.md Reference for Total Recall (Cortex)

> This is a **reference template** showing the memory rules to add to your existing `AGENTS.md`.
> Do NOT replace your AGENTS.md with this file — copy the relevant sections into it instead.

---

## Memory Startup

Add this to your AGENTS.md to load memory at session start:

```markdown
## Memory Startup

At session start, load:
1. Last 7 days from `memory/YYYY-MM-DD.md` — instant recall
2. `MEMORY.md` — curated long-term notes
```

---

## User Triggers

Add this table to your AGENTS.md:

```markdown
## Memory Triggers

| Trigger | Action |
|---------|--------|
| `log this: [info]` | Save to daily log in GIGO format (Context, Why, What, Decision, Outcome) |
| `sync` | Reload all memory files |
| `full sync` | Full system check + Git backup |
| `huddle` | Generate quality session summary in GIGO format. Skip if no messages. |
```

---

## System Triggers (Agent-Invoked)

```markdown
## Memory System Triggers

| Trigger | When | Action |
|---------|------|--------|
| `cortex backup` | Weekly cron | Extract GIGO entries from `memory/`, insert to Cortex DB, archive processed files |
| `cortex check` | Before backup | Preview what would sync (dry-run) |
```

---

## Cortex Query Logic (Agent Behavior)

**IMPORTANT:** This is NOT a user trigger — the agent proactively queries when needed.

```markdown
## Cortex Query Logic (Agent Behavior)

Query Cortex DB when:
- **Context is fuzzy** — needs to enrich what it remembers
- **Cold start** — new session, no recent context, needs history trail
- **User asks about past topics** — decisions, projects, or info from >7 days ago

Query command:
    python3 scripts/query_cortex.py "<search_term>"

Response handling:
1. If results found → incorporate naturally into response
2. If no results → acknowledge gap honestly

Key: This is proactive agent behaviour, NOT a user command.
```

---

## GIGO Format

```markdown
## Memory Writing (GIGO)

Every memory entry uses 5 fields:

| Field | Description |
|-------|-------------|
| **Context** | What happened |
| **Why it matters** | Importance |
| **What we tried/did** | Actions taken |
| **Decision** | Outcome of discussion |
| **Outcome** | Result |

The AGENT does summarization, not scripts. Quality input = quality output.
```

---

## File Locations

```markdown
## Cortex File Locations

| File | Purpose |
|------|---------|
| `memory/YYYY-MM-DD.md` | Daily session logs |
| `db/cortex_memory_bank.db` | Long-term SQLite storage |
| `scripts/query_cortex.py` | Query script |
| `scripts/memory_log_sync_to_cortex.py` | Weekly sync script |
```

---

*Template for Total Recall (Cortex) — Agent Jam #1*
*Copy these sections into your existing AGENTS.md — do not replace it.*
