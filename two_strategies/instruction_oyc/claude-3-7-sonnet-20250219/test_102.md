# test_102.png

![test_102.png](../../../eval_dataset/images/test_102.png)

# 1. Overview
The image shows a quantile plot with multiple lines representing different models: Factual, Target, and three Counterfactual approaches (MLPNet, SVM, RBFNet). The x-axis shows Quantiles (0-1) and the y-axis shows Cumulative Risk (0-1). The lines have different colors and follow different trajectories, with notable changes around the 0.6-0.8 quantile range.

# 2. Document Skeleton & Dependencies
```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{xcolor}
\usepackage{amsmath}
\usepackage{amssymb}
```

# 3. Layout & Canvas Settings
```latex
\begin{tikzpicture}
\begin{axis}[
    width=10cm,
    height=7cm,
    xlabel={Quantiles},
    ylabel={Cumulative Risk},
    xmin=0, xmax=1,
    ymin=0, ymax=1,
    legend style={at={(1.05,0.5)}, anchor=west},
    grid=none,
    axis lines=left,
]
```

# 4. Fonts & Colors
```latex
% Define colors
\definecolor{factual}{RGB}{0,0,0}        % Black
\definecolor{target}{RGB}{0,0,128}       % Dark blue
\definecolor{mlpnet}{RGB}{128,0,128}     % Purple
\definecolor{svm}{RGB}{0,128,0}          % Green
\definecolor{rbfnet}{RGB}{0,192,0}       % Light green
\definecolor{redline}{RGB}{255,0,0}      % Red (vertical line)
```

# 5. Structure & Component Styles
- Main plot area with axes and tick marks
- Five line plots with different colors
- One vertical red line at approximately x=0.6
- Legend with five entries positioned to the right of the plot

# 6. Math/Table/Graphic Details
- Superscript notation "a*" in the legend for "Target a*"
- Greek letter "ρ" (rho) in the legend for the counterfactual models
- No special mathematical symbols beyond standard notation

# 7. Custom Macros & Commands
```latex
\pgfplotsset{
    every axis plot/.append style={line width=1pt},
    every axis/.append style={
        label style={font=\small},
        tick label style={font=\small}
    }
}
```

# 8. MWE (Minimum Working Example)
```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{document}

\begin{tikzpicture}
\begin{axis}[
    width=10cm,
    height=7cm,
    xlabel={Quantiles},
    ylabel={Cumulative Risk},
    xmin=0, xmax=1,
    ymin=0, ymax=1,
    legend style={at={(1.05,0.5)}, anchor=west},
    grid=none,
    axis lines=left,
]

% Vertical red line
\draw[red, dashed, thick] (axis cs:0.6,0) -- (axis cs:0.6,1);

% Factual line (black)
\addplot[color=black, mark=none] coordinates {
    (0,0.05) (0.1,0.08) (0.2,0.12) (0.3,0.15) (0.4,0.18) 
    (0.5,0.22) (0.6,0.25) (0.7,0.3) (0.8,0.4) (0.9,0.55) (1,0.85)
};

% Target line (dark blue)
\addplot[color=blue!80!black, mark=none] coordinates {
    (0,0.02) (0.1,0.03) (0.2,0.05) (0.3,0.07) (0.4,0.09) 
    (0.5,0.12) (0.6,0.15) (0.7,0.25) (0.8,0.4) (0.9,0.65) (1,0.9)
};

% Counterfactual MLPNet (purple)
\addplot[color=purple, mark=none] coordinates {
    (0,0.03) (0.1,0.05) (0.2,0.08) (0.3,0.1) (0.4,0.13) 
    (0.5,0.15) (0.6,0.2) (0.7,0.35) (0.8,0.5) (0.9,0.7) (1,0.88)
};

% Counterfactual SVM (green)
\addplot[color=green!60!black, mark=none] coordinates {
    (0,0.04) (0.1,0.07) (0.2,0.1) (0.3,0.13) (0.4,0.16) 
    (0.5,0.2) (0.6,0.28) (0.7,0.45) (0.8,0.65) (0.9,0.8) (1,0.92)
};

% Counterfactual RBFNet (light green)
\addplot[color=green!80!black, mark=none] coordinates {
    (0,0.03) (0.1,0.06) (0.2,0.09) (0.3,0.12) (0.4,0.15) 
    (0.5,0.19) (0.6,0.25) (0.7,0.5) (0.8,0.7) (0.9,0.82) (1,0.93)
};

\legend{Factual $\rho$ (Labels), Target $a^*$ (Labels), Counterfactual $\rho$ (MLPNet), Counterfactual $\rho$ (SVM), Counterfactual $\rho$ (RBFNet)};

\end{axis}
\end{tikzpicture}

\end{document}
```

# 9. Replication Checklist
- [ ] Five distinct colored lines are present
- [ ] Vertical red dashed line appears at x=0.6
- [ ] Legend shows all five entries with correct symbols
- [ ] Axes labeled "Quantiles" (x) and "Cumulative Risk" (y)
- [ ] Plot ranges from 0 to 1 on both axes
- [ ] Legend positioned to the right of the plot

# 10. Risks & Alternatives
- Exact curve shapes may require fine-tuning of coordinates
- Font sizes might need adjustment based on document context
- Consider using `\pgfplotstableread` for data if available in tabular format
- For more precise color matching, use a color picker tool on the original image
- Consider using `groupplots` from `pgfplots` if this is part of a larger figure set
