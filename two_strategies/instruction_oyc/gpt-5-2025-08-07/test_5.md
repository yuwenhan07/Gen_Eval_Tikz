# test_5.png

![test_5.png](../../../eval_dataset/images/test_5.png)

1. Overview
- The image is a clean scientific plot showing test accuracy (%) versus the time (in hours) required to obtain a sparse trainable network.
- The y-axis spans roughly 55–90% with dashed horizontal grid lines.
- A horizontal black line marks the “Unpruned Accuracy”.
- Three methods are indicated with colored markers:
  - IMP: red upward triangle.
  - SynFlow: blue open circle.
  - SNIP: green filled diamond.
- A boxed legend with a white background appears inside the plot area.

2. Document Skeleton & Dependencies
- Recommended document class:
  - \documentclass[tikz,border=5pt]{standalone}  (easy to compile a single figure)
- Required packages:
  - \usepackage{tikz}
  - \usepackage{xcolor}
  - \usepackage{pgfplots}
- Optional (not strictly needed, but common):
  - \usepackage{siunitx}  (if you want unit formatting)
- pgfplots compatibility:
  - \pgfplotsset{compat=1.18}

3. Layout & Canvas Settings
- Canvas size for the axis: width ≈ 12 cm, height ≈ 5.2 cm.
- Axis ranges:
  - x ∈ [0, 7] hours with integer ticks.
  - y ∈ [55, 90] % with 5% step ticks.
- Global styles:
  - axis lines=box to draw a full rectangular frame.
  - y-major grid only, dashed, light gray.
  - Tick labels and axis labels in small font for compactness.

4. Fonts & Colors
- Fonts:
  - Default Computer Modern is fine. Use \small for labels/ticks to match the compact style.
- Suggested color definitions:
  - Grid lines: gridgray = RGB(180,180,180)
  - IMP: impred = RGB(215,40,40)
  - SynFlow: synblue = RGB(60,110,230)
  - SNIP: snipgreen = RGB(60,190,90)
  - Axes/lines/text: black
- Marker fills:
  - SynFlow circle appears open (white fill).
  - SNIP diamond filled.
  - IMP triangle filled.

5. Structure & Component Styles
- Axis frame:
  - Boxed frame, line width ≈ 0.8 pt, black.
- Grid:
  - Horizontal major grid only, dashed, light gray (gridgray).
- Ticks:
  - Outside ticks, black, compact spacing (every 1 on x, every 5 on y).
- Legend:
  - Inside plot, white background, black border, small font, two columns, entries: IMP, SynFlow, SNIP, Unpruned Accuracy.
- Data:
  - IMP: one red triangle point, mark size ≈ 2.8 pt around (0.25, 65).
  - SynFlow: one blue open circle, mark size ≈ 3.2 pt around (0.6, 70).
  - SNIP: one green filled diamond, mark size ≈ 3.0 pt around (0.12, 57.5).
  - Unpruned Accuracy: solid black horizontal line at y = 75 across the plot.

6. Math/Table/Graphic Details
- Special characters:
  - Percent sign in labels must be escaped: \%.
- Units:
  - “hrs” directly in text. If using siunitx: \si{h}.
- Markers:
  - triangle*: filled triangle.
  - o: open circle (use fill=white).
  - diamond*: filled diamond.
- Horizontal reference line:
  - \addplot {<constant>} with samples=2 for a straight line.

7. Custom Macros & Commands
- Define colors and reusable styles to keep the code tidy:
  - \definecolor{...} for all custom colors.
  - \pgfplotsset{myaxis/.style={...}} for the axis.
  - Dedicated plot styles for each method.

8. MWE (Minimum Working Example)
- Copy, paste, and compile to reproduce a plot closely matching the original.

