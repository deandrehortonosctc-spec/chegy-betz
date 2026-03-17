import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List
import streamlit as st
import pandas as pd
import requests
import random

from app import get_odds, find_arbitrage, compute_stakes
from data_store import save_snapshot, save_detailed_odds

st.set_page_config(page_title="Chegy Bets - Smart Arbitrage Betting", layout="wide")

# ============================================================================
# PROFESSIONAL THEME & STYLING
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

html, body {
    background: #f8f9fa;
    color: #1a1a1a;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    color: #1a1a1a;
    letter-spacing: -0.3px;
}

.main {
    background: #f8f9fa;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Hero Section - Clean Professional */
.hero-section {
    background: white;
    border-radius: 16px;
    padding: 48px;
    margin-bottom: 40px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-top: 4px solid #6366f1;
}

.hero-title {
    font-size: 2.8em;
    color: #1a1a1a;
    margin-bottom: 12px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 1.05em;
    color: #666;
    font-weight: 400;
    letter-spacing: 0px;
}

/* Game Card - Professional */
.game-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    position: relative;
}

.game-card:hover {
    border-color: #6366f1;
    box-shadow: 0 8px 24px rgba(99,102,241,0.12);
    transform: translateY(-2px);
}

.team-section {
    text-align: center;
    padding: 16px;
}

.team-image {
    width: 100%;
    max-width: 100px;
    height: 100px;
    object-fit: contain;
    margin-bottom: 12px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    transition: all 0.3s ease;
}

.team-image:hover {
    transform: scale(1.05);
}

.team-name {
    font-size: 1em;
    color: #1a1a1a;
    font-weight: 600;
    margin-bottom: 8px;
}

.odds-display {
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px;
    margin-top: 12px;
}

.odds-value {
    font-size: 1.8em;
    color: #6366f1;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.odds-label {
    font-size: 0.8em;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 6px;
    font-weight: 600;
}

/* Bookmaker Grid */
.bookmaker-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    transition: all 0.2s ease;
}

.bookmaker-card:hover {
    background: #f3f4f6;
    border-color: #6366f1;
}

.bookmaker-name {
    font-size: 0.85em;
    color: #666;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    font-weight: 600;
}

.bookmaker-odds {
    font-size: 1.4em;
    color: #6366f1;
    font-weight: 700;
}

/* Metrics */
.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #6366f1;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.metric-value {
    font-size: 1.8em;
    color: #6366f1;
    font-weight: 700;
}

.metric-label {
    font-size: 0.8em;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-top: 8px;
    font-weight: 600;
}

/* Status Badges */
.badge-success {
    background: #f0fdf4;
    border: 1px solid #86efac;
    color: #166534;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 0.9em;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 20px;
}

.badge-empty {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 0.9em;
    font-weight: 600;
    display: inline-block;
}

/* Divider */
.divider {
    height: 1px;
    background: #e5e7eb;
    margin: 30px 0;
}

/* Geometric background elements */
.geo-element {
    position: fixed;
    pointer-events: none;
    opacity: 0.03;
    z-index: -1;
}

.geo-circle-1 {
    top: 5%;
    right: 5%;
}

/* Form Elements */
input[type="password"],
input[type="text"],
input[type="number"],
select,
textarea {
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
    font-size: 0.95em !important;
    font-family: 'Inter', sans-serif !important;
    background: white !important;
    color: #1a1a1a !important;
}

input[type="password"]:focus,
input[type="text"]:focus,
input[type="number"]:focus,
select:focus,
textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* Buttons */
.stButton > button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 0.95em;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: #4f46e5;
    box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}

/* Sidebar */
.sidebar .sidebar-content {
    background: #f8f9fa;
}

.sidebar .stSubheader {
    color: #1a1a1a;
    font-weight: 700;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1px;
}

.stTabs [data-baseweb="tab"] {
    padding: 12px 20px;
    font-weight: 600;
    border-bottom: 2px solid transparent;
    color: #666;
}

.stTabs [aria-selected="true"] {
    color: #6366f1;
    border-bottom-color: #6366f1;
}

/* Select Boxes */
.stMultiSelect [data-baseweb="tag"] {
    background: #6366f1 !important;
    color: white !important;
    border-radius: 6px !important;
}

/* Spinner */
.stSpinner {
    color: #6366f1 !important;
}

