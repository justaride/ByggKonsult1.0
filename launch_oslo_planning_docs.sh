#!/bin/bash

# Oslo Planning Documents Integration Launcher
# Complete integration of all Oslo kommune planning documents

echo "🏛️ Starting Oslo Planning Documents Integration..."
echo "=================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 to continue."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip3 install -q streamlit pandas plotly sqlite3 requests

# Check if the main application file exists
if [ ! -f "oslo_planning_documents_integration.py" ]; then
    echo "❌ oslo_planning_documents_integration.py not found!"
    exit 1
fi

# Launch the application
echo "🚀 Launching Oslo Planning Documents Integration..."
echo ""
echo "📋 Complete database of all current Oslo kommune planning documents"
echo "📊 13 major categories with comprehensive coverage"
echo "✅ Verified links to official Oslo kommune sources"
echo ""
echo "The application will open in your default browser..."
echo "To stop the application, press Ctrl+C"
echo ""

# Run Streamlit app
streamlit run oslo_planning_documents_integration.py --server.port 8502 --server.headless false

echo ""
echo "✅ Oslo Planning Documents Integration stopped."