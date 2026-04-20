# OrganicFlow — Design System & Identity

> Read this file at the start of any new session before touching HTML/CSS.
> It encodes every visual decision made so far. Follow it exactly.

---

## 1. Design Philosophy

The visual identity mirrors the product's core idea: **intelligence that emerges, not optimises.**

- **No decoration for its own sake.** Every visual element carries meaning.
- **Whitespace is architecture.** Empty space is not waste — it is the equivalent of a cell's resting state.
- **Structure through contrast, not borders.** Depth is created by background colour shifts, not by drawing boxes.
- **Typography does the heavy lifting.** When in doubt, the answer is scale and weight, not colour or ornament.
- **The pitch deck is the reference bar.** Every page should feel like it belongs to the same universe as slides 1–12.

---

## 2. Colour Tokens

All colours are from a single Material-You green palette. Never introduce new colours.

### Surfaces (light → dark)
| Token | Hex | Usage |
|---|---|---|
| `surface-lowest` | `#ffffff` | Absolute white, rarely used |
| `surface` | `#fcf9f0` | Primary page background, content body |
| `surface-low` | `#f6f3ea` | Sidebar, cards, code collapse buttons |
| `surface-container` | `#f1eee5` | Mid-level containers |
| `surface-high` | `#ebe8df` | Table headers, highlight boxes |
| `surface-highest` | `#e5e2da` | Strongest surface, used sparingly |
| `surface-dim` | `#dddad1` | Disabled / muted areas |

### Brand greens
| Token | Hex | Usage |
|---|---|---|
| `primary` | `#173318` | Headings, active states, borders, dark cards |
| `secondary` | `#456647` | Labels, tags, section markers, links |
| `tertiary` | `#1b321f` | Italic emphasis in dark contexts |
| `primary-container` | `#2d4a2d` | Dark card secondary |
| `secondary-container` | `#c4e9c2` | Light accent backgrounds |
| `primary-fixed` | `#c9ecc4` | Text on dark green backgrounds |
| `muted-green` | `rgba(174,207,169,0.75)` | Body text on `primary` dark background |

### Text
| Token | Hex | Usage |
|---|---|---|
| `on-surface` | `#1c1c17` | Strongest body text, metric names |
| `on-surface-variant` | `#434841` | Default body text |
| `outline` | `#737970` | Muted text, subtitles, notes |
| `outline-variant` | `#c3c8be` | Disabled, placeholder |

### Semantic
| Token | Hex | Usage |
|---|---|---|
| `error` | `#ba1a1a` | FAIL verdicts, error states |
| `code-bg` | `#1c1c17` | Code block background |
| `code-text` | `#c7ecc5` | Code text on dark background |

### Borders
Always use `rgba`, never solid flat colours.
- **Standard:** `rgba(195,200,190,0.3)` — dividers, table rows
- **Slightly stronger:** `rgba(195,200,190,0.35)` — section borders
- **Active/accent:** `2–3px solid #173318` — left-border claims, active indicators

---

## 3. Typography

Three families. Each has a role. Never swap them.

| Family | Variable | Role |
|---|---|---|
| Newsreader | `font-headline` | All display headings, titles, blockquotes, numbers, italic emphasis |
| Inter | `font-body` | All body text, UI labels, problem/setup text |
| Space Grotesk | `font-label` | All uppercase labels, tags, code buttons, tab items, metadata |

### Type Scale

| Element | Size | Family | Weight | Notes |
|---|---|---|---|---|
| Page title (`wp-title`) | `3.2rem` | Newsreader | 400 | `letter-spacing: -0.025em`, `line-height: 1.1` |
| Section title (`wp-section-title`) | `2rem` | Newsreader | 400 | italic, `line-height: 1.15` |
| Highlight title (`wp-highlight-title`) | `1.6rem` | Newsreader | 400 | `line-height: 1.2` |
| Abstract title | `1.25rem` | Newsreader | 400 | `line-height: 1.2` |
| Concept/bench-cat title | `1.2–1.3rem` | Newsreader | 400 | `line-height: 1.2` |
| Stat value | `2.2rem` | Newsreader | 400 | `letter-spacing: -0.02em` |
| Blockquote | `1.2rem` | Newsreader | 400 | italic |
| Vision text | `1.15rem` | Newsreader | 400 | italic, on dark bg |
| Subtitle | `1.05rem` | Inter | 400 | `line-height: 1.75`, muted |
| Body / prose | `0.92rem` | Inter | 400 | `line-height: 1.8` |
| Problem/setup body | `0.86–0.9rem` | Inter | 400 | `line-height: 1.75` |
| Section label | `0.58rem` | Space Grotesk | 400 | `letter-spacing: 0.35em`, uppercase, `color: #456647` |
| Tags / eyebrow | `0.58rem` | Space Grotesk | 400 | `letter-spacing: 0.22em`, uppercase |
| Tab items | `0.65rem` | Space Grotesk | 400 | `letter-spacing: 0.15em`, uppercase |
| Sidebar items | `0.8rem` | Space Grotesk | 400 | `letter-spacing: 0.05em` |
| Table headers | `0.58–0.62rem` | Space Grotesk | 600 | uppercase |
| Inline code / collapse btn | `0.68–0.78rem` | Space Grotesk | 400 | |

