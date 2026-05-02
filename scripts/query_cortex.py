#!/usr/bin/env python3
"""
Query Cortex Memory Database
Usage: python3 query_cortex.py "search term"
Returns matching entries from Cortex DB with relevance scores.
"""

import sqlite3
import sys
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "cortex_memory_bank.db")

def query_cortex(search_term: str, limit: int = 5):
    """Query Cortex DB for entries matching search term."""

    if not os.path.exists(DB_PATH):
        return f"No Cortex DB found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Search across topic, context, what_we_tried, outcome fields
    query = """
    SELECT date, topic, context, why_it_matters, what_we_tried, decision, outcome, source_log
    FROM memories
    WHERE topic LIKE ? OR context LIKE ? OR what_we_tried LIKE ? OR outcome LIKE ?
    ORDER BY date DESC
    LIMIT ?
    """

    search_pattern = f"%{search_term}%"
    cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, limit))

    results = cursor.fetchall()
    conn.close()

    if not results:
        return f"No Cortex entries found for: {search_term}"

    output = [f"=== Cortex Query: \"{search_term}\" ===\n"]

    for row in results:
        output.append(f"📅 {row['date']} | 📁 {row['topic']}")
        output.append(f"   Context: {row['context'][:100]}...")
        output.append(f"   What: {row['what_we_tried'][:100]}...")
        if row['outcome']:
            output.append(f"   Outcome: {row['outcome'][:100]}...")
        output.append(f"   Source: {row['source_log']}")
        output.append("")

    return "\n".join(output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_cortex.py \"search term\"")
        sys.exit(1)

    search_term = " ".join(sys.argv[1:])
    print(query_cortex(search_term))
