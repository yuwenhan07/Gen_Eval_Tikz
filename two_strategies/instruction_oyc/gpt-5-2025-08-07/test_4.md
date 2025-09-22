# test_4.png

![test_4.png](../../../eval_dataset/images/test_4.png)

1. Overview
- Theme: Decomposition of heterogeneous preferences into the sum of two observable-related preference components, each multiplied by covariates.
- Main components:
  - Three small Gaussian “bells” on horizontal axes: left = heterogeneous preferences; middle = x-related preference; right = z-related preference.
  - Equation structure: left bell = • x_ijt + right bell • z_ijt, with “=” and “+” in black.
  - Top annotation in red with a pair of downward-curved arrows indicating that mixed logit models estimate mixing distribution parameters of the components.
  - Bottom annotation in blue with a long U-shaped double-headed arrow linking the left group to the right group, emphasizing the HAVAN framework statement.

2. Document Skeleton & Dependencies
- \documentclass: standalone (compact and ideal for figures). Article also works; use standalone for a self-contained graphic.
- Required packages:
  - tikz
  - xcolor
  - amsmath, amssymb
  - lmodern (clean Computer Modern fonts)
  - if needed: geometry (not required with standalone)
- TikZ libraries:
  - arrows.meta
  - calc
  - positioning

3. Layout & Canvas Settings
- Recommended canvas: about 12 cm wide by 7–8 cm tall.
- Use a single tikzpicture with a 12 cm wide logical span; place three groups at x ≈ 0 cm, 5.2 cm, and 10.4 cm.
- Global styles:
  - Use consistent line widths: bells ≈ 0.9 pt, arrows ≈ 1.0–1.1 pt.
  - Arrowheads: Latex arrow tips for a clean look.
  - Font sizes: main labels small; annotations small/bold colored.

4. Fonts & Colors
- Fonts:
  - Default Computer Modern (via lmodern). Math labels in standard math italics.
  - Small text for axis captions and annotations.
- Colors (suggested):
  - Black for bells, axes, equation symbols, and axis labels.
  - RedDeep = RGB(200, 0, 0) for the top annotation and red arrows.
  - BlueDeep = RGB(0, 55, 200) for the bottom annotation and U-shaped arrow.

5. Structure & Component Styles
- Bells with baseline axis:
  - Shape: smooth symmetric “bell” (Bezier approximation).
  - Approx. width: 2.2 cm; height: 1.1 cm above the baseline.
  - Baseline: solid horizontal axis with a rightward arrowhead.
- Three groups:
  - Left: bell + caption “Heterogeneous preferences.”
  - Middle: bell + caption “x-related preference” and a • x_ijt to its right.
  - Right: bell + caption “z-related preference” and a • z_ijt to its right.
- Equation symbols:
  - “=” centered between left and middle groups; “+” centered between middle and right groups.
- Annotations:
  - Top red text centered above middle; two short red curved arrows pointing down toward the two component bells (middle and right).
  - Bottom blue text centered below; a long blue U-shaped double-headed arrow sweeping from left area to near the right variable.

6. Math/Table/Graphic Details
- Multiplication bullets: use either \(\bullet\) or \(\cdot\). The graphic appears closer to a filled bullet; we’ll use \(\bullet\).
- Subscripts: \(x_{ijt}\) and \(z_{ijt}\) are standard math-mode constructions.
- No special Greek letters are needed; all math is basic Latin with subscripts.

7. Custom Macros & Commands
- Provide a reusable TikZ pic to draw a bell with its axis.
- Provide styles for consistent line widths and colored annotations.

8. MWE (Minimum Working Example)
- Copy-paste the following into a file (e.g., figure.tex) and compile with pdflatex.

