#!/bin/bash
# Oslo Planning Dashboard - Quick Launch Script

echo "🏛️ OSLO PLANNING DASHBOARD - STANDALONE"
echo "========================================"
echo ""

# Check if dependencies are installed
echo "🔧 Checking dependencies..."
python3 -c "import streamlit, plotly, pandas, pdfplumber" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install streamlit plotly pandas pdfplumber openpyxl xlsxwriter
else
    echo "✅ All dependencies found"
fi

echo ""
echo "🚀 Starting Oslo Planning Dashboard..."
echo "📱 Opening in browser at: http://localhost:8501"
echo "🔄 Press Ctrl+C to stop the application"
echo ""

# Skip Streamlit welcome email prompt
export STREAMLIT_CONFIG_FILE="$(mktemp)"
cat > "$STREAMLIT_CONFIG_FILE" << EOF
[browser]
gatherUsageStats = false

[client]
showErrorDetails = false

[server]
headless = true
EOF

# Launch Streamlit with config
streamlit run oslo_standalone_implementation.py --server.port=8501 --server.headless=true

# Cleanup
rm -f "$STREAMLIT_CONFIG_FILE"