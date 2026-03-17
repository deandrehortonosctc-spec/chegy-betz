# 🎨 Design System & Color Palette

## Color Palette

### Primary Colors
| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Teal Accent** | #14b8a6 | (20, 184, 166) | Buttons, borders, highlights |
| **Deep Navy** | #0f0f1e | (15, 15, 30) | Main background |
| **Dark Gray** | #1a1a2e | (26, 26, 46) | Secondary background |
| **Light Gray** | #e5e7eb | (229, 231, 235) | Primary text |

### Semantic Colors
| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Purple** | #8b5cf6 | (139, 92, 246) | Secondary accent, ROI |
| **Green (Success)** | #10b981 | (16, 185, 129) | Profit, arbitrage found |
| **Red (Warning)** | #ef4444 | (239, 68, 68) | No arbitrage, errors |
| **Gray (Text)** | #a0a0b0 | (160, 160, 176) | Secondary text |

## Typography

### Headers
```css
font-family: 'Space Mono', monospace;
font-weight: 700;
letter-spacing: 0.5px;
```
- **Hero Title**: 3.5em, gradient text (teal → purple)
- **Section Headers**: 2em, teal color
- **Card Titles**: 1.1em, light gray

### Body Text
```css
font-family: 'Inter', sans-serif;
font-weight: 300-600;
letter-spacing: 0px;
```
- **Normal Text**: 1em, light gray
- **Labels**: 0.85em, gray, uppercase
- **Odds Display**: 2.2em, Space Mono, teal

## Component Styles

### Hero Section
```css
background: linear-gradient(135deg, rgba(20,184,166,0.1), rgba(139,92,246,0.1));
border-left: 5px solid #14b8a6;
border-radius: 12px;
padding: 40px;
box-shadow: 0 8px 32px rgba(20,184,166,0.15);
```

### Game Card
```css
background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
border: 1px solid rgba(20,184,166,0.3);
border-radius: 16px;
padding: 24px;
box-shadow: 0 10px 40px rgba(0,0,0,0.4);
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

&:hover {
    border-color: #14b8a6;
    box-shadow: 0 20px 60px rgba(20,184,166,0.2);
    transform: translateY(-4px);
}
```

### Bookmaker Card
```css
background: rgba(20,184,166,0.05);
border: 1px solid rgba(20,184,166,0.2);
border-radius: 10px;
padding: 16px;
transition: all 0.2s ease;

&:hover {
    background: rgba(20,184,166,0.1);
    border-color: #14b8a6;
}
```

### Metric Card
```css
background: linear-gradient(135deg, rgba(20,184,166,0.1), rgba(139,92,246,0.1));
border-left: 4px solid #14b8a6;
border-radius: 8px;
padding: 20px;
```

### Odds Display
```css
background: rgba(20,184,166,0.1);
border: 2px solid #14b8a6;
border-radius: 12px;
padding: 16px;

.odds-value {
    font-size: 2.2em;
    color: #14b8a6;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 1px;
}
```

### Status Badges
```css
/* Success */
.badge-success {
    background: rgba(16,185,129,0.2);
    border: 1px solid #10b981;
    color: #10b981;
    padding: 8px 16px;
    border-radius: 20px;
}

/* Empty/Error */
.badge-empty {
    background: rgba(239,68,68,0.2);
    border: 1px solid #ef4444;
    color: #ef4444;
    padding: 8px 16px;
    border-radius: 20px;
}
```

## Spacing

- **Hero Section Padding**: 40px
- **Card Padding**: 24px
- **Team Section Padding**: 20px
- **Gap Between Elements**: 12-20px
- **Margin Bottom**: 20-30px

## Border Radius

- **Hero/Cards**: 12-16px
- **Buttons/Badges**: 20px (pill-shaped)
- **Small Elements**: 8-10px

## Shadows

- **Light Shadow**: `0 4px 12px rgba(20,184,166,0.2)`
- **Medium Shadow**: `0 10px 40px rgba(0,0,0,0.4)`
- **Heavy Shadow**: `0 20px 60px rgba(20,184,166,0.2)`

## Geometric Elements

- **Fixed Circles**: 300px & 400px diameter, 2px borders, 3% opacity
- **Triangle**: 200px width × 300px height, teal color, positioned top-50% right-10%
- **Positioning**: Fixed, pointer-events: none, z-index: -1

## Responsive Breakpoints

- **Desktop**: Full 3-column layout
- **Tablet**: 2-column layout, adjusted sizing
- **Mobile**: 1-column layout, collapsed sidebar

## Animation & Transitions

```css
/* Card Hover */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
transform: translateY(-4px);

/* Text Transitions */
transition: color 0.2s ease;

/* Image Hover */
.team-image:hover {
    transform: scale(1.05);
    filter: drop-shadow(0 8px 16px rgba(20,184,166,0.4));
}
```

## Accessibility

- **Color Contrast**: All text meets WCAG AA standards
- **Font Sizing**: Minimum 0.85em for all readable text
- **Focus States**: Visible borders on interactive elements
- **Alternative Text**: Team logo images have fallback behavior

## Dark Mode Support

The entire theme is dark-mode optimized:
- No bright whites (use #e5e7eb for text)
- No pure blacks (use #0f0f1e for background)
- Gradient overlays reduce visual strain
- Semi-transparent elements avoid harsh contrasts

---

## Implementation Example

### Adding a New Game Card

```python
def display_professional_game_card(teams, best_odds, all_bookmaker_odds, arb_value, profit, profit_pct):
    away, home = teams[0], teams[1]
    
    st.markdown(f"""
    <div class="game-card">
        <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center;">
            <!-- Layout with teal-accented cards -->
            <!-- Each section: logo, name, odds-display div -->
        </div>
    </div>
    """, unsafe_allow_html=True)
```

### CSS Usage Pattern

```python
st.markdown("""
<style>
/* Use variables for consistency */
--teal: #14b8a6;
--navy: #0f0f1e;
--gray-dark: #1a1a2e;
--gray-text: #e5e7eb;
--accent: #8b5cf6;

/* Apply to components */
.component { color: var(--teal); }
</style>
""", unsafe_allow_html=True)
```

## Future Enhancements

- [ ] Dark/Light theme toggle
- [ ] Custom color scheme selection
- [ ] Font size adjustment (accessibility)
- [ ] High contrast mode
- [ ] Animation speed preferences
- [ ] Mobile-optimized tooltips
