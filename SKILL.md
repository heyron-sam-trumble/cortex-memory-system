# Cortex — Total Recall Memory Skill

**You are an agent with persistent memory. This skill tells you how to use it.**

Cortex is a two-layer memory system that keeps you informed across sessions. Session memory gives you the last 7 days instantly. The Cortex database gives you everything beyond that when context is fuzzy or cold.

---

## Memory File Naming Convention

**Critical — the entire system depends on this.**

Daily memory logs must be named using ISO 8601 date format:

```
memory/YYYY-MM-DD.md
```

Examples: `memory/2026-05-02.md`, `memory/2026-04-28.md`

This naming convention is not optional. The session startup loader, the 7-day window calculation, and the `cortex backup` sync script all parse filenames to determine dates. A file named anything else — `today.md`, `log-02-05.md`, `notes.md` — will be silently ignored by every part of the system.

When writing a new daily log entry, always check today's date and use it exactly. Do not reuse yesterday's file.

---

## Session Start — Do This Every Time

When a session begins, load memory automatically. No user trigger needed.

1. Read all files in `memory/` matching the pattern `YYYY-MM-DD.md` dated within the last 7 days
2. Read `memory/MEMORY.md` if it exists — this is the promoted long-term reference layer
3. Say nothing about this to the user unless relevant — just use what you loaded

If `memory/` is empty or missing, treat this as a cold start. Query Cortex DB proactively (see below).

---

## User Triggers

Respond to these commands whenever the user sends them:

| Trigger | What to do |
|---------|------------|
| `log this: [info]` | Save a GIGO entry to today's daily log (`memory/YYYY-MM-DD.md`) |
| `huddle` | Generate a session summary in GIGO format. Skip silently if nothing meaningful happened. |
| `sync` | Reload all files in `memory/` |
| `full sync` | Reload memory files + run a Git backup of the workspace |

### Example — `log this:`

```
User: log this: Jane confirmed the API keys will be rotated before the deployment window
Agent: Saved to memory.

**Context:** Jane confirmed API key rotation ahead of scheduled deployment
**Why it matters:** Unblocks the deployment — keys must be rotated first or the service will reject auth
**What we tried:** Chased confirmation after two days without a response
**Decision:** Proceed with deployment once Jane confirms rotation is done
**Outcome:** Pending
```

### Example — `huddle`

```
User: huddle
Agent: Session summary saved.

## API rate limiting investigation — 2026-05-02
**Context:** Investigated why the overnight batch job was hitting rate limit errors on the third-party data feed
**Why it matters:** Job failures mean stale data in the dashboard — users are seeing yesterday's numbers
**What we tried:** Reviewed API docs, checked request volume, tested with reduced batch size
**Decision:** Split batch into two smaller windows — 2am and 4am — to stay under the hourly limit
**Outcome:** Test run completed without errors; monitoring overnight to confirm
```

---

## System Triggers — Agent-Invoked

These run on schedule or when you decide they are needed. They are not user commands.

| Trigger | When | What to do |
|---------|------|------------|
| `cortex backup` | Weekly (or manually) | Extract GIGO entries older than 48hrs from daily logs, insert into Cortex DB, archive source files |
| `cortex check` | Before running backup | Preview what would sync — show the user, write nothing yet |

Run `cortex backup` by invoking:
```bash
python3 scripts/memory_log_sync_to_cortex.py
```

---

## GIGO Format — How to Write Memory Entries

GIGO stands for **Great In, Great Out** — a deliberate inversion of the usual "Garbage In, Garbage Out". The principle is simple: structured, thoughtful input produces memory that is actually useful to retrieve. Vague input produces noise.

Every entry you save — whether from `log this:` or `huddle` — must use this structure. You do the summarisation. Do not dump raw conversation text.

```
**Context:** What happened — the raw facts
**Why it matters:** Why this is significant to the user
**What we tried:** Actions or approach taken
**Decision:** What was decided or concluded
**Outcome:** What actually happened as a result
```

Always add a short topic label above the GIGO block:
```
## API rate limit fix — 2026-05-02
```

If an entry does not have a clear Decision or Outcome yet, write `Pending` — do not pad it. Incomplete but honest entries are more useful than vague ones.

---

## Proactive Cortex Queries — When to Do This Without Being Asked

Query the Cortex database on your own when:

- The user references something from more than 7 days ago
- You are in a cold start with no recent memory loaded
- Context is fuzzy and you suspect there is more

```bash
python3 scripts/query_cortex.py "search term"
```

The script searches across four fields: `topic`, `context`, `what_we_tried`, and `outcome`. It does not search `why_it_matters` or `decision`. Choose search terms that are likely to appear in those four fields — the topic label, what actually happened, or what the outcome was. Searching for a decision keyword alone will not match unless that word also appears elsewhere in the entry.

Use 2–3 word search terms. Summarise what you found and how it relates — do not dump raw DB output. You do not need to tell the user you queried Cortex. Just use the results naturally.

---

## Deduplication

Before writing a `log this:` or `huddle` entry, check `configs/trigger_state.json` for the current source. If one has already run recently for this session or channel, skip it and tell the user why.

Each platform source (Discord channel, Telegram chat, console) tracks separately. See the Configuration section below.

---

## Integrating with Your AGENTS.md

The installer never touches your existing `AGENTS.md`. Copy these sections into it manually.

### Memory Startup

