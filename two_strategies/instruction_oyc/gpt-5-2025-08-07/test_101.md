# test_101.png

![test_101.png](../../../eval_dataset/images/test_101.png)

1. Overview
- The figure is a small schematic diagram showing an “agent” at position (Xi, Yj) looking toward a waypoint/exit Wk = (Xk, Yk).
- Core elements:
  - A reference frame centered at the scene’s origin, drawn as dash-dotted crosshairs.
  - A circular sensing/interaction region around the origin.
  - A green vertical rectangle labeled “Exit” with a small black triangular marker pointing at it.
  - A dotted sight/LOS segment from the agent to the marker, labeled Li,j,k.
  - An angle marker θk between the horizontal reference and the sight line, and a secondary label αk near the circle.
  - An icon for the agent and explanatory labels.

2. Document Skeleton & Dependencies
- \documentclass: standalone (recommended for figures) or article.
- Required packages:
  - tikz
  - xcolor
  - amsmath, amssymb
  - if using article: geometry (optional for margins)
- TikZ libraries:
  - calc
  - arrows.meta
  - positioning
  - decorations.pathreplacing (for flexible angle arcs if needed)
  - backgrounds (optional)

3. Layout & Canvas Settings
- Recommended canvas: roughly 8 cm × 8 cm.
- Use a TikZ scale so that the main circle radius is about 2.4 cm.
- Global settings:
  - line cap=round, line join=round to keep smooth endings/corners.
  - font=\small for labels; math is used for variables.
  - A modest thin line width for most strokes; slightly thicker for the circle outline.

4. Fonts & Colors
- Fonts:
  - Default Computer Modern is fine.
  - Math labels for symbols and subscripts (e.g., $\theta_k$, $L_{i,j,k}$).
