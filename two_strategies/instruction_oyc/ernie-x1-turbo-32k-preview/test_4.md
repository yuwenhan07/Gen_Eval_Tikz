# test_4.png

![test_4.png](../../../eval_dataset/images/test_4.png)

```markdown
# LaTeX/TikZ Reconstruction Guide

## 1. Overview
The image depicts a technical flowchart illustrating a **computational process** with four primary components: input/output nodes, processing blocks, decision diamonds, and connecting arrows. The diagram uses color-coded elements (blue/red/green) with sans-serif labels and mathematical symbols. Key components include rounded rectangles for processes, diamonds for decisions, parallelograms for I/O, and directional arrows with text annotations.

## 2. Document Skeleton & Dependencies
```latex
\documentclass[10pt]{article}
\usepackage{tikz}
\usepackage{xcolor}
\usepackage{amssymb}
\usepackage{mathrsfs}
\usepackage{geometry}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning}
```

## 3. Layout & Canvas Settings
- **Canvas Dimensions**: 12cm × 8cm
- **Scaling**: `scale=1.0` with `transform shape`
- **Global Styles**:
  ```latex
  \tikzset{
    base/.style={draw, align=center, minimum height=1cm},
    process/.style={base, rectangle, rounded corners=0.3cm, fill=blue!20},
    io/.style={base, trapezium, trapezium left angle=70, trapezium right angle=110, fill=green!20},
    decision/.style={base, diamond, aspect=1.5, fill=red!20},
    arrow/.style={-Stealth, thick, shorten >=2pt, shorten <=2pt}
  }
  ```

## 4. Fonts & Colors
**Colors**:
- Process: `\colorlet{process}{blue!30}`
- Decision: `\colorlet{decision}{red!30}`
- I/O: `\colorlet{io}{green!30}`
- Text: Black with `\sffamily`

**Fonts**:
- Title: `\Large\sffamily\bfseries`
- Labels: `\sffamily`
- Math: `$\chi$`, `$\beta$` in standard math mode

## 5. Structure & Component Styles
- **Rounded Rectangles** (Process): 3cm × 1cm, border=0.6pt
- **Diamonds** (Decision): 2cm diagonal, aspect=1.5
- **Parallelograms** (I/O): 3cm base width, 60° angles
- **Arrows**: 0.6pt thick with Stealth tip
- **Opacity**: 20% fill for all shapes

## 6. Math/Table/Graphic Details
- Greek Letters: `$\chi$`, `$\beta$`, `$\gamma$`
- Symbols: `$\blacksquare$`, `$\checkmark$`
- Equations: Use `align` environment inside nodes
- Special: Decision diamond contains `$\chi \geq 0$`

## 7. Custom Macros & Commands
```latex
\tikzset{
  module/.style={process, minimum width=#1},
  decision/.append style={align=flush center},
  io/.append style={font=\itshape}
}
\newcommand{\proc}[3]{\node[#1] (#2) {#3};}
```

## 8. MWE (Minimum Working Example)
```latex
\documentclass[tikz]{standalone}
\usepackage{amssymb,mathrsfs}
\usetikzlibrary{shapes, arrows.meta}

\colorlet{process}{blue!30}
\colorlet{decision}{red!30}
\colorlet{io}{green!30}

\tikzset{
  base/.style={draw, align=center, minimum height=1cm},
  process/.style={base, rectangle, rounded corners=0.3cm, fill=process},
  io/.style={base, trapezium, trapezium left angle=70, trapezium right angle=110, shape border rotate=90, fill=io},
  decision/.style={base, diamond, aspect=1.5, fill=decision},
  arrow/.style={-Stealth, thick, shorten >=2pt, shorten <=2pt}
}

\begin{document}
\begin{tikzpicture}[node distance=1.5cm, scale=1, transform shape]
  % Nodes
  \node (start) at (0,0) [io] {Input\\$\chi$};
  \node (proc1) [process, right=of start] {Process $\beta$};
  \node (dec1) [decision, below=of proc1] {$\chi \geq 0$?};
  \node (end) [io, right=of proc1] {Output\\$\gamma$};
  
  % Arrows
  \draw[arrow] (start) -- (proc1);
  \draw[arrow] (proc1) -- (end);
  \draw[arrow] (proc1) -- (dec1);
  \draw[arrow] (dec1) -| node[pos=0.25, above] {No} (start);
  \draw[arrow] (dec1) -- node[right] {Yes} ++(0,-1.5) node[below] {End};
\end{tikzpicture}
\end{document}
```

## 9. Replication Checklist
- [ ] Verify all nodes use correct shapes (rect/diamond/trapezoid)
- [ ] Confirm color coding matches original (blue/red/green)
- [ ] Check arrow directions and label positions
- [ ] Ensure math symbols ($\chi$, $\beta$) appear correctly
- [ ] Validate node dimensions (3cm wide processes, 2cm diamonds)
- [ ] Confirm text uses sans-serif font

## 10. Risks & Alternatives
- **Color Matching**: Use RGB values (`\definecolor`) if CMYK is required
- **Font Substitution**: Replace `\sffamily` with `\ttfamily` if monospace needed
- **Arrow Precision**: Adjust `shorten` parameters for exact tip positioning
- **Scaling Issues**: Use `standalone` class to avoid margin problems
- **Alternative Shapes**: Replace trapezium with `rectangle` + rotation for I/O
- **Compatibility**: Test with PDFLaTeX/LuaLaTeX for font rendering consistency
```
