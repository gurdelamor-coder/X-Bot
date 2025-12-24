#!/bin/bash
# Quick test script for the bot (use locally before pushing to GitHub)

echo "🤖 X Bot Local Test"
echo "===================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "✓ Virtual environment ready"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Check for environment variables
if [ -z "$X_BEARER_TOKEN" ]; then
    echo "⚠️  WARNING: X_BEARER_TOKEN not set"
    echo "Set your environment variables before running:"
    echo ""
    echo "export X_BEARER_TOKEN='your_token'"
    echo "export X_API_KEY='your_key'"
    echo "export X_API_SECRET='your_secret'"
    echo "export X_ACCESS_TOKEN='your_token'"
    echo "export X_ACCESS_SECRET='your_secret'"
    echo ""
    exit 1
fi

echo "✓ Environment variables found"
echo ""
echo "Running bot..."
echo "===================="
echo ""

python3 x_bot.py

echo ""
echo "===================="
echo "✓ Test complete!"
