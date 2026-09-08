# 🦅 rentFalcon

## *get the swoop on landlords*
**Fast, Multi-Source Rental Search for York Region, Ontario**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

---

## 🎯 What is rentFalcon?

rentFalcon is a powerful rental listing aggregator that searches **multiple rental websites simultaneously** and displays all results in one clean interface. Stop checking Kijiji, Rentals.ca, and other sites separately!

**Perfect for finding rentals in Newmarket, ON and surrounding areas** (Aurora, Richmond Hill, Bradford, Markham, Vaughan, and more).

### ✨ Key Features

- 🔍 **Multi-Source Search** - Searches Kijiji and Rentals.ca at once
- ⚡ **Fast Results** - Get 30-50 listings in 10-15 seconds
- 🎯 **Smart Deduplication** - Automatically removes duplicate listings
- 🏘️ **8 Cities Supported** - Newmarket area within 25 km radius
- 💰 **Price Filtering** - Set your budget and find matches
- 🆓 **Completely Free** - No ads, no subscriptions, no hidden costs
- 🖥️ **User-Friendly** - Clean web interface, no technical knowledge required

---

## 📸 Screenshots

### Search Interface
Clean, simple search form with location and price filters.

### Results View
All listings from multiple sources in one place, with duplicate removal.

---

## 🚀 Quick Start

### For Non-Technical Users (Windows)

1. **Download** the project (.zip file)
2. **Double-click** `EASY_SETUP.bat`
3. **Follow** on-screen instructions (5 minutes)
4. **Start searching!** Use desktop shortcut or `START_RENTAL_SCANNER.bat`

That's it! Everything installs automatically.

### For Developers

```bash
# Clone the repository
git clone https://github.com/yourusername/rentFalcon.git
cd rentFalcon

# Install dependencies
pip install -r requirements.txt

# Copy the environment template and set a real secret key
cp .env.example .env
#   SECRET_KEY is REQUIRED for stable sessions. Generate one with:
#   python -c "import secrets; print(secrets.token_hex(32))"

# Run the application
python app.py
```

> **Security:** `SECRET_KEY` is read from the environment. If unset, the app falls back to an ephemeral random key (sessions reset on restart) — fine for local dev, never for production. All state-changing routes are CSRF-protected via Flask-WTF; programmatic clients must fetch a token from `GET /api/csrf-token` and send it as the `X-CSRFToken` header.

Visit `http://localhost:5000` in your browser.

---

## 💻 System Requirements

- **Python 3.8+**
- **Google Chrome** (for Rentals.ca scraper)
- **Internet connection**
- **Windows 10/11** (batch files for Windows; manual setup for Mac/Linux)

---

## 🏘️ Supported Cities

rentFalcon searches rentals in these cities within 25 km of Newmarket:

| City | Distance | Typical Rent Range |
|------|----------|-------------------|
| Newmarket | Center | $1,400 - $2,800 |
| Aurora | 8 km | $1,600 - $2,900 |
| Richmond Hill | 12 km | $1,800 - $3,500 |
| Bradford | 20 km | $1,200 - $2,200 |
| East Gwillimbury | 15 km | $1,400 - $2,500 |
| Markham | 18 km | $1,800 - $3,200 |
| Vaughan | 20 km | $1,900 - $3,500 |
| King City | 10 km | $1,800 - $3,000 |

---

## 📖 Documentation

- **[User Guide](USER_GUIDE_SIMPLE.md)** - Complete guide for non-technical users
- **[Quick Reference](QUICK_REFERENCE.md)** - Quick tips and commands
- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Newmarket Quick Start](NEWMARKET_QUICK_START.md)** - Search examples and tips

---

## 🔧 Installation

### Automatic Setup (Windows)

```bash
# Run the easy setup script
EASY_SETUP.bat
```

This will:
- ✅ Check Python installation
- ✅ Check Chrome installation
- ✅ Install all required packages
- ✅ Create desktop shortcut
- ✅ Launch the application

### Manual Installation

```bash
# Install core dependencies
pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler

# Run the application
python app.py
```

---

## 🎮 Usage

### Starting the Application

**Windows:**
- Double-click `START_RENTAL_SCANNER.bat`
- Or use the desktop shortcut "rentFalcon"

**Manual:**
```bash
python app.py
```

### Searching for Rentals

1. Open `http://localhost:5000` in your browser
2. Enter location (default: Newmarket)
3. Set price range (optional)
4. Click "Search Rentals"
5. View 30-50 results in 10-15 seconds!

### Example Searches

**Affordable 1-Bedroom in Newmarket:**
```
Location: Newmarket
Min Price: 1400
Max Price: 1800
```

**Family Home in Aurora:**
```
Location: Aurora
Min Price: 2000
Max Price: 2800
```

---

## 🏗️ Architecture

### Technology Stack

- **Backend:** Python 3.13, Flask 3.1
- **Scraping:** BeautifulSoup, Selenium, Requests
- **Browser Automation:** Selenium WebDriver, ChromeDriver
- **Scheduling:** APScheduler
- **Frontend:** HTML, CSS, Vanilla JavaScript

### Data Sources

