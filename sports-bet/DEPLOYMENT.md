# 🚀 Deploy Chegy Bets to Streamlit Cloud

## Quick Deploy (5 minutes)

### Step 1: Push Code to GitHub
```bash
git init
git add .
git commit -m "Chegy Bets - Professional Arbitrage Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/chegy-bets.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to **https://streamlit.io/cloud**
2. Click **"Sign in with GitHub"** (create account if needed)
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/chegy-bets`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Click **"Deploy!"**

### Step 3: Add API Key Secret
1. In Streamlit Cloud dashboard, click your app
2. Go to **Settings** → **Secrets**
3. Add your Odds API key:
```toml
ODDS_API_KEY = "your_api_key_here"
```
4. Save

### Step 4: Share Your Link
Your app is now live at:
```
https://chegy-bets-YOUR_USERNAME.streamlit.app
```

Share this link with friends/users - they can login and use it!

---

## Share URL Examples
- **Demo**: `https://chegy-bets-demo.streamlit.app`
- **Production**: `https://chegy-bets-prod.streamlit.app`
- **Personal**: `https://chegy-bets-yourname.streamlit.app`

## Default Test Account
```
Username: admin
Password: chegy2024
```

Users can create their own accounts once they sign up!

---

## Verified Requirements
✅ All dependencies in `requirements.txt`
✅ Authentication system working
✅ Professional UI/UX
✅ AI bet summaries included
✅ Ready for production

## Support
For issues:
1. Check Streamlit Cloud logs
2. Check API key is valid
3. Verify secrets.toml is configured
4. Restart the deployed app

---

**Your app is now shareable worldwide!** 🌍