### Italic emphasis rule
When a headline contains a secondary clause or an emotional word, wrap it in `<em>`. Color: `#456647` on light, `#c9ecc4` on dark.
Example: `Spontaneous Self-Organisation<br><em>From Chaos to Structure</em>`

---

## 4. Spacing System

Based on `0.25rem` (4px) increments. Key values:

| Use | Value |
|---|---|
| Tight gap (tags, inline) | `0.5rem` |
| Component padding (small) | `1.25rem` |
| Component padding (standard) | `1.75–2rem` |
| Component padding (generous) | `2.5rem` |
| Section divider margin | `3rem` |
| Header margin-bottom | `3.5rem` |
| Content body padding (sides) | `6rem` |
| Content body padding (top) | `4rem` |
| Max content width | `1000px` (centered, `margin: 0 auto`) |
| Prose max-width | `680px` |
| Subtitle max-width | `580px` |

---

## 5. Component Patterns

### wp-header
```
eyebrow tags → 1.75rem gap below
wp-title (3.2rem Newsreader) → 1.25rem gap
wp-subtitle (1.05rem Inter, muted) → max-width 580px
header margin-bottom: 3.5rem
```

### wp-divider
`1px`, `rgba(195,200,190,0.35)`, `margin: 3rem 0`

### wp-section-label
`0.58rem Space Grotesk`, `letter-spacing: 0.35em`, `color: #456647`, `margin-bottom: 0.75rem`
Always appears above a section title or a component.

### Dark card (abstract highlight, vision box)
- Background: `#173318`
- Padding: `2–2.5rem`
- Label: `rgba(174,207,169,0.45)`
- Title: `#c9ecc4`
- Body: `rgba(174,207,169,0.75)`
- Strong: `#c9ecc4`
This is the "wow" card. Use it once per page, maximum twice.

### bench-claim
```
border-left: 3px solid #173318
background: #f6f3ea
padding: 2rem 2.5rem
label: 0.58rem Space Grotesk, letter-spacing: 0.3em, color: #456647
text: 1rem Inter, line-height: 1.8
```
The claim box is the single most important element on a bench page.
It must be the first thing that draws the eye.

### Results table (bench)
```
Header bg: #ebe8df, padding: 0.85rem 1.5rem
Row padding: 1rem 1.5rem
Metric name: 0.88rem Inter, weight 600
Values: 0.88rem Space Grotesk
PASS verdict: border 1px rgba(23,51,24,0.35), bg rgba(23,51,24,0.06), padding 0.3em 0.8em
FAIL verdict: border 1px rgba(186,26,26,0.35), color #ba1a1a, padding 0.3em 0.8em
```

### Numbered setup/problem grid
```
Number: Newsreader 2.2–2.4rem, color rgba(23,51,24,0.09–0.12) — decorative, not readable
Title: Inter 0.9–0.92rem, weight 700, color #173318
Body: Inter 0.86rem, line-height 1.75
Border between rows: 1px rgba(195,200,190,0.2)
```

### Q&A list
```
Q row: bg #f6f3ea, padding 1.25rem 1.75rem
A row: bg #fcf9f0, padding 1.25rem 1.75rem
Icon: 1.4rem square, Q=dark (#173318 bg), A=light (rgba(23,51,24,0.15) bg)
Text: 0.85rem Inter
```

### Code collapse
```
Button: bg #f6f3ea, hover #ebe8df, padding 0.85rem 1.25rem
Lang tag: rgba(23,51,24,0.1) bg, #173318 text
Code block: bg #1c1c17, text #c7ecc5, padding 1.5rem 2rem
Font: Space Grotesk 0.78rem, line-height 1.75
```

