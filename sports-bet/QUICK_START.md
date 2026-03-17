# 🚀 Quick Start Guide - Odds Hunter Dashboard

## ⚡ 30-Second Setup

### 1. Install Dependencies
```powershell
cd "c:\Users\Heemt\OneDrive\Desktop\sports-bet"
python -m pip install -r requirements.txt
```

### 2. Set Your API Key
```powershell
$env:ODDS_API_KEY="YOUR_API_KEY_HERE"
```

Get free API key at: https://the-odds-api.com

### 3. Run Dashboard
```powershell
python -m streamlit run streamlit_app.py
```

### 4. Open Browser
Navigate to: **http://localhost:8501**

---

## 🎯 Using the Dashboard

### Step 1: Configure Settings (Left Sidebar)
1. **Enter API Key** in the text field
2. **Select Sport** from dropdown (all available sports auto-loaded)
3. **Pick Region**: US, EU, or UK
4. **Choose Markets**: Head-to-Head, Spreads, Totals (or combo)
5. **Set Stake Amount**: How much you're betting total
6. **Adjust Max Arb %**: Threshold (lower = better opportunities)

### Step 2: Search for Arbitrage
- Click blue **"🔍 SEARCH ARBITRAGE"** button
- Wait for scanner to check all sportsbooks...

### Step 3: Review Results
You'll see:
- **✅ Badge** showing how many opportunities found
- **Metrics** at top (Total, Avg Profit, Max Profit, ROI)
- **Professional Game Cards** with:
  - Team logos & names
  - Best odds in American format (+150, -120)
  - Guaranteed profit in USD
  - ROI percentage
  - All competing sportsbook odds

### Step 4: Export or Share
- Click **"📥 Export Results (CSV)"** to download
- Save arbitrage data for records

---

## 💎 What You'll See

### Game Card Layout
```
┌─────────────────────────────────────────────────┐
│                                                 │
│  [TEAM A LOGO]  vs  [$$ PROFIT]  [TEAM B LOGO]│
│   Team Name           +12.34 (12%)    Team Name│
│   +150 ODDS      0.9876 ARB VAL      -120 ODDS│
│                                                 │
├─────────────────────────────────────────────────┤
│ 📊 Best Odds by Sportsbook                      │
│                                                 │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│ │DraftKings  │ │ FanDuel    │ │  BetMGM    │  │
│ │   +150     │ │   -120     │ │   +160     │  │
│ └────────────┘ └────────────┘ └────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Dashboard Header
```
⚡ ODDS HUNTER
Professional Arbitrage Detection Across All Major Sports & Sportsbooks

✅ 5 ARBITRAGE OPPORTUNITIES FOUND

