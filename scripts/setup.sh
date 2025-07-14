#!/bin/bash
set -e

echo "🚀 Setting up SystemCallExplorer..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_warning "SystemCallExplorer is designed for Linux systems. Some features may not work on other platforms."
fi

# Check for required commands
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is required but not installed."
        return 1
    else
        print_status "$1 is available"
        return 0
    fi
}

print_status "Checking prerequisites..."

# Check Python
if ! check_command python3; then
    print_error "Please install Python 3.9 or later"
    exit 1
fi

# Check Node.js
if ! check_command node; then
    print_error "Please install Node.js 18 or later"
    exit 1
fi

# Check npm
if ! check_command npm; then
    print_error "Please install npm"
    exit 1
fi

# Check strace
if ! check_command strace; then
    print_warning "strace not found. Some features will be limited."
    print_status "You can install strace with: sudo apt-get install strace (Ubuntu/Debian)"
fi

# Check GCC (optional)
if ! check_command gcc; then
    print_warning "gcc not found. You won't be able to compile C examples."
else
    print_status "gcc is available for compiling examples"
fi

# Setup backend
print_status "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

print_status "Activating virtual environment..."
source venv/bin/activate

print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Test backend import
print_status "Testing backend configuration..."
if python3 -c "from core.config import settings; print('✅ Backend configuration loaded successfully')"; then
    print_status "Backend setup completed successfully"
else
    print_error "Backend configuration test failed"
    exit 1
fi

deactivate
cd ..

# Setup frontend
print_status "Setting up frontend..."
cd frontend

print_status "Installing Node.js dependencies..."
npm install

print_status "Testing frontend build..."
if npm run build; then
    print_status "Frontend build test successful"
else
    print_error "Frontend build test failed"
    exit 1
fi

cd ..

# Create necessary directories
print_status "Creating application directories..."
mkdir -p logs
mkdir -p /tmp/systemcall_explorer 2>/dev/null || true

# Make scripts executable
print_status "Setting up scripts..."
chmod +x scripts/*.sh
chmod +x tools/*.py

# Test example compilation
print_status "Testing C example compilation..."
cd examples
if gcc -o basic_file_operations basic_file_operations.c; then
    print_status "C example compiled successfully"
    rm -f basic_file_operations  # Clean up
else
    print_warning "C example compilation failed. GCC may not be properly configured."
fi
cd ..

print_status "✅ Setup completed successfully!"
echo
echo "🎉 SystemCallExplorer is ready to use!"
echo
echo "To start the application:"
echo "  1. Backend:  cd backend && source venv/bin/activate && python3 main.py"
echo "  2. Frontend: cd frontend && npm run dev"
echo
echo "Or use the Makefile:"
echo "  make dev"
echo
echo "📚 Read the documentation in docs/getting-started.md"
echo "🌐 Access the app at http://localhost:5173"
echo "📖 API docs at http://localhost:8000/docs"