/* Success/Error Messages */
.stSuccess {
    background: #f0fdf4 !important;
    color: #166534 !important;
    border: 1px solid #86efac !important;
    border-radius: 8px !important;
}

.stError {
    background: #fef2f2 !important;
    color: #991b1b !important;
    border: 1px solid #fecaca !important;
    border-radius: 8px !important;
}

.stWarning {
    background: #fffbeb !important;
    color: #92400e !important;
    border: 1px solid #fde047 !important;
    border-radius: 8px !important;
}

.stInfo {
    background: #f0f9ff !important;
    color: #0c4a6e !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# USERS DATABASE (Local JSON)
# ============================================================================

USERS_FILE = "users.json"

def load_users() -> Dict:
    """Load users from JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users: Dict):
    """Save users to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("chegy2024")

def login(username: str, password: str) -> bool:
    """Authenticate user."""
    if username == ADMIN_USERNAME:
        return hash_password(password) == ADMIN_PASSWORD_HASH
    users = load_users()
    if username in users:
        return users[username]["password_hash"] == hash_password(password)
    return False

def register_user(username: str, password: str, tier: str = "free"):
    """Register new user."""
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password_hash": hash_password(password),
        "tier": tier,
        "created_at": datetime.now().isoformat(),
    }
    save_users(users)
    return True

def get_user_tier(username: str) -> str:
    """Get user tier."""
    if username == ADMIN_USERNAME:
        return "admin"
    users = load_users()
    return users.get(username, {}).get("tier", "free")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def american_odds(decimal_odds):
    """Convert decimal odds to American format."""
    if decimal_odds >= 2:
        return f"+{int((decimal_odds - 1) * 100)}"
    else:
        return f"{int(-100 / (decimal_odds - 1))}"

@st.cache_data(ttl=3600)
def get_available_sports(api_key):
    """Fetch all available sports from API."""
    try:
        resp = requests.get(f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}")
        if resp.status_code == 200:
            sports = resp.json()
            return {s['title']: s['key'] for s in sports}
        return {"NFL": "americanfootball_nfl", "NBA": "basketball_nba", "MLB": "baseball_mlb", "NHL": "icehockey_nhl", "MLS": "soccer_usa_mls"}
    except:
        return {"NFL": "americanfootball_nfl", "NBA": "basketball_nba", "MLB": "baseball_mlb", "NHL": "icehockey_nhl", "MLS": "soccer_usa_mls"}

# Popular sportsbooks
SPORTSBOOKS = {
    "DraftKings": "draftkings",
    "FanDuel": "fanduel",
    "BetMGM": "betmgm",
    "Caesars": "caesars",
    "PointsBet": "pointsbet",
    "Barstool": "barstool",
}

# Team logos mapping
TEAM_LOGOS = {
    "Kansas City Chiefs": "https://a.espncdn.com/media/motion/2022/0328/dm_220328_nfl_chiefs_logo.png",
    "Buffalo Bills": "https://a.espncdn.com/media/motion/2022/0328/dm_220328_nfl_bills_logo.png",
    "Los Angeles Lakers": "https://a.espncdn.com/media/motion/2022/0328/dm_220328_nba_lakers_logo.png",
    "Boston Celtics": "https://a.espncdn.com/media/motion/2022/0328/dm_220328_nba_celtics_logo.png",
}

