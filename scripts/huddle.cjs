#!/usr/bin/env node
/**
 * Huddle - Session summary to memory
 * 
 * Skill version: Simplified GIGO flow
 * 1. Read last huddle time from trigger_state.json
 * 2. Write GIGO entry to today's memory file
 * 3. Update trigger_state.json
 * 
 * Note: Session reading not available in skill context - relies on trigger input
 */

const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '..', 'configs', 'trigger_state.json');
const MEMORY_DIR = path.join(__dirname, '..', 'memory');
const TODAY = new Date().toISOString().split('T')[0];

function loadTriggerState() {
  if (!fs.existsSync(CONFIG_FILE)) {
    return { huddle: {}, log_this: {} };
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
}

function getLastHuddleTime(state, sourceKey) {
  return state.huddle?.[sourceKey]?.last_time || null;
}

function saveTriggerState(state) {
  state.last_updated = new Date().toISOString();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(state, null, 2));
}

function generateGigoEntry(messageText) {
  // Simple GIGO format from trigger input
  const lines = messageText.trim().split('\n');
  const topic = lines[0] || 'Session Note';
  
  let context = '', why = '', what = '', decision = '', outcome = '';
  
  // Parse if multi-line provided, otherwise use single line
  if (lines.length > 1) {
    context = lines.slice(1).join(' ').substring(0, 500);
  } else {
    context = topic;
  }
  
  return {
    topic,
    context,
    why: 'Captured from session',
    what: 'Manual huddle entry',
    decision: 'Logged to memory',
    outcome: 'Persisted'
  };
}

function writeToMemory(gigoEntry) {
  const todayFile = path.join(MEMORY_DIR, `${TODAY}.md`);
  let memoryContent = '';
  
  if (fs.existsSync(todayFile)) {
    memoryContent = fs.readFileSync(todayFile, 'utf8');
  } else {
    memoryContent = `# ${TODAY} — Session Notes\n\n`;
  }
  
  // Check if already has entry for this topic
  if (memoryContent.includes(`### ${gigoEntry.topic}`)) {
    console.log('⚠️ Entry already exists for:', gigoEntry.topic);
    return false;
  }
  
  // Write GIGO entry
  const entry = `
### ${gigoEntry.topic}
- **Context:** ${gigoEntry.context}
- **Why:** ${gigoEntry.why}
- **What:** ${gigoEntry.what}
- **Decision:** ${gigoEntry.decision}
- **Outcome:** ${gigoEntry.outcome}

*Logged: ${TODAY}*`;
  
  memoryContent += entry + '\n\n';
  fs.writeFileSync(todayFile, memoryContent);
  console.log('✅ Written to', todayFile);
  return true;
}

function getSourceKey() {
  // Priority: env var > default
  const channelId = process.env.OPENCLAW_CHANNEL_ID;
  const platform = process.env.OPENCLAW_PLATFORM;
  
  if (channelId) return channelId;
  if (platform) return platform;
  return 'default';
}

function main(messageText) {
  console.log('🧠 Running huddle...\n');
  
  // Get source key (env var or default)
  const sourceKey = getSourceKey();
  console.log('Source:', sourceKey);
  
  // 1. Load trigger state
  const state = loadTriggerState();
  const lastHuddle = getLastHuddleTime(state, sourceKey) || 'Never';
  console.log('Last huddle for this source:', lastHuddle);
  
  // 2. Generate GIGO entry (from provided text or default)
  const entryText = messageText || `Session huddle ${TODAY}`;
  const gigo = generateGigoEntry(entryText);
  
  // 3. Write to memory
  const written = writeToMemory(gigo);
  
  if (!written) {
    console.log('⚠️ Skipped - duplicate entry');
  }
  
  // 4. Update trigger state for this source
  const now = new Date().toISOString();
  
  if (!state.huddle) state.huddle = {};
  state.huddle[sourceKey] = { last_time: now };
  
  saveTriggerState(state);
  console.log('✅ Updated trigger_state.json');
  
  return '💾 Huddle complete';
}

// Run if called directly
if (require.main === module) {
  const args = process.argv.slice(2);
  const messageText = args.join(' ');
  main(messageText);
}

module.exports = { main, generateGigoEntry, writeToMemory };
