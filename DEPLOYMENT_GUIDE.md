# 🚀 COMPLETE DEPLOYMENT GUIDE - Railway (Easiest)

## ✅ FIXES APPLIED
1. Fixed CORS initialization bug (was called before app creation)
2. Added missing `flask-cors` dependency
3. Added missing `import sys`
4. Cleaned requirements.txt (removed 60+ unnecessary packages)
5. Removed build artifacts

---

## 📋 PREREQUISITES
- GitHub account
- Railway account (sign up at https://railway.app)
- Git installed on your computer

---

## 🔧 STEP-BY-STEP DEPLOYMENT

### STEP 1: Push Fixed Code to GitHub

Open Terminal/Command Prompt in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Stage all files
git add .

# Commit changes
git commit -m "Fix deployment issues"

# Add your GitHub repository as remote
git remote add origin https://github.com/csparx/combine-secured-pdfs.git

# Push to GitHub
git push -u origin main
```

**If you get an error about 'main' branch**, try:
```bash
git branch -M main
git push -u origin main
```

---

### STEP 2: Deploy on Railway

1. **Go to Railway**
   - Visit: https://railway.app
   - Click "Start a New Project"
   - Login with GitHub

2. **Select Your Repository**
   - Click "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select: `csparx/combine-secured-pdfs`

3. **Configure Environment Variables**
   - After selecting repo, Railway will start deploying
   - Click on your project
   - Go to "Variables" tab
   - Click "Add Variable"
   - Add:
     * Name: `PDF_PASSWORD`
     * Value: `your_secure_password_here`
   - Click "Add"

4. **Wait for Deployment** (2-5 minutes)
   - Railway will automatically:
     * Install Python 3.12
     * Install all dependencies
     * Start your app with gunicorn
   - Watch the build logs in the "Deployments" tab

5. **Get Your URL**
   - Once deployed, click "Settings" tab
   - Under "Networking", click "Generate Domain"
   - Copy your app URL (e.g., `your-app.railway.app`)

6. **Test Your App**
   - Visit the URL
   - Upload test files
   - Verify PDF combining works

---

## 🎯 ALTERNATIVE: Deploy on Render

If you prefer Render:

### STEP 1: Push to GitHub (same as above)

### STEP 2: Deploy on Render

1. **Go to Render**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select: `csparx/combine-secured-pdfs`

3. **Configure Service**
   - **Name**: `combine-secured-pdfs`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add:
     * Key: `PDF_PASSWORD`
     * Value: `your_secure_password_here`

5. **Choose Plan**
   - Free: 750 hours/month (sleeps after 15 min inactivity)
   - Starter ($7/mo): Always-on, better performance

6. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Get your URL from dashboard

---

## 🎯 ALTERNATIVE: Deploy on Heroku (If you're already set up)

### STEP 1: Push Fixed Code to Heroku

```bash
# Add all changes
git add .

# Commit
git commit -m "Fix deployment issues"

# Push to Heroku
git push heroku main
```

### STEP 2: Set Environment Variable

```bash
heroku config:set PDF_PASSWORD=your_secure_password_here --app combine-secured-pdfs-507031818448
```

### STEP 3: Check Logs

```bash
heroku logs --tail --app combine-secured-pdfs-507031818448
```

### STEP 4: Open App

```bash
heroku open --app combine-secured-pdfs-507031818448
```

---

## ✅ VERIFICATION CHECKLIST

After deployment, test:
- [ ] Homepage loads
- [ ] Can upload PDF files
- [ ] Can upload Word (.docx) files
- [ ] Can upload Excel (.xlsx) files
- [ ] Files combine successfully
- [ ] Combined PDF is password-protected
- [ ] Can download the combined PDF

---

## 🐛 TROUBLESHOOTING

### If build fails on pandas/numpy:
**Railway**: Should work fine (better build resources)
**Render Free**: May need Starter plan ($7/mo)
**Heroku**: Should work fine

### If app crashes:
```bash
# Railway: Check logs in dashboard
# Render: Check logs in "Logs" tab
# Heroku: 
heroku logs --tail --app YOUR_APP_NAME
```

### If files aren't being processed:
- Check environment variable `PDF_PASSWORD` is set
- Verify uploads/ and processed/ folders exist
- Check file size limits (100 MB max)

---

## 🎉 RECOMMENDED PLATFORM

**🥇 Railway** - Easiest, best build resources, $5 free credit/month
**🥈 Render** - 750 free hours/month, good for testing
**🥉 Heroku** - Classic choice, requires credit card for add-ons

---

## 📞 NEED HELP?

If deployment fails, share:
1. Platform you're using (Railway/Render/Heroku)
2. Error messages from logs
3. Screenshot of error (if possible)

Good luck! 🚀
