#!/usr/bin/env python3
"""
Memory Log Sync to Cortex - Weekly routine to sync GIGO entries to Cortex DB

Flow:
1. Scans /memory/*.md files (YYYY-MM-DD naming convention)
2. Extracts GIGO entries from each file
3. Dedupe check (topic + context + outcome)
4. Inserts NEW entries to Cortex DB
5. Archives file to /memory/archive/ ONLY if new entries were added
6. Commits changes to git (optional --push for remote backup)

Usage:
    python3 scripts/memory_log_sync_to_cortex.py              # Weekly mode (default)
    python3 scripts/memory_log_sync_to_cortex.py --manual    # Manual mode (process all)
    python3 scripts/memory_log_sync_to_cortex.py --dry-run   # Show what would be added
    python3 scripts/memory_log_sync_to_cortex.py --push      # Commit AND push to remote

Scope:
- Skips: today's file, yesterday's file (48hr grace period)
- Processes: memory/*.md (YYYY-MM-DD pattern)
- Only archives files that had NEW entries inserted

Dedupe: topic + context + outcome (all 3 must match to skip)

Cortex DB: <skill_dir>/db/cortex_memory_bank.db
"""

import os
import sys
import re
import sqlite3
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from glob import glob

# Use relative paths from script location for portability
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(SKILL_DIR, "db", "cortex_memory_bank.db")
MEMORY_DIR = os.path.join(SKILL_DIR, "memory")
ARCHIVE_DIR = os.path.join(MEMORY_DIR, "archive")

def get_files_to_process(manual=False):
    """Get list of memory files, excluding today and yesterday unless manual."""
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    # Get all files
    files = []

    # Current year files
    for f in glob(os.path.join(MEMORY_DIR, "*.md")):
        basename = os.path.basename(f)
        if not manual and basename in (f"{today_str}.md", f"{yesterday}.md"):
            continue
        files.append(f)

    # Archive files
    for f in glob(os.path.join(ARCHIVE_DIR, "*.md")):
        basename = os.path.basename(f)
        # Extract date from filename like 2026-03-28.md or 2026-03-28-0631.md
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', basename)
        if date_match:
            file_date = date_match.group(1)
            if not manual and (file_date == today_str or file_date == yesterday):
                continue
        files.append(f)

    return sorted(files)

def extract_gigo_entries(content, filepath):
    """Extract GIGO entries from a memory file."""
    # Find GIGO section
    match = re.search(r'## GIGO Extracted Memories.*', content, re.DOTALL)
    if not match:
        return []

    section = match.group(0)
    entries = []

    # Split by ### to get individual entries
    parts = re.split(r'### ', section)

    for part in parts:
        if not part.strip():
            continue

        lines = part.strip().split('\n')
        topic = lines[0].strip()

        # Extract fields - handle multi-line content
        context_lines = []
        why_lines = []
        what_lines = []
        decision_lines = []
        outcome_lines = []

        current_field = None

        for line in lines[1:]:
            stripped = line.strip()
            if '**Context:**' in line:
                current_field = 'context'
                val = line.replace('**Context:**', '').strip()
                if val:
                    context_lines.append(val)
            elif '**Why' in line:
                current_field = 'why'
                val = line.replace('**Why it matters:**', '').strip()
                if val:
                    why_lines.append(val)
            elif '**What:' in line:
                current_field = 'what'
                val = line.replace('**What we tried/did:**', '').replace('**What:**', '').strip()
                if val:
                    what_lines.append(val)
            elif '**Decision:**' in line:
                current_field = 'decision'
                val = line.replace('**Decision:**', '').strip()
                if val:
                    decision_lines.append(val)
            elif '**Outcome:**' in line:
                current_field = 'outcome'
                val = line.replace('**Outcome:**', '').strip()
                if val:
                    outcome_lines.append(val)
            elif current_field and stripped:
                # Continuation line - add to current field
                if current_field == 'context':
                    context_lines.append(stripped)
                elif current_field == 'why':
                    why_lines.append(stripped)
                elif current_field == 'what':
                    what_lines.append(stripped)
                elif current_field == 'decision':
                    decision_lines.append(stripped)
                elif current_field == 'outcome':
                    outcome_lines.append(stripped)

        # Join multi-line content with newlines
        context = '\n'.join(context_lines)
        why_it = '\n'.join(why_lines)
        what = '\n'.join(what_lines)
        decision = '\n'.join(decision_lines)
        outcome = '\n'.join(outcome_lines)

        if topic and context:
            entries.append({
                'topic': topic,
                'context': context,
                'why_it_matters': why_it,
                'what_we_tried': what,
                'decision': decision,
                'outcome': outcome,
                'source_log': filepath
            })

    return entries

