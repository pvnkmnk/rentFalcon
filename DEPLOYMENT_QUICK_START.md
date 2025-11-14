# Rental Scanner - Quick Start Deployment Guide

Choose your deployment method and get started in minutes.

---

## 🚀 Quick Comparison

| Deployment Method | Setup Time | Best For | Cost | Multi-User |
|-------------------|------------|----------|------|------------|
| **Local Python** | 5 min | Development, testing | Free | No |
| **Standalone .exe** | 10 min | Personal desktop use | Free | No |
| **Hosted VPS** | 30 min | Small team (4-5 users) | $10-15/mo | Yes |
| **Docker** | 15 min | Production, scalability | Free-$20/mo | Yes |

---

## Option 1: Local Python (Fastest Start)

**Perfect for:** Trying it out, development, personal use

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/rental-scanner.git
cd rental-scanner
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install and configure
pip install -r requirements.txt
cp .env.example .env
# Edit .env: Set SECRET_KEY and DATABASE_URL

# 4. Initialize database
flask db upgrade
python -c "from models.database import db, create_default_user; from app import app; app.app_context().push(); db.create_all(); create_default_user()"

# 5. Run
python app.py
```

**Access at:** http://localhost:5000

**Pros:** ✅ Quick setup, easy debugging, no build needed  
**Cons:** ❌ Requires Python, single user, not portable

---

## Option 2: Standalone Executable

**Perfect for:** Desktop app, no Python installation, sharing with friends

```bash
# 1. Build (requires Python first)
cd rental-scanner
pip install pyinstaller
cd deployment
pyinstaller rental-scanner.spec

# 2. Package
cd dist
# Windows:
powershell Compress-Archive -Path rental-scanner -DestinationPath rental-scanner-windows.zip
# Linux/Mac:
tar -czf rental-scanner.tar.gz rental-scanner/

# 3. Distribute
# Copy entire rental-scanner folder to target machine
# Include .env file with configuration

# 4. Run
cd rental-scanner
./rental-scanner  # or rental-scanner.exe on Windows
```

**Access at:** http://localhost:5000

**Pros:** ✅ No Python needed, portable, self-contained  
**Cons:** ❌ Large file size (100-200MB), slower startup, platform-specific

---

## Option 3: Hosted VPS (Small Team)

**Perfect for:** 4-5 users, remote access, always available

**One-Command Setup (Ubuntu 22.04):**

```bash
# Run this automated setup script
curl -sSL https://raw.githubusercontent.com/yourusername/rental-scanner/main/deployment/setup-vps.sh | bash
```

**Manual Setup:**

```bash
# 1. Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv postgresql nginx redis-server git

# 2. Setup database
sudo -u postgres psql -c "CREATE DATABASE rental_scanner;"
sudo -u postgres psql -c "CREATE USER rental_user WITH PASSWORD 'your-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE rental_scanner TO rental_user;"

# 3. Deploy application
sudo mkdir -p /opt/rental-scanner
cd /opt/rental-scanner
git clone https://github.com/yourusername/rental-scanner.git app
cd app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn

# 4. Configure
cp .env.example .env
nano .env  # Set production values

# 5. Setup systemd service (see DEPLOYMENT_GUIDE.md for service file)
sudo systemctl enable rental-scanner
sudo systemctl start rental-scanner

# 6. Configure Nginx (see DEPLOYMENT_GUIDE.md for nginx config)
sudo systemctl restart nginx
```

**Access at:** http://your-server-ip or http://your-domain.com

**Pros:** ✅ Multi-user, remote access, always on, scheduled scans  
**Cons:** ❌ Monthly cost, requires server maintenance, more complex

---

## Option 4: Docker (Recommended for Production)

**Perfect for:** Production deployment, scalability, easy updates

**One-Command Start:**

```bash
# 1. Clone repository
git clone https://github.com/yourusername/rental-scanner.git
cd rental-scanner/deployment

# 2. Configure environment
cp ../.env.example .env
nano .env  # Set production values

