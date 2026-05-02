# Cortex — Installation

**Time:** 5 minutes  
**Requirement:** OpenClaw workspace, **Python 3.x, SQLite** (built into Python - no separate install needed)

---

## Quick Install

```bash
# 1. Copy skill folder to workspace
cp -r skill/ ~/workspace/cortex/skill/

# 2. Run installer
cd ~/workspace
chmod +x cortex/skill/install.sh
./cortex/skill/install.sh

# 3. Copy memory rules into your AGENTS.md
#    See the "Integrating with Your AGENTS.md" section in SKILL.md
```

---

## What Happens

1. Creates `memory/`, `configs/`, `db/`, `scripts/` directories in your workspace
2. Copies `scripts/` — huddle.cjs, memory_log_sync_to_cortex.py, query_cortex.py
3. Copies `db/cortex_memory_bank.db` — SQLite database with GIGO schema
4. Copies `configs/trigger_state.json` — tracks last trigger times per source
5. Copies documentation — SKILL.md, TRIGGERS.md, TRIGGER_STATE_GUIDE.md, README.md

> ℹ️ The installer does **not** touch your `AGENTS.md`. Memory rules are provided in `SKILL.md` for you to merge in manually — this way your existing agent configuration is never overwritten.

---

## Important: Manual Setup Required

After running the installer, you need to:

1. **Merge memory rules into your AGENTS.md:**
   - Open `SKILL.md` and find the **Integrating with Your AGENTS.md** section
   - Copy the relevant blocks into your existing `AGENTS.md`
   - At minimum, add: Memory Startup, User Triggers, and Cortex Query Logic

2. **Configure trigger_state.json** (optional):
   - See [TRIGGER_STATE_GUIDE.md](TRIGGER_STATE_GUIDE.md) for platform-specific setup

---

## Included Files

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
├── INSTALL.md                        # This file
├── SKILL.md                          # Agent instructions + integration guide
├── TRIGGERS.md                       # Full trigger reference
├── TRIGGER_STATE_GUIDE.md            # Trigger state config guide
├── OUR_STORY_SO_FAR.md               # Background and design decisions
├── install.sh                        # Auto-install
└── LICENSE                           # MIT
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

Run `cortex backup` weekly to populate from memory logs.

---

## First Steps After Install

1. Open `SKILL.md` and merge the memory rules into your `AGENTS.md`
2. Try triggers: `log this:`, `sync`, `huddle`
3. Check `memory/` folder — daily logs will appear here
4. Run `cortex check` to preview what would be synced
5. Run `cortex backup` to populate Cortex DB

---

## Troubleshooting

**Q: Nothing seems to be happening**  
A: Check script output for errors. Ensure Python 3.x is installed.

**Q: Daily logs aren't being created**  
A: Ensure `memory/` folder exists and is writable.

**Q: Memory doesn't persist between sessions**  
A: Ensure `memory/` is in your Git backup path.

---

*Cortex — the Total Recall Memory System 🧠*
