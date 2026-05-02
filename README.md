# Cortex — the Total Recall Memory System

**Drop-in memory system for AI agents — remembers between sessions.**

---

## The Problem

Every chat, your AI forgets everything. Cortex solves this with a two-layer memory system:

| Layer | What | When |
|-------|------|------|
| **Session** | Last 7 days loaded at start | Instant recall |
| **Cortex DB** | Long-term storage | Query when needed |

## Prerequisites

- **Python 3.x** — required for scripts
- **SQLite** — built into Python standard library, no separate install needed
- **OpenClaw** — or compatible agent framework

---

## Why Cortex Works

1. **Agent does summarization** — GIGO format (Context, Why, What, Decision, Outcome)
2. **Two-layer architecture** — Fast session memory + searchable DB
3. **Proactive recall** — Agent queries DB when context is fuzzy
4. **Deduplication** — Same topic + context = no duplicate entries

---

## Quick Start

```bash
# 1. Copy skill to workspace
cp -r skill/ ~/workspace/cortex/skill/

# 2. Run installer
cd ~/workspace
chmod +x cortex/skill/install.sh
./cortex/skill/install.sh

# 3. Copy memory rules into your AGENTS.md (see SKILL.md)
```

That's it. See [INSTALL.md](INSTALL.md) for full details.

---

## Commands

| Trigger | Action |
|---------|--------|
| `log this: [info]` | Save to daily log in GIGO format |
| `huddle` | Session summary in GIGO. Skip if no messages. |
| `sync` | Reload all memory files |
| `full sync` | Full check + Git backup |
| `cortex backup` | Extract GIGO → sync to DB → archive |
| `cortex check` | Preview what would sync (dry-run) |

---

## What's Included

```
cortex-memory-system/
├── scripts/
│   ├── huddle.cjs
│   ├── memory_log_sync_to_cortex.py
│   └── query_cortex.py
├── db/
│   └── cortex_memory_bank.db
├── configs/
│   └── trigger_state.json
├── README.md
├── INSTALL.md
├── SKILL.md
├── TRIGGERS.md
├── TRIGGER_STATE_GUIDE.md
├── OUR_STORY_SO_FAR.md
├── install.sh
└── LICENSE
```

---

## GIGO Format

**GIGO = Great In, Great Out** — we inverted the traditional "Garbage In, Garbage Out" concept.

In data terms, GIGO is a 5-field structure that maps directly to our Cortex DB schema:

| GIGO Field | DB Field | Why It Matters |
|------------|----------|----------------|
| Context | context | What happened — the raw facts |
| Why it matters | why_it_matters | Significance — why this matters to the user |
| What we tried/did | what_we_tried | Actions — what approach we took |
| Decision | decision | Conclusion — what was decided |
| Outcome | outcome | Result — what actually happened |

**Key insight:** The agent does summarization, not scripts. We structured it this way because:
- **Context** = raw data
- **Why** = filters noise (if it doesn't matter, skip it)
- **What** = action taken
- **Decision** = the actual insight
- **Outcome** = proof it worked

Quality input = quality output. Every entry forces the agent to think, not just log.

---

## Database

Cortex DB uses SQLite with GIGO schema. The included `cortex_memory_bank.db` has one sample entry (not real data).

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
| retrieved_count | INTEGER | How many times this entry has been queried |
| last_retrieved_at | TEXT | Timestamp of last retrieval |
| promoted | INTEGER | Whether entry has been promoted (0/1) |
| promoted_to | TEXT | Destination if promoted |

---

## Setup Summary

1. Copy `skill/` to your workspace
2. Run `install.sh`
3. Open `SKILL.md` and copy the memory rules from the Integrating with Your `AGENTS.md` section into your existing `AGENTS.md`
4. Restart your agent (to load new rules)
5. In chat, use triggers to create GIGO entries:
   - `log this: [info]` — saves single entry
   - `huddle` — generates session summary
6. Check `memory/` folder — daily logs appear here
7. Agent runs `cortex backup` weekly — extracts GIGO entries from logs, syncs to DB

⚠️ **Important:** cortex backup only extracts entries that use GIGO format. Regular chat messages won't sync — you must use the triggers (log this:, huddle) to create structured entries.

**Existing memory?** Convert old logs to GIGO format — review each entry, structure it with the 5 fields, add to the `## GIGO Extracted Memories` section. That's exactly what we did to get started.

---

*Cortex — the Total Recall Memory System 🧠*
*Built for Heyron.ai Agent Jam #1 - May 2026*
