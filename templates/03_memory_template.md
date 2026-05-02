# MEMORY_TEMPLATE.md — Total Recall (Cortex) Reference

> This is a **reference template** showing the memory structure for the Agent Jam submission.
> The installer preserves your existing `MEMORY.md` — use this as a guide to add Cortex-specific sections.

---

## Total Recall (Cortex) Sections

These are the sections that make Cortex work:

### Memory Logging (GIGO Format)

```markdown
## Memory Logging

**Format:** `log this: [your info]`

- Saves to `memory/YYYY-MM-DD.md` in GIGO format
- GIGO = Great In Great Out: Context, Why, What, Decision, Outcome
- Session loads last 7 days for instant recall
```

### Session Triggers

```markdown
## Triggers

| Trigger | Action |
|---------|--------|
| `log this:` | Save to memory in GIGO format |
| `sync` | Reload memory files |
| `full sync` | Full check + Git backup |
| `huddle` | Generate GIGO summary. Skip if no messages. |
| `cortex backup` | Weekly sync: GIGO entries → Cortex DB → archive |
| `cortex check` | Preview what would be synced |
```

### Two-Layer Memory System

```markdown
## Memory Layers

- **Session Layer:** Last 7 days loaded at start → instant recall
- **Cortex Layer:** Long-term DB → enriches fuzzy context OR cold start

Use cortex backup weekly to populate Cortex DB.
```

---

*This template covers the Cortex-specific sections. Add these to your existing MEMORY.md if not present.*