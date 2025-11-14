# Rental Scanner - Implementation Roadmap (Approach #2)

## Overview

This roadmap outlines the step-by-step implementation of the **Hybrid API + Scraping with Database Layer** approach for expanding the Rental Scanner application to support multiple listing sources with tracking and reporting capabilities.

**Current State:** Single-source scraper (Kijiji) with basic Flask web interface

**Target State:** Multi-source aggregator with database persistence, scheduled scans, listing tracking, and automated reporting

**Estimated Total Time:** 4-6 weeks (part-time development)

---

## Implementation Phases

### Phase 0: Project Setup & Refactoring (Week 1)
**Priority:** Critical | **Estimated Time:** 1 week

#### Tasks

1. **Setup Enhanced Project Structure**
   - Create directories: `models/`, `tasks/`, `reports/`, `deployment/`
   - Add `config.py` for centralized configuration
   - Create `.env.example` template
   - Update `.gitignore` (add `.env`, `*.db`, `debug_output/`)

2. **Refactor Existing Kijiji Scraper**
   - Create `scrapers/base_scraper.py` with abstract base class
   - Refactor `kijiji_scraper.py` to inherit from `BaseScraper`
   - Standardize data output format
   - Add comprehensive logging
   - Test that existing functionality still works

3. **Setup Database Layer**
   - Install SQLAlchemy and Flask-SQLAlchemy
   - Create database models (`models/database.py`):
     - `User` model (for multi-user support)
     - `Listing` model (rental listings)
     - `SavedSearch` model (user search criteria)
     - `ListingHistory` model (track changes)
     - `SearchHistory` model (execution logs)
   - Create database initialization script
   - Add Alembic for migrations

4. **Update Requirements**
   - Add all new dependencies to `requirements.txt`
   - Document minimum Python version (3.11+)
   - Test installation in clean virtual environment

**Success Criteria:**
- ✅ Existing Kijiji scraper works with new structure
- ✅ Database models create successfully
- ✅ All tests pass
- ✅ No regression in existing functionality

---

### Phase 1: Add New Scrapers (Weeks 2-3)
**Priority:** High | **Estimated Time:** 2 weeks

Implement scrapers one at a time, testing each before moving to the next.

#### 1.1 Realtor.ca Scraper (3-4 days)

**Implementation Steps:**
```python
# scrapers/realtor_ca_scraper.py
class RealtorCAScraper(BaseScraper):
    def get_source_name(self) -> str:
        return "realtor_ca"
    
    def build_search_url(self, location, min_price, max_price) -> str:
        # Build Realtor.ca search URL
        # URL format: https://www.realtor.ca/map#...
        pass
    
    def parse_listings(self, html: str) -> List[Dict]:
        # Parse Realtor.ca listing data
        # Look for JSON data in <script> tags or API responses
        pass
```

**Challenges:**
- May use client-side rendering (JavaScript)
- Possible CAPTCHA protection
- API endpoints may be undocumented

**Fallback:** Use Selenium/Playwright if needed

#### 1.2 Rentals.ca Scraper (2-3 days)

**Implementation Steps:**
- Similar structure to Realtor.ca
- URL format: `https://rentals.ca/{city}/search?...`
- Parse HTML or JSON-LD structured data

#### 1.3 Viewit.ca Scraper (2-3 days)

**Implementation Steps:**
- URL format: `https://www.viewit.ca/...`
- May have simpler HTML structure
- Look for listing cards or JSON data

#### 1.4 Apartments.ca Scraper (2-3 days)

**Implementation Steps:**
- URL format: `https://www.apartments.ca/...`
- Parse listing data from HTML
- Handle pagination if needed

#### 1.5 Facebook Marketplace (Optional - 5-7 days)

**⚠️ Warning:** Most complex implementation

**Requirements:**
- Selenium or Playwright (browser automation)
- May require Facebook login
- Rate limiting is strict
- Frequent changes to DOM structure

**Recommendation:** Skip for initial release, add later if needed

#### 1.6 Zillow (Optional - 3-5 days)

**⚠️ Warning:** Geographic restrictions for Canadian users

**Considerations:**
- May not have Canadian rental listings
- Strong anti-scraping measures
- Consider using RapidAPI unofficial APIs instead
- May require API key

**Recommendation:** Low priority, add only if user demand exists

