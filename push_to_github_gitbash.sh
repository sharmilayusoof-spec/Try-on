#!/bin/bash
echo "========================================"
echo " Push Virtual Try-On to GitHub"
echo "========================================"
echo ""
echo "[INFO] Pushing to: sharmilayusoof-spec/Try-on"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed"
    echo "Please install Git from: https://git-scm.com/download/win"
    exit 1
fi

# Check if repository exists on GitHub
echo "Step 1: Make sure you created the repository on GitHub:"
echo "        https://github.com/sharmilayusoof-spec/Try-on"
echo ""
read -p "Have you created the repository? (y/n): " created
if [[ ! $created =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please create the repository first:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: Try-on"
    echo "3. DO NOT initialize with README"
    echo "4. Click 'Create repository'"
    echo ""
    exit 1
fi

echo ""
echo "Step 2: Removing old remote (if exists)..."
git remote remove origin 2>/dev/null

echo ""
echo "Step 3: Adding YOUR repository as remote..."
git remote add origin https://github.com/sharmilayusoof-spec/Try-on.git

echo ""
echo "Step 4: Verifying remote..."
git remote -v

echo ""
echo "Step 5: Initializing repository..."
git init

echo ""
echo "Step 6: Adding all files..."
git add .

echo ""
echo "Step 7: Creating commit..."
git commit -m "Initial commit: Virtual Try-On Application"

echo ""
echo "Step 8: Renaming branch to main..."
git branch -M main

echo ""
echo "Step 9: Pushing to GitHub..."
echo "[INFO] You will be prompted to authenticate"
echo "[INFO] Use your Personal Access Token (NOT password)"
echo ""
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo " SUCCESS! Repository pushed to GitHub"
    echo "========================================"
    echo ""
    echo "View your repository at:"
    echo "https://github.com/sharmilayusoof-spec/Try-on"
    echo ""
else
    echo ""
    echo "========================================"
    echo " Push failed. Common issues:"
    echo "========================================"
    echo ""
    echo "1. Authentication failed:"
    echo "   - Use Personal Access Token (not password)"
    echo "   - Create token at: https://github.com/settings/tokens"
    echo ""
    echo "2. Repository doesn't exist:"
    echo "   - Create it at: https://github.com/new"
    echo ""
    echo "3. Permission denied:"
    echo "   - Make sure you own the repository"
    echo ""
    echo "See GITHUB_PUSH_GUIDE.md for detailed help"
    echo ""
fi

# Made with Bob