# 3. Start everything
docker compose up -d

# 4. Initialize database
docker compose exec web flask db upgrade
docker compose exec web python -c "
from models.database import db, User
from app import app
with app.app_context():
    user = User(username='admin', email='admin@localhost', password='changeme')
    db.session.add(user)
    db.session.commit()
"
```

**Access at:** http://localhost:5000

**Pros:** ✅ Isolated environment, easy updates, includes PostgreSQL + Redis  
**Cons:** ❌ Requires Docker knowledge, higher resource usage

---

## 🔧 Essential Configuration (All Methods)

### Minimum .env Settings

```ini
# Required
FLASK_ENV=production  # or development
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=sqlite:///rental_scanner.db  # or postgresql://...

# Scrapers
ENABLED_SCRAPERS=kijiji,realtor,rentals,viewit,apartments

# Email (optional)
MAIL_ENABLED=false
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📊 Decision Tree

```
Do you need multiple users?
├─ NO → Do you have Python installed?
│        ├─ YES → Use Option 1 (Local Python)
│        └─ NO → Use Option 2 (Standalone Executable)
│
└─ YES → Do you want easiest deployment?
         ├─ YES → Use Option 4 (Docker)
         └─ NO → Use Option 3 (Hosted VPS)
```

---

## 🚨 Common First-Time Issues

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Change port in .env
WEB_PORT=8000
```

### Issue: "Database connection failed"

**Solution:**
```bash
# Check DATABASE_URL in .env
# For SQLite: sqlite:///rental_scanner.db
# For PostgreSQL: postgresql://user:pass@localhost:5432/dbname
```

### Issue: "No listings found"

**Solution:**
```ini
# Enable debug mode in .env
SAVE_DEBUG_HTML=true
LOG_LEVEL=DEBUG
# Check debug_output/ folder for saved HTML
```

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Next Steps

1. **After Setup:**
   - Access the web interface
   - Create your first search
   - Verify results from multiple sources
   - Save a search (optional)

2. **For Production Use:**
   - Enable HTTPS (use Let's Encrypt)
   - Set up email notifications
   - Configure scheduled scans
   - Set up database backups

3. **For Development:**
   - Read IMPLEMENTATION_ROADMAP.md
   - Check out the code structure
   - Add new scrapers
   - Run tests with `pytest`

---

## 🆘 Getting Help

**Documentation:**
- Full deployment guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Implementation roadmap: [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)
- Application overview: [APPLICATION_DESCRIPTION.md](APPLICATION_DESCRIPTION.md)

**Troubleshooting:**
- Check logs: `tail -f rental_scanner.log`
- Docker logs: `docker compose logs -f`
- System logs: `journalctl -u rental-scanner -f`

**Support:**
- GitHub Issues: [Report a bug or request feature](https://github.com/yourusername/rental-scanner/issues)
- Email: support@rentalscanner.com

---

## 🎯 Quick Test

After deployment, verify everything works:

```bash
# Test 1: Check if server is running
curl http://localhost:5000/health

# Test 2: Run a test search (Python)
python -c "
from scrapers.kijiji_scraper import KijijiScraper
scraper = KijijiScraper()
results = scraper.search('ottawa', 1000, 2000)
print(f'Found {len(results)} listings')
"

# Test 3: Check database
sqlite3 rental_scanner.db "SELECT COUNT(*) FROM listings;"
# or for PostgreSQL:
psql rental_scanner -c "SELECT COUNT(*) FROM listings;"
```

---

## 🎉 You're Ready!

Choose your deployment method above and follow the steps. Most setups take less than 15 minutes.

**Recommended Path for Beginners:**
1. Start with **Option 1 (Local Python)** to try it out
2. If you like it, move to **Option 4 (Docker)** for production

**Recommended Path for Teams:**
1. Use **Option 4 (Docker)** from the start
2. Deploy on a $12/month DigitalOcean droplet
3. Point a domain to it and enable HTTPS

Good luck! 🚀