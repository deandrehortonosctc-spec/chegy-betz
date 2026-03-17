# 🔐 CHEGY BETS - Authentication Guide

## Quick Start

### Test Account (Admin)
```
Username: admin
Password: chegy2024
```

Login with this account to:
- ✅ Input your own API key
- ✅ See all features
- ✅ Manage the platform

### Create New Account
1. Click **"📝 Sign Up"** tab
2. Choose username (3+ characters)
3. Create password
4. Select tier: **Free** or **Premium**
5. Click **"✍️ Create Account"**

---

## Account Tiers

### 👑 Admin
- **API Key Access**: Can input/change API key
- **Feature Access**: All features enabled
- **User Management**: Can help manage other users (future)

### ⭐ Free
- **API Key Access**: ❌ Restricted (shows contact message)
- **Feature Access**: View arbitrage results (when admin provides API)
- **Limitations**: Cannot search without admin setting up API

### ⭐ Premium (Future)
- **API Key Access**: ✅ Can input personal API key
- **Priority**: Faster searches, more results
- **Features**: All advanced tools

---

## How to Use

### First Time
1. Run the app
2. See login screen
3. Click **"📝 Sign Up"** tab
4. Create your account
5. Login

### As Admin
1. Login with: `admin` / `chegy2024`
2. See "👑 ADMIN" badge in sidebar
3. Input API key → **Must have valid key from odds-api.com**
4. All settings appear:
   - Sport selection
   - Region selection
   - Market types (with Select All/Deselect buttons)
   - Stake amount
   - Arbitrage threshold
5. Click **"🔍 SEARCH ARBITRAGE"**

### As Free User
1. Login with your account
2. See "⭐ FREE" badge  
3. API Key shows: **"📌 Contact admin for API key access"**
4. Wait for admin to set up API
5. Once API is active, you can search

---

## Security Features

✅ **Passwords**: Hashed with SHA256 (never stored plain text)
✅ **Local Storage**: `users.json` file in workspace (private)
✅ **Session State**: Login persists during session
✅ **Admin Protection**: Only admin can change API key

---

## File Storage

User data stored in: `users.json`

```json
{
  "admin": {
    "password_hash": "4c2e...",
    "tier": "admin",
    "created": "2024-03-17"
  },
  "john_doe": {
    "password_hash": "a1b2...",
    "tier": "free",
    "created": "2024-03-17"
  }
}
```

---

## Troubleshooting

**"Invalid username or password"**
- Check spelling (case-sensitive)
- Use test account: `admin` / `chegy2024`

**"No arbitrage found" error**
- Make sure API key is valid
- Try different sports or markets
- Check region setting

**Can't see API key input**
- You're logged in as free user
- Ask admin to configure API first
- Contact admin to add premium tier

**Lost admin password**
- Edit `users.json` directly
- Or recreate by deleting `users.json` and restarting app
- Admin account auto-creates on first run

---

## Next Steps

1. ✅ Login as admin
2. ✅ Add API key (get free key from odds-api.com)
3. ✅ Create test user account
4. ✅ Verify free user sees restricted view
5. ✅ Deploy on Streamlit Cloud

---

**Color Theme**: Indigo (#6366f1) - Modern, professional look
**Built With**: Streamlit + SHA256 hashing + Local JSON storage
