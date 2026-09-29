# 🎨 UI/UX Design System Specification

## 1. Aesthetic Philosophy: Vintage Comic Paper & Ben-Day Halftone Dot
The visual identity of ComicCraft is deliberately crafted to evoke the tactile, nostalgic sensation of reading a classic Silver/Bronze-age comic book printed on warm pulp paper. Rather than relying on generic modern flat or dark-mode interfaces, ComicCraft features an authentic comic book design system implemented in `static/css/comic.css`.

---

## 2. Design Tokens & Color Palette

```
┌────────────────────────────────────────────────────────┐
│                   COMIC COLOR TOKENS                   │
├────────────────────┬───────────┬───────────────────────┤
│ Token Name         │ Hex Value │ Semantic Role         │
├────────────────────┼───────────┼───────────────────────┤
│ --comic-bg         │ #faf6ea   │ Aged parchment canvas │
│ --comic-paper      │ #fffef9   │ Pure paper card base  │
│ --comic-ink        │ #18181b   │ Heavy black ink lines │
│ --comic-yellow     │ #ffe600   │ Primary comic yellow  │
│ --comic-red        │ #ff2a44   │ Action buttons & tags │
│ --comic-blue       │ #00a8ff   │ Accent links & badges │
│ --comic-green      │ #05c46b   │ Success indicators    │
│ --comic-purple     │ #8854d0   │ Special issue badges  │
└────────────────────┴───────────┴───────────────────────┘
```

### Halftone Dot Matrix Pattern
The background uses a dual radial gradient simulating the 4-color CMYK offset Ben-Day printing process:
```css
background-image: 
    radial-gradient(circle, rgba(24, 24, 27, 0.08) 1.5px, transparent 1.5px),
    radial-gradient(circle, rgba(255, 230, 0, 0.15) 1.5px, transparent 1.5px);
background-size: 20px 20px, 40px 40px;
```

---

## 3. Typography Hierarchy

| Style Role | Font Family | Fallback | Characteristics |
| :--- | :--- | :--- | :--- |
| **Action Titles & SFX** | `'Bangers'` | cursive, sans-serif | High impact, all-caps, energetic condensed letterforms |
| **Story & Narration** | `'Comic Neue'` | cursive, sans-serif | Highly legible, casual handwriting feel, balanced spacing |
| **Notes & Signatures** | `'Permanent Marker'`| cursive, sans-serif | Authentic felt-tip ink pen look |
| **System Labels & UI** | `'Outfit'` | sans-serif | Modern, crisp geometric sans for clean form labels |

---

## 4. Tactile Comic Component System

### 1. Comic Action Shadows & Ink Borders
- Heavy black ink lines: `3.5px solid #18181b`.
- Offset pop-art shadows: `6px 6px 0px #18181b`.
- Active button press effect: `transform: translate(2px, 2px); box-shadow: 2px 2px 0px #18181b;`.

### 2. Action Starburst Callouts
- Starburst badges with comic sound effects (`POW!`, `BAM!`, `WHAM!`) tilted at `-5deg` to `8deg` angles.
- Yellow and red speech bubbles with triangular SVG tail pointers.

### 3. Comics Code Authority Stamp
- Vintage regulatory stamp in the navigation bar (`★ CODE APPROVED ★`), paying homage to classic American comic book history.

### 4. Interactive Loading Flipbook Modal
- An interactive overlay that appears on form submission.
- Displays an animated rotating comic starburst, progress bar, and cycling comic status messages:
  - *"Calling the Inker..."*
  - *"Brainstorming Comic Outline with Gemini Flash..."*
  - *"Drafting Dialogue & Onomatopoeia with Gemini Pro..."*
  - *"Inking Comic Panels with Halftone Diffuser..."*
  - *"Stitching Pages into Printable PDF..."*

---

## 5. Responsive Layout Structure
- **Desktop (>= 1024px)**: Generous 2-column or centered card layouts with 860px max-width container, prominent action buttons, and side-by-side preview panels.
- **Tablet (768px - 1023px)**: Single column flow, fluid inputs, stacked navigation controls.
- **Mobile (< 768px)**: Optimized touch targets (minimum 48px height), reduced margins, full-width inputs, and sticky download buttons.