| Source | Status | Method | Speed |
|--------|--------|--------|-------|
| Kijiji | ✅ Active | HTML/JSON-LD parsing | 3-5s |
| Rentals.ca | ✅ Active | Selenium automation | 10-15s |
| Realtor.ca | ⚠️ Disabled | API blocked | N/A |

### Features

- **Parallel Scraping** - All scrapers run simultaneously
- **Smart Deduplication** - 85% similarity threshold
- **Automatic Retries** - Handles temporary failures
- **Rate Limiting** - Respects source websites
- **Caching** - ChromeDriver cached after first download
- **Error Handling** - Graceful failures, app continues

---

## 🔒 Privacy & Safety

- ✅ **No data collection** - Everything runs locally
- ✅ **No tracking** - Your searches are private
- ✅ **No accounts** - No login required
- ✅ **Read-only** - Only reads public listings
- ✅ **Open source** - Inspect the code yourself

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Average search time | 10-15 seconds |
| Typical results | 30-50 unique listings |
| Deduplication rate | ~32% duplicates removed |
| First search time | 30-60 seconds (one-time ChromeDriver setup) |
| Success rate | 100% (2/2 active scrapers) |

---

## 🛠️ Development

### Project Structure

```
rentFalcon/
├── app.py                  # Main Flask application
├── config.py              # Configuration
├── scrapers/              # Scraper modules
│   ├── base_scraper.py   # Base scraper class
│   ├── kijiji_scraper.py # Kijiji implementation
│   ├── rentals_ca_scraper.py # Rentals.ca implementation
│   └── scraper_manager.py # Coordinates scrapers
├── templates/             # HTML templates
│   └── index.html        # Main search interface
├── static/               # CSS and assets
├── models/               # Database models
└── docs/                 # Documentation

```

### Running Tests

```bash
python test_scrapers.py
```

### Adding a New Scraper

1. Create new scraper class in `scrapers/`
2. Inherit from `BaseScraper`
3. Implement required methods
4. Register in `scraper_manager.py`
5. Test and submit PR!

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Ideas for Contributions

- [ ] Add more rental sources (Facebook Marketplace, PadMapper, etc.)
- [ ] Support for Mac/Linux
- [ ] Add saved searches feature
- [ ] Email notifications for new listings
- [ ] Map view of results
- [ ] Export to CSV/Excel
- [ ] Mobile app version
- [ ] More cities/regions

---

## 🐛 Troubleshooting

### "Python is not installed"
- Install Python from [python.org](https://www.python.org/downloads/)
- **Important:** Check "Add Python to PATH" during installation
- Restart computer

### "Chrome not found"
- Install Chrome from [google.com/chrome](https://www.google.com/chrome/)
- Run `EASY_SETUP.bat` again

### No results found
- Check spelling of city name
- Remove price filters
- Try a different city
- Verify internet connection

### First search is slow
- **Normal!** ChromeDriver downloads on first run (30-60 seconds)
- Only happens once
- Subsequent searches are fast (10-15 seconds)

More help: See [USER_GUIDE_SIMPLE.md](USER_GUIDE_SIMPLE.md)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Original Creator** - [jd gramsci](https://github.com/pvnkmnk)

---

## 🙏 Acknowledgments

- Thanks to all the rental websites for providing public data, thank you to Inn from the Cold for the inspiration
- Built with Flask, BeautifulSoup, and Selenium
- Inspired by the need for streamlined housing access, and the desire to build dual power where ever I can.

---

## 📞 Support

- **Documentation:** Check the `docs/` folder
- **Issues:** Open an issue on GitHub
- **Questions:** See [USER_GUIDE_SIMPLE.md](USER_GUIDE_SIMPLE.md)

---

## 🗺️ Roadmap

### Version 2.1 (Current)
- ✅ Multi-source scraping (Kijiji + Rentals.ca)
- ✅ 8 cities in Newmarket area
- ✅ Easy setup for non-technical users
- ✅ Desktop shortcut support

### Version 2.2 (Planned)
- [ ] Add Facebook Marketplace scraper
- [ ] Saved searches feature
- [ ] Email/Discord/Telegram notifications
- [ ] Mac/Linux support

### Version 3.0 (Future)
- [ ] Map view of listings
- [ ] Mobile app
- [ ] Web App
- [ ] Docker Image
- [ ] User accounts (optional)
- [ ] Expand to all Canadian provinces/territories

---

## ⭐ Star This Project!

If rentFalcon helps you find a rental, please give it a star! ⭐

Share with your friends and take care of your community! Housing First!

---

## 📊 Stats

- **Lines of Code:** ~5,000+
- **Files:** 50+
- **Scrapers:** 2 active (3 total)
- **Cities Supported:** 8
- **Documentation Pages:** 10+
- **Development Time:** 5 days
- **Status:** ✅ Production Ready

---

**Made with ❤️ for the working class**

🦅 **rentFalcon** - *get the swoop on landlords*

---

## 📌 Quick Links

- [Download Latest Release](https://github.com/yourusername/rentFalcon/releases)
- [Report a Bug](https://github.com/yourusername/rentFalcon/issues)
- [Request a Feature](https://github.com/yourusername/rentFalcon/issues)
- [View Documentation](https://github.com/yourusername/rentFalcon/tree/main/docs)

---

*Last Updated: November 2025*
