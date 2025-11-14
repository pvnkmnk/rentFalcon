# 🏠 Rental Scanner - Simple User Guide

**Find Rentals in Newmarket, Ontario - No Tech Skills Required!**

---

## 🎯 What Is This?

Rental Scanner is a tool that searches **multiple rental websites at once** to find apartments and houses for rent in the Newmarket area.

Instead of checking Kijiji, Rentals.ca, and other sites separately, this tool does it all for you in one click!

---

## 📋 What You Need Before Starting

### Required (Must Have):
1. **A Windows Computer** (Windows 10 or 11)
2. **Internet Connection**
3. **Google Chrome Browser** - [Download Here](https://www.google.com/chrome/)

### That's It! Everything Else Installs Automatically!

---

## 🚀 First Time Setup (5 Minutes)

### Step 1: Download Python (If Not Installed)

1. Go to: https://www.python.org/downloads/
2. Click the big yellow button that says "Download Python"
3. Run the installer
4. **⚠️ IMPORTANT:** Check the box that says **"Add Python to PATH"**
5. Click "Install Now"
6. Wait for it to finish
7. **Restart your computer**

### Step 2: Run Easy Setup

1. Find the folder called `rental-scanner` on your computer
2. Double-click the file called: **`EASY_SETUP.bat`**
3. Follow the on-screen instructions
4. The setup will:
   - ✅ Check if everything is installed
   - ✅ Download needed files (takes 2-3 minutes)
   - ✅ Create a desktop shortcut
   - ✅ Start the app automatically

### Step 3: Done!

After setup completes, you'll have an icon on your desktop called:
**"Rental Scanner - Newmarket"**

---

## 💻 How to Use (Every Day)

### Starting the App

**Option 1: Desktop Shortcut** (Easiest)
- Double-click the "Rental Scanner - Newmarket" icon on your desktop
- That's it!

**Option 2: Folder Method**
- Go to the `rental-scanner` folder
- Double-click: **`START_RENTAL_SCANNER.bat`**

### What Happens Next

1. A black window opens (don't close it!)
2. Your web browser opens automatically
3. You see a search page

### Searching for Rentals

1. **Location** is already set to "Newmarket" (you can change it!)
2. **Min Price** - Enter lowest rent you want (example: 1500)
3. **Max Price** - Enter highest rent you want (example: 2500)
4. Click the blue **"Search Rentals"** button
5. Wait 10-15 seconds
6. See your results!

### Understanding Results

Each listing shows:
- **Title** - What type of place it is
- **Price** - Monthly rent
- **Location** - Address or area
- **Bedrooms/Bathrooms** - How many
- **View Listing** - Click to see full details on the original website

### Sorting Results

- Click **"Lowest Price"** to see cheapest first
- Click **"Highest Price"** to see most expensive first
- Click **"Newest First"** to see latest listings

---

## 🏘️ Supported Cities

You can search any of these cities (all within 25 km of Newmarket):

| City | Distance from Newmarket | Typical Prices |
|------|------------------------|----------------|
| **Newmarket** | 0 km (center) | $1,400 - $2,800 |
| **Aurora** | 8 km south | $1,600 - $2,900 |
| **Richmond Hill** | 12 km south | $1,800 - $3,500 |
| **Bradford** | 20 km northwest | $1,200 - $2,200 |
| **East Gwillimbury** | 15 km north | $1,400 - $2,500 |
| **Markham** | 18 km southeast | $1,800 - $3,200 |
| **Vaughan** | 20 km southwest | $1,900 - $3,500 |
| **King City** | 10 km west | $1,800 - $3,000 |

---

## 📊 Example Searches

### Example 1: Affordable 1-Bedroom in Newmarket

```
Location: Newmarket
Min Price: 1400
Max Price: 1800
```

**Expected Results:** 20-30 listings

---

### Example 2: Family Home in Aurora

```
Location: Aurora
Min Price: 2000
Max Price: 2800
```

**Expected Results:** 25-35 listings

---

### Example 3: Budget Rental in Bradford

```
Location: Bradford
Min Price: 1200
Max Price: 1600
```

**Expected Results:** 15-25 listings

---

### Example 4: Luxury Rental in Richmond Hill

```
Location: Richmond Hill
Min Price: 2500
Max Price: 3500
```

**Expected Results:** 20-40 listings

---

## ⏱️ How Long Does It Take?

| Search Type | Time |
|-------------|------|
| **First search ever** | 30-60 seconds (downloads driver) |
| **Regular searches** | 10-15 seconds |
| **Very narrow search** | 5-10 seconds |

**The first search is always slowest** - this is normal! The app downloads a file it needs (ChromeDriver) and caches it for future use.

---

## 🛑 Stopping the App

When you're done searching:

1. Close the web browser
2. Go to the black window (command prompt)
3. Press **Ctrl + C** on your keyboard
4. Close the window

**Or just close the black window** - that stops everything.

---

## ❓ Common Questions

### Q: Why is my first search taking forever?
**A:** This is normal! The app downloads ChromeDriver (a file it needs). This only happens once. After that, searches are fast (10-15 seconds).

### Q: Can I search multiple cities at once?
**A:** No, but you can do multiple searches quickly! Search Newmarket, then Aurora, then Richmond Hill - each takes only 10 seconds.

### Q: How do I know if a listing is real?
**A:** Click "View Listing" to see the full post on the original website (Kijiji or Rentals.ca). Always verify before contacting landlords!

### Q: Do I need to keep the black window open?
**A:** Yes! That's the app running. Don't close it while searching. Close it when you're done.

### Q: Can I use this on Mac or Linux?
**A:** Currently only Windows is supported. Mac/Linux support could be added in the future.

### Q: Is this free?
**A:** Yes! Completely free and always will be.

### Q: Does this work on my phone?
**A:** No, this runs on your computer. However, you can access it from your phone if both are on the same WiFi network (advanced users only).

### Q: Where does the data come from?
**A:** The app searches:
- ✅ Kijiji (Canada's largest classifieds)
- ✅ Rentals.ca (dedicated rental platform)

### Q: Will I see duplicate listings?
**A:** No! The app automatically removes duplicates when the same property appears on multiple sites.

---

## 🐛 Troubleshooting

### Problem: "Python is not installed"

**Solution:**
1. Install Python from: https://www.python.org/downloads/
2. During installation, CHECK the box: "Add Python to PATH"
3. Restart your computer
4. Run EASY_SETUP.bat again

---

### Problem: "Chrome not found"

**Solution:**
1. Install Chrome: https://www.google.com/chrome/
2. Run EASY_SETUP.bat again
3. Or continue without Chrome (you'll get fewer results)

---

### Problem: No results found

**Try these:**
1. Check spelling of city name
2. Remove price filters (leave Min/Max empty)
3. Try a different city (Aurora, Richmond Hill, etc.)
4. Make sure you have internet connection
5. Try again - sometimes websites are slow

---

### Problem: App won't start

**Try these:**
1. Run EASY_SETUP.bat again
2. Make sure Python is installed
3. Restart your computer
4. Check that you're in the rental-scanner folder
5. Right-click START_RENTAL_SCANNER.bat → "Run as administrator"

---

### Problem: Search is very slow

**This is normal if:**
- ✅ It's your first search (ChromeDriver download)
- ✅ Internet is slow
- ✅ Searching broad area with no price limits

**Not normal if:**
- ❌ Every search takes 30+ seconds
- ❌ Searches never complete

**Solution:**
- Close the app completely
- Restart your computer
- Start the app again

---

## 💡 Tips for Best Results

### Getting More Listings

✅ **DO:**
- Search multiple cities (Newmarket, Aurora, Bradford)
- Use wide price ranges ($1200 - $2500)
- Search during business hours (9 AM - 5 PM)
- Check daily for new listings

❌ **DON'T:**
- Filter too much (very narrow price range)
- Misspell city names
- Search very late at night (fewer new listings)

---

### Avoiding Scams

✅ **Good Signs:**
- Real photos (not stock images)
- Detailed description
- Reasonable price for the area
- Contact information provided
- Property management company name

🚩 **Red Flags:**
- Price way too low ($800 for 3-bedroom house = scam!)
- No photos or stolen photos
- Landlord "out of country"
- Requests money before viewing
- Only accepts wire transfers
- Poor grammar/spelling
- Too good to be true

**Always:**
- View the property in person
- Meet the landlord face-to-face
- Never send money without seeing the place
- Get everything in writing
- Check references

---

## 📞 Need More Help?

### Documentation Files

Look in the rental-scanner folder for these helpful files:

- **QUICK_REFERENCE.md** - Quick tips and commands
- **NEWMARKET_QUICK_START.md** - Detailed usage guide
- **INSTALLATION.md** - Technical installation help
- **SCRAPER_STATUS_FINAL.md** - What's working and what's not

### Still Stuck?

1. Read the error message carefully
2. Try restarting your computer
3. Run EASY_SETUP.bat again
4. Check the troubleshooting section above
5. Make sure Python and Chrome are installed

---

## 🎉 You're Ready!

**To get started:**
1. Double-click the desktop shortcut
2. Wait for browser to open
3. Click "Search Rentals"
4. Start finding your new home!

---

## 📝 Quick Reference Card

**Starting the App:**
- Desktop Icon: "Rental Scanner - Newmarket"
- Or: START_RENTAL_SCANNER.bat

**Stopping the App:**
- Close browser
- Press Ctrl+C in black window
- Close the black window

**Default Settings:**
- Location: Newmarket
- Sources: Kijiji + Rentals.ca
- Results: 30-50 listings per search

**Supported Cities:**
Newmarket, Aurora, Richmond Hill, Bradford, East Gwillimbury, Markham, Vaughan, King City

**Typical Prices:**
- 1-Bedroom: $1,400 - $1,900
- 2-Bedroom: $1,800 - $2,400
- 3-Bedroom: $2,200 - $3,200
- 4+ Bedroom: $2,800 - $4,000+

---

**Last Updated:** November 13, 2025  
**Version:** 2.1 - Newmarket Edition  
**Status:** ✅ Ready to Use

---

**Happy House Hunting! 🏠✨**