#### Testing Checklist for Each Scraper:
- [ ] Successfully fetches search results
- [ ] Correctly parses all required fields
- [ ] Handles price filtering
- [ ] Handles errors gracefully (network, parsing)
- [ ] Returns standardized data format
- [ ] Respects rate limiting
- [ ] Logs appropriately

**Success Criteria:**
- ✅ At least 3 scrapers fully functional (Kijiji + 2 new)
- ✅ All scrapers return consistent data format
- ✅ Error handling works correctly
- ✅ Manual testing shows relevant results

---

### Phase 2: Scraper Coordinator & Database Integration (Week 3)
**Priority:** High | **Estimated Time:** 3-4 days

#### 2.1 Create Scraper Manager

```python
# scrapers/scraper_manager.py
class ScraperManager:
    def __init__(self, enabled_scrapers: List[str]):
        # Initialize all enabled scrapers
        pass
    
    def search_all(self, location, min_price, max_price) -> Dict:
        # Run all scrapers in parallel
        # Aggregate results
        # Handle failures gracefully
        pass
    
    def save_to_database(self, listings: List[Dict]):
        # Save new listings
        # Update existing listings
        # Track changes
        pass
```

**Features:**
- Parallel execution using `ThreadPoolExecutor`
- Aggregate results from all sources
- Remove duplicates (same listing on multiple sites)
- Save results to database

#### 2.2 Implement Listing Persistence

**Logic:**
1. For each scraped listing:
   - Check if URL exists in database
   - If new: Create `Listing` record with `status='active'`
   - If exists: Update `last_seen` timestamp
   - If price changed: Update price and create `ListingHistory` entry

2. Mark expired listings:
   - Find listings not seen in X days
   - Update `status='expired'`

**SQL Optimization:**
- Add indexes on frequently queried fields
- Use bulk inserts where possible
- Implement database connection pooling

#### 2.3 Update Flask Application

**Modify `app.py`:**
- Replace single scraper with `ScraperManager`
- Save results to database after each search
- Display results from database (with source badges)
- Add loading indicators for long searches

**Success Criteria:**
- ✅ All scrapers run in parallel
- ✅ Results saved to database correctly
- ✅ Duplicate detection works
- ✅ Price changes tracked
- ✅ Web interface shows aggregated results

---

### Phase 3: Scheduled Scanning (Week 4)
**Priority:** Medium | **Estimated Time:** 4-5 days

#### 3.1 Implement Saved Searches

**User Interface:**
- Form to create saved search (name, location, price range, sources)
- List of saved searches
- Edit/delete functionality
- Toggle schedule on/off

**Backend:**
- CRUD operations for `SavedSearch` model
- Store search parameters in database
- Link to user account (if multi-user enabled)

#### 3.2 Setup APScheduler

```python
# tasks/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def run_saved_search(search_id):
    # Load search from database
    # Execute scraping
    # Save results
    # Compare with previous results
    # Send notifications if enabled
    pass

def schedule_search(search):
    # Add job to scheduler based on frequency
    if search.schedule_frequency == 'hourly':
        scheduler.add_job(run_saved_search, 'interval', hours=1, args=[search.id])
    elif search.schedule_frequency == 'daily':
        scheduler.add_job(run_saved_search, 'cron', hour=9, args=[search.id])
    # etc.

scheduler.start()
```

#### 3.3 Background Task Execution

**Options:**
1. **APScheduler** (simpler, good for 1-5 users)
2. **Celery + Redis** (better for production, more complex)

**Recommendation:** Start with APScheduler, migrate to Celery if needed

#### 3.4 Search History & Logging

- Log each search execution to `SearchHistory`
- Track execution time, success/failure, result counts
- Display search history in UI
- Show when next search will run

**Success Criteria:**
- ✅ Users can save searches
- ✅ Scheduled scans run automatically
- ✅ Results saved to database
- ✅ Execution logs captured
- ✅ No memory leaks from long-running scheduler

---

### Phase 4: Change Tracking & Notifications (Week 4-5)
**Priority:** Medium | **Estimated Time:** 3-4 days

#### 4.1 Implement Change Detection

**Track these events:**
- New listing appears
- Listing removed/expired
- Price change (up or down)
- Description update

**Logic:**
```python
def track_changes(old_listing, new_data):
    changes = []
    
    if old_listing.price != new_data['price']:
        changes.append({
            'type': 'price_change',
            'old': old_listing.price,
            'new': new_data['price']
        })
    
    # Save to ListingHistory
    for change in changes:
        history = ListingHistory(
            listing_id=old_listing.id,
            change_type=change['type'],
            old_value=str(change['old']),
            new_value=str(change['new'])
        )
        db.session.add(history)
    
    return changes
```

