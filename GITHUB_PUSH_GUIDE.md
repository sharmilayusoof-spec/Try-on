# GitHub Push Guide for Virtual Try-On Application

## Problem
You're getting a 403 error because you're trying to push to `ishumusian/Try-on.git` but you're authenticated as `sharmilayusoof-spec`.

## Solution

### Step 1: Create Your Own Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `Try-on` (or any name you prefer)
3. Make it **Public** or **Private** (your choice)
4. **DO NOT** check "Initialize this repository with a README"
5. Click **"Create repository"**

### Step 2: Open Git Bash Terminal
- Right-click in your project folder (`c:/Users/SharmilaBegamM/AI Projects/Try-on`)
- Select **"Git Bash Here"**
- OR open Git Bash and navigate to your project:
  ```bash
  cd "/c/Users/SharmilaBegamM/AI Projects/Try-on"
  ```

### Step 3: Remove Old Remote and Add Your Repository
Run these commands in Git Bash:

```bash
# Remove the old remote (if it exists)
git remote remove origin

# Add your new repository as origin
git remote add origin https://github.com/sharmilayusoof-spec/Try-on.git

# Verify the remote is correct
git remote -v
```

### Step 4: Initialize Git (if not already done)
```bash
# Initialize git repository (if needed)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Virtual Try-On Application"

# Rename branch to main (if needed)
git branch -M main
```

### Step 5: Push to GitHub
```bash
# Push to your repository
git push -u origin main
```

### Step 6: Authenticate
When prompted, authenticate with your GitHub account:
- Username: `sharmilayusoof-spec`
- Password: Use a **Personal Access Token** (not your GitHub password)

#### How to Create a Personal Access Token:
1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Try-on-upload`
4. Select scopes: Check **"repo"** (full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

## Alternative: Use GitHub Desktop
If you prefer a GUI:
1. Download GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop
3. File → Add Local Repository → Select your project folder
4. Publish repository to GitHub
5. Choose repository name and visibility
6. Click "Publish repository"

## Quick Reference Commands

```bash
# Check current remote
git remote -v

# Change remote URL
git remote set-url origin https://github.com/sharmilayusoof-spec/Try-on.git

# Check git status
git status

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push -u origin main

# Pull latest changes
git pull origin main
```

## Troubleshooting

### Error: "Git is not recognized"
- Install Git from: https://git-scm.com/download/win
- Use **Git Bash** terminal instead of PowerShell/CMD

### Error: "Permission denied"
- Make sure you're pushing to YOUR repository (sharmilayusoof-spec/Try-on)
- Use a Personal Access Token instead of password
- Check you have write access to the repository

### Error: "Repository not found"
- Make sure the repository exists on GitHub
- Check the repository name is correct
- Verify the remote URL: `git remote -v`

## Files That Will Be Uploaded
Based on your `.gitignore`, these files will be uploaded:
- ✅ All Python source code (`app/`, `run.py`)
- ✅ Frontend files (`frontend/`)
- ✅ Configuration files (`.env.example`, `requirements.txt`, `README.md`)
- ✅ VITON source code (excluding large model files)
- ❌ Virtual environments (`venv/`, `env/`)
- ❌ User uploaded files (`storage/uploads/*`, `results/*`)
- ❌ Python cache files (`__pycache__/`)
- ❌ Environment variables (`.env`)

## Need Help?
If you continue to have issues, check:
1. You're using Git Bash (not PowerShell)
2. The repository exists on GitHub under your account
3. You're using a Personal Access Token for authentication
4. The remote URL points to your repository