# Newmarket Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 0: Prerequisites

**Required Software:**
- Python 3.8+ installed
- **Google Chrome browser** (required for Rentals.ca scraper)
- Internet connection

**First-Time Setup:**
The first search may take 30-60 seconds as ChromeDriver is automatically downloaded for Selenium.

### Step 1: Run the Application

```bash
cd rental-scanner
python app.py
```

The app will start at: **http://localhost:5000**

### Step 2: Open Your Browser

Navigate to: `http://localhost:5000`

### Step 3: Search!

The form is already pre-filled for Newmarket searches. Just click **"Search Rentals"** to see available listings.

---

## 🏘️ Searching the Newmarket Area

### Default Search
- **Location**: Already set to "Newmarket"
- **Price Range**: Leave blank to see all prices, or enter your budget
- **Results**: Combines listings from Kijiji, Realtor.ca, and Rentals.ca
- **Search Time**: 10-20 seconds (Rentals.ca uses browser automation)

⚠️ **Note**: First search may take longer while ChromeDriver downloads automatically.

### Example Searches

#### 1. Affordable 1-Bedroom in Newmarket
```
Location: Newmarket
Min Price: 1400
Max Price: 1800
```

#### 2. Family Home in Aurora
```
Location: Aurora
Min Price: 2000
Max Price: 2800
```

#### 3. Budget-Friendly in Bradford
```
Location: Bradford
Min Price: 1200
Max Price: 1600
```

#### 4. Luxury Rental in Richmond Hill
```
Location: Richmond Hill
Min Price: 2500
Max Price: 3500
```

---

## 📍 Supported Cities (Within 25 km)

Search any of these locations:

- **Newmarket** (default)
- **Aurora** (8 km south)
- **Richmond Hill** (12 km south)
- **East Gwillimbury** (15 km north)
- **Bradford** (20 km northwest)
- **Markham** (18 km southeast)
- **Vaughan** (20 km southwest)
- **King City** (10 km west)

💡 **Pro Tip**: Try searching multiple cities to maximize your options!

---

## 💰 Typical Rental Prices (Newmarket Area)

Based on market averages:

| Property Type | Price Range |
|---------------|-------------|
| 1 Bedroom Apartment | $1,400 - $1,900 |
| 2 Bedroom Apartment | $1,800 - $2,400 |
| 3 Bedroom House | $2,200 - $3,200 |
| 4+ Bedroom House | $2,800 - $4,000+ |

*Prices vary by city, amenities, and condition*

---

## 🔍 Understanding Your Results

### What You'll See

Each listing shows:
- **Title**: Property description
- **Price**: Monthly rent
- **Location**: Address or area
- **Bedrooms/Bathrooms**: Unit size
- **Source Badge**: Where it was found (Kijiji, Realtor.ca, or Rentals.ca)
- **Link**: Click "View Listing" to see full details

### Result Statistics

After each search, you'll see:
- **Total Listings**: How many properties were found
- **Unique Listings**: After removing duplicates
- **Sources**: Which sites returned results (Kijiji, Realtor.ca, Rentals.ca)
- **Search Time**: How long it took (typically 10-20 seconds)

**Why Searches Take Time:**
- **Kijiji & Realtor.ca**: Fast (2-5 seconds each)
- **Rentals.ca**: Slower (10-15 seconds) - uses headless Chrome browser to render JavaScript
</text>

<old_text line=223>
### Number of Results

Typical search results:
- **Newmarket**: 15-40 listings
- **Aurora**: 10-25 listings
- **Richmond Hill**: 20-50 listings
- **Bradford**: 5-15 listings
- **Smaller cities**: 5-20 listings

*Note: Numbers vary by season and market conditions*

### Search Speed

- **First search**: 10-15 seconds (cold start)
- **Subsequent searches**: 5-10 seconds
- **All three scrapers**: Run simultaneously

### Source Badges

- 🟦 **Kijiji**: Blue badge - Largest selection, includes private landlords
- 🟥 **Realtor.ca**: Red badge - Professional listings, often new developments
- 🟩 **Rentals.ca**: Green badge - Dedicated rental platform

---

## ⚡ Quick Tips

### Finding the Best Deals

1. **Search early in the month** - More listings available
2. **Check all three sources** - Some listings appear on only one site
3. **Search nearby cities** - Aurora and Bradford often have lower prices
4. **Set realistic price ranges** - Don't filter too aggressively
5. **Refresh daily** - New listings appear constantly

### Avoiding Scams

✅ **Good Signs**:
- Professional photos
- Detailed descriptions
- Reasonable prices
- Verifiable address
- Property management companies

⚠️ **Red Flags**:
- Prices way below market
- No photos or stock photos
- Requests for money before viewing
- Landlord "out of country"
- Too good to be true

### Making Your Search Efficient

**Narrow Search** (when you know what you want):
```
Location: Newmarket
Min Price: 1800
Max Price: 2000
```

**Broad Search** (exploring options):
```
Location: Newmarket
Min Price: [leave blank]
Max Price: [leave blank]
```