### Stats row (highlight box)
```
Value: 2.2rem Newsreader, color #173318, letter-spacing -0.02em
Label: 0.58rem Space Grotesk, color #737970, letter-spacing 0.18em
Gap between stats: 2.5rem
```

---

## 6. Layout Shell

```
app-shell: CSS Grid
  rows: 56px (top-nav) | 1fr (content)
  cols: 220px (sidebar) | 1fr (main)

top-nav: full-width, bg rgba(252,249,240,0.92), backdrop-blur 12px
sidebar: bg #f6f3ea, border-right rgba(195,200,190,0.3)
tab-bar: bg #f6f3ea, border-bottom rgba(195,200,190,0.3), overflow-x scroll
content-body: padding 4rem 6rem 5rem, overflow-y scroll
content-inner: max-width 1000px, margin 0 auto
```

### Scrollbars
```
width/height: 5–6px
thumb: rgba(69,102,71,0.45), border-radius 3px
thumb hover: rgba(23,51,24,0.65)
track: rgba(195,200,190,0.15)
```

### Sidebar decoration (SVG node graph)
- Opacity: `0.45`
- Shows organic topology — more nodes = better
- Varied node sizes (r: 2.5–6.5), varied edge opacity (0.45–0.6)
- Cross-links as dashed lines (`stroke-dasharray: 4 4`, opacity 0.25–0.3)
- Color: always `#173318`

---

## 7. Page Structure per Bench

Every bench page follows this exact sequence:

```
1. wp-eyebrow (tags: product name, bench number, PASS/FAIL)
2. wp-title (main claim as headline, em for italic sub-clause)
3. wp-subtitle (one sentence: what it proves)
4. wp-divider
5. bench-claim (THE CLAIM — bordered box, most important)
6. wp-divider
7. wp-section "The Problem with Classical Approaches" + wp-prose
8. wp-divider
9. wp-section "Experiment Setup" + bench-setup-grid (numbered 01/02/03)
10. wp-divider
11. wp-section "Results — N Epochs" + bench-results-table + bench-result-note
12. wp-divider
13. wp-section "Technical Due Diligence" + bench-qa-list (Q/A pairs)
14. wp-divider
15. wp-section "Raw Data & Source Code" + bench-collapse (Python + JSON)
```

---

## 8. What to Never Do

- **No border-radius** beyond `2px` (design uses sharp corners by default)
- **No shadows** — depth through background colour only
- **No new colours** outside the token set
- **No decorative borders** — borders only as left-accent (2–3px) or structural dividers (1px)
- **No centered text** — all text left-aligned
- **No button-style CTA components** in documentation pages
- **No font sizes above 3.2rem** on a single page (one title dominates)
- **No more than one dark card per page**
- **Never use Space Grotesk for body text**
- **Never use Inter for display headings**

---

## 9. The Pitch Deck Reference

The 12-slide deck sets the aspirational bar. Key lessons:

| Slide | Lesson |
|---|---|
| 1 (Cover) | One large serif headline + one inline SVG is enough. Negative space does the rest. |
| 2 (Problem) | 4-column grid with short headers. No fluff. Each cell = one idea. |
| 3 (Solution) | Split layout: diagram left, bullet points right. Labels in Space Grotesk caps. |
| 4 (Proof) | Large serif numbers (`O(N)`, `99%`, `0`) carry the whole slide. Let numbers speak. |
| 5 (GTM) | Three phases, dark card = moonshot. |
| 8 (Vision) | Full dark background. One serif statement. Maximum contrast moment. |
| 12 (Close) | Full dark, massive italic serif, node graph background. Emotional ending. |

**The rule:** Every page should have one moment that matches the emotional weight of slide 12.
In the whitepaper, that is the `wp-vision-box`. In benches, it is the `bench-claim`.

---

## 10. Files Reference

| File | Role |
|---|---|
| `dashboard.html` | Shell layout, all shared dashboard CSS, scrollbars, nav |
| `pages/shared.css` | Base wp-article styles shared across all pages |
| `pages/organicflow_whitepaper.html` | Full whitepaper, also source of all wp-* component styles |
| `pages/organicflow_bench1.html` | Bench template — copy structure for benches 2–14 |
| `flow_testing/results/bench{N}.json` | Authoritative results for each bench — always use these exact numbers |
| `flow_testing/bench{N}_*.py` | Authoritative source code — copy verbatim into collapse sections |