```latex
\documentclass[tikz,border=5pt]{standalone}

\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,positioning}

% Colors
\definecolor{RedDeep}{RGB}{200,0,0}
\definecolor{BlueDeep}{RGB}{0,55,200}

% TikZ styles
\tikzset{
  >={Latex[length=2.6mm,width=2mm]},
  bell/.style={line width=0.9pt, draw=black},
  axisline/.style={line width=0.8pt, draw=black},
  eqsym/.style={font=\normalsize},
  smalllab/.style={font=\small},
  rednote/.style={RedDeep, font=\small},
  bluenote/.style={BlueDeep, font=\small},
}

% Reusable "bell with axis" pic
\tikzset{
  pics/bellaxis/.style args={#1}{
    code={
      % #1 = width of the bell (cm)
      \def\w{#1}%
      \def\h{1.1}%
      \def\axext{1.3}% axis extension to the right
      % bell curve
      \draw[bell]
        (-\w/2,0)
        .. controls (-0.25*\w,0) and (-0.18*\w,\h) ..
        (0,\h)
        .. controls (0.18*\w,\h) and (0.25*\w,0) ..
        (\w/2,0);
      % baseline + arrow
      \draw[axisline,-{Latex[length=2.2mm]}] (-\w/2,0) -- (\w/2+\axext,0);
    }
  },
  pics/bellaxis/.default=2.2
}

\begin{document}
\begin{tikzpicture}[x=1cm,y=1cm]
  % Horizontal reference positions of the three groups
  \coordinate (L) at (0,0);
  \coordinate (M) at (5.2,0);
  \coordinate (R) at (10.4,0);

  % Bells
  \pic at (L) {bellaxis=2.2};
  \pic at (M) {bellaxis=2.2};
  \pic at (R) {bellaxis=2.2};

  % Captions under bells
  \node[smalllab, anchor=north] at ($(L)+(0,-0.05)$) {Heterogeneous preferences};
  \node[smalllab, anchor=north] at ($(M)+(0,-0.05)$) {$x$-related preference};
  \node[smalllab, anchor=north] at ($(R)+(0,-0.05)$) {$z$-related preference};

  % Equation symbols
  \node[eqsym] at ($(L)!0.5!(M)+(0,0.75)$) {$=$};
  \node[eqsym] at ($(M)!0.5!(R)+(0,0.75)$) {$+$};

  % Multiplying covariates (bullets with variables)
  \fill ($(M)+(2.0,0.52)$) circle (1.4pt);
  \node[anchor=west] at ($(M)+(2.12,0.52)$) {$x_{ijt}$};

  \fill ($(R)+(2.0,0.52)$) circle (1.4pt);
  \node[anchor=west] at ($(R)+(2.12,0.52)$) {$z_{ijt}$};

  % Top red annotation
  \node[rednote, align=center] (toptext) at ($(M)!0.5!(R)+(0,2.2)$)
    {Mixed logit models estimate \\ constituent mixing distribution parameters};

  % Red curved arrows from the text toward the two component bells
  \draw[RedDeep, line width=0.9pt, -{Latex[length=2.2mm]}]
    ($(toptext.south)+( -0.9,0.0)$) .. controls ($(M)+( -0.6,1.6)$) and ($(M)+( -0.2,1.4)$) ..
    ($(M)+( 0.0,1.15)$);
  \draw[RedDeep, line width=0.9pt, -{Latex[length=2.2mm]}]
    ($(toptext.south)+(  0.9,0.0)$) .. controls ($(R)+( 0.3,1.6)$) and ($(R)+( 0.2,1.4)$) ..
    ($(R)+( 0.0,1.15)$);

  % Bottom blue annotation (two lines)
  \node[bluenote, align=center] (bottomtext) at ($(M)!0.5!(R)+( -2.6,-2.1)$)
    {HAVAN Framework directly relates model inputs\\
     to distributional parameters of aggregate observables-related preference};

  % Long blue U-shaped double-headed arrow
  \draw[BlueDeep, line width=1.1pt, <->]
    ($(L)+(-0.3,-0.8)$)
    .. controls ($(L)+(2.6,-1.8)$) and ($(R)+(-2.2,-1.8)$) ..
    ($(R)+(1.0,0.35)$);

\end{tikzpicture}
\end{document}
```

9. Replication Checklist
- Three bells present with rightward axes; captions read:
  - “Heterogeneous preferences”
  - “x-related preference”
  - “z-related preference”
- Equation layout: left bell = (• x_ijt) + (right bell • z_ijt).
- Bullets and variables are slightly above the baseline near the ends of middle/right axes.
- Red two-line message centered above middle/right; two short red curved arrows point down toward the middle and right bells.
- Blue two-line message centered below; a long blue U-shaped double-headed arrow sweeps from below the left area toward the right area.
- Line weights and arrowheads consistent; colors: deep red for top elements, deep blue for bottom elements.

10. Risks & Alternatives
- Exact geometry: The hand-drawn bell shape and arrow curvature are approximations; adjust control points in the Bezier curves for a closer match.
- Color matching: If your document uses a different color profile, tweak RGB values (e.g., RedDeep or BlueDeep) or use xcolor mixes like red!75!black and blue!70!black.
- Fonts: If you need Times-like math, load newtxtext/newtxmath instead of lmodern; for Palatino, use mathpazo.
- Engine differences: With XeLaTeX/LuaLaTeX you can choose system fonts via fontspec; the code is pdflatex-safe.
- Scaling: To globally resize, wrap the tikzpicture in \begin{tikzpicture}[scale=...] or adjust the x/y units; ensure text size remains readable (you can also use transform shape).