```markdown
## Memory Startup

At session start, load:
1. Last 7 days from `memory/YYYY-MM-DD.md` — instant recall
2. `MEMORY.md` — curated long-term notes
```

### User Triggers

```markdown
## Memory Triggers

| Trigger | Action |
|---------|--------|
| `log this: [info]` | Save to daily log in GIGO format (Context, Why, What, Decision, Outcome) |
| `sync` | Reload all memory files |
| `full sync` | Full system check + Git backup |
| `huddle` | Generate session summary in GIGO format. Skip if no messages. |
```

### System Triggers

```markdown
## Memory System Triggers

| Trigger | When | Action |
|---------|------|--------|
| `cortex backup` | Weekly cron | Extract GIGO entries from `memory/`, insert to Cortex DB, archive processed files |
| `cortex check` | Before backup | Preview what would sync (dry-run) |
```

### Cortex Query Logic

```markdown
## Cortex Query Logic

Query Cortex DB when:
- Context is fuzzy — needs enrichment
- Cold start — no recent memory, needs history
- User asks about decisions or topics from more than 7 days ago

Query command:
    python3 scripts/query_cortex.py "<search_term>"

This is proactive agent behaviour, not a user command. Use results naturally.
```

### GIGO Format

```markdown
## Memory Writing (GIGO)

Every memory entry uses 5 fields:

| Field | Description |
|-------|-------------|
| **Context** | What happened |
| **Why it matters** | Why this is significant |
| **What we tried** | Actions taken |
| **Decision** | What was decided |
| **Outcome** | What resulted |

The agent does summarisation, not scripts. Great In, Great Out.
```

---

## Integrating with Your MEMORY.md

Add these sections to your existing `MEMORY.md` if not already present:

```markdown
## Memory Logging

**Format:** `log this: [your info]`

- Saves to `memory/YYYY-MM-DD.md` in GIGO format
- Session loads last 7 days for instant recall

## Memory Layers

- **Session Layer:** Last 7 days loaded at start → instant recall
- **Cortex Layer:** Long-term DB → enriches fuzzy context or cold start

Run `cortex backup` weekly to populate Cortex DB.
```

---

## Configuration

### Trigger State (`configs/trigger_state.json`)

Tracks when `huddle` and `log this:` last ran per source to prevent duplicates.

**Simple setup (single platform):**
```json
{
  "huddle": {
    "default": { "last_time": null }
  },
  "log_this": {
    "default": { "last_time": null }
  },
  "last_updated": ""
}
```

**Example — multi-platform setup:**
```json
{
  "huddle": {
    "1234567890123456789": { "last_time": "2026-05-02T09:30:00.000Z" },
    "telegram:-100123456789": { "last_time": "2026-05-02T10:15:00.000Z" }
  }
}
```

| Platform | Key format | Example |
|----------|------------|---------|
| Discord | Channel ID | `1234567890123456789` |
| Telegram | `telegram:chat_id` | `telegram:-100123456789` |
| Console | `console` | `console` |

You can ask your agent to configure this directly — for example: *"Hook up trigger_state for Discord channel #general"* — it will detect the platform and update the config with the correct channel ID.

### Greeting State (`configs/greeting_state.json`)

Prevents repeated full greetings within the same day.

```json
{
  "last_greeted": "YYYY-MM-DD",
  "last_greeted_time": "HH:MM"
}
```

- If `last_greeted` does not match today → full greeting
- If it matches → brief acknowledgement only

Create if missing:
```bash
mkdir -p configs
echo '{"last_greeted": "", "last_greeted_time": ""}' > configs/greeting_state.json
```

---

## File Layout

```
cortex/skill/
├── scripts/
│   ├── huddle.cjs                    # Session summaries
│   ├── memory_log_sync_to_cortex.py  # Weekly sync to Cortex DB
│   └── query_cortex.py               # Query long-term memory
├── db/
│   └── cortex_memory_bank.db         # SQLite — GIGO schema
├── configs/
│   └── trigger_state.json            # Per-source trigger tracking
├── README.md                         # Overview and quick start
├── INSTALL.md                        # Full installation guide
├── SKILL.md                          # This file — agent instructions + integration guide
├── TRIGGERS.md                       # Full trigger reference
├── TRIGGER_STATE_GUIDE.md            # Trigger state config guide
├── OUR_STORY_SO_FAR.md               # Background and design decisions
├── install.sh                        # Auto-install
└── LICENSE                           # MIT
```

---

## Installing This Skill

```bash
# Copy skill to workspace
cp -r skill/ ~/workspace/cortex/skill/

# Run installer
cd ~/workspace
chmod +x cortex/skill/install.sh
./cortex/skill/install.sh

# Add memory rules to your AGENTS.md
# Copy the sections from the "Integrating with Your AGENTS.md" section above
```

⚠️ The installer does not touch your existing `AGENTS.md`. You merge manually. This is intentional — your config is yours.

---

## What This Skill Does Not Do

- Does not write to your `AGENTS.md` automatically
- Does not write to your `MEMORY.md` automatically — that file is managed by the agent or user directly
- Does not share memory between users or containers
- Does not capture regular chat messages — only entries created with `log this:` or `huddle` will sync to Cortex DB
- Does not use embeddings or vector search — recall is keyword-based via SQLite

---

*Cortex — the Total Recall Memory System 🧠*
*Built for Heyron Agent Jam #1 — May 2026*