def display_professional_game_card(teams: List[str], best_odds: Dict, all_bookmaker_odds: Dict, arb_value: float, profit: float, profit_pct: float):
    """Display game as professional card."""
    away, home = (teams[0], teams[1]) if len(teams) >= 2 else ("Team A", "Team B")
    
    # Build sportsbooks HTML
    sportsbooks_html = ""
    for i, (book_name, odds) in enumerate(all_bookmaker_odds.items()):
        if i < 4:
            sportsbooks_html += f"""
                <div class="bookmaker-card">
                    <div class="bookmaker-name">{book_name}</div>
                    <div class="bookmaker-odds">{american_odds(odds)}</div>
                </div>"""
    
    # Get summary
    summary = generate_bet_summary(teams, arb_value, profit, profit_pct, all_bookmaker_odds)
    
    # Build complete card HTML in one go
    card_html = f"""
    <div class="game-card">
        <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center;">
            <!-- Away Team -->
            <div class="team-section">
                <img src="{TEAM_LOGOS.get(away, 'https://via.placeholder.com/120')}" class="team-image" onerror="this.style.display='none';">
                <div class="team-name">{away}</div>
                <div class="odds-display">
                    <div class="odds-label">Best Odds</div>
                    <div class="odds-value">{american_odds(best_odds.get(away, 0))}</div>
                </div>
            </div>
            
            <!-- Match Info & Arbitrage -->
            <div style="text-align: center; padding: 20px; border-right: 1px solid #e5e7eb; border-left: 1px solid #e5e7eb;">
                <div style="color: #999; font-size: 0.85em; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.3px; font-weight: 600;">vs</div>
                <div style="background: #f3f4f6; border-radius: 8px; padding: 12px; margin-bottom: 15px; border: 1px solid #e5e7eb;">
                    <div style="color: #666; font-size: 0.75em; text-transform: uppercase; letter-spacing: 0.3px; font-weight: 600;">ARB VALUE</div>
                    <div style="color: #6366f1; font-size: 1.6em; font-weight: 700;">{arb_value:.4f}</div>
                </div>
                <div style="color: #10b981; font-size: 1.1em; font-weight: 700;">💰 +${profit:.2f}</div>
                <div style="color: #6366f1; font-size: 0.9em; font-weight: 600;">{profit_pct:.1f}% ROI</div>
            </div>
            
            <!-- Home Team -->
            <div class="team-section">
                <img src="{TEAM_LOGOS.get(home, 'https://via.placeholder.com/120')}" class="team-image" onerror="this.style.display='none';">
                <div class="team-name">{home}</div>
                <div class="odds-display">
                    <div class="odds-label">Best Odds</div>
                    <div class="odds-value">{american_odds(best_odds.get(home, 0))}</div>
                </div>
            </div>
        </div>
        
        <!-- Sportsbooks Row -->
        <div class="divider"></div>
        <div style="margin-top: 20px;">
            <div style="color: #666; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 15px; font-weight: 600;">📊 Best Odds by Sportsbook</div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px;">
                {sportsbooks_html}
            </div>
        </div>
        
        <!-- AI Summary -->
        <div style="background: #f0f4ff; border-left: 4px solid #6366f1; border-radius: 8px; padding: 14px; margin-top: 16px;">
            <div style="color: #333; font-size: 0.95em; line-height: 1.6;">
                {summary}
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

# ============================================================================
# AI BET SUMMARY GENERATOR
# ============================================================================

def generate_bet_summary(teams: List[str], arb_value: float, profit: float, profit_pct: float, all_bookmaker_odds: Dict) -> str:
    """Generate AI-like summary explaining why this is a good bet."""
    
    # Analyze opportunity strength
    if arb_value < 0.985:
        strength = "EXTREMELY STRONG"
        emoji = "🔥"
    elif arb_value < 0.990:
        strength = "VERY STRONG"
        emoji = "⚡"
    elif arb_value < 0.995:
        strength = "STRONG"
        emoji = "💪"
    else:
        strength = "GOOD"
        emoji = "✅"
    
    # Analyze profit level
    if profit > 50:
        profit_desc = "exceptional profit potential"
    elif profit > 25:
        profit_desc = "substantial profit margin"
    elif profit > 10:
        profit_desc = "solid profit opportunity"
    else:
        profit_desc = "consistent profit opportunity"
    
    # Analyze odds discrepancy
    odds_list = list(all_bookmaker_odds.values())
    if odds_list:
        odds_variance = max(odds_list) - min(odds_list)
        if odds_variance > 0.5:
            variance_desc = "significant odds variation across sportsbooks"
        elif odds_variance > 0.2:
            variance_desc = "notable odds differences between books"
        else:
            variance_desc = "consistent odds across major sportsbooks"
    else:
        variance_desc = "consistent market pricing"
    
    # Analyze ROI
    if profit_pct > 2.0:
        roi_desc = f"impressive {profit_pct:.1f}% return"
    elif profit_pct > 1.0:
        roi_desc = f"solid {profit_pct:.1f}% return on investment"
    else:
        roi_desc = f"reliable {profit_pct:.1f}% guaranteed return"
    
    # Build summary
    team_matchup = f"{teams[0]} vs {teams[1]}" if len(teams) >= 2 else "this matchup"
    
    summaries = [
        f"{emoji} **{strength} Opportunity**: {team_matchup} presents {profit_desc} with {variance_desc}. Arb value of {arb_value:.4f} means virtually risk-free profit.",
        f"{emoji} **Market Inefficiency Detected**: The {variance_desc} creates a {strength.lower()} arbitrage at {arb_value:.4f}. Expect {roi_desc}.",
        f"{emoji} **Exceptional Value**: This {strength.lower()} opportunity exploits pricing disparities to guarantee ${profit:.2f} profit ({profit_pct:.1f}% ROI).",
        f"{emoji} **Smart Money Play**: {strength} arbitrage found on {team_matchup}. The market pricing creates {profit_desc}. Lock in {roi_desc}.",
        f"{emoji} **Locked-In Profit**: This {strength.lower()} bet eliminates risk. {team_matchup} shows {variance_desc}, guaranteeing ${profit:.2f}.",
    ]
    
    return random.choice(summaries)


# ============================================================================
# AUTHENTICATION PAGES
# ============================================================================

def page_auth():
    """Login and signup page for unauthenticated users"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">💰 Chegy Bets</div>
        <div class="hero-subtitle">Professional Arbitrage Detection Across All Major Sports</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.markdown("### Log In to Your Account")
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("🔓 Login", use_container_width=True):
                if login_username and login_password:
                    if login(login_username, login_password):
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        st.session_state.user_tier = get_user_tier(login_username)
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter username and password")
            
            st.markdown("---")
            st.markdown("""
            **Demo Account:**
            - Username: `admin`
            - Password: `chegy2024`
            """)
        
        with tab2:
            st.markdown("### Create New Account")
            signup_username = st.text_input("Choose Username", key="signup_user")
            signup_password = st.text_input("Choose Password", type="password", key="signup_pass")
            signup_tier = st.selectbox("Account Tier", ["free", "premium"], key="signup_tier")
            
            if st.button("✍️ Create Account", use_container_width=True):
                if signup_username and signup_password:
                    if len(signup_username) < 3:
                        st.error("❌ Username must be at least 3 characters")
                    elif signup_username == ADMIN_USERNAME:
                        st.error("❌ That username is reserved")
                    else:
                        users = load_users()
                        if signup_username in users:
                            st.error("❌ Username already taken")
                        else:
                            register_user(signup_username, signup_password, signup_tier)
                            st.success("✅ Account created! Please log in.")
                            st.session_state.logged_in = False
                else:
                    st.warning("⚠️ Please enter username and password")


