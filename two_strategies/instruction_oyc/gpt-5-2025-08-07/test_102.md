# test_102.png

![test_102.png](../../../eval_dataset/images/test_102.png)

1. Overview
- The image is a square, boxed 2D plot (similar to a CDF-style curve set) with:
  - X-axis labeled “Quantiles” ranging from 0 to 1.
  - Y-axis labeled “Cardiovascular Risk” ranging from 0 to 1.
  - Two vertical reference lines: a black one (factual labels) and a red one (target labels).
  - Three smooth, monotone-increasing curves representing counterfactual risk predicted by different models (MLPNet, SVM, RBFNet) in blue/green tones.
  - A legend placed to the right of the plot area listing the five items.

2. Document Skeleton & Dependencies
- \documentclass: standalone (compact and ideal for single figures)
- Required packages:
  - tikz
  - pgfplots
  - xcolor (with dvipsnames for named colors)
  - amsmath, amssymb (for math in legend: y', g*)
- Recommended preamble:
  - \pgfplotsset{compat=1.18} (or your installed version)

3. Layout & Canvas Settings
- Overall figure: about 11–12 cm wide to leave space for the legend at right.
- Axis (plot box) size: roughly 6.5–7 cm wide by 6–6.5 cm high.
- Axis style:
  - axis lines=box
  - ticks at 0, 0.2, …, 1 on both axes
  - no grid lines
  - medium/thick line widths for visibility
- Legend: outside the axis on the right, vertically stacked, no frame.

4. Fonts & Colors
- Fonts:
  - Default Computer Modern is fine; boldface is not required.
  - Math in legend: use inline math for y' and g*.
- Suggested color definitions (close to the image):
  - factual (black): black
  - target (red): TargetRed = RGB(196,30,58) [deep red]
  - MLP curve (blue): RoyalBlue (dvipsnames)
  - SVM curve (green): ForestGreen (dvipsnames)
  - RBF curve (greenish): SeaGreen (dvipsnames)
- You can tweak hues later if you need a closer match.

5. Structure & Component Styles
- Axes/box:
  - axis lines=box, line width ≈ 0.8 pt, tick style=black
- Vertical reference lines (factual/target):
  - ultra thick (≈ 1.2–1.4 pt)
  - full height (from y=0 to y=1)
  - positions near x ≈ 0.53 (black) and x ≈ 0.67 (red), respectively
- Counterfactual curves:
  - three smooth, monotone-increasing curves
  - very thick (≈ 1.0–1.2 pt), smoothed
  - colors as noted above
- Legend:
  - right of axis, draw=none, font=\small, left-aligned entries

6. Math/Table/Graphic Details
- Special symbols in legend:
  - y' (prime): $y'$
  - g* (star/supremum): $g^\*$
- Axis labels are plain text.
- No special markers; only lines.

7. Custom Macros & Commands
- Define reusable styles to simplify:
  - cfcurve for all counterfactual curves
  - vline for the two vertical reference lines
  - separate styles per series color

8. MWE (Minimum Working Example)
Copy-paste and compile:

\documentclass[tikz,border=6pt]{standalone}
\usepackage{pgfplots}
\usepackage[dvipsnames]{xcolor}
\usepackage{amsmath,amssymb}
\pgfplotsset{compat=1.18}

% Colors
\definecolor{TargetRed}{RGB}{196,30,58}
\colorlet{MLPBlue}{RoyalBlue}
\colorlet{SVMGreen}{ForestGreen}
\colorlet{RBFGreen}{SeaGreen}

% Styles
\tikzset{
  cfcurve/.style={very thick, smooth, line cap=round},
  vline/.style={ultra thick, line cap=round},
  factual/.style={black},
  target/.style={TargetRed},
  mlp/.style={MLPBlue},
  svm/.style={SVMGreen},
  rbf/.style={RBFGreen},
}

\begin{document}
\begin{tikzpicture}
  \begin{axis}[
    width=7cm, height=6.2cm,
    axis lines=box,
    xmin=0, xmax=1,
    ymin=0, ymax=1,
    xtick={0,0.2,0.4,0.6,0.8,1},
    ytick={0,0.2,0.4,0.6,0.8,1},
    xlabel=Quantiles,
    ylabel={Cardiovascular Risk},
    tick style={black},
    line width=0.8pt,
    legend style={
      at={(1.30,0.5)}, anchor=west,
      draw=none, fill=none, font=\small,
      row sep=2pt, column sep=6pt
    },
    legend cell align=left,
    clip=false,
  ]

    % Vertical reference lines (positions approx.)
    \addplot[vline,factual] coordinates {(0.53,0) (0.53,1)};
    \addlegendentry{Factual $y'$ (Labels)}

    \addplot[vline,target] coordinates {(0.67,0) (0.67,1)};
    \addlegendentry{Target $g^\*$ (Labels)}

    % Counterfactual y (MLPNet) -- blue
    \addplot[cfcurve,mlp,domain=0:1,samples=350,
             restrict y to domain=0:1, unbounded coords=discard]
      { 1/(1 + exp(-8*(x-0.58))) + 0.020*sin(deg(6*x + 0.2)) };
    \addlegendentry{Counterfactual $y$ (MLPNet)}

    % Counterfactual y (SVM) -- darker green
    \addplot[cfcurve,svm,domain=0:1,samples=350,
             restrict y to domain=0:1, unbounded coords=discard]
      { 1/(1 + exp(-6.5*(x-0.55))) + 0.015*sin(deg(7*x - 0.4)) };
    \addlegendentry{Counterfactual $y$ (SVM)}

    % Counterfactual y (RBFNet) -- lighter green
    \addplot[cfcurve,rbf,domain=0:1,samples=350,
             restrict y to domain=0:1, unbounded coords=discard]
      { 1/(1 + exp(-9.5*(x-0.62))) + 0.012*sin(deg(8*x + 0.7)) };
    \addlegendentry{Counterfactual $y$ (RBFNet)}

  \end{axis}
\end{tikzpicture}
\end{document}

9. Replication Checklist
- Canvas:
  - Boxed axis, ticks at 0–1 in steps of 0.2 on both axes.
  - X label “Quantiles”; Y label “Cardiovascular Risk”.
- Legend:
  - Positioned to the right of the plot; no border; five entries in this order:
    1) black line Factual $y'$
    2) red line Target $g^\*$
    3) blue curve MLPNet
    4) green curve SVM
    5) greenish curve RBFNet
- Lines:
  - Two vertical lines, one black near x≈0.53 and one red near x≈0.67, spanning the full height.
  - Three smooth, increasing colored curves within [0,1]×[0,1].
- Overall proportions similar to the original square-like plot.

10. Risks & Alternatives
- Color matching: Named colors may not exactly match your source. Adjust with \definecolor{<name>}{RGB}{r,g,b} using sampled values if you need an exact tone.
- Curve shapes: Without the original data, smooth logistic-like curves approximate the look. If you have data, replace each \addplot expression with coordinates or \addplot table from file for exact replication.
- Font differences: If your document uses different fonts, metrics may change slightly. For consistent results, compile this figure as standalone and include the PDF.
- Legend placement: Depending on your axis width, the legend may overlap. Tweak at={(1.30,0.5)} or widen the axis (width=7.5cm) as needed.
- Export/printing: Thin lines can look weak at small sizes. Increase line widths slightly if the figure will be reduced in a paper.
