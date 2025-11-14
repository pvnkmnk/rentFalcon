# Rental Scanner - Installation Guide

Complete installation instructions for the Newmarket Rental Scanner application.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Install](#quick-install)
- [Detailed Installation](#detailed-installation)
- [Verifying Installation](#verifying-installation)
- [First Run](#first-run)
- [Troubleshooting](#troubleshooting)
- [Updating](#updating)

---

## 🖥️ System Requirements

### Operating System
- **Windows** 10/11 (tested)
- **macOS** 10.14+ (should work)
- **Linux** Ubuntu 20.04+ or equivalent (should work)

### Required Software

1. **Python 3.8 or higher**
   - Check version: `python --version`
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Windows users**: Check "Add Python to PATH" during installation

2. **Google Chrome Browser** (required)
   - Latest version recommended
   - Download from: https://www.google.com/chrome/
   - Required for Rentals.ca scraper (uses browser automation)

3. **Internet Connection**
   - For downloading packages
   - For scraping rental listings
   - For automatic ChromeDriver installation

### Recommended

- **Git** (for cloning/updating) - https://git-scm.com/
- **Virtual environment** (for isolated Python environment)
- 2 GB free disk space
- 4 GB RAM minimum

---

## ⚡ Quick Install

If you already have Python 3.8+ and Chrome installed:

```bash
# Navigate to the project directory
cd rental-scanner

# Install core dependencies
pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler

# Run the application
python app.py
```

Open browser to: **http://localhost:5000**

**First search will take 30-60 seconds** while ChromeDriver downloads automatically.

---

## 📦 Detailed Installation

### Step 1: Install Python

#### Windows
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ **Important**: Check "Add Python to PATH"
4. Complete installation
5. Open Command Prompt and verify:
   ```cmd
   python --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python3

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip

# Verify
python3 --version
pip3 --version
```

### Step 2: Install Google Chrome

#### Windows / macOS
1. Download from: https://www.google.com/chrome/
2. Run installer
3. Complete installation
4. Verify by opening Chrome browser

#### Linux (Ubuntu/Debian)
```bash
# Download and install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Verify
google-chrome --version
```

### Step 3: Get the Project Files

If you have the project already, skip to Step 4.

```bash
# If using Git
git clone <repository-url>
cd rental-scanner

# Or extract from ZIP file
# Then navigate to the directory
cd rental-scanner
```

### Step 4: Install Python Dependencies

#### Option A: Install Core Dependencies Only (Recommended)

```bash
# Navigate to project directory
cd rental-scanner

# Install core packages
pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler
```

#### Option B: Install from requirements.txt (Advanced)

This attempts to install all packages (may fail on some that need compilation):

```bash
pip install -r requirements.txt
```

**Note**: If this fails on packages like `psycopg2-binary` or `lxml`, use Option A instead. These packages are optional for local development.

### Step 5: Verify Installation

Check that all required packages are installed:

```bash
python -c "import flask; import requests; import bs4; import selenium; print('✓ All packages installed successfully!')"
```

Expected output:
```
✓ All packages installed successfully!
```

### Step 6: Test Scrapers

```bash
python -c "from scrapers.scraper_manager import ScraperManager; manager = ScraperManager({'enabled_scrapers': ['kijiji', 'realtor_ca', 'rentals_ca']}); print('✓ All scrapers loaded'); print('✓ Enabled:', ', '.join(manager.get_enabled_scrapers()))"
```

Expected output:
```
✓ All scrapers loaded
✓ Enabled: kijiji, realtor_ca, rentals_ca
```

---

## ✅ Verifying Installation

### Check Python Version
```bash
python --version
# Should show: Python 3.8.x or higher
```

### Check Chrome Installation
```bash
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Linux
google-chrome --version
```

### Check Required Packages
```bash
pip list | grep -E "Flask|requests|beautifulsoup4|selenium|webdriver-manager"
```

Should show:
- Flask (3.x)
- requests (2.x)
- beautifulsoup4 (4.x)
- selenium (4.x)
- webdriver-manager (4.x)

---

## 🚀 First Run

### Start the Application

```bash
# Make sure you're in the rental-scanner directory
cd rental-scanner

# Run the application
python app.py
```

You should see:
```
Starting Rental Scanner application...
Enabled scrapers: kijiji, realtor_ca, rentals_ca
 * Running on http://0.0.0.0:5000
```

### Access the Web Interface

Open your browser and navigate to:
- **Local access**: http://localhost:5000
- **Network access**: http://127.0.0.1:5000
- **Mobile/other device**: http://[your-computer-ip]:5000

### First Search

1. The location field should already say "Newmarket"
2. Optionally enter price range (e.g., Min: 1500, Max: 2500)
3. Click **"Search Rentals"**
4. ⏳ **Wait 30-60 seconds** on first search (ChromeDriver auto-download)
5. Subsequent searches will be faster (10-20 seconds)

### What to Expect

**First Search:**
- Duration: 30-60 seconds
- ChromeDriver downloads automatically to `~/.wdm/` folder
- Browser automation initializes
- Results appear from all three sources

**Subsequent Searches:**
- Duration: 10-20 seconds
- Kijiji: 2-5 seconds
- Realtor.ca: 2-5 seconds
- Rentals.ca: 10-15 seconds (uses headless Chrome)
- Results combined and deduplicated

---

## 🔧 Troubleshooting

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solutions**:
1. Reinstall Python with "Add to PATH" checked
2. Use `python3` instead of `python` (macOS/Linux)
3. Use full path: `C:\Python310\python.exe` (Windows)
4. Restart terminal/command prompt after installation

### pip Not Found

**Error**: `'pip' is not recognized...`

**Solutions**:
1. Use `python -m pip` instead of `pip`
2. Use `pip3` instead of `pip` (macOS/Linux)
3. Reinstall Python ensuring pip is included

### Permission Denied (Windows)

**Error**: `Access is denied` or `Permission denied`

**Solutions**:
1. Run Command Prompt as Administrator
2. Use `--user` flag: `pip install --user <package>`
3. Check antivirus/firewall settings

### Permission Denied (macOS/Linux)

**Error**: `Permission denied` when installing packages

**Solutions**:
```bash
# Use --user flag (recommended)
pip install --user <package>

# Or use sudo (not recommended)
sudo pip install <package>
```

### Chrome Not Found

**Error**: `chrome not reachable` or `Chrome binary not found`

**Solutions**:
1. Install Google Chrome browser
2. Verify installation: `google-chrome --version`
3. Restart terminal after installation
4. Check Chrome is in default location

### ChromeDriver Issues

**Error**: `ChromeDriver not found` or `session not created`

**Solutions**:
1. **First run**: Wait 60 seconds for auto-download
2. **Internet required**: Check connection
3. **Clear cache**: Delete `~/.wdm/` folder
4. **Chrome version**: Update Chrome to latest version
5. **Manual install**: Download from https://chromedriver.chromium.org/

### Selenium Errors

**Error**: `No module named 'selenium'`

**Solution**:
```bash
pip install selenium webdriver-manager
```

**Error**: `Message: session not created: This version of ChromeDriver only supports Chrome version X`

**Solution**:
- Update Google Chrome to latest version
- Or delete `~/.wdm/` folder to force ChromeDriver re-download

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solutions**:
```bash
# Install missing package
pip install flask

# Or reinstall all dependencies
pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler
```

### Port Already in Use

**Error**: `Address already in use: Port 5000`

**Solutions**:
1. Stop other application using port 5000
2. Use different port:
   ```bash
   # Edit app.py, change last line to:
   app.run(host="0.0.0.0", port=8000, debug=True)
   ```
3. Find and kill process using port 5000 (advanced)

### No Results Found

**Issue**: Search completes but shows 0 results

**Solutions**:
1. Check internet connection
2. Try different city name (spelling matters)
3. Remove price filters (search all prices)
4. Check console for error messages
5. Verify scrapers loaded: Look for "Enabled scrapers: kijiji, realtor_ca, rentals_ca"

### Slow Searches

**Issue**: Every search takes 30+ seconds

**Solutions**:
1. First search is always slower (normal)
2. Check internet speed
3. Rentals.ca uses browser automation (10-15 seconds is normal)
4. Disable Rentals.ca if too slow:
   - Edit `app.py`
   - Change line 26 to: `"enabled_scrapers": ["kijiji", "realtor_ca"],`

---

## 🔄 Updating

### Update Python Packages

```bash
# Update all packages
pip install --upgrade Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler

# Or update from requirements.txt
pip install --upgrade -r requirements.txt
```

### Update ChromeDriver

ChromeDriver is updated automatically by webdriver-manager.

To force update:
```bash
# Delete cache
rm -rf ~/.wdm/  # macOS/Linux
# or
rmdir /s %USERPROFILE%\.wdm  # Windows

# Next run will download latest version
```

### Update Application Code

```bash
# If using Git
git pull origin main

# Or download new version and replace files
```

---

## 🐍 Virtual Environment (Optional but Recommended)

Using a virtual environment keeps dependencies isolated.

### Create Virtual Environment

```bash
# Navigate to project directory
cd rental-scanner

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Install Dependencies in Virtual Environment

```bash
# After activation, install packages
pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler
```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## 📝 Installation Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] Google Chrome browser installed
- [ ] Project files downloaded/extracted
- [ ] Core dependencies installed (Flask, requests, beautifulsoup4, selenium, etc.)
- [ ] Test command runs successfully
- [ ] Scrapers load without errors
- [ ] Application starts: `python app.py`
- [ ] Web interface accessible at http://localhost:5000
- [ ] First search completes (may take 60 seconds)
- [ ] Subsequent searches work faster

---

## 🎓 Next Steps

Once installation is complete:

1. **Read the Quick Start**: `NEWMARKET_QUICK_START.md`
2. **Learn the configuration**: `NEWMARKET_CONFIG.md`
3. **Start searching**: Default is set to Newmarket, ON
4. **Explore nearby cities**: Aurora, Richmond Hill, Bradford, etc.

---

## 💡 Tips

- **First search**: Takes longer (ChromeDriver download), be patient
- **Antivirus**: May slow down Selenium, add exception if needed
- **Firewall**: Allow Python and Chrome through firewall
- **Updates**: Keep Chrome updated for best compatibility
- **Cache**: ChromeDriver cache is stored in `~/.wdm/` folder
- **Logs**: Check console output for detailed information
- **Help**: See `NEWMARKET_QUICK_START.md` for usage examples

---

## 🆘 Getting Help

If you're still having issues:

1. Check console output for error messages
2. Verify all system requirements are met
3. Try the quick install commands again
4. Check that Chrome is properly installed
5. Review the troubleshooting section above

### Common Issues Summary

| Issue | Quick Fix |
|-------|-----------|
| Python not found | Add Python to PATH, restart terminal |
| pip not found | Use `python -m pip` instead |
| Chrome not found | Install Google Chrome browser |
| Permission denied | Use `pip install --user` or run as admin |
| Import errors | Install missing package: `pip install <package>` |
| First search slow | Normal - ChromeDriver downloading (60 seconds) |
| Port in use | Change port in app.py or stop other app |

---

## ✅ Installation Complete!

You're ready to start finding rentals in the Newmarket area!

Run: `python app.py`  
Visit: **http://localhost:5000**

**Happy House Hunting! 🏠**

---

*Last Updated: January 2025*  
*Version: 2.1 - Newmarket Edition*