```latex
\documentclass[tikz,border=5pt]{standalone}

\usepackage{xcolor}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

% ---- Colors ----
\definecolor{gridgray}{RGB}{180,180,180}
\definecolor{impred}{RGB}{215,40,40}
\definecolor{synblue}{RGB}{60,110,230}
\definecolor{snipgreen}{RGB}{60,190,90}

% ---- Global styles (optional but helpful) ----
\pgfplotsset{
  myaxis/.style={
    width=12cm, height=5.2cm,
    xmin=0, xmax=7,
    ymin=55, ymax=90,
    axis lines=box,
    axis line style={black, line width=0.8pt},
    enlargelimits=false,
    xtick={0,1,2,3,4,5,6,7},
    ytick={55,60,65,70,75,80,85,90},
    ymajorgrids=true,
    xmajorgrids=false,
    grid style={gridgray, dashed},
    tick style={black},
    tick align=outside,
    label style={font=\small},
    ticklabel style={font=\small},
    legend cell align=left,
    legend columns=2,
    legend style={
      draw=black, fill=white, fill opacity=1,
      line width=0.6pt,
      font=\small,
      at={(axis cs:2.2,69)}, anchor=south west
    },
    xlabel={Time to obtain the sparse trainable network (hrs)},
    ylabel={Test accuracy (\%)}
  },
  styleIMP/.style={
    only marks, mark=triangle*, mark size=2.8pt,
    line width=0.8pt, draw=impred, fill=impred
  },
  styleSynFlow/.style={
    only marks, mark=o, mark size=3.2pt,
    line width=1.0pt, draw=synblue, fill=white
  },
  styleSNIP/.style={
    only marks, mark=diamond*, mark size=3.0pt,
    line width=0.8pt, draw=snipgreen, fill=snipgreen
  }
}

\begin{document}
\begin{tikzpicture}
  \begin{axis}[myaxis]

    % IMP (red triangle)
    \addplot+[styleIMP] coordinates {(0.25,65)};
    \addlegendentry{IMP}

    % SynFlow (blue open circle)
    \addplot+[styleSynFlow] coordinates {(0.60,70)};
    \addlegendentry{SynFlow}

    % SNIP (green filled diamond)
    \addplot+[styleSNIP] coordinates {(0.12,57.5)};
    \addlegendentry{SNIP}

    % Unpruned Accuracy (horizontal black line)
    \addplot+[domain=0:7, samples=2, black, line width=1.0pt] {75};
    \addlegendentry{Unpruned Accuracy}

  \end{axis}
\end{tikzpicture}
\end{document}
```

9. Replication Checklist
- Axis box present on all four sides.
- x-range 0–7 with integer ticks; y-range 55–90 with ticks every 5.
- Light gray dashed horizontal grid lines across the plot.
- Legend inside the plot, white background, black border, two columns, entries in the order: IMP, SynFlow, SNIP, Unpruned Accuracy.
- Markers:
  - Red filled triangle around (0.25, 65).
  - Blue open circle around (0.6, 70).
  - Green filled diamond around (0.12, 57.5).
- Solid black horizontal line at y = 75.
- Axis labels:
  - x: “Time to obtain the sparse trainable network (hrs)”.
  - y: “Test accuracy (%)”.

10. Risks & Alternatives
- Color matching: The exact hues may differ by viewer or printer. Adjust RGB values to taste (e.g., tweak synblue or snipgreen) to better match the screenshot.
- Fonts: If your main document uses a different font, the figure appearance can change. Either compile with the same preamble/fonts as your main document or wrap the figure into that document to ensure consistency.
- Legend placement: Depending on label sizes, the legend might overlap with marks. Fine-tune the at={(axis cs:...)} coordinate or use relative positioning, e.g., at={(rel axis cs:0.52,0.23)}.
- Marker sizes: Different backends or scaling can alter perceived sizes. Adjust mark size values slightly (±0.3 pt) to match your target.
- Alternative implementation: While pgfplots is ideal for this, you could also:
  - Use raw TikZ and manually place lines/markers (more work, less flexible).
  - Import data from a CSV with pgfplots’ table feature if you later add more points.
