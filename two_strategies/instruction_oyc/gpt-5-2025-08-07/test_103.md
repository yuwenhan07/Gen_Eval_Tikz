# test_103.png

![test_103.png](../../../eval_dataset/images/test_103.png)

1. Overview
- The image shows a simple game/flow diagram with three parties:
  - Left: “Leader (Supplier)” represented by a person icon.
  - Middle: “Follower (Retailer)” with another person icon.
  - Right: “Market” represented by four smaller person icons arranged 2×2.
- Between Leader and Follower there is a pair of opposite horizontal arrows:
  - Top arrow to the right labeled a.
  - Bottom arrow to the left labeled b_a.
- Between Follower and Market there are two parallel rightward arrows:
  - Top labeled p_a.
  - Bottom labeled d(p_a).
- Payoff formulas appear below the two large actors:
  - GA(a) = a b_a
  - GB(p_a, b_a) = p_a min{ d(p_a), b_a }

2. Document Skeleton & Dependencies
- \documentclass: standalone (easy border handling for figures).
- Required packages:
  - tikz
  - amsmath, amssymb (math typesetting)
  - xcolor (color definitions, even if only black is used)
- TikZ libraries:
  - arrows.meta (modern arrowheads)
  - positioning (clean relative node placement)
  - calc (coordinate arithmetic)

3. Layout & Canvas Settings
- Canvas: a wide, short figure. Recommended standalone border: 3mm.
- TikZ picture scale: 1.0.
- Global line settings:
  - line width ≈ 0.6 pt
  - line cap = round, line join = round
  - Arrowheads: Stealth with length ≈ 3.1 mm and width ≈ 2.2 mm.
- Coordinate plan:
  - Leader center at (0,0), Follower at (5,0), Market at (9.3,0).
  - Parallel arrows located around y = ±0.35.

4. Fonts & Colors
- Colors:
  - All strokes and text are black. Define:
    - \colorlet{ink}{black}
- Fonts:
  - Default LaTeX serif (Computer Modern) for labels and math.
  - Labels above actors in \normalsize; math formulas in inline math style.

5. Structure & Component Styles
- Person icon (large):
  - Head: circle of radius ≈ 0.38 cm.
  - Body: a “shirt” shape formed by a rectangle with a concave top (a downward semicircle), width ≈ 1.2 cm, height ≈ 1.2 cm. Outline only, no fill.
- Person icon (small/market):
  - Same shape scaled to ≈ 0.55, four instances in a 2×2 grid.
- Arrows:
  - Between Leader and Follower:
    - Top: rightward; label a above.
    - Bottom: leftward; label b_a below.
  - Between Follower and Market:
    - Two rightward arrows; labels p_a (top) and d(p_a) (bottom).
- Text:
  - Titles above each group.
  - Payoff formulas centered beneath the two large actors.

6. Math/Table/Graphic Details
- Subscripts and functions:
  - b_a (use b_{a}), p_a (p_{a}), d(p_a) written as d(p_{a}).
- Payoff functions:
  - G_A and G_B can be plain G or calligraphic; here we use \mathcal{G}.
  - min{…} with \min\{ … \}.
- No special symbols beyond standard math, so amsmath suffices.

7. Custom Macros & Commands
- Define a reusable TikZ pic for a person and a common arrow style:
  - pics/person for the icon.
  - >={Stealth[…]} and a local \tikzset for consistent arrows/lines.

8. MWE (Minimum Working Example)
- Copy-paste and compile with pdflatex, lualatex, or xelatex.