📊 Metrics:
[5 Total Arbs]  [$12.34 Avg Profit]  [$25.67 Max Profit]  [12.3% Avg ROI]
```

---

## 🎨 Design Features

✨ **Professional Theme**
- Deep navy background with teal accents
- Modern typography (Space Mono + Inter fonts)
- Smooth hover animations
- Geometric gradient art elements

📸 **Team Photos**
- Automatic team logo display
- High-quality NFL/NBA/MLB/NHL logos
- Hover zoom effect

💰 **American Odds**
- Familiar +150 / -120 format (not decimal)
- Large, easy-to-read font
- Color-coded profit display (green = profit)

📊 **All Sportsbooks**
- Top 4 books shown per game
- Comparative odds grid
- Best odds highlighted

---

## 🔑 API Key Setup

### Option A: Environment Variable (Recommended)
```powershell
$env:ODDS_API_KEY="YOUR_KEY_HERE"
```

### Option B: Streamlit Secrets File
1. Create file: `.streamlit/secrets.toml`
2. Add: `ODDS_API_KEY = "YOUR_KEY_HERE"`
3. Streamlit automatically loads this

### Getting a Free API Key
1. Visit https://the-odds-api.com
2. Click "Free Tier"
3. Sign up (email only)
4. Copy your API key
5. Paste into dashboard

**Free Tier Limits:**
- 500 requests/month
- ~16-17 requests per day
- Perfect for testing!

---

## ⚙️ Advanced Settings

### Stake Amount
- Example: $100 total
- App calculates: $40 on Team A @ 2.50, $60 on Team B @ 1.67
- Guaranteed return: ~$100 → profit of $0-2

### Max Arb Threshold
- Default: 0.99
- Lower value = better opportunities (but rarer)
- 0.95 = only show great arbitrage (very few)
- 0.999 = show all (even tiny margins)

### Markets
- **h2h**: Head-to-Head (Team A vs Team B)
- **spreads**: Point spreads (Team A -7.5 vs Team B +7.5)
- **totals**: Over/Under on total points
- Mix and match for comprehensive scan

---

## 🎯 Tips for Best Results

### Finding More Arbitrage
1. **Scan Spreads & Totals** — Often have better opportunities than h2h
2. **Try Multiple Regions** — EU and UK odds differ from US
3. **Check During Events** — Live lines move faster
4. **Morning Scans** — Before bookmakers align on early games
5. **Niche Sports** — Tennis, golf, esports have less efficient markets

### Professional Workflow
1. Set up **auto-refresh** (scan periodically)
2. Log results to CSV for **analysis**
3. Track which **sportsbooks** offer best lines
4. Monitor **line movement** over time
5. Build **historical database** for future advantage

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No arbitrage found" | Try different sport, region, or markets. Real arb is rare. |
| "API Key Error" | Check key is valid, ensure $env:ODDS_API_KEY is set, try secrets file |
| "Dashboard won't load" | Run `python -m pip install -r requirements.txt` to install dependencies |
| "Timeout" | Your internet is slow or API is down. Check https://the-odds-api.com/status |
| "No team logos" | Fallback displays OK. Add more to TEAM_LOGOS dict in streamlit_app.py |

---

## 📱 Mobile Use

- Dashboard is **responsive**
- Sidebar collapses on small screens
- Touch-friendly buttons
- Works on iPad, phones (via tunnel)

To access from phone:
```powershell
python -m streamlit run streamlit_app.py --server.address 0.0.0.0
```
Then access: `http://[YOUR-COMPUTER-IP]:8501`

---

## 💻 System Requirements

- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: 500MB minimum (1GB+ recommended)
- **Storage**: 100MB for app (CSV grows over time)
- **Internet**: Stable connection for API calls
- **OS**: Windows, Mac, or Linux

---

## 🚀 Next Steps

1. **Deploy Online** → See DEPLOY.md for free Streamlit Cloud hosting
2. **Customize** → Add your own sportsbooks to BOOKMAKERS dict
3. **Automate** → Set up task scheduler to run searches hourly
4. **Analyze** → Load CSV data into Excel/Python for analysis
5. **Extend** → Add prediction model (see Phase 3 roadmap)

---

## ❓ Common Questions

**Q: Is this legal?**
A: Yes, arbitrage betting is legal. Just be aware sportsbooks may limit accounts that consistently exploit it.

**Q: Can I make money?**
A: Theoretically yes, but real arbitrage is rare. Market-making algorithms close most opportunities within seconds.

**Q: How often should I check?**
A: Dashboard can auto-refresh every 10-600 seconds. 60-second interval is typical.

**Q: What's my profit if I find one?**
A: Profit = Stake × (1 - Arb Value). E.g., $100 × 0.02 = $2 profit.

**Q: Do I need multiple sportsbook accounts?**
A: Yes, you need accounts at all books you want to use for arbitrage.

---

## 📞 Support

- **Bug Reports**: Open GitHub Issue
- **API Issues**: Check https://the-odds-api.com/status
- **Questions**: See README.md FAQ section
- **Feedback**: Open GitHub Discussion

---

**Ready? Run this command now:**
```powershell
python -m streamlit run streamlit_app.py
```

**That's it! Enjoy your professional arbitrage dashboard! 🚀**
