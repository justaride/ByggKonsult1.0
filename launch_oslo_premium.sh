#!/bin/bash

# Oslo Planning Documents - Premium Professional Interface
# Enhanced launcher with dependency management and system checks

clear
echo "🏛️  OSLO PLANNING DOCUMENTS - PREMIUM"
echo "=============================================="
echo "Professional Planning Intelligence Platform"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check Python installation
print_info "Checking system requirements..."

if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed. Please install Python 3.7+ to continue."
    exit 1
else
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION detected"
fi

# Check pip installation
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 to continue."
    exit 1
else
    print_status "pip3 available"
fi

# Check if application file exists
if [ ! -f "oslo_planning_premium.py" ]; then
    print_error "oslo_planning_premium.py not found in current directory!"
    print_info "Please ensure you're in the correct directory."
    exit 1
fi

# Install/upgrade required packages
print_info "Installing/upgrading required packages..."

PACKAGES=(
    "streamlit>=1.28.0"
    "pandas>=1.5.0"
    "plotly>=5.15.0"
    "requests>=2.28.0"
)

for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    pip3 install -q --upgrade "$package"
    if [ $? -eq 0 ]; then
        print_status "$package installed/upgraded"
    else
        print_warning "Warning: $package installation may have issues"
    fi
done

echo ""
print_status "All dependencies installed successfully!"
echo ""

# System information
print_info "System Information:"
echo "   🐍 Python: $(python3 --version | cut -d' ' -f2)"
echo "   📊 Streamlit: $(pip3 show streamlit | grep Version | cut -d' ' -f2)"
echo "   📈 Plotly: $(pip3 show plotly | grep Version | cut -d' ' -f2)"
echo "   🐼 Pandas: $(pip3 show pandas | grep Version | cut -d' ' -f2)"
echo ""

# Launch application
print_info "🚀 Launching Oslo Planning Documents - Premium Interface..."
echo ""
echo "📋 Features:"
echo "   • Verified and deduplicated planning documents"
echo "   • Professional UI/UX with premium styling"
echo "   • Advanced search and filtering capabilities"
echo "   • Comprehensive analytics dashboard"
echo "   • System verification and quality control"
echo "   • Administrative tools and data export"
echo ""
echo "🌐 The application will open in your default browser..."
echo "📍 URL: http://localhost:8503"
echo ""
echo "⚡ To stop the application, press Ctrl+C"
echo ""

# Check if port is available
if lsof -Pi :8503 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port 8503 is already in use. Trying alternative port 8504..."
    PORT=8504
else
    PORT=8503
fi

# Start the application
print_status "Starting premium application on port $PORT..."
echo ""

# Run Streamlit with optimized settings
streamlit run oslo_planning_premium.py \
    --server.port $PORT \
    --server.headless false \
    --browser.gatherUsageStats false \
    --server.fileWatcherType none \
    --server.enableCORS false \
    --server.enableXsrfProtection false

echo ""
print_info "Oslo Planning Documents - Premium stopped."
echo "Thank you for using the Professional Planning Intelligence Platform!"