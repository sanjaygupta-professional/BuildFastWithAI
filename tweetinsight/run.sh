#!/bin/bash
# TweetInsight startup script

echo "🐦 TweetInsight - Twitter Research Application"
echo "=============================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your API keys before continuing."
    echo "Required:"
    echo "  - TWITTER_BEARER_TOKEN (or Twitter OAuth credentials)"
    echo "  - OPENAI_API_KEY or ANTHROPIC_API_KEY"
    echo ""
    echo "After configuring .env, run this script again."
    exit 1
fi

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create data directory
echo "Creating data directory..."
mkdir -p data
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Start the application
echo "🚀 Starting TweetInsight..."
echo "The application will be available at: http://localhost:8501"
echo ""
streamlit run app.py
