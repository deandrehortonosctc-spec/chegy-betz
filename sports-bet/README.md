# ⚡ ODDS HUNTER - Professional Sports Betting Arbitrage Detection

**Enterprise-grade arbitrage detection dashboard for all major sports and sportsbooks**

![Professional Design](https://img.shields.io/badge/Design-Professional-teal) ![All Sports](https://img.shields.io/badge/Sports-All%20Major-blue) ![Multi-Book](https://img.shields.io/badge/Sportsbooks-8%2B-purple)

---

## 🎯 Features

### 🏆 **Comprehensive Sports Coverage**
- NFL, NBA, MLB, NHL, MLS, Premier League, and 100+ more sports
- All major betting markets (Head-to-Head, Spreads, Totals, Props)
- Real-time odds from 8+ sportsbooks (DraftKings, FanDuel, BetMGM, Caesars, PointsBet, and more)

### 💎 **Professional UI Design**
- **Studio-quality interface** — inspired by Pikkit & Action app
- **Team/Player Photo Integration** — visual match previews with team logos
- **Geometric Design** — modern gradient backgrounds with subtle geometric art elements
- **Gray Professional Theme** — elegant color palette with teal accents and cyan highlights
- **Modern Typography** — Space Mono monospace + Inter sans-serif fonts for readability
- **Big Popping Results Display** — large American odds format (+/-) with instant visual feedback

### 🎨 **Individual Game Cards**
- Team logos and names prominently displayed
- American odds format (e.g., +150, -120) with best odds highlighted
- Arbitrage value clearly shown with profit in USD and ROI percentage
- All competing sportsbook odds in a comparative grid below each match
- Hover effects for interactive browsing

### 📊 **Real-Time Analytics**
- Metrics dashboard: Total Opportunities, Average Profit, Max Profit, Average ROI
- Line movement tracking across sportsbooks over time
- Historical data storage in CSV format
- Export results to CSV for further analysis

### 🔐 **Enterprise Features**
- Environment variable support for secure API key management
- Multi-region support (US, EU, UK)
- Configurable profit thresholds
- Auto-refresh with custom TTL
- Professional error handling and timeout management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- The Odds API key (free tier available: https://the-odds-api.com)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/sports-bet.git
cd sports-bet
```

2. Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

3. Set your API key (choose one):
```powershell
# Option A: Environment variable
$env:ODDS_API_KEY="YOUR_API_KEY_HERE"

# Option B: Streamlit secrets file (.streamlit/secrets.toml)
# ODDS_API_KEY = "YOUR_API_KEY_HERE"
```

### Running the Dashboard

```powershell
python -m streamlit run streamlit_app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📖 Usage

### CLI Tool (app.py)

```powershell
# Basic usage
$env:ODDS_API_KEY="YOUR_KEY"
python app.py --sport basketball_nba --region us --markets h2h --stake 100

# With CSV export
python app.py --sport americanfootball_nfl --region us --markets h2h,spreads --save-csv nfl_arbs.csv
```

**Available Options:**
- `--api-key`: Your Odds API key (or use env var)
- `--sport`: Sport key (e.g., basketball_nba, americanfootball_nfl)
- `--region`: Region (us, eu, uk, au)
- `--markets`: Comma-separated markets (h2h, spreads, totals)
- `--stake`: Total stake for calculations (default: 100)
- `--save-csv`: Save results to CSV file

### Web Dashboard (streamlit_app.py)

1. **Select Sport** — Dynamic dropdown with all available sports
2. **Choose Market** — Head-to-Head, Spreads, Totals, or multiple
3. **Set Parameters** — Stake amount, max arbitrage threshold
4. **Search Arbitrage** — Scans all sportsbooks in real-time
5. **View Results** — Professional card layout with team photos, odds, and profit
6. **Export Data** — Download opportunities as CSV

---

## 🎨 Design Highlights

### Color Scheme
- **Primary**: Teal Accent (#14b8a6)
- **Background**: Deep Navy (#0f0f1e to #1a1a2e)
- **Secondary**: Purple (#8b5cf6)
- **Text**: Light Gray (#e5e7eb)

### Typography
- Headers: Space Mono (monospace, 700 weight)
- Body: Inter (sans-serif, 300-600 weight)
- Odds: Space Mono (for consistency and professional look)

### Geometric Art
- Circular gradient backgrounds (fixed positioning, low opacity)
- Triangular design elements
- Smooth transitions and hover states
- Modern border-radius and shadows

---

## 📊 Data Storage

The app automatically stores:

- **Arbitrage Snapshots** → `data/arbs_{timestamp}.csv` + `data/arbs_master.csv`
- **Bookmaker-Level Odds** → `data/odds_detailed.csv` (for line movement analysis)
- **Fields Tracked:**
  - Sport, Teams, Team Name, Bookmaker, Market Type, Odds, Timestamp

---

## 🌐 Deployment (Streamlit Cloud)

**Free deployement** on Streamlit Cloud. See [DEPLOY.md](DEPLOY.md) for step-by-step instructions.

Quick setup:
1. Push code to GitHub
2. Go to https://share.streamlit.app
3. Connect GitHub repo
4. Add API key via Streamlit secrets
5. Live at `https://YOUR_USERNAME-sports-bet.streamlit.app`

---

## 🗺️ Roadmap

| Phase | Status | Task |
|-------|--------|------|
| ✅ **Phase 1** | Complete | Professional UI Design, All Sports, Multi-Sportsbook Display, Team Photos |
| ✅ **Phase 2** | Complete | Streamlit Cloud Deployment, Data Logging, Line Movement Tracking |
---

## ❓ FAQ

**Q: Why am I not seeing any arbitrage?**
- Real arbitrage is rare due to market efficiency. The app finds legitimate opportunities, but they may only exist for seconds.
- Try different sports, leagues, or regions where odds lines are less efficient.

**Q: Can I use this for betting?**
- Use at your own risk. Arbitrage works in theory but sportsbooks may limit/close accounts that consistently exploit it.
- This tool is educational and for research purposes.

**Q: How often should I check for arbitrage?**
- The dashboard auto-refreshes every 60 seconds by default. You can adjust in settings.

**Q: What if I get "API limits exceeded"?**
- Free tier is 500 requests/month. Consider upgrading or spreading API calls over time.

---

## 👨‍💻 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — See LICENSE file for details

---

## 🙋 Support

- **Issues?** Open a GitHub Issue
- **Questions?** Check the FAQ or open a Discussion
- **API Issues?** Visit https://the-odds-api.com/status

---

**Made with ❤️ by the Odds Hunter Team**

*Professional arbitrage detection. Enterprise-grade design. Completely free.*