#### 4.2 Email Notifications

**Setup Flask-Mail:**
```python
# config.py
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
```

**Notification Types:**
1. **Instant:** Send email immediately when new listings found
2. **Daily Digest:** Summary of all new listings once per day
3. **Weekly Report:** Comprehensive report with charts

**Email Template:**
```html
<!-- templates/email/new_listings.html -->
<h2>New Rental Listings</h2>
<p>Found {{ listings|length }} new listings for "{{ search_name }}"</p>

{% for listing in listings %}
<div class="listing">
    <h3>{{ listing.title }}</h3>
    <p><strong>${{ listing.price }}/month</strong> - {{ listing.location }}</p>
    <p>{{ listing.description[:200] }}...</p>
    <a href="{{ listing.url }}">View Listing</a>
    <span class="source">Source: {{ listing.source }}</span>
</div>
{% endfor %}
```

#### 4.3 User Preferences

- Email notification on/off toggle
- Notification frequency preference
- Email address for notifications
- Filter criteria for notifications (e.g., only listings under $X)

**Success Criteria:**
- ✅ Changes detected accurately
- ✅ Emails send successfully
- ✅ Email templates look good
- ✅ Users can control notification preferences
- ✅ No spam (rate limiting on emails)

---

### Phase 5: Reports & Analytics (Week 5)
**Priority:** Low | **Estimated Time:** 3-5 days

#### 5.1 Data Analytics

**Implement these analyses:**
```python
# reports/analytics.py

def get_price_statistics(location, days=30):
    """Average, median, min, max prices by location"""
    listings = Listing.query.filter(
        Listing.location.ilike(f'%{location}%'),
        Listing.scraped_at >= datetime.now() - timedelta(days=days)
    ).all()
    
    prices = [l.price for l in listings]
    return {
        'average': statistics.mean(prices),
        'median': statistics.median(prices),
        'min': min(prices),
        'max': max(prices)
    }

def get_price_trends(location, days=90):
    """Price trends over time"""
    # Query listings grouped by week
    # Return time series data
    pass

def get_listing_velocity(location):
    """How fast do listings appear/disappear"""
    # Calculate average time listings stay active
    pass
```

#### 5.2 Visualization (Optional)

**Using Chart.js or Matplotlib:**
- Price distribution histogram
- Price trends line chart
- Listings by source pie chart
- Average price by bedroom count bar chart

#### 5.3 Report Generation

**Weekly Report Email:**
- Market summary (average prices, total listings)
- New listings count
- Price trends
- Most active areas
- Expired listings

**CSV Export:**
- Allow users to download search results as CSV
- Include all fields and metadata
- Useful for further analysis

**Success Criteria:**
- ✅ Statistics calculated correctly
- ✅ Reports generated automatically
- ✅ Charts display properly (if implemented)
- ✅ Export functionality works

---

### Phase 6: User Interface Improvements (Week 5-6)
**Priority:** Medium | **Estimated Time:** 4-5 days

#### 6.1 Enhanced Search Interface

**Features:**
- Multi-source selector (checkboxes for each site)
- Advanced filters:
  - Bedrooms (min/max)
  - Bathrooms (min/max)
  - Property type (apartment, house, condo)
  - Keywords in description
- Save search button
- Recent searches dropdown

#### 6.2 Results Display

**Improvements:**
- Source badge for each listing
- Thumbnail images
- Price history indicator (🔽 Price dropped)
- Days since posted
- "New" badge for recent listings
- Mark as favorite/hide functionality
- Sorting options (price, date, location)
- Filtering options (bedrooms, source, date range)

#### 6.3 Dashboard Page

**Widgets:**
- Saved searches panel
- Recent activity feed
- Quick statistics (total listings, new today)
- Price trends chart
- Upcoming scheduled scans

#### 6.4 Responsive Design

**Mobile optimization:**
- Responsive grid layout
- Touch-friendly buttons
- Simplified mobile navigation
- Mobile-optimized listing cards

**Success Criteria:**
- ✅ UI is intuitive and easy to use
- ✅ Search works on mobile devices
- ✅ All features accessible
- ✅ Fast page load times

---

### Phase 7: Multi-User Support (Week 6 - Optional)
**Priority:** Low | **Estimated Time:** 3-4 days

