# Rental Scanner - Comprehensive Deployment Guide

This guide covers all deployment options for the Rental Scanner application, from local development to production Docker deployment.

---

## Table of Contents

1. [Option 1: Local Python Development](#option-1-local-python-development)
2. [Option 2: Standalone Executable (Windows/Mac/Linux)](#option-2-standalone-executable-windowsmaclinux)
3. [Option 3: Single Hosted Web Service (4-5 Users)](#option-3-single-hosted-web-service-4-5-users)
4. [Option 4: Docker Container Deployment](#option-4-docker-container-deployment)
5. [Post-Deployment Configuration](#post-deployment-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Option 1: Local Python Development

**Best for:** Personal use, testing, development

**Requirements:**
- Python 3.11 or higher
- 1GB RAM minimum
- Windows, macOS, or Linux

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/yourusername/rental-scanner.git
cd rental-scanner
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred text editor
# At minimum, set these values:
# FLASK_ENV=development
# SECRET_KEY=your-random-secret-key-here
# DATABASE_URL=sqlite:///rental_scanner.db
```

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5: Initialize Database

```bash
# Initialize the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Create default user (if in single-user mode)
python -c "from models.database import db, create_default_user; from app import app; app.app_context().push(); db.create_all(); create_default_user()"
```

### Step 6: Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Step 7: (Optional) Run Scheduled Tasks

In a separate terminal, with the virtual environment activated:

```bash
python tasks/scheduler.py
```

### Pros and Cons

✅ **Pros:**
- Easy to modify and test
- No build process required
- Direct access to logs and debugging
- Minimal resource usage

❌ **Cons:**
- Requires Python installation
- Must keep terminal open
- Not suitable for multiple users
- Manual updates required

---

## Option 2: Standalone Executable (Windows/Mac/Linux)

**Best for:** Single-user desktop application, no Python installation required

**Requirements:**
- Python 3.11+ (for building only)
- 2GB RAM
- 500MB disk space

### Step 1: Prepare the Application

Follow Option 1, Steps 1-3 to set up the development environment.

### Step 2: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 3: Build the Executable

**Navigate to deployment directory:**
```bash
cd deployment
```

**Build (One-Folder Distribution - Recommended):**
```bash
pyinstaller rental-scanner.spec
```

This creates a `dist/rental-scanner/` folder with the executable and all dependencies.

**Build (One-File Distribution - Alternative):**

Edit `rental-scanner.spec` and uncomment the "ONE-FILE" section, then:
```bash
pyinstaller rental-scanner.spec --onefile
```

### Step 4: Package the Application

Create a distribution package:

**Windows:**
```bash
# Navigate to dist folder
cd dist

# Create a zip file
powershell Compress-Archive -Path rental-scanner -DestinationPath rental-scanner-windows.zip
```

**Linux/macOS:**
```bash
cd dist
tar -czf rental-scanner-linux.tar.gz rental-scanner/
```

### Step 5: Distribution

1. Copy the entire `rental-scanner` folder to the target machine
2. Include the `.env.example` file (renamed to `.env`)
3. Create a `data` folder for the SQLite database
4. Create a README with instructions

### Step 6: Running the Executable

**Windows:**
```bash
cd rental-scanner
rental-scanner.exe
```

**Linux/macOS:**
```bash
cd rental-scanner
chmod +x rental-scanner
./rental-scanner
```

Access the application at: `http://localhost:5000`

### Creating Desktop Shortcuts

**Windows (.bat launcher):**
Create `start-rental-scanner.bat`:
```batch
@echo off
cd /d "%~dp0rental-scanner"
start "" rental-scanner.exe
start http://localhost:5000
```

**macOS (Automator App):**
1. Open Automator
2. Create new Application
3. Add "Run Shell Script" action:
```bash
cd ~/Applications/rental-scanner
./rental-scanner &
sleep 2
open http://localhost:5000
```
4. Save as "Rental Scanner.app"

**Linux (.desktop launcher):**
Create `rental-scanner.desktop`:
```ini
[Desktop Entry]
Name=Rental Scanner
Comment=Apartment Rental Search Tool
Exec=/path/to/rental-scanner/rental-scanner
Icon=/path/to/icon.png
Terminal=false
Type=Application
Categories=Utility;
```

### Pros and Cons

✅ **Pros:**
- No Python installation needed
- Easy to distribute
- Self-contained application
- Works offline (for database queries)

❌ **Cons:**
- Large file size (100-200MB)
- Slower startup time
- Platform-specific builds required
- Still single-user only

---

## Option 3: Single Hosted Web Service (4-5 Users)

**Best for:** Small team, remote access, always available

**Requirements:**
- VPS or cloud server (DigitalOcean, Linode, AWS EC2, etc.)
- Ubuntu 22.04 LTS (recommended)
- 2GB RAM minimum (4GB recommended)
- 20GB disk space
- Domain name (optional but recommended)

### Infrastructure Options

**Recommended Providers:**
- DigitalOcean Droplet ($12/month for 2GB RAM)
- Linode Nanode ($10/month for 2GB RAM)
- AWS EC2 t3.small (~$15/month)
- Hetzner Cloud CX21 (~$6/month)

### Step 1: Server Setup

**SSH into your server:**
```bash
ssh root@your-server-ip
```

**Update system:**
```bash
apt update && apt upgrade -y
```

**Install required packages:**
```bash
apt install -y python3.11 python3.11-venv python3-pip postgresql nginx certbot python3-certbot-nginx redis-server git
```

### Step 2: Create Application User

```bash
adduser --system --group --home /opt/rental-scanner rental-scanner
```

### Step 3: Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE rental_scanner;
CREATE USER rental_user WITH PASSWORD 'your-secure-password-here';
GRANT ALL PRIVILEGES ON DATABASE rental_scanner TO rental_user;
\q
```

### Step 4: Deploy Application

```bash
# Switch to application user
sudo -iu rental-scanner

# Clone repository
cd /opt/rental-scanner
git clone https://github.com/yourusername/rental-scanner.git app
cd app

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### Step 5: Configure Environment

```bash
# Create .env file
cp .env.example .env
nano .env
```

**Update these settings:**
```ini
FLASK_ENV=production
SECRET_KEY=generate-a-strong-random-key
DATABASE_URL=postgresql://rental_user:your-secure-password-here@localhost:5432/rental_scanner
MULTI_USER_ENABLED=true
REQUIRE_LOGIN=true
MAX_SAVED_SEARCHES_PER_USER=10
REDIS_URL=redis://localhost:6379/0
```

### Step 6: Initialize Database

```bash
flask db upgrade
python -c "from models.database import db, User; from app import app; app.app_context().push(); db.create_all()"
```

### Step 7: Create Systemd Service

Exit from rental-scanner user:
```bash
exit
```

Create service file:
```bash
nano /etc/systemd/system/rental-scanner.service
```

**Add this content:**
```ini
[Unit]
Description=Rental Scanner Web Application
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=rental-scanner
Group=rental-scanner
WorkingDirectory=/opt/rental-scanner/app
Environment="PATH=/opt/rental-scanner/app/venv/bin"
ExecStart=/opt/rental-scanner/app/venv/bin/gunicorn \
    --workers 2 \
    --threads 4 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/rental-scanner/access.log \
    --error-logfile /var/log/rental-scanner/error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Create log directory:**
```bash
mkdir -p /var/log/rental-scanner
chown rental-scanner:rental-scanner /var/log/rental-scanner
```

### Step 8: Configure Nginx

```bash
nano /etc/nginx/sites-available/rental-scanner
```

**Add this configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or use server IP

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 120s;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /opt/rental-scanner/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Enable the site:**
```bash
ln -s /etc/nginx/sites-available/rental-scanner /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 9: Setup SSL Certificate (Recommended)

```bash
certbot --nginx -d your-domain.com
```

Follow the prompts to configure HTTPS.

### Step 10: Start Services

```bash
systemctl enable rental-scanner
systemctl start rental-scanner
systemctl status rental-scanner
```

### Step 11: Setup Scheduler (Optional)

Create scheduler service:
```bash
nano /etc/systemd/system/rental-scanner-scheduler.service
```

```ini
[Unit]
Description=Rental Scanner Task Scheduler
After=network.target rental-scanner.service

[Service]
Type=simple
User=rental-scanner
Group=rental-scanner
WorkingDirectory=/opt/rental-scanner/app
Environment="PATH=/opt/rental-scanner/app/venv/bin"
ExecStart=/opt/rental-scanner/app/venv/bin/python tasks/scheduler.py

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable rental-scanner-scheduler
systemctl start rental-scanner-scheduler
```

### Step 12: Configure Firewall

```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### User Management

Create users through Python shell:
```bash
sudo -u rental-scanner -i
cd /opt/rental-scanner/app
source venv/bin/activate
python
```

```python
from app import app
from models.database import db, User

with app.app_context():
    user = User(username='john', email='john@example.com', password='secure-password')
    db.session.add(user)
    db.session.commit()
    print(f"Created user: {user.username}")
```

### Monitoring and Maintenance

**View logs:**
```bash
# Application logs
tail -f /var/log/rental-scanner/access.log
tail -f /var/log/rental-scanner/error.log

# Service logs
journalctl -u rental-scanner -f
```

**Update application:**
```bash
sudo -u rental-scanner -i
cd /opt/rental-scanner/app
git pull
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
exit
systemctl restart rental-scanner
```

### Pros and Cons

✅ **Pros:**
- Multiple users supported
- Access from anywhere
- Always running
- Centralized data
- Automatic scheduled scans

❌ **Cons:**
- Monthly hosting costs
- Requires server maintenance
- Need to manage security updates
- More complex setup

---

## Option 4: Docker Container Deployment

**Best for:** Easy deployment, scalability, consistency across environments

**Requirements:**
- Docker 24.0+ and Docker Compose 2.0+
- 4GB RAM minimum
- 20GB disk space
- Linux (Ubuntu 22.04 recommended)

### Method A: Simple Docker Compose (Recommended)

### Step 1: Install Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable docker
systemctl start docker

# Install Docker Compose
apt install docker-compose-plugin
```

**Verify installation:**
```bash
docker --version
docker compose version
```

### Step 2: Prepare Application

```bash
# Clone repository
git clone https://github.com/yourusername/rental-scanner.git
cd rental-scanner
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Update for Docker deployment:**
```ini
FLASK_ENV=docker
SECRET_KEY=generate-strong-random-key-here
POSTGRES_DB=rental_scanner
POSTGRES_USER=rental_user
POSTGRES_PASSWORD=strong-database-password
REDIS_URL=redis://redis:6379/0
MULTI_USER_ENABLED=true
REQUIRE_LOGIN=true
ENABLED_SCRAPERS=kijiji,realtor,rentals,viewit,apartments
```

### Step 4: Build and Start

```bash
cd deployment

# Build images
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

### Step 5: Initialize Database

```bash
# Run migrations
docker compose exec web flask db upgrade

# Create initial user
docker compose exec web python -c "
from models.database import db, User
from app import app
with app.app_context():
    user = User(username='admin', email='admin@localhost', password='changeme')
    db.session.add(user)
    db.session.commit()
    print('Created admin user')
"
```

### Step 6: Access Application

The application will be available at:
- `http://localhost:5000` (or your server IP)

### Step 7: Setup Nginx Reverse Proxy (Production)

**Uncomment nginx service in docker-compose.yml**, then create:

```bash
nano deployment/nginx.conf
```

```nginx
events {
    worker_connections 1024;
}

http {
    upstream rental_scanner {
        server web:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://rental_scanner;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

Restart:
```bash
docker compose restart nginx
```

### Docker Management Commands

**View running containers:**
```bash
docker compose ps
```

**Stop all services:**
```bash
docker compose down
```

**Stop and remove volumes (WARNING: deletes data):**
```bash
docker compose down -v
```

**View logs:**
```bash
docker compose logs -f web
docker compose logs -f celery-worker
```

**Restart specific service:**
```bash
docker compose restart web
```

**Execute commands in container:**
```bash
docker compose exec web bash
```

**Update and restart:**
```bash
git pull
docker compose build
docker compose up -d
```

### Method B: Docker Image Distribution

### Build Standalone Image

```bash
cd rental-scanner
docker build -f deployment/Dockerfile -t rental-scanner:latest .
```

### Save and Transfer Image

```bash
# Save to file
docker save rental-scanner:latest | gzip > rental-scanner-docker.tar.gz

# Transfer to target machine (use scp, USB, etc.)

# Load on target machine
docker load < rental-scanner-docker.tar.gz
```

### Run with Docker Run

```bash
# Create network
docker network create rental-network

# Run PostgreSQL
docker run -d \
  --name rental-db \
  --network rental-network \
  -e POSTGRES_DB=rental_scanner \
  -e POSTGRES_USER=rental_user \
  -e POSTGRES_PASSWORD=secure-password \
  -v rental-db-data:/var/lib/postgresql/data \
  postgres:15-alpine

# Run Redis
docker run -d \
  --name rental-redis \
  --network rental-network \
  -v rental-redis-data:/data \
  redis:7-alpine

# Run Application
docker run -d \
  --name rental-scanner \
  --network rental-network \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgresql://rental_user:secure-password@rental-db:5432/rental_scanner \
  -e REDIS_URL=redis://rental-redis:6379/0 \
  -v rental-app-data:/app/data \
  rental-scanner:latest
```

### Backup and Restore

**Backup database:**
```bash
docker compose exec db pg_dump -U rental_user rental_scanner > backup_$(date +%Y%m%d).sql
```

**Restore database:**
```bash
cat backup_20240101.sql | docker compose exec -T db psql -U rental_user rental_scanner
```

**Backup volumes:**
```bash
docker run --rm -v rental-scanner_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres_backup.tar.gz /data
```

### Pros and Cons

✅ **Pros:**
- Consistent environment
- Easy to deploy and update
- Isolated from host system
- Includes all dependencies
- Scalable architecture
- Easy backup/restore

❌ **Cons:**
- Requires Docker knowledge
- Higher resource usage
- More complex troubleshooting
- Larger disk space needed

---

## Post-Deployment Configuration

### Configure Email Notifications

Update `.env` file:
```ini
MAIL_ENABLED=true
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@rentalscanner.com
```

**For Gmail:** Generate app password at https://myaccount.google.com/apppasswords

### Setup Scheduled Searches

1. Log into the application
2. Navigate to "Saved Searches"
3. Create a new search with your criteria
4. Enable "Schedule" option
5. Choose frequency (hourly, daily, weekly)
6. Save the search

### Configure Scrapers

Enable/disable specific scrapers in `.env`:
```ini
ENABLED_SCRAPERS=kijiji,realtor,rentals,viewit,apartments
```

### Performance Tuning

**For high traffic (10+ concurrent users):**
```ini
WORKERS=4
THREADS=8
CACHE_TYPE=redis
REDIS_URL=redis://localhost:6379/0
```

**For resource-constrained systems:**
```ini
WORKERS=1
THREADS=2
CACHE_TYPE=simple
SCRAPER_DELAY=2
```

### Security Best Practices

1. **Change default passwords immediately**
2. **Use strong SECRET_KEY** (64+ characters)
3. **Enable HTTPS** (use Let's Encrypt)
4. **Keep software updated** (security patches)
5. **Use firewall** (UFW, iptables, or cloud firewall)
6. **Regular backups** (daily database backups)
7. **Monitor logs** for suspicious activity

---

## Troubleshooting

### Common Issues

#### 1. "Address already in use" Error

**Problem:** Port 5000 is already in use

**Solution:**
```bash
# Find process using port
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill the process or change port
# In .env: WEB_PORT=8000
```

#### 2. Database Connection Errors

**Problem:** Cannot connect to database

**Solutions:**
```bash
# Check PostgreSQL is running
systemctl status postgresql  # Linux
docker compose ps  # Docker

# Verify connection string
echo $DATABASE_URL

# Test connection
psql postgresql://rental_user:password@localhost:5432/rental_scanner
```

#### 3. Scrapers Return No Results

**Problem:** No listings found

**Debugging:**
```ini
# Enable debug mode in .env
SAVE_DEBUG_HTML=true
LOG_LEVEL=DEBUG
```

Check `debug_output/` folder for saved HTML responses.

#### 4. "ModuleNotFoundError"

**Problem:** Missing Python package

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

#### 5. Docker Container Won't Start

**Check logs:**
```bash
docker compose logs web
docker compose logs db
```

**Common fixes:**
```bash
# Remove old containers
docker compose down
docker compose up -d --force-recreate

# Check disk space
df -h

# Check permissions
ls -la
```

#### 6. Slow Performance

**Optimizations:**
1. Enable Redis caching
2. Increase worker count
3. Add database indexes
4. Reduce scraper frequency
5. Clean old listings from database

```sql
-- Remove listings older than 30 days
DELETE FROM listings WHERE last_seen < NOW() - INTERVAL '30 days';
```

### Getting Help

1. **Check logs** first (application and system logs)
2. **Search GitHub Issues** for similar problems
3. **Enable debug mode** to get detailed error messages
4. **Create GitHub Issue** with:
   - Deployment method used
   - Error messages (full stack trace)
   - Configuration (remove sensitive data)
   - Steps to reproduce

### Maintenance Tasks

**Weekly:**
- Review application logs
- Check disk space usage
- Verify scheduled tasks are running

**Monthly:**
- Update dependencies (`pip install -r requirements.txt --upgrade`)
- Review and clean old listings
- Backup database
- Check for security updates

**Quarterly:**
- Review scraper functionality (sites may change)
- Update Python/system packages
- Review user accounts and permissions
- Test backup restoration

---

## Comparison Table

| Feature | Local Python | Standalone Exe | Hosted VPS | Docker |
|---------|-------------|----------------|------------|--------|
| **Setup Complexity** | Easy | Medium | Hard | Medium |
| **Multi-User** | No | No | Yes | Yes |
| **Remote Access** | No | No | Yes | Yes |
| **Resource Usage** | Low | Low | Medium | High |
| **Maintenance** | Easy | Easy | Hard | Medium |
| **Scalability** | None | None | Limited | High |
| **Cost** | Free | Free | $10-15/mo | $0-20/mo |
| **Updates** | Easy | Manual | Medium | Easy |
| **Best For** | Development | Personal | Small Team | Production |

---

## Recommended Deployment by Use Case

### Personal Use, Learning, Testing
→ **Option 1: Local Python Development**

### Single User, No Internet Access Required
→ **Option 2: Standalone Executable**

### Small Team (4-5 users), Remote Access
→ **Option 3: Hosted VPS** or **Option 4: Docker on VPS**

### Production, Multiple Teams, High Availability
→ **Option 4: Docker with orchestration** (Kubernetes, Docker Swarm)

---

## Next Steps

1. Choose your deployment method
2. Follow the step-by-step instructions
3. Configure environment variables
4. Test with a sample search
5. Setup scheduled scans (optional)
6. Configure email notifications (optional)
7. Create user accounts (multi-user mode)
8. Setup backups
9. Monitor and maintain

For additional support or questions, please open an issue on GitHub or consult the project documentation.