```latex
\documentclass[tikz,border=3mm]{standalone}

\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}

\colorlet{ink}{black}

\begin{document}
\begin{tikzpicture}[
  line cap=round, line join=round,
  draw=ink, text=ink,
  >=Stealth,
  % Reusable "person" icon as a pic
  person/.pic={
    % Tunable dimensions
    \def\R{0.38}   % head radius
    \def\W{1.20}   % body width
    \def\H{1.20}   % body height
    \def\YT{0.05}  % top y of the body (where the concave arc sits)
    % Head
    \draw[pic actions,line width=0.6pt] (0,\YT+\R) circle (\R);
    % Body with a concave top (downward semicircle)
    \draw[pic actions,line width=0.6pt]
      (-\W/2,\YT) arc (180:360:{\W/2}) -- (\W/2,-\H) -- (-\W/2,-\H) -- cycle;
  }
]

% Key positions
\coordinate (L) at (0,0);     % Leader
\coordinate (F) at (5.0,0);   % Follower
\coordinate (M) at (9.3,0);   % Market group center

% Draw the two main actors
\pic at (L) {person};
\pic at (F) {person};

% Market group: four small persons (2x2)
\begin{scope}[shift={(M)},scale=0.55]
  \pic at (0,0.30) {person};
  \pic at (1.20,0.30) {person};
  \pic at (0,-1.10) {person};
  \pic at (1.20,-1.10) {person};
\end{scope}

% Titles
\node[font=\normalsize,anchor=south]   at ($(L)+(0,1.80)$) {Leader (Supplier)};
\node[font=\normalsize,anchor=south]   at ($(F)+(0,1.80)$) {Follower (Retailer)};
\node[font=\normalsize,anchor=south]   at ($(M)+(0,1.80)$) {Market};

% Arrows between Leader and Follower (two-way)
\draw[-{Stealth[length=3.1mm,width=2.2mm]},line width=0.6pt]
  ($(L)+(1.60,0.35)$) -- node[above=2pt] {$a$} ($(F)+(-1.60,0.35)$);
\draw[{Stealth[length=3.1mm,width=2.2mm]}-,line width=0.6pt]
  ($(L)+(1.60,-0.35)$) -- node[below=2pt] {$b_{a}$} ($(F)+(-1.60,-0.35)$);

% Arrows from Follower to Market (both rightward)
\draw[-{Stealth[length=3.1mm,width=2.2mm]},line width=0.6pt]
  ($(F)+(1.60,0.35)$) -- node[above=2pt] {$p_{a}$} ($(M)+(-1.00,0.35)$);
\draw[-{Stealth[length=3.1mm,width=2.2mm]},line width=0.6pt]
  ($(F)+(1.60,-0.35)$) -- node[below=2pt] {$d(p_{a})$} ($(M)+(-1.00,-0.35)$);

% Payoff formulas
\node[anchor=north] at ($(L)+(0,-1.35)$) {$\mathcal{G}_A(a)=a\,b_{a}$};
\node[anchor=north] at ($(F)+(0,-1.35)$) {$\mathcal{G}_B(p_{a},b_{a})=p_{a}\,\min\{d(p_{a}),\,b_{a}\}$};

\end{tikzpicture}
\end{document}
```

9. Replication Checklist
- Three headings: “Leader (Supplier)”, “Follower (Retailer)”, “Market”.
- Two large person icons (left and center) and a 2×2 grid of smaller person icons (right).
- Between Leader and Follower:
  - Top arrow points right and is labeled a above the line.
  - Bottom arrow points left and is labeled b_a below the line.
- Between Follower and Market:
  - Two parallel rightward arrows labeled p_a (top) and d(p_a) (bottom).
- Payoff text under Leader: GA(a) = a b_a.
- Payoff text under Follower: GB(p_a, b_a) = p_a min{d(p_a), b_a}.
- All elements in black; thin outlines; round joins and caps.

10. Risks & Alternatives
- Exact geometry of the torso’s concave “shoulders” can vary by taste. If you want a simpler body, replace it with a rounded rectangle: use \draw[rounded corners=2pt] (-0.6,-1.2) rectangle (0.6,0.0); or swap the pic with a font symbol (e.g., FontAwesome) if available.
- Font differences may slightly change text widths and alignment. If you use Times or another font, adjust arrow lengths (the ($(…)$) coordinates) to avoid overlaps.
- Arrowhead sizes can shift the perceived spacing; tweak Stealth length/width or use {Latex} arrow tips if you prefer.
- If color matching is important (e.g., gray strokes), set \colorlet{ink}{black!80} and adjust line width accordingly.
- For engines without pic support (very old PGF), replace the pic with a \tikzset style drawing in a scope or use a small macro that draws the person at the current coordinate.
