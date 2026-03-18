mport os
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

st.set_page_config(page_title="Chegy Bets - Easy Betting", layout="wide")

# ============================================================================
# SIMPLE KID-FRIENDLY THEME & STYLING
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');

* {
    font-family: 'Fredoka', sans-serif;
}

html, body {
    background: #f0f4ff;
    color: #1a1a1a;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    color: #1a1a1a;
}

.main {
    background: #f0f4ff;
}

.block-container {
    max-width: 900px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Big Hero Title */
.hero-big {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 24px rgba(99,102,241,0.3);
}

.hero-big h1 {
    font-size: 3.5em;
    color: white;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.hero-big p {
    font-size: 1.3em;
    color: white;
    margin: 10px 0 0 0;
    opacity: 0.95;
}

/* Big Simple Buttons */
.stButton > button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 20px 40px;
    font-weight: 700;
    font-size: 1.2em;
    height: auto;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}

.stButton > button:hover {
    background: #4f46e5;
    box-shadow: 0 8px 20px rgba(99,102,241,0.4);
    transform: scale(1.05);
}

/* Game Card - VERY SIMPLE */
.game-card-simple {
    background: white;
    border: 3px solid #6366f1;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.teams-display {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 20px;
    gap: 15px;
}

.team-big {
    text-align: center;
    font-size: 1.8em;
    font-weight: 700;
    color: #1a1a1a;
}

.vs-text {
    font-size: 1.5em;
    color: #6366f1;
    font-weight: 700;
}

.odds-big {
    background: #fff3cd;
    border: 3px solid #ffc107;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    font-size: 2em;
    font-weight: 700;
    color: #d39e00;
    margin: 15px 0;
}

.profit-box {
    background: #d1f3d1;
    border: 3px solid #10b981;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    font-size: 1.5em;
    font-weight: 700;
    color: #10b981;
}

/* Information boxes */
.info-box {
    background: #e0e7ff;
    border-left: 5px solid #6366f1;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    font-size: 1.1em;
}

.step-number {
    background: #6366f1;
    color: white;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Tabs - Simplified */
.stTabs [data-baseweb="tab"] {
    padding: 15px 25px;
    font-weight: 700;
    font-size: 1.1em;
}

/* Form inputs */
input, select {
    font-size: 1.1em !important;
    padding: 12px !important;
    border-radius: 10px !important;
    border: 2px solid #e5e7eb !important;
}

input:focus, select:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.2) !important;
}

