#!/bin/bash
# ===========================================================
# VIRAL YOUTUBE DOCUMENTARY SYSTEM - Mac/Linux Quick Start
# ===========================================================
#
# This script automatically sets up everything you need!
# 
# Usage:
#   chmod +x quick_start_unix.sh
#   ./quick_start_unix.sh
#
# What it does:
# 1. Checks if Python is installed
# 2. Creates a virtual environment
# 3. Installs all required packages
# 4. Creates configuration files
# 5. Tests the installation
#
# ===========================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}➜ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Start setup
echo ""
echo "========================================"
echo "  VIRAL DOCUMENTARY SYSTEM SETUP"
echo "========================================"
echo ""

# Check if Python is installed
print_info "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo ""
    echo "Please install Python 3.11 or higher:"
    echo "  - Mac: brew install python@3.11"
    echo "  - Ubuntu/Debian: sudo apt install python3.11"
    echo "  - Or download from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

python3 --version
print_success "Python is installed!"
echo ""

# Check Python version
print_info "[2/6] Verifying Python version..."
python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"
if [ $? -ne 0 ]; then
    print_error "Python 3.11+ required!"
    echo "Your version is too old. Please upgrade Python."
    exit 1
fi
print_success "Python version is compatible!"
echo ""

# Create virtual environment
print_info "[3/6] Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment!"
        exit 1
    fi
    print_success "Virtual environment created!"
fi
echo ""

# Activate virtual environment
print_info "[4/6] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment!"
    exit 1
fi
print_success "Virtual environment activated!"
echo ""

# Upgrade pip
print_info "[5/6] Upgrading pip..."
python -m pip install --upgrade pip --quiet
print_success "Pip upgraded!"
echo ""

# Install requirements
print_info "[6/6] Installing required packages..."
echo "This may take 5-10 minutes depending on your internet speed..."
echo ""
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    print_error "Package installation failed!"
    echo ""
    echo "Common fixes:"
    echo "1. Check your internet connection"
    echo "2. Try running: pip install --upgrade pip"
    echo "3. On Mac with M1/M2: Install Rosetta 2"
    echo "4. On Linux: Install python3-dev (sudo apt install python3-dev)"
    echo ""
    exit 1
fi
echo ""
print_success "All packages installed!"
echo ""

# Create .env file if it doesn't exist
print_info "Creating configuration files..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Viral YouTube Documentary System - Environment Variables

# REQUIRED: Anthropic Claude API Key
# Get your key at: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# REQUIRED: OpenAI API Key (for embeddings)
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# OPTIONAL: JSTOR API Key (for academic research)
# Apply at: https://about.jstor.org/whats-in-jstor/text-mining-support/
JSTOR_API_KEY=your_jstor_api_key_here

# OPTIONAL: Semantic Scholar API Key
SEMANTIC_SCHOLAR_API_KEY=

# OPTIONAL: YouTube API Key
YOUTUBE_API_KEY=
EOF
    print_success "Created .env file"
else
    print_warning ".env file already exists, skipping..."
fi

# Copy config example
if [ ! -f "config/config.yaml" ]; then
    if [ -f "config/config.example.yaml" ]; then
        cp config/config.example.yaml config/config.yaml
        print_success "Created config.yaml from template"
    fi
else
    print_warning "config.yaml already exists, skipping..."
fi
echo ""

# Create necessary directories
print_info "Creating project directories..."
mkdir -p logs backups chroma_db outputs
print_success "Directories created!"
echo ""

# Make scripts executable
print_info "Making scripts executable..."
chmod +x scripts/*.py 2>/dev/null
print_success "Scripts are now executable!"
echo ""

echo "========================================"
echo "  SETUP COMPLETE! 🎉"
echo "========================================"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. ADD YOUR API KEYS:"
echo "   - Open .env file in a text editor"
echo "   - Add your Anthropic API key"
echo "   - Add your OpenAI API key"
echo ""
echo "2. TEST THE SYSTEM:"
echo "   - Run: python scripts/quick_test.py"
echo ""
echo "3. START CREATING:"
echo "   - Run: python scripts/generate_documentary.py"
echo ""
echo "DOCUMENTATION:"
echo "   - Read: README.md (getting started)"
echo "   - Read: docs/MULTI_AGENT_SYSTEM_SUMMARY.md (system overview)"
echo ""
echo "========================================"
echo ""
echo "Virtual environment is now active!"
echo "To deactivate it, type: deactivate"
echo ""
