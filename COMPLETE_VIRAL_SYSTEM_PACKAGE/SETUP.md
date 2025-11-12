# 🚀 Setup Guide - Viral YouTube Documentary System

## Complete Installation Instructions

This guide will walk you through setting up the Viral YouTube Documentary System from scratch. Expected time: **15-20 minutes**.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Automated Setup](#automated-setup-recommended)
3. [Manual Setup](#manual-setup-advanced)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## Prerequisites

### Required Software

#### 1. Python 3.11 or Higher

**Check if you have Python:**
```bash
python3 --version
# or
python --version
```

**If you need to install:**
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
  - ⚠️ IMPORTANT: Check "Add Python to PATH" during installation!
- **Mac:** 
  ```bash
  brew install python@3.11
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv python3-pip
  ```

#### 2. Git (Optional but recommended)

**Check if you have Git:**
```bash
git --version
```

**If you need to install:**
- **Windows:** Download from [git-scm.com](https://git-scm.com/download/win)
- **Mac:** `brew install git`
- **Linux:** `sudo apt install git`

### Required API Keys

You'll need these API keys to use the system:

#### 1. Anthropic Claude API Key (REQUIRED)

- **Get it:** [console.anthropic.com](https://console.anthropic.com/)
- **Cost:** Free $5 credit (enough for 50-500 documentaries)
- **Time:** 2 minutes to sign up

#### 2. OpenAI API Key (REQUIRED)

- **Get it:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Cost:** Pay as you go (~$0.001 per documentary)
- **Time:** 2 minutes to sign up

#### 3. JSTOR API Key (OPTIONAL)

- **Get it:** [Apply here](https://about.jstor.org/whats-in-jstor/text-mining-support/)
- **Cost:** Usually requires institutional affiliation
- **Note:** System works without this, but research quality is enhanced with it

---

## Automated Setup (Recommended)

The fastest way to get started! Just run the setup script for your operating system.

### Windows

1. **Download the package** (you're already here!)

2. **Open the package folder** in File Explorer

3. **Double-click:** `quick_start_windows.bat`

4. **Wait** for the script to complete (5-10 minutes)

5. **Done!** ✅

**What the script does:**
- ✓ Checks Python version
- ✓ Creates virtual environment
- ✓ Installs all packages (35+)
- ✓ Creates configuration files
- ✓ Sets up directory structure

### Mac / Linux

1. **Open Terminal**

2. **Navigate to the package folder:**
   ```bash
   cd /path/to/COMPLETE_VIRAL_SYSTEM_PACKAGE
   ```

3. **Make the script executable:**
   ```bash
   chmod +x quick_start_unix.sh
   ```

4. **Run the script:**
   ```bash
   ./quick_start_unix.sh
   ```

5. **Wait** for completion (5-10 minutes)

6. **Done!** ✅

---

## Manual Setup (Advanced)

If you prefer manual control or the automated setup fails:

### Step 1: Extract Package

Extract the complete package to your desired location.

### Step 2: Create Virtual Environment

```bash
# Navigate to package directory
cd /path/to/COMPLETE_VIRAL_SYSTEM_PACKAGE

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**Why virtual environment?**
- Isolates packages from your system Python
- Prevents version conflicts
- Makes the project portable

### Step 3: Upgrade Pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**This installs 35+ packages including:**
- anthropic (Claude API)
- langchain, langgraph (AI workflows)
- chromadb (vector database)
- openai (embeddings)
- And many more...

**Time:** 5-10 minutes depending on internet speed

### Step 5: Create Configuration Files

```bash
# Copy .env example
cp .env.example .env

# Copy config example
cp config/config.example.yaml config/config.yaml
```

### Step 6: Create Directories

```bash
mkdir -p logs backups chroma_db outputs
```

---

## Configuration

### Step 1: Add API Keys to .env

1. Open `.env` in your text editor:
   ```bash
   # Mac/Linux
   nano .env
   # or
   code .env  # if you have VS Code
   
   # Windows
   notepad .env
   ```

2. Replace placeholder values:
   ```bash
   # Before:
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # After:
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
   ```

3. **Required keys:**
   - `ANTHROPIC_API_KEY` - Your Claude API key
   - `OPENAI_API_KEY` - Your OpenAI API key

4. **Optional keys:**
   - `JSTOR_API_KEY` - Enhanced academic research
   - `YOUTUBE_API_KEY` - Video analysis
   - `SEMANTIC_SCHOLAR_API_KEY` - More paper sources

5. Save and close the file

### Step 2: Review config.yaml (Optional)

The default config works great out of the box, but you can customize:

```yaml
# config/config.yaml

models:
  gatekeeper:
    name: "claude-sonnet-4-20250514"  # Change if needed
    max_tokens: 4000
    temperature: 0.3
  
research:
  quality:
    min_credibility_score: 7.0  # Adjust quality threshold
    max_age_years: 10  # Maximum paper age
```

**Most users can skip this step!**

---

## Testing

### Quick Test

Run the quick test to verify everything is working:

```bash
python scripts/quick_test.py
```

**Expected output:**
```
========================================
  VIRAL DOCUMENTARY SYSTEM - QUICK TEST
========================================

Testing Python Version...
✓ Python 3.11.5 is compatible!

Testing Required Packages...
✓ anthropic is installed
✓ langchain is installed
✓ langgraph is installed
...

Testing API Keys...
✓ .env file found
✓ Anthropic API key is configured
✓ OpenAI API key is configured

Testing Project Structure...
✓ agents/gatekeepers/ exists
✓ agents/subagents/ exists
...

Testing API Connectivity...
✓ API connection successful!

========================================
Test Summary
========================================
✓ Python Version: PASS
✓ Packages: PASS
✓ API Keys: PASS
✓ Directories: PASS
✓ Agent Imports: PASS
✓ API Connectivity: PASS

Results: 6/6 tests passed

🎉 All tests passed! System is ready to use!
```

### Test Individual Agents

```bash
# Test Academic Specialist
python agents/subagents/academic_depth_specialist.py

# Test Accessibility Translator
python agents/subagents/accessibility_translator.py

# Test other agents...
```

Each agent has a built-in test that demonstrates its capabilities.

---

## Troubleshooting

### Common Issues

#### Issue: "Python command not found"

**Solution:**
- Make sure Python is installed
- Make sure Python is in your PATH
- Try `python3` instead of `python`

#### Issue: "Permission denied" on Mac/Linux

**Solution:**
```bash
chmod +x quick_start_unix.sh
chmod +x scripts/*.py
```

#### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall packages
pip install -r requirements.txt

# Or install specific package
pip install anthropic
```

#### Issue: "ANTHROPIC_API_KEY not found"

**Solution:**
- Make sure `.env` file exists (not `.env.example`)
- Check that API key is added to `.env`
- Restart terminal/shell after editing `.env`

#### Issue: "API key is invalid"

**Solution:**
- Double-check you copied the full key
- No extra spaces before/after the key
- Key is for the correct service (Anthropic vs OpenAI)
- Key hasn't been revoked or expired

#### Issue: Package installation fails on Windows

**Solution:**
- Install Visual Studio Build Tools
- Download from: [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

#### Issue: "Command not found" in virtual environment

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# If not activated:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

#### Issue: Slow package installation

**Solution:**
```bash
# Use a faster mirror
pip install -r requirements.txt --index-url https://pypi.org/simple

# Or install in smaller batches
pip install anthropic langchain langgraph
pip install chromadb openai
# etc...
```

---

## System Requirements

### Minimum
- **OS:** Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Python:** 3.11+
- **RAM:** 4GB
- **Disk:** 1GB free space
- **Internet:** Required for API calls

### Recommended
- **OS:** Windows 11, macOS 13+, Ubuntu 22.04+
- **Python:** 3.11+
- **RAM:** 8GB
- **Disk:** 2GB free space
- **Internet:** High-speed broadband

### Optimal
- **OS:** Latest stable OS version
- **Python:** 3.11+
- **RAM:** 16GB
- **Disk:** 5GB free space
- **Internet:** Fiber/10Mbps+

---

## Next Steps

Now that you're set up, here's what to do next:

### 1. Learn the System (15 minutes)

Read in this order:
1. `PACKAGE_README.md` - Complete overview
2. `MULTI_AGENT_SYSTEM_SUMMARY.md` - How the agents work
3. `QUICK_REFERENCE.md` - Command reference

### 2. Test the Agents (15 minutes)

```bash
# Run each agent's test
python agents/subagents/academic_depth_specialist.py
python agents/subagents/accessibility_translator.py
python agents/subagents/historical_context_miner.py
python agents/subagents/interdisciplinary_connector.py
python agents/subagents/contrarian_viewpoint_hunter.py
```

### 3. Generate First Documentary (5 minutes)

```python
from agents.gatekeepers.research_gatekeeper import ResearchGatekeeper

gatekeeper = ResearchGatekeeper()
result = gatekeeper.execute({
    "topic": "The Science of Sleep",
    "target_audience": "Science enthusiasts",
    "video_style": "Documentary"
})

print(f"Research Confidence: {result['research_confidence']}")
print(f"Papers Found: {len(result['academic_findings'])}")
```

### 4. Explore Advanced Features

- Read: `RESEARCH_GATEKEEPER_ANALYSIS.md` - Deep dive
- Read: `JSTOR_QUICK_START.md` - Enhanced research
- Study: Bonus PDFs on viral techniques

---

## Getting Help

### Documentation
- **Overview:** `PACKAGE_README.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **Navigation Guide:** `docs/NAVIGATION_GUIDE.md`

### Support Resources
- **Test System:** `python scripts/quick_test.py`
- **Diagnostics:** `python scripts/system_diagnostics.py`
- **Agent Tests:** Built into each agent file

### Community
- GitHub Issues (coming soon)
- Discord (coming soon)
- Email support (coming soon)

---

## Summary Checklist

- [ ] Python 3.11+ installed
- [ ] Package extracted to desired location
- [ ] Virtual environment created
- [ ] Packages installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API keys
- [ ] `config.yaml` file created
- [ ] Directories created (logs, backups, etc.)
- [ ] Quick test passed (`python scripts/quick_test.py`)
- [ ] Individual agents tested
- [ ] Documentation read

**If all boxes are checked, you're ready to create viral documentaries! 🎬**

---

**Having issues? Check the Troubleshooting section above or run:**
```bash
python scripts/system_diagnostics.py
```

**Good luck creating amazing content! 🚀**
