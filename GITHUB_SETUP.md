# 🦅 rentFalcon - GitHub Setup Guide

## 📤 How to Push rentFalcon to GitHub

Follow these steps to upload your rentFalcon project to GitHub.

---

## Step 1: Configure Git Identity

First, set up your Git identity (only needed once):

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"
```

**Example:**
```bash
git config --global user.name "John Doe"
git config --global user.email "johndoe@example.com"
```

---

## Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: **rentFalcon**
3. Description: "Fast multi-source rental search for Newmarket, Ontario"
4. Set to: **Public** (or Private if you prefer)
5. **DO NOT** check "Initialize with README" (we already have one!)
6. **DO NOT** add .gitignore or license (we have them!)
7. Click **"Create repository"**

---

## Step 3: Commit Your Code

```bash
# Navigate to the project folder
cd "C:\Users\idols\development files\rental-scanner"

# Add all files
git add -A

# Commit with message
git commit -m "Initial commit - rentFalcon v2.1 Newmarket Edition

- Multi-source rental search (Kijiji + Rentals.ca)
- 8 cities supported in Newmarket area (25 km radius)
- Easy setup for non-technical users
- Desktop shortcut support
- Comprehensive documentation
- Smart deduplication
- Price filtering
- Clean web interface"
```

---

## Step 4: Add GitHub Remote

Replace `yourusername` with your actual GitHub username:

```bash
git remote add origin https://github.com/yourusername/rentFalcon.git
```

**Example:**
```bash
git remote add origin https://github.com/johndoe/rentFalcon.git
```

---

## Step 5: Push to GitHub

```bash
# Create main branch and push
git branch -M main
git push -u origin main
```

Enter your GitHub credentials when prompted.

---

## Step 6: Verify Upload

1. Go to: `https://github.com/yourusername/rentFalcon`
2. You should see all your files!
3. Check that README.md displays nicely

---

## 🎉 Success!

Your rentFalcon project is now on GitHub!

### Next Steps (Optional):

#### Add Topics
Go to your repository → Click ⚙️ → Add topics:
- `python`
- `flask`
- `web-scraping`
- `rental-search`
- `selenium`
- `newmarket`
- `ontario`

#### Create Release
1. Go to: Releases → Create a new release
2. Tag version: `v2.1`
3. Release title: "rentFalcon v2.1 - Newmarket Edition"
4. Description: Copy from README.md features section
5. Publish release

#### Enable GitHub Pages (Optional)
If you want to host documentation:
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main → /docs
4. Save

---

## 🔄 Making Changes Later

When you make changes to the code:

```bash
# Add changes
git add -A

# Commit with message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

---

## 🆘 Common Issues

### "Permission denied"
- Make sure you're logged into GitHub
- Check that repository name is correct
- Verify you have push access

### "Repository not found"
- Check spelling of username and repo name
- Make sure repository exists on GitHub
- Verify the remote URL: `git remote -v`

### "Failed to push"
- Pull first: `git pull origin main`
- Then push: `git push`

### Want to start over?
```bash
# Remove git history
rm -rf .git

# Start fresh
git init
git add -A
git commit -m "Your message"
git remote add origin https://github.com/yourusername/rentFalcon.git
git branch -M main
git push -u origin main
```

---

## 📋 Complete Command List

Here's everything in one place:

```bash
# 1. Configure Git (one time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 2. Navigate to project
cd "C:\Users\idols\development files\rental-scanner"

# 3. Initialize and commit
git add -A
git commit -m "Initial commit - rentFalcon v2.1"

# 4. Add remote (replace yourusername!)
git remote add origin https://github.com/yourusername/rentFalcon.git

# 5. Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🔗 After Pushing

Update these files with your actual GitHub username:

1. **README.md** - Replace `yourusername` with your GitHub username in all links
2. **PACKAGE_READY.md** - Update distribution links if needed

Search and replace:
- Find: `yourusername`
- Replace with: `your-actual-github-username`

---

## 📝 Example Repository URLs

Once uploaded, your repository will be at:
- **Main page:** `https://github.com/yourusername/rentFalcon`
- **Code:** `https://github.com/yourusername/rentFalcon/tree/main`
- **Releases:** `https://github.com/yourusername/rentFalcon/releases`
- **Issues:** `https://github.com/yourusername/rentFalcon/issues`

Clone command for others:
```bash
git clone https://github.com/yourusername/rentFalcon.git
```

Download ZIP:
```
https://github.com/yourusername/rentFalcon/archive/refs/heads/main.zip
```

---

## 🎊 All Done!

Your rentFalcon project is now public and shareable on GitHub!

Anyone can:
- ⭐ Star your project
- 🍴 Fork and contribute
- 📥 Download and use
- 🐛 Report issues
- 💡 Suggest features

**Share your repository link with the world!** 🚀

---

*Last Updated: November 2025*