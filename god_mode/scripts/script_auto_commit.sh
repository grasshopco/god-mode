#!/bin/bash

# Auto-commit changes to Git repository
echo "📝 Auto-committing changes..."

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$PROJECT_DIR")"

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if git is initialized
if [ ! -d ".git" ]; then
  echo "⚠️ Git repository not initialized. Run \"git init\" first."
  exit 1
fi

# Add all changes
git add .

# Create commit with timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Auto-commit: $TIMESTAMP"

echo "✅ Changes committed successfully!"

# Push changes if a remote is configured
if git remote -v | grep -q origin; then
  echo "🔄 Pushing changes to remote repository..."
  git push origin main
  echo "✅ Changes pushed successfully!"
fi 