**Multi-City Search** (run multiple searches):
1. Search Newmarket
2. Search Aurora
3. Search Richmond Hill
4. Compare results

---

## 🎯 Common Newmarket Search Scenarios

### Scenario 1: Young Professional
**Need**: 1-bedroom, close to GO Train, under $2000

```
Search 1: Newmarket, $1400-$2000
Search 2: Aurora, $1400-$2000
```

Best areas: Downtown Newmarket, Aurora GO area

### Scenario 2: Small Family
**Need**: 2-3 bedroom house, family-friendly, under $2500

```
Search 1: East Gwillimbury, $2000-$2500
Search 2: Bradford, $2000-$2500
Search 3: Newmarket, $2000-$2500
```

Best areas: Bradford, East Gwillimbury

### Scenario 3: Commuter to Toronto
**Need**: Any size, near Highway 404, affordable

```
Search 1: Newmarket, $1500-$2200
Search 2: Richmond Hill, $1800-$2500
Search 3: Aurora, $1500-$2200
```

Best areas: Richmond Hill, Aurora (close to 404)

### Scenario 4: Student/Shared Housing
**Need**: Affordable, any location

```
Search 1: Bradford, $1200-$1600
Search 2: Newmarket, $1200-$1600
```

Best areas: Bradford, smaller units in Newmarket

---

## 📊 What to Expect

### Number of Results

Typical search results:
- **Newmarket**: 15-40 listings
- **Aurora**: 10-25 listings
- **Richmond Hill**: 20-50 listings
- **Bradford**: 5-15 listings
- **Smaller cities**: 5-20 listings

*Note: Numbers vary by season and market conditions*

### Search Speed

- **First search**: 10-15 seconds (cold start)
- **Subsequent searches**: 5-10 seconds
- **All three scrapers**: Run simultaneously

### Duplicate Removal

The system automatically removes duplicates when the same property appears on multiple sites. You'll see:
- Original count: Total found
- After deduplication: Unique properties

---

## 🛠️ Troubleshooting

### "No results found"

Try:
1. Remove price filters (search all prices)
2. Check spelling: "Newmarket" not "New Market"
3. Try a nearby city
4. Wait a few minutes and search again

### "Search taking too long"

- First search is always slower (loading scrapers + ChromeDriver download)
- Maximum wait is 60 seconds
- Check your internet connection
- Try again if it times out
- Rentals.ca takes 10-15 seconds normally (uses browser automation)

### "Some sources failed"

- This is normal - not all sites have every city
- You'll still get results from working scrapers
- Check the error messages for details

### Chrome/Selenium Errors

If you see Selenium or ChromeDriver errors:

1. **Install Chrome**: Make sure Google Chrome browser is installed
2. **First run**: Wait 30-60 seconds for automatic ChromeDriver download
3. **ChromeDriver cache**: Located in `~/.wdm/` folder (auto-managed)
4. **Clear cache**: Delete `.wdm` folder if persistent issues
5. **Check logs**: Look for detailed error messages in console

**Common Selenium Issues:**
- `"ChromeDriver not found"`: Wait for auto-download, or check Chrome installation
- `"Chrome binary not found"`: Install Google Chrome browser
- `"Timeout"`: Normal on first run, try again
- `"Session not created"`: Chrome version mismatch, update Chrome

### Rentals.ca Not Working

If Rentals.ca scraper fails:

1. **Chrome required**: Ensure Google Chrome is installed
2. **First search**: May take 30-60 seconds for ChromeDriver download
3. **Still works without it**: Kijiji and Realtor.ca will still return results
4. **Check browser**: Try opening Chrome manually to verify it works
5. **Fallback**: App continues even if one scraper fails
</text>

<old_text line=292>
## 📞 Need Help?

Common solutions:
- **App won't start**: Check if Python and dependencies are installed
- **No results**: Try different cities or remove filters
- **Slow searches**: Normal for first search, should improve
- **Missing packages**: Run `pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium python-dotenv APScheduler`

---

## 📱 Mobile Access

The app works on mobile devices:
1. Make sure your computer is running the app
2. Find your computer's local IP address
3. On mobile browser: `http://[YOUR-IP]:5000`
4. Example: `http://192.168.1.100:5000`

---

## 🎓 Learning More

For detailed information:
- **NEWMARKET_CONFIG.md** - Technical configuration details
- **README.md** - Full application documentation
- **SCRAPER_GUIDE.md** - How the scrapers work
- **WEB_INTERFACE_GUIDE.md** - Interface features

---

## 📞 Need Help?

Common solutions:
- **App won't start**: Check if Python and dependencies are installed
- **No results**: Try different cities or remove filters
- **Slow searches**: Normal for first search, should improve
- **Missing packages**: Run `pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium python-dotenv APScheduler`

---

## 🎉 You're Ready!

That's it! You're now ready to find your perfect rental in the Newmarket area.

**Happy House Hunting! 🏠**

---

*Last Updated: January 2025*
*Version: 2.1 - Newmarket Edition*