def page_dashboard():
    """Main dashboard - only shown to authenticated users"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username.upper()}")
        st.markdown(f"**Tier:** {'👑 ADMIN' if st.session_state.user_tier == 'admin' else f'⭐ {st.session_state.user_tier.upper()}'}")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_tier = None
            st.rerun()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">💰 Chegy Bets</div>
        <div class="hero-subtitle">Professional Arbitrage Detection Across All Major Sports</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Settings
    with st.sidebar:
        st.markdown("---")
        st.subheader("⚙️ Settings")
        
        # API Key - Admin Only
        if st.session_state.user_tier == "admin":
            api_key = st.text_input("API Key", value=os.environ.get('ODDS_API_KEY', ''), type='password')
        else:
            api_key = os.environ.get('ODDS_API_KEY', '')
            st.info("📌 Contact admin for API key access")
        
        if api_key:
            sports_map = get_available_sports(api_key)
            sport_name = st.selectbox("🏆 Sport", list(sports_map.keys()))
            sport = sports_map[sport_name]
        else:
            sport = "basketball_nba"
            if st.session_state.user_tier == "admin":
                st.warning("Add API key to unlock all sports")
        
        region = st.selectbox("🌍 Region", ["us", "eu", "uk"], index=0)
        
        st.markdown("**📊 Markets**")
        col_sel_all, col_desel_all = st.columns(2)
        with col_sel_all:
            select_all = st.button("✅ Select All", use_container_width=True, key="select_all_btn")
        with col_desel_all:
            deselect_all = st.button("❌ Deselect All", use_container_width=True, key="deselect_all_btn")
        
        if select_all:
            st.session_state.selected_markets = ["h2h", "spreads", "totals"]
        if deselect_all:
            st.session_state.selected_markets = []
        
        markets = st.multiselect(
            "Select Markets",
            ["h2h", "spreads", "totals"],
            default=st.session_state.get("selected_markets", ["h2h"]),
            key="markets_select"
        )
        st.session_state.selected_markets = markets
        
        if not markets:
            markets = ["h2h"]
        markets_str = ",".join(markets)
        
        stake = st.number_input("💵 Stake Amount", value=100.0, min_value=1.0, step=10.0)
        arb_threshold = st.number_input("🎯 Max Arb (%)", value=0.99, step=0.001, format="%.3f")
        
        if st.button("🔍 SEARCH ARBITRAGE", use_container_width=True):
            st.session_state.search = True

    # Check if search requested
    search = st.session_state.get("search", False)

    if not api_key:
        st.warning("🔑 Please provide The Odds API key in settings")
    elif search:
        with st.spinner("🔄 Scanning all sportsbooks..."):
            data = get_odds(api_key, sport, region, markets_str)
        
        if not data:
            st.markdown('<div class="badge-empty">❌ No games available</div>', unsafe_allow_html=True)
        else:
            save_detailed_odds(data)
            arbs = find_arbitrage(data)
            
            # Filter & build display
            opportunities = []
            for arb in arbs:
                if arb["arb_value"] > arb_threshold:
                    continue
                
                teams = arb["teams"]
                best = arb["odds"]
                team_names = list(best.keys())
                odds_vals = [best[team_names[0]], best[team_names[1]]]
                stake_a, stake_b, profit, profit_pct = compute_stakes(odds_vals[0], odds_vals[1], total=stake)
                
                # Collect all bookmaker odds
                all_bookmaker_odds = {}
                for game in data:
                    if game.get("teams") == teams:
                        for bm in game.get("bookmakers", []):
                            for market in bm.get("markets", []):
                                for outcome in market.get("outcomes", []):
                                    team = outcome.get("name")
                                    odds = outcome.get("price")
                                    if team == team_names[0]:
                                        all_bookmaker_odds[bm.get("title")] = odds
                
                opportunities.append({
                    "teams": teams,
                    "best_odds": best,
                    "all_odds": all_bookmaker_odds,
                    "arb_value": arb["arb_value"],
                    "profit": profit,
                    "profit_pct": profit_pct,
                    "stake_a": stake_a,
                    "stake_b": stake_b,
                })
            
            if not opportunities:
                st.markdown('<div class="badge-empty">❌ No arbitrage found. Try adjusting filters.</div>', unsafe_allow_html=True)
            else:
                # Show summary
                st.markdown(f'<div class="badge-success">✅ {len(opportunities)} ARBITRAGE OPPORTUNITIES FOUND</div>', unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(opportunities)}</div>
                        <div class="metric-label">Total Arbs</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    avg_profit = sum(o["profit"] for o in opportunities) / len(opportunities)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">${avg_profit:.2f}</div>
                        <div class="metric-label">Avg Profit</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    max_profit = max(o["profit"] for o in opportunities)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">${max_profit:.2f}</div>
                        <div class="metric-label">Max Profit</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    avg_roi = sum(o["profit_pct"] for o in opportunities) / len(opportunities)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{avg_roi:.1f}%</div>
                        <div class="metric-label">Avg ROI</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display opportunities
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                st.subheader("🎯 Available Opportunities")
                
                for opp in opportunities:
                    display_professional_game_card(
                        opp["teams"],
                        opp["best_odds"],
                        opp["all_odds"],
                        opp["arb_value"],
                        opp["profit"],
                        opp["profit_pct"]
                    )
                
                # Download option
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                df_export = pd.DataFrame([
                    {
                        "Game": " vs ".join(o["teams"]),
                        "Profit": f"${o['profit']:.2f}",
                        "ROI": f"{o['profit_pct']:.1f}%",
                        "Arb Value": f"{o['arb_value']:.4f}"
                    }
                    for o in opportunities
                ])
                
                csv = df_export.to_csv(index=False)
                st.download_button("📥 Export Results (CSV)", csv, "arbitrage_opportunities.csv", "text/csv", use_container_width=True)


# ============================================================================
# MAIN APP - Session State Check
# ============================================================================

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_tier = None
    st.session_state.selected_markets = ["h2h"]

# Show appropriate page based on login state
if not st.session_state.logged_in:
    page_auth()
else:
    page_dashboard()
