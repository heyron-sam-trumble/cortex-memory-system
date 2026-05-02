# Total Recall (Cortex) — Installation

**Time:** 5 minutes  
**Requirement:** OpenClaw workspace, **Python 3.x**

---

## Quick Install

```bash
# 1. Copy skill folder to workspace
cp -r skill/ /path/to/your/workspace/projects/agent-jam-1/

# 2. Run installer
cd /path/to/your/workspace
chmod +x projects/agent-jam-1/skill/install.sh
./projects/agent-jam-1/skill/install.sh

# 3. Copy memory rules into your AGENTS.md (see templates/04_agents_template.md)
```

---

## What Happens

1. Creates `memory/`, `configs/`, `db/`, `scripts/` directories
2. Copies `scripts/` — huddle.cjs, memory_log_sync_to_cortex.py, query_cortex.py
3. Copies `db/cortex_memory_bank.db` — SQLite database with GIGO schema
4. Copies `configs/trigger_state.json` — tracks last trigger times
5. Copies `templates/` — including `04_agents_template.md`, the memory rules merge guide
6. Copies `TRIGGERS.md` — trigger documentation
7. Copies `TRIGGER_STATE_GUIDE.md` — trigger config guide

> ℹ️ The installer does **not** touch your `AGENTS.md`. Memory rules are provided in `templates/04_agents_template.md` for you to merge in manually — this way your existing agent configuration is never overwritten.

---

## Important: Manual Setup Required

After running the installer, you need to:

1. **Merge memory rules into your AGENTS.md:**
   - Open `templates/04_agents_template.md`
   - Copy the sections relevant to your setup into your existing `AGENTS.md`
   - At minimum, add: Memory Startup, User Triggers, and Cortex Query Logic

2. **Configure trigger_state.json** (optional):
   - See [TRIGGER_STATE_GUIDE.md](TRIGGER_STATE_GUIDE.md) for platform-specific setup

---

## Included Components

```
skill/
├── scripts/                    # Memory scripts
│   ├── huddle.cjs              # Capture session summaries
│   ├── memory_log_sync_to_cortex.py  # Weekly sync to Cortex DB
│   └── query_cortex.py        # Query long-term memory
├── db/                        # SQLite database
│   └── cortex_memory_bank.db # Long-term storage with GIGO schema
├── configs/
│   └── trigger_state.json     # Trigger state tracking
├── templates/                 # Reference materials (safe to copy/read)
│   ├── 01_triggers_template.md
│   ├── 02_greeting_state_template.md
│   ├── 03_memory_template.md
│   └── 04_agents_template.md  # Memory rules — merge into your AGENTS.md
├── TRIGGERS.md                # User & system triggers guide
├── TRIGGER_STATE_GUIDE.md     # Trigger config guide
├── LICENSE                    # MIT License
├── README.md                  # Overview
└── INSTALL.md                # This file
```

---

## Database Setup

The skill includes a SQLite database in `db/` with the full GIGO schema.

**Cortex DB schema:**

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

Run `cortex backup` weekly to populate from memory logs.

---

## First Steps After Install

1. Open `templates/04_agents_template.md` and merge the memory rules into your `AGENTS.md`
2. Try triggers: `log this:`, `sync`, `huddle`
3. Check `memory/` folder — daily logs will appear here
4. Run `cortex check` to preview what would be synced
5. Run `cortex backup` to populate Cortex DB

---

## Troubleshooting

**Q: Nothing seems to be happening**
A: Check script output for errors. Ensure Python 3.x is installed.

**Q: Daily logs aren't being created**
A: Ensure memory/ folder exists and is writable.

**Q: Memory doesn't persist between sessions**
A: Ensure `memory/` is in your Git backup path.

---

*Total Recall (Cortex) — Agent Jam #1 🧠*