.label-big {
    font-size: 1.3em;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 10px;
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
    try:
        if not decimal_odds or decimal_odds <= 0 or decimal_odds == 1:
            return "N/A"
        
        if decimal_odds >= 2:
            american = int((decimal_odds - 1) * 100)
            return f"+{american}"
        else:
            american = int(-100 / (decimal_odds - 1))
            return str(american)
    except:
        return "N/A"

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
    
    away_odds_display = american_odds(best_odds.get(away, 0))
    home_odds_display = american_odds(best_odds.get(home, 0))
    
    # Build sportsbooks grid HTML separately
    books_cards = []
    for i, (book_name, odds) in enumerate(all_bookmaker_odds.items()):
        if i < 4:
            odds_display = american_odds(odds)
            books_cards.append(f'<div class="bookmaker-card"><div class="bookmaker-name">{book_name}</div><div class="bookmaker-odds">{odds_display}</div></div>')
    
    sportsbooks_html = "".join(books_cards)
    
    # Get summary
    summary = generate_bet_summary(teams, arb_value, profit, profit_pct, all_bookmaker_odds)
    
    # Build card HTML
    html_content = f'''<div class="game-card">
    <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center;">
        <div class="team-section">
            <img src="{TEAM_LOGOS.get(away, '')}" class="team-image" onerror="this.style.display='none'">
            <div class="team-name">{away}</div>
            <div class="odds-display">
                <div class="odds-label">Best Odds</div>
                <div class="odds-value">{away_odds_display}</div>
            </div>
        </div>
        <div style="text-align: center; padding: 20px; border-right: 1px solid #e5e7eb; border-left: 1px solid #e5e7eb;">
            <div style="color: #999; font-size: 0.85em; margin-bottom: 15px; text-transform: uppercase; font-weight: 600;">vs</div>
            <div style="background: #f3f4f6; border-radius: 8px; padding: 12px; margin-bottom: 15px;">
                <div style="color: #666; font-size: 0.75em; text-transform: uppercase; font-weight: 600;">ARB VALUE</div>
                <div style="color: #6366f1; font-size: 1.6em; font-weight: 700;">{arb_value:.4f}</div>
            </div>
            <div style="color: #10b981; font-size: 1.1em; font-weight: 700;">💰 +${profit:.2f}</div>
            <div style="color: #6366f1; font-size: 0.9em; font-weight: 600;">{profit_pct:.1f}% ROI</div>
        </div>
        <div class="team-section">
            <img src="{TEAM_LOGOS.get(home, '')}" class="team-image" onerror="this.style.display='none'">
            <div class="team-name">{home}</div>
            <div class="odds-display">
                <div class="odds-label">Best Odds</div>
                <div class="odds-value">{home_odds_display}</div>
            </div>
        </div>
    </div>
    <div class="divider"></div>
    <div style="margin-top: 20px;">
        <div style="color: #666; font-size: 0.8em; text-transform: uppercase; margin-bottom: 15px; font-weight: 600;">📊 Best Odds by Sportsbook</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px;">
            {sportsbooks_html}
        </div>
    </div>
    <div style="background: #f0f4ff; border-left: 4px solid #6366f1; border-radius: 8px; padding: 14px; margin-top: 16px; margin-bottom: 0;">
        <div style="color: #333; font-size: 0.95em; line-height: 1.6;">{summary}</div>
    </div>
</div>'''
    
    st.markdown(html_content, unsafe_allow_html=True)

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
    """Super simple login/signup page"""
    
    st.markdown('<div class="hero-big"><h1>⚽ CHEGY BETS</h1><p>Find FREE Money in Sports Betting!</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="info-box" style="text-align: center; font-size: 1.2em; margin-top: 20px;">👉 Pick one option below 👈</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔓 LOGIN", "📝 NEW USER"])
        
        with tab1:
            st.markdown('<div class="label-big">🔑 Your Username:</div>', unsafe_allow_html=True)
            username = st.text_input("", key="login_user", placeholder="Type your name here")
            
            st.markdown('<div class="label-big">🔐 Your Password:</div>', unsafe_allow_html=True)
            password = st.text_input("", type="password", key="login_pass", placeholder="Type your password")
            
            if st.button("✅ LOGIN", use_container_width=True):
                if username and password:
                    if login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_tier = get_user_tier(username)
                        st.success("🎉 Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Wrong name or password")
                else:
                    st.warning("⚠️ Please fill in both boxes")
            
            st.markdown('---')
            st.markdown('<div class="info-box"><b>👤 Try Demo:</b><br>Username: <code>admin</code><br>Password: <code>chegy2024</code></div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="label-big">📝 Pick a Username:</div>', unsafe_allow_html=True)
            new_user = st.text_input("", key="signup_user", placeholder="Your name (3+ letters)")
            
            st.markdown('<div class="label-big">🔐 Pick a Password:</div>', unsafe_allow_html=True)
            new_pass = st.text_input("", type="password", key="signup_pass", placeholder="Your secret password")
            
            if st.button("✅ CREATE ACCOUNT", use_container_width=True):
                if new_user and new_pass:
                    if len(new_user) < 3:
                        st.error("❌ Name must be 3+ letters")
                    elif new_user == ADMIN_USERNAME:
                        st.error("❌ That name is taken")
                    elif new_user in load_users():
                        st.error("❌ Someone already has that name")
                    else:
                        register_user(new_user, new_pass, "free")
                        st.success("🎉 Account created! Now log in above")
                else:
                    st.warning("⚠️ Fill in both boxes")


def page_dashboard():
    """Super simple dashboard showing bet opportunities"""
    
    # Header
    st.markdown('<div class="hero-big"><h1>🏆 Find FREE Money!</h1><p>Pick a Sport → See the Bets → Make Money</p></div>', unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown('<div class="label-big">👤 ' + st.session_state.username.upper() + '</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown('<div class="label-big">🏟️ Pick Your Sport:</div>', unsafe_allow_html=True)
        sports = ["NBA Basketball", "NFL Football", "MLB Baseball", "Soccer", "Hockey"]
        selected_sport = st.selectbox("", sports, key="sport_select")
        
        st.markdown('<div class="label-big">📊 Pick Markets:</div>', unsafe_allow_html=True)
        col_sel, col_desel = st.columns(2)
        with col_sel:
            if st.button("✅ ALL", use_container_width=True, key="sel_all"):
                st.session_state.selected_markets = ["Spread", "Moneyline", "Total"]
        with col_desel:
            if st.button("❌ NONE", use_container_width=True, key="desel_all"):
                st.session_state.selected_markets = []
        
        markets = st.multiselect("",
            ["Spread", "Moneyline", "Total"],
            default=st.session_state.get("selected_markets", ["Spread"]),
            key="markets_select"
        )
        st.session_state.selected_markets = markets
        
        # Admin API Key
        if st.session_state.user_tier == "admin":
            st.markdown("---")
            st.markdown('<div class="label-big">🔑 Admin API Key:</div>', unsafe_allow_html=True)
            api_key = st.text_input("", type="password", key="api_key_input", placeholder="Paste key here")
            if api_key:
                st.session_state.api_key = api_key
                st.success("✅ Key Set!")
        
        st.markdown("---")
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_tier = None
            st.rerun()
    
    # Main content
    st.markdown(f'<div class="info-box"><b>🎯 Showing:</b> {", ".join(markets) if markets else "None selected"}</div>', unsafe_allow_html=True)
    
    if not st.session_state.get("api_key"):
        if st.session_state.user_tier == "admin":
            st.warning("⚠️ Set your API Key in settings →")
        else:
            st.info("✋ Admin must set API Key first")
    else:
        if st.button("🔍 FIND BETS", use_container_width=True):
            with st.spinner("🔄 Looking for FREE money..."):
                try:
                    api_key = st.session_state.api_key
                    data = get_odds(api_key, selected_sport)
                    
                    if not data:
                        st.info("🏟️ No games today")
                    else:
                        arbs = find_arbitrage(data)
                        
                        if arbs:
                            st.markdown(f'<div class="info-box" style="text-align:center; font-size: 1.5em;">🎉 Found {len(arbs)} Bets!</div>', unsafe_allow_html=True)
                            
                            for idx, arb in enumerate(arbs[:10]):
                                display_professional_game_card(arb["teams"], arb["odds"], {}, arb.get("arb_value", 0), arb.get("profit", 0), arb.get("profit_pct", 0))
                        else:
                            st.info("😴 No bets right now")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


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