Only implement if deploying for multiple users.

#### 7.1 Authentication System

**Install Flask-Login:**
```python
from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

**Pages needed:**
- Registration page
- Login page
- Logout endpoint
- Password reset (optional)

#### 7.2 User Isolation

**Ensure:**
- Users only see their own saved searches
- Search history is per-user
- Email notifications go to correct user
- Prevent access to other users' data

#### 7.3 Admin Interface (Optional)

**Admin features:**
- View all users
- Disable/enable scrapers globally
- View system statistics
- Manage scheduled tasks

**Success Criteria:**
- ✅ Users can register and login
- ✅ Data is isolated per user
- ✅ Sessions work correctly
- ✅ Secure password storage (bcrypt)

---

### Phase 8: Testing & Quality Assurance (Ongoing)
**Priority:** Critical | **Duration:** Throughout development

#### 8.1 Unit Tests

**Test coverage for:**
- Each scraper (mock HTTP responses)
- Database models (CRUD operations)
- Scraper manager (aggregation, deduplication)
- Analytics functions (correct calculations)

```python
# tests/test_scrapers.py
import pytest
from scrapers.kijiji_scraper import KijijiScraper

def test_kijiji_scraper():
    with open('tests/fixtures/kijiji_sample.html') as f:
        html = f.read()
    
    scraper = KijijiScraper()
    listings = scraper.parse_listings(html)
    
    assert len(listings) > 0
    assert listings[0]['price'] is not None
    assert listings[0]['url'].startswith('http')
```

#### 8.2 Integration Tests

**Test workflows:**
- Complete search flow (frontend → scraper → database)
- Saved search creation and execution
- Email notification sending
- Scheduled task execution

#### 8.3 Performance Testing

**Metrics to measure:**
- Search response time (target: < 30 seconds)
- Database query performance
- Memory usage over time (check for leaks)
- Concurrent user handling

#### 8.4 Manual Testing

**Test scenarios:**
- Search with various parameters
- Schedule multiple searches
- Verify emails arrive
- Check mobile responsiveness
- Test error conditions (site down, invalid input)

**Success Criteria:**
- ✅ 80%+ test coverage on core functionality
- ✅ All critical paths tested
- ✅ No memory leaks
- ✅ Performance meets targets

---

### Phase 9: Documentation (Week 6)
**Priority:** Medium | **Estimated Time:** 2-3 days

#### 9.1 User Documentation

**Create:**
- User guide (how to search, save searches, setup notifications)
- FAQ page
- Troubleshooting guide
- Video tutorials (optional)

#### 9.2 Technical Documentation

**Create:**
- Architecture diagram
- API documentation (if exposing APIs)
- Database schema documentation
- Deployment guide (already created)
- Contributing guidelines (for open source)

#### 9.3 Code Documentation

**Ensure:**
- All classes have docstrings
- Complex functions explained
- README is up to date
- Inline comments for tricky logic

**Success Criteria:**
- ✅ All documentation complete
- ✅ README has quick start guide
- ✅ Deployment guide tested on clean system
- ✅ Code is well-commented

---

### Phase 10: Deployment & Monitoring (Week 6)
**Priority:** High | **Estimated Time:** 2-3 days

#### 10.1 Production Deployment

**Choose deployment method:**
- Local Python (development only)
- Standalone executable (single user)
- Hosted VPS (small team)
- Docker containers (production)

**Follow deployment guide** for chosen method.

#### 10.2 Monitoring Setup

**Implement:**
- Error logging to file
- Email alerts for critical errors
- Health check endpoint (`/health`)
- Uptime monitoring (e.g., UptimeRobot)
- Database backup automation

```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        # Check Redis connection (if used)
        # etc.
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

#### 10.3 Performance Monitoring

**Track:**
- Average search response time
- Database query performance
- Memory usage trends
- Failed scraper attempts
- Email delivery rates

#### 10.4 Security Hardening

**Checklist:**
- [ ] Environment variables for secrets (no hardcoded passwords)
- [ ] HTTPS enabled (SSL certificate)
- [ ] CSRF protection enabled
- [ ] SQL injection prevention (use parameterized queries)
- [ ] XSS prevention (escape user input)
- [ ] Rate limiting on endpoints
- [ ] Regular security updates

**Success Criteria:**
- ✅ Application deployed successfully
- ✅ Monitoring in place
- ✅ No security vulnerabilities
- ✅ Backups working

