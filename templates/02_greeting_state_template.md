# Greeting State Config

**For:** configs/greeting_state.json  
**Purpose:** Track greeting state to avoid repeats

---

## File Content

```json
{
  "last_greeted": "YYYY-MM-DD",
  "last_greeted_time": "HH:MM"
}
```

## Usage

- Check on session start
- If `last_greeted` != today's date → full greeting
- If `last_greeted` == today's date → brief "hey" only

## Create Folder

If `configs/` doesn't exist:
```bash
mkdir -p configs
```

Then create the file:
```bash
echo '{"last_greeted": "", "last_greeted_time": ""}' > configs/greeting_state.json
```

---

*Template for Total Recall Memory System*