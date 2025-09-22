# test_102.png

![test_102.png](../../../eval_dataset/images/test_102.png)

Sure, here is a detailed Markdown guide for reconstructing the given image using LaTeX and TikZ:

---

### 1. Overview

The image is a line plot with multiple colored lines representing different datasets. The plot shows "Cardiovascular Risk" against "Quantiles" and includes a legend describing each line. The lines are colored in black, red, blue, orange, and green.

### 2. Document Skeleton & Dependencies

```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{amsmath}
```

### 3. Layout & Canvas Settings

- Canvas dimensions: `8cm` x `6cm`
- Legend placement: to the right of the plot
- Axis style: `axis lines=left, xlabel=Quantiles, ylabel=Cardiovascular Risk`

### 4. Fonts & Colors

- Font: Default LaTeX font for plot text
- Colors:
  - Black: `black`
  - Red: `red`
  - Blue: `blue`
  - Orange: `orange`
  - Green: `green`

### 5. Structure & Component Styles

- **Axes**: Standard Cartesian axes
- **Lines**: Solid lines with thickness around `1pt`
- **Legend**: Positioned to the right with corresponding colored line entries
- **Plot size**: Adjusted to accommodate multiple legend entries

### 6. Math/Table/Graphic Details

- No special mathematical symbols apart from text labels

### 7. Custom Macros & Commands

Define color styles for each line:

```latex
\tikzset{
    factual/.style={black},
    target/.style={red},
    mlpnet/.style={blue},
    svm/.style={orange},
    rbfnet/.style={green}
}
```

### 8. MWE (Minimum Working Example)

```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{amsmath}

\tikzset{
    factual/.style={black},
    target/.style={red},
    mlpnet/.style={blue},
    svm/.style={orange},
    rbfnet/.style={green}
}

\begin{document}

\begin{figure}
\centering
\begin{tikzpicture}
\begin{axis}[
    width=8cm,
    height=6cm,
    xlabel={Quantiles},
    ylabel={Cardiovascular Risk},
    legend style={at={(1.05,0.5)},anchor=west},
    legend cell align={left}
]

\addplot+[factual, thick] coordinates {
    (0.0, 0.0) (0.1, 0.2) (0.2, 0.3) (0.3, 0.45) 
    (0.4, 0.6) (0.5, 0.65) (0.6, 0.7) (0.7, 0.75) 
    (0.8, 0.85) (0.9, 0.9) (1.0, 1.0)
};
\addlegendentry{Factual $y'$ (Labels)}

\addplot+[target, thick] coordinates {
    (0.0, 0.05) (0.1, 0.15) (0.2, 0.25) (0.3, 0.35) 
    (0.4, 0.5) (0.5, 0.6) (0.6, 0.65) (0.7, 0.7)
    (0.8, 0.8) (0.9, 0.9) (1.0, 0.95)
};
\addlegendentry{Target $y^*$ (Labels)}

\addplot+[mlpnet, thick] coordinates {
    (0.0, 0.1) (0.1, 0.25) (0.2, 0.35) (0.3, 0.5) 
    (0.4, 0.55) (0.5, 0.6) (0.6, 0.7) (0.7, 0.8)
    (0.8, 0.85) (0.9, 0.95) (1.0, 1.0)
};
\addlegendentry{Counterfactual $y$ (MLPNet)}

\addplot+[svm, thick] coordinates {
    (0.0, 0.12) (0.1, 0.22) (0.2, 0.32) (0.3, 0.42) 
    (0.4, 0.52) (0.5, 0.6) (0.6, 0.65) (0.7, 0.72)
    (0.8, 0.82) (0.9, 0.92) (1.0, 0.98)
};
\addlegendentry{Counterfactual $y$ (SVM)}

\addplot+[rbfnet, thick] coordinates {
    (0.0, 0.2) (0.1, 0.3) (0.2, 0.4) (0.3, 0.5)
    (0.4, 0.6) (0.5, 0.65) (0.6, 0.7) (0.7, 0.75)
    (0.8, 0.85) (0.9, 0.9) (1.0, 1.0)
};
\addlegendentry{Counterfactual $y$ (RBFNet)}

\end{axis}
\end{tikzpicture}
\end{figure}

\end{document}
```

### 9. Replication Checklist

- Verify axes labels: "Quantiles" and "Cardiovascular Risk"
- Check line colors match the description
- Ensure legend is correctly positioned and labeled

### 10. Risks & Alternatives

- **Color Matching**: Ensure RGB values or color names match intended shades.
- **Font Availability**: If default fonts do not match, use `\usepackage{helvet}` or similar for Helvetica.
- **Alignment**: If legend overlaps, adjust `legend style` options.

--- 

This guide provides a framework for replicating the provided graph image using LaTeX and TikZ.