- Colors (define with \definecolor or \colorlet):
  - exitGreen: a vivid green for the exit block (e.g., HTML 00B300).
  - axisGray: dark gray for crosshairs (#555555).
  - guideGray: medium gray for dotted LOS and agent outline (#7A7A7A).
  - textWhite: for the “Exit” text inside the green rectangle.
- Suggested definitions:
  - \definecolor{exitGreen}{HTML}{00B300}
  - \definecolor{axisGray}{HTML}{555555}
  - \definecolor{guideGray}{HTML}{7A7A7A}

5. Structure & Component Styles
- Crosshair axes:
  - Dash-dotted lines through the origin, length ≈ 6 cm each.
  - Style: axisGray, dash pattern=on 6pt off 3pt on 1pt off 3pt (TikZ’s dashdotted).
- Circle:
  - Center at (0,0), radius R ≈ 2.4 cm.
  - Line width ≈ 0.8pt; no fill.
- Exit:
  - Vertical rectangle near the right side of the circle, width ≈ 0.45 cm, height ≈ 1.6 cm.
  - Fill exitGreen, draw=none; text “Exit” rotated 90° in white.
- Waypoint marker:
  - Small filled black triangle pointing toward the exit, placed slightly left of the exit rectangle.
- Agent:
  - A small cartoonish glyph built from an ellipse (body) and 3 tiny circles (head/arms), drawn in guideGray with no fill.
- Dotted line of sight:
  - Densely dotted line from agent to the triangle marker.
  - Label L_{i,j,k} along the segment in slanted italic.
- Angle indicators:
  - θk: small arc from the positive x-axis to the LOS direction; label near the arc.
  - αk: text near the lower-right part of the circle (as a parameter/sector label).

6. Math/Table/Graphic Details
- Use math mode for all indexed symbols:
  - Agent label: “Agent cell i,j (Xi, Yj)” → Agent cell $i,j$ $(X_i,Y_j)$
  - LOS: $L_{i,j,k}$
  - Waypoint: $W_k\ (X_k,Y_k)$
  - Angles: $\theta_k$, $\alpha_k$
- Greek letters: \theta, \alpha.
- The triangular marker can be drawn with a tiny isosceles triangle; in TikZ use regular polygon with 3 sides or a mark.

7. Custom Macros & Commands
- Suggested TikZ styles to simplify:
  - axis/.style for crosshairs
  - sensing/.style for the circle
  - los/.style for the dotted line of sight
  - wp/.style for waypoint triangle
  - exitbox/.style for the green rectangle
  - label/.style for math labels
- A small macro \agentSymbol to place the agent icon at a given coordinate and rotation.

8. MWE (Minimum Working Example)
- Copy-paste and compile. Produces a figure closely matching the uploaded image.

```latex
\documentclass[tikz]{standalone}

\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usetikzlibrary{calc,arrows.meta,positioning,decorations.pathreplacing,backgrounds}

% Colors
\definecolor{exitGreen}{HTML}{00B300}
\definecolor{axisGray}{HTML}{555555}
\definecolor{guideGray}{HTML}{7A7A7A}

% Global TikZ styles
\tikzset{
  axis/.style = {axisGray, line width=0.6pt, dashdotted},
  sensing/.style = {black, line width=0.8pt},
  los/.style   = {guideGray, densely dotted, line width=0.7pt},
  wp/.style    = {black, fill=black},
  exitbox/.style = {fill=exitGreen, draw=none},
  label/.style = {font=\small, inner sep=1pt},
}

% A tiny agent glyph
\newcommand{\agentSymbol}[2][]{%
  % #1 optional TikZ options, #2 position
  \begin{scope}[shift={#2}, #1, guideGray]
    % body
    \draw[line width=0.7pt] (0,0) ellipse [x radius=0.35cm, y radius=0.22cm];
    % head and "arms"
    \draw[line width=0.7pt] (-0.15,0.23) circle [radius=0.07cm];
    \draw[line width=0.7pt] (0.28,0.06) circle [radius=0.06cm];
    \draw[line width=0.7pt] (-0.34,0.05) circle [radius=0.06cm];
  \end{scope}%
}

\begin{document}
\begin{tikzpicture}[line cap=round, line join=round, font=\small, scale=1]

  % Parameters
  \def\R{2.4}              % circle radius in cm
  \def\theta{20}           % angle of LOS from +x (degrees)
  \coordinate (O) at (0,0);

  % Crosshair axes
  \draw[axis] (-3.2,0) -- (3.2,0);
  \draw[axis] (0,-3.2) -- (0,3.2);

  % Sensing circle
  \draw[sensing] (O) circle[radius=\R];

  % Exit rectangle on the right side of the circle
  % Positioned slightly inside the circle
  \path let \p1 = (O) in coordinate (ExitC) at (\R-0.3,0);
  \node[exitbox, minimum width=0.45cm, minimum height=1.6cm, rotate=90] (exit) at (ExitC) {\color{white}\bfseries Exit};

  % Waypoint triangular marker pointing to the exit
  % Put a small triangle just to the left of the exit
  \coordinate (Wptr) at ($(ExitC)+(-0.45,0.15)$);
  \draw[wp] ($(Wptr)+(-0.12,0)$) -- ($(Wptr)+(0.12,0.08)$) -- ($(Wptr)+(0.12,-0.08)$) -- cycle;

  % Dotted line-of-sight from agent to the marker
  % Agent location (choose at upper-left)
  \coordinate (Agent) at (-2.3,1.35);
  \draw[los] (Agent) -- ($(Wptr)+(0,0)$);

  % Angle theta_k at the origin relative to +x axis:
  % draw a short guide ray at angle \theta (for the arc)
  \draw[guideGray] (O) -- ++(\theta:1.5);
  \draw[->, guideGray, line width=0.5pt] ($(O)+(0.9,0)$) arc [start angle=0, end angle=\theta, radius=0.9];
  \node[label] at ($(O)+(\theta/2:1.15)$) {$\theta_k$};

  % Label alpha_k near the lower-right arc of the circle (as a parameter label)
  \node[label] at ($(O)+(-15:\R-0.6)$) {$\alpha_k$};

  % Agent glyph and label
  \agentSymbol{(Agent)}
  \node[align=left, anchor=west, label] at ($(Agent)+(-0.15,0.65)$)
    {Agent cell $i,j$\\$(X_i,Y_j)$};

  % Label along the dotted LOS
  \node[label, rotate=\theta, anchor=south west, text=guideGray] at ($(Agent)!0.55!(Wptr)$) {$L_{i,j,k}$};

  % Waypoint label near exit
  \node[anchor=west, label] at ($(ExitC)+(0.55,0)$) {$W_k$\\$(X_k,Y_k)$};

\end{tikzpicture}
\end{document}
```

9. Replication Checklist
- Crosshair axes:
  - Do you see two dash-dotted lines crossing at the circle’s center?
- Circle:
  - Single clear circle centered at the crosshairs with radius similar to the figure.
- Exit:
  - Bright green vertical rectangle near the right side of the circle; “Exit” in white, rotated 90°.
  - Small black triangle pointing to the exit’s left side.
- Agent:
  - Small outline glyph in the upper-left; label “Agent cell i,j (Xi, Yj)” nearby.
- Dotted LOS:
  - Densely dotted segment from the agent to the triangle; label “L_{i,j,k}” along it.
- Angles:
  - θk arc at the origin between +x and the LOS direction.
  - αk label near the lower-right arc of the circle.
- Waypoint label:
  - “Wk (Xk, Yk)” to the right of the exit.
- Overall proportions:
  - The circle, exit, and labels match the approximate sizes in the reference.

10. Risks & Alternatives
- Exact color matching:
  - The green may look different on various displays/printers. Adjust exitGreen with another HTML hex code or xcolor mixing (e.g., green!80!black).
- Font differences:
  - If your main document uses a different font family, math spacing may shift slightly. Compile the MWE first; then integrate and adjust font sizes.
- Angle and placement:
  - If you need θk to match a specific geometry, recompute \theta and reposition the triangle Wptr (and the agent) so the dotted LOS aligns precisely.
- Overlap/occlusion:
  - If you want the circle line to be hidden behind the exit block, keep the drawing order as in the MWE (exit drawn after circle). To clip the circle precisely around the exit, use a clip path or draw the circle in two arcs that stop at the rectangle edges.
- Alternative implementations:
  - Use \pic for angle marks (tikzlibrary angles and quotes) if you prefer standardized angle annotations.
  - Replace the hand-drawn agent with a simple node shape (e.g., a filled circle) if a minimalist style is desired.