---

## Priority Matrix

### Must Have (MVP)
1. ✅ Refactored base scraper architecture
2. ✅ Database persistence
3. ✅ At least 3 working scrapers (Kijiji + 2 new)
4. ✅ Web interface for search
5. ✅ Basic listing tracking

### Should Have (v1.0)
6. ✅ Saved searches
7. ✅ Scheduled scanning
8. ✅ Email notifications
9. ✅ Price change tracking
10. ✅ Responsive UI

### Could Have (v1.1)
11. ✅ Reports and analytics
12. ✅ Multi-user support
13. ✅ Advanced filters
14. ✅ Visualization charts

### Won't Have (Future)
15. ❌ Facebook Marketplace (too complex)
16. ❌ Zillow (limited Canadian data)
17. ❌ Mobile app
18. ❌ Browser extension

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Sites change HTML structure | High | High | Regular monitoring, modular scraper design |
| Anti-scraping measures (CAPTCHA) | Medium | High | Rate limiting, user-agent rotation, fallback options |
| Database performance issues | Low | Medium | Proper indexing, query optimization |
| Email delivery fails | Medium | Low | Use reputable SMTP provider, test thoroughly |
| Scheduling not reliable | Low | Medium | Use robust library (APScheduler), add monitoring |
| Security vulnerabilities | Medium | High | Follow best practices, regular updates, security audit |

---

## Success Metrics

### Technical Metrics
- ✅ All scrapers return results > 90% of the time
- ✅ Average search time < 30 seconds
- ✅ Database query time < 100ms for most queries
- ✅ Zero data loss incidents
- ✅ 99% uptime (for hosted deployments)

### User Metrics
- ✅ Users find relevant listings
- ✅ Email notifications are helpful (not spam)
- ✅ Interface is intuitive (minimal support requests)
- ✅ Scheduled scans work reliably

---

## Development Best Practices

### Version Control
- Commit frequently with descriptive messages
- Use feature branches for new scrapers
- Tag releases (v1.0, v1.1, etc.)
- Keep `main` branch stable

### Code Quality
- Follow PEP 8 style guide
- Use type hints where helpful
- Write docstrings for all public functions
- Run linter (flake8) regularly
- Use formatter (black) for consistency

### Testing Strategy
- Write tests before implementing (TDD when appropriate)
- Test with real HTML fixtures (save samples)
- Mock external API calls
- Test error conditions
- Automate test runs (GitHub Actions, etc.)

### Deployment Strategy
- Test in staging environment first
- Use database migrations (never manual schema changes)
- Keep deployment scripts in version control
- Document rollback procedures
- Have backup/restore plan

---

## Post-Launch Roadmap

### Month 1-2
- Monitor scraper reliability
- Fix bugs reported by users
- Optimize slow queries
- Add missing features based on feedback

### Month 3-6
- Add more scrapers if needed
- Improve UI based on usage patterns
- Add advanced analytics
- Consider mobile app (if demand exists)

### Month 6+
- Machine learning for price predictions
- Recommendation engine
- Integration with calendar/mapping tools
- API for third-party integrations

---

## Quick Reference Commands

### Development
```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
python app.py

# Test
pytest tests/

# Database
flask db migrate -m "Description"
flask db upgrade
```

### Docker
```bash
# Build and run
cd deployment
docker compose up -d

# View logs
docker compose logs -f

# Restart
docker compose restart web
```

### Maintenance
```bash
# Backup database
pg_dump rental_scanner > backup.sql

# Update code
git pull
pip install -r requirements.txt --upgrade
flask db upgrade
systemctl restart rental-scanner
```

---

## Resources

### Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
- APScheduler: https://apscheduler.readthedocs.io/

### Tools
- Postman (API testing)
- DB Browser for SQLite (database inspection)
- Chrome DevTools (scraper development)
- Sentry (error monitoring)

---

## Conclusion

This roadmap provides a comprehensive guide to implementing the enhanced Rental Scanner application. Follow the phases in order, testing thoroughly at each stage. Remember that the goal is to create a reliable, maintainable application that helps users find rental properties efficiently.

**Key Principles:**
1. **Incremental development** - Build and test one feature at a time
2. **User focus** - Ensure features solve real problems
3. **Maintainability** - Write clean, documented code
4. **Reliability** - Handle errors gracefully, monitor actively
5. **Security** - Protect user data, follow best practices

Good luck with your implementation! 🚀