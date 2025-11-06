# 🎨 Plexboxd Color Palette

These are the official color definitions for the Plexboxd brand assets.  
All values are locked for consistency across PNG, SVG, and web interfaces.

| Element | Color Name | HEX | RGB | Usage |
|----------|-------------|------|------|--------|
| **P** | Plex Amber | `#E5A00D` | `229, 160, 13` | Primary Plex reference tone |
| **b** | Letterboxd Orange | `#FF8000` | `255, 128, 0` | First color in the “boxd” sequence |
| **o** | Letterboxd Blue | `#00B3E6` | `0, 179, 230` | Second color in the “boxd” sequence |
| **x** | Letterboxd Green | `#00E054` | `0, 224, 84` | Third color in the “boxd” sequence |
| **d** | Letterboxd Gold | `#F5C518` | `245, 197, 24` | Final color in the “boxd” sequence |
| **Tagline** | Light Gray | `#CCCCCC` | `204, 204, 204` | Subtitle text |
| **Background (top)** | Charcoal Gray | `#141414` | `20, 20, 20` | Banner / logo gradient start |
| **Background (bottom)** | Black | `#000000` | `0, 0, 0` | Banner / logo gradient end |

---

### 🧭 Notes
- All letter fills are **flat solid colors** — no gradients or blending.  
- The **gradient** is applied *only* to the background layer.  
- Anti-aliasing should be disabled on vector edges to prevent bleed between color blocks.  
- When reproducing the logo in HTML/CSS, use:
  ```css
  background: linear-gradient(to bottom, #141414, #000000);
  font-family: 'Inter', sans-serif;
