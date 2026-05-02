#!/bin/bash
# Total Recall (Cortex) — Install Script

echo "🧠 Installing Total Recall (Cortex)..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ERRORS=0

# ===== CREATE DIRECTORIES =====
echo ""
echo "📁 Creating directories..."

mkdir -p memory
if [ -d memory ]; then
    echo "✅ Created memory/"
else
    echo "❌ Failed to create memory/"
    ERRORS=$((ERRORS + 1))
fi

mkdir -p configs
if [ -d configs ]; then
    echo "✅ Created configs/"
else
    echo "❌ Failed to create configs/"
    ERRORS=$((ERRORS + 1))
fi

mkdir -p db
if [ -d db ]; then
    echo "✅ Created db/"
else
    echo "❌ Failed to create db/"
    ERRORS=$((ERRORS + 1))
fi

mkdir -p scripts
if [ -d scripts ]; then
    echo "✅ Created scripts/"
else
    echo "❌ Failed to create scripts/"
    ERRORS=$((ERRORS + 1))
fi

# ===== COPY SKILL FILES =====
echo ""
echo "📦 Copying skill files..."

# Copy scripts
if [ -d "$SCRIPT_DIR/scripts" ]; then
    cp -r "$SCRIPT_DIR/scripts/"* scripts/
    echo "✅ Copied scripts/"
else
    echo "❌ Scripts folder missing in skill package"
    ERRORS=$((ERRORS + 1))
fi

# Copy database
if [ -f "$SCRIPT_DIR/db/cortex_memory_bank.db" ]; then
    cp "$SCRIPT_DIR/db/cortex_memory_bank.db" db/
    echo "✅ Copied Cortex DB"
else
    echo "❌ Cortex DB missing in skill package"
    ERRORS=$((ERRORS + 1))
fi

# Copy trigger state config
if [ -f "$SCRIPT_DIR/configs/trigger_state.json" ]; then
    cp "$SCRIPT_DIR/configs/trigger_state.json" configs/
    echo "✅ Copied trigger_state.json"
else
    # Create default if missing
    echo '{"huddle": {"default": {"last_time": null}}, "log_this": {"default": {"last_time": null}}, "last_updated": null}' > configs/trigger_state.json
    echo "✅ Created default trigger_state.json"
fi

# Copy templates (includes 04_agents_template.md as a merge guide)
if [ -d "$SCRIPT_DIR/templates" ]; then
    mkdir -p templates
    cp -r "$SCRIPT_DIR/templates/"* templates/
    echo "✅ Copied templates/"
fi

# Copy reference docs (never overwrites user's own AGENTS.md)
for doc in README.md INSTALL.md TRIGGERS.md TRIGGER_STATE_GUIDE.md LICENSE; do
    if [ -f "$SCRIPT_DIR/$doc" ]; then
        cp "$SCRIPT_DIR/$doc" . 2>/dev/null || true
    fi
done
echo "✅ Copied documentation"

# ===== VALIDATION =====
echo ""
echo "🔍 Validating installation..."

# Check key directories
if [ -d memory ] && [ -d configs ] && [ -d db ] && [ -d scripts ]; then
    echo "✅ All directories created"
else
    echo "❌ Missing required directories"
    ERRORS=$((ERRORS + 1))
fi

# Check scripts
for script in huddle.cjs memory_log_sync_to_cortex.py query_cortex.py; do
    if [ -f "scripts/$script" ]; then
        echo "✅ scripts/$script exists"
    else
        echo "❌ scripts/$script missing"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check database
if [ -f db/cortex_memory_bank.db ]; then
    echo "✅ Cortex DB exists"
else
    echo "❌ Cortex DB missing"
    ERRORS=$((ERRORS + 1))
fi

# Check config
if [ -f configs/trigger_state.json ]; then
    echo "✅ trigger_state.json exists"
else
    echo "❌ trigger_state.json missing"
    ERRORS=$((ERRORS + 1))
fi

# ===== SUMMARY =====
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 Total Recall (Cortex) installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Open templates/04_agents_template.md and copy the memory rules into your AGENTS.md"
    echo "2. Try: log this: test → sync → huddle"
    echo "3. Check memory/ folder — daily logs will appear here"
    echo ""
    echo "For full setup guide, see INSTALL.md"
else
    echo "⚠️  $ERRORS error(s) found — check above"
    exit 1
fi
