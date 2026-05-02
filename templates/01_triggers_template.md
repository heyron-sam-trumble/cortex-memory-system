# Trigger Reference

**For:** TRIGGERS.md or skill documentation  
**Purpose:** Document available triggers for users

---

## Available Triggers

| Trigger | Say This | What It Does |
|---------|----------|--------------|
| **Log** | `log this: [info]` | Saves info to today's memory log (GIGO format) |
| **Huddle** | `huddle` | Generate session summary in GIGO format. Skip if no messages. |
| **Sync** | `sync` | Reloads all memory files |
| **Full Sync** | `full sync` | Full system check + git backup |
| **Cortex Backup** | `cortex backup` | Sync GIGO entries (>48hrs) to Cortex DB |
| **Cortex Check** | `cortex check` | Preview what would sync (dry-run) |

---

## Log

Saves specific information to today's memory log in GIGO format.

**Format:** `log this: [your info here]`

**Example:**
```
User: "log this: Lisa's birthday is May 15th"
Agent: "Saved to memory: Lisa's birthday is May 15th"
```

---

## Huddle

Saves key decisions and progress from the current session to memory.

**Format:** `huddle`

**Example:**
```
User: "huddle"
Agent: "Session summary saved in GIGO format"
- **Context:** Company name discussion
- **Why:** Needed for business registration
- **What:** Multiple names checked, availability verified
- **Decision:** Orion Digital Consulting
- **Outcome:** Name available, proceeding with registration
```

---

## Sync

Reloads all memory files — use after agent has been offline.

**Format:** `sync`

---

## Full Sync

Runs full system check + git backup.

**Format:** `full sync`

---

## Cortex Backup

Syncs GIGO entries older than 48 hours to the Cortex long-term memory database.

**Format:** `cortex backup`

---

## Cortex Check

Preview what would be synced to Cortex DB (dry-run, no changes).

**Format:** `cortex check`

---

*Template for Total Recall Memory System — Cortex*
