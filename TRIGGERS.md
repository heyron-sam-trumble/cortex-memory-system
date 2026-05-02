# Cortex — Triggers

**The memory system that learns and grows.**

---

## Architecture

Cortex is a two-layer memory system:

| Layer | Storage | Purpose |
|-------|---------|---------|
| Session Memory | `memory/YYYY-MM-DD.md` | Instant recall - loads last 7 days on startup |
| Cortex DB | `cortex_memory_bank.db` | Long-term storage - enriches fuzzy context OR cold start recall |

---

## User Triggers

| Trigger | Action |
|---------|--------|
| `log this: [info]` | Agent saves to daily log in GIGO format |
| `huddle` | Agent generates quality session summary in GIGO format. Skip if no messages. |
| `sync` | Agent reloads all memory files |
| `full sync` | Agent does full system check + Git backup |

## System Triggers (Agent-Invoked)

| Trigger | When | Action |
|---------|------|--------|
| `cortex backup` | Weekly cron / manual | Agent extracts GIGO entries (>48hrs), inserts to Cortex DB, archives files |
| `cortex check` | Before backup | Agent shows preview of what would sync (dry-run) |

---

## log this:

**Save to daily memory with GIGO format.**

```
log this: Jane found great API documentation site today
```

→ Saves to today's log in GIGO format: Context, Why, What, Decision, Outcome

**GIGO Format:** Great In Great Out - structured entries ensure quality input = quality output

---

## Memory Flow

1. **Session Start:** Loads last 7 days → instant recall
2. **Daily:** GIGO entries go to `memory/YYYY-MM-DD.md`
3. **Weekly:** `cortex backup` → extracts GIGO, inserts to Cortex DB, archives files
4. **When needed:** Cortex DB enriches fuzzy context OR provides cold-start history

---

## Cortex DB Schema

The Cortex database uses GIGO format:

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Auto-increment primary key |
| date | TEXT | Date of the memory entry |
| topic | TEXT | Short label for the entry |
| context | TEXT | What happened |
| why_it_matters | TEXT | Why this is significant |
| what_we_tried | TEXT | Actions taken |
| decision | TEXT | What was decided |
| outcome | TEXT | What actually happened |
| source_log | TEXT | Which memory file this came from |
| stored_at | TEXT | Timestamp when inserted into Cortex DB |

---

## Setup

Open `SKILL.md` and copy the memory rules from the Integrating with Your `AGENTS.md` section into your existing `AGENTS.md`. At minimum, add:

- **Memory Startup** — loads last 7 days + MEMORY.md at session start
- **User Triggers** — log this:, huddle, sync, full sync
- **Cortex Query Logic** — proactive DB querying when context is fuzzy

The installer never touches your `AGENTS.md` directly, so your existing configuration is always safe.

---

## Agent Behavior - When to Query Cortex (IMPORTANT)

**This is NOT a user trigger** — the agent proactively queries Cortex when needed.

**When agent should query Cortex:**
- Context is fuzzy — agent needs to enrich what it remembers
- No current context (cold start) — fresh session, needs history
- User asks about past decisions, projects, or info from >7 days ago

**How agent queries:**
```bash
python3 scripts/query_cortex.py "search term"
```

Returns matching entries from Cortex DB with relevance scores.

---

## Configuration

For trigger state tracking (prevents duplicate entries), see [TRIGGER_STATE_GUIDE.md](TRIGGER_STATE_GUIDE.md).

---

*Cortex — the Total Recall Memory System 🧠*
