---
version: alpha
colors:
  ink: "#203450"
  muted: "#536783"
  brand: "#315cbd"
  brandHover: "#21499f"
  sky: "#eaf3ff"
  mint: "#e3f5ec"
  peach: "#fff1e5"
  paper: "#f8fbff"
  surface: "#ffffff"
  line: "#dce6f2"
  focus: "#d07716"
typography:
  display:
    fontFamily: "Outfit, Arial, sans-serif"
  body:
    fontFamily: "DM Sans, Arial, sans-serif"
rounded:
  card: "18px"
omitted:
  - section: spacing
    reason: "A small vanilla CSS project uses page and component-specific spacing rather than a generated spacing scale."
  - section: components
    reason: "Shared button, card and input styles are owned by static/css/styles.css."
---
## Overview
A friendly, usable education planner for Indian students around 10th standard. The design resembles a paper pathway guide with clear route markers, not an exam portal or a corporate dashboard. Landing pages can be expressive; workflow screens favor clarity. The colored journey stack on the landing page is the memorable signature.
## Colors
Blue signals navigation and action; mint signals selected choices and skills; peach is reserved for cautionary guidance. Dark ink and muted copy remain readable on white and pale blue. There is no dark theme in this first version.
## Typography
Outfit carries headings and large numbers. DM Sans carries text and controls. Arial is the offline fallback. Keep plain language and short labels.
## Layout
A maximum width of 1160px and two or three columns where space permits. Mobile reduces to one column with the same action order. Route stages use a vertical timeline because the order is meaningful.
## Elevation & Depth
One quiet card shadow and bordered surfaces. No heavy floating panels or glass effects.
## Shapes
Cards use 18px corners; controls use 12px. Pills communicate categories, not status.
## Components
Runtime tokens are canonical in `static/css/styles.css` under `:root`; this file mirrors their accepted values. Buttons, cards, inputs, focus states and scrollbars are shared selectors in that stylesheet. Orange focus remains visible without color alone. Native select menus are acceptable for the small local roadmap and profile controls.
## Do's and Don'ts
Do explain uncertainty and show an actionable next step. Do not use match percentages or imply official course eligibility. Do not make color the only indicator of selection. Respect reduced motion.
