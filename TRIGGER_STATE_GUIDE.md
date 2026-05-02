# Trigger State Configuration

## Overview

The `trigger_state.json` tracks when `huddle` and `log this:` were last triggered, to prevent duplicate entries.

## Structure

```json
{
  "huddle": {
    "default": { "last_time": "2026-05-02T11:00:00.000Z" }
  },
  "log_this": {
    "default": { "last_time": null }
  },
  "last_updated": "2026-05-02T11:00:00.000Z"
}
```

## Per-Source Tracking

Different chat sources (Discord channels, Telegram chats, Console sessions) can have their own timestamps. This prevents huddle triggers in one channel from affecting another.

### Example: Discord + Telegram User

```json
{
  "huddle": {
    "1234567890123456789": { "last_time": "2026-05-02T09:30:00.000Z" },
    "telegram:-100123456789": { "last_time": "2026-05-02T10:15:00.000Z" }
  }
}
```

- `1234567890123456789` = Discord channel ID
- `telegram:-100123456789` = Telegram chat ID

## Setting Up Your Platform

### Option 1: Simple (Default)

The skill ships with `"default"` key. Edit `configs/trigger_state.json`:

```json
{
  "huddle": {
    "default": { "last_time": null }
  }
}
```

### Option 2: Platform-Specific

For multi-platform users, add keys for each source:

| Platform | Key Format | Example |
|----------|------------|---------|
| Discord | Channel ID | `1234567890123456789` |
| Telegram | `telegram:chat_id` | `telegram:-100123456789` |
| Console | `console` | `console` |

### Ask Your Agent

You can simply tell your agent to configure it:

- **Discord:** "Hey, hook up trigger_state for Discord channel #projects"
- **Telegram:** "Configure trigger_state for this Telegram chat"

The agent will detect the platform and update the config automatically.

## How It Works

1. When `huddle` triggers, script reads the source key from environment
2. Looks up `huddle.<source_key>.last_time` in trigger_state.json
3. If no entry for that source, assumes first run
4. After huddle, updates the timestamp for that specific source

## Environment Variables

The skill checks these variables (if available):

- `OPENCLAW_CHANNEL_ID` — Discord channel or Telegram chat ID
- `OPENCLAW_PLATFORM` — Platform name (discord, telegram, console)

## First Install Checklist

- [ ] Review `configs/trigger_state.json`
- [ ] Decide: Simple (default) or platform-specific keys
- [ ] For platform-specific: Add your channel/chat ID key with `last_time: null`
- [ ] Done — ready to use `huddle` and `log this:` triggers

---

## Optional: Midnight Huddle via Cron

Instead of a blind script running at midnight, you can set a cron job to **ping your agent** with a huddle command. The agent then captures with full session context.

### Setup

```bash
# Cron example (runs at midnight)
0 0 * * * curl -X POST http://localhost:18789/message -d " huddle"
```

Or use OpenClaw's cron to schedule a message to the agent.

### Why This Works Better

- Agent has **full conversation context** from the day
- Can filter noise, capture meaningful GIGO entries
- No blind script running with no context