def is_duplicate(cursor, entry):
    """Check if entry already exists (topic + context + outcome)."""
    cursor.execute('''
        SELECT COUNT(*) FROM memories
        WHERE topic = ? AND context = ? AND outcome = ?
    ''', (entry['topic'], entry['context'], entry['outcome']))
    return cursor.fetchone()[0] > 0

def sync_to_cortex(dry_run=False, manual=False, push=False):
    """Main sync function."""
    files = get_files_to_process(manual)

    print(f"Processing {len(files)} files...")

    if dry_run:
        print("DRY RUN - no changes will be made")

    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    total_found = 0
    total_added = 0
    total_skipped = 0
    files_with_entries = []  # Track files that had new entries

    for filepath in files:
        with open(filepath, 'r') as f:
            content = f.read()

        entries = extract_gigo_entries(content, filepath)

        for entry in entries:
            total_found += 1

            if is_duplicate(cursor, entry):
                total_skipped += 1
                continue

            if not dry_run:
                # Extract date from filename
                basename = os.path.basename(filepath)
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})', basename)
                date_str = date_match.group(1) if date_match else "unknown"

                cursor.execute('''
                    INSERT INTO memories (date, topic, context, why_it_matters, what_we_tried, decision, outcome, source_log)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (date_str, entry['topic'], entry['context'], entry['why_it_matters'],
                      entry['what_we_tried'], entry['decision'], entry['outcome'], entry['source_log']))
                total_added += 1
                if filepath not in files_with_entries:
                    files_with_entries.append(filepath)

    db.commit()
    db.close()

    print(f"\nResults:")
    print(f"  Entries found: {total_found}")
    print(f"  Added to Cortex: {total_added}")
    print(f"  Skipped (duplicate): {total_skipped}")

    # Archive files that had NEW entries added to Cortex (not duplicates)
    if not dry_run and files_with_entries:
        archive_processed_files(files_with_entries, push=push)

    if dry_run:
        print("\nRun without --dry-run to apply changes.")

def archive_processed_files(files_with_entries, push=False):
    """Move only files that had NEW entries added to archive."""
    archive_dir = os.path.join(MEMORY_DIR, "archive")

    moved = 0
    for filepath in files_with_entries:
        basename = os.path.basename(filepath)
        dest = os.path.join(archive_dir, basename)

        if os.path.exists(filepath) and not os.path.exists(dest):
            os.rename(filepath, dest)
            print(f"  Archived: {basename}")
            moved += 1

    if moved > 0:
        print(f"\nArchived {moved} processed memory files")
        commit_changes(push=push)
    else:
        print("\nNo files to archive")

def commit_changes(push=False):
    """Commit changes to git (optional push for Agent Jam notes)."""
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=SKILL_DIR,
            capture_output=True, text=True
        )

        result = subprocess.run(
            ["git", "commit", "-m", "Memory: Sync GIGO entries to Cortex"],
            cwd=SKILL_DIR,
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print("  Committed to git")

            if push:
                result = subprocess.run(
                    ["git", "push"],
                    cwd=SKILL_DIR,
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print("  Pushed to remote")
                else:
                    print("  Push skipped (no remote configured)")
        else:
            # No changes or no git
            pass

    except Exception as e:
        print(f"  Git commit skipped: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync GIGO memory entries to Cortex DB')
    parser.add_argument('--manual', action='store_true', help='Process all files including today/yesterday')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be added without making changes')
    parser.add_argument('--push', action='store_true', help='Push to remote after commit (optional)')

    args = parser.parse_args()
    sync_to_cortex(dry_run=args.dry_run, manual=args.manual, push=args.push)
