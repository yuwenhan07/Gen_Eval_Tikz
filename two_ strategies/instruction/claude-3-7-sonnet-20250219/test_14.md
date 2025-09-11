# test_14.png

![test_14.png](../../../eval_dataset/images/test_14.png)

# LaTeX/TikZ 重构指导：对数坐标系稳定性直方图

## 1. 概览

图像为一个双面板对数坐标系直方图，展示了不同算法在旋转稳定性和平移稳定性上的表现。左侧显示旋转误差频率分布，右侧显示平移误差频率分布。图顶部有图例，包含6种不同算法的线型和颜色表示。

## 2. 文档骨架与依赖

```latex
\documentclass[border=5pt]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{amsmath}
\usepackage{xcolor}

% 需要的TikZ库
\usetikzlibrary{patterns}
```

## 3. 版面与画布设置

- 图形总宽度：约10cm
- 图形高度：约7cm
- 坐标系范围：x轴为对数坐标 10^-18 到 10^-6，y轴为线性坐标 0 到 1.5×10^4
- 建议使用 `groupplot` 环境以保持两个子图的一致性

## 4. 字体与配色

- 字体：默认的 Computer Modern
- 颜色方案：
  - 绿色 (P2LI our): RGB(0,180,0) 或 `green!80!black`
  - 红色 (P2LI 3Q3): RGB(220,0,0) 或 `red!80!black`
  - 红色虚线 (P2LI Ram.+SVD): RGB(220,0,0) 或 `red!80!black`
  - 橙色虚线 (P2LI Ram.+LU): RGB(255,140,0) 或 `orange!80!black`
  - 青色 (P1L2 our): RGB(0,180,220) 或 `cyan!80!blue`
  - 黑色虚线 (P1L2 3Q3): RGB(0,0,0)

## 5. 结构与组件样式

- 线型：
  - 实线：P2LI our, P2LI 3Q3, P1L2 our
  - 虚线：P2LI Ram.+SVD, P2LI Ram.+LU, P1L2 3Q3
- 坐标轴：
  - x轴为对数坐标，标签为 "log₁₀ of rotation error" 和 "log₁₀ of translation error"
  - y轴为线性坐标，标签为 "Frequency"
  - 网格线为灰色，背景为白色
  - 标题分别为 "Rotation stability" 和 "Translation stability"，上方标注 "×10⁴"

## 6. 数学/表格/图形细节

- 直方图数据需要从原图估算
- 使用 `hist` 或 `addplot` 命令绘制直方图
- y轴刻度需要缩放处理，显示为 0, 0.5, 1, 1.5，实际值为 0, 5000, 10000, 15000

## 7. 自定义宏与命令

```latex
% 定义颜色
\definecolor{p2liour}{RGB}{0,180,0}
\definecolor{p2li3q3}{RGB}{220,0,0}
\definecolor{p2liramsvd}{RGB}{220,0,0}
\definecolor{p2liramlu}{RGB}{255,140,0}
\definecolor{p1l2our}{RGB}{0,180,220}
\definecolor{p1l23q3}{RGB}{0,0,0}

% 定义线型样式
\pgfplotsset{
  p2liour/.style={p2liour, thick, solid},
  p2li3q3/.style={p2li3q3, thick, solid},
  p2liramsvd/.style={p2liramsvd, thick, densely dashed},
  p2liramlu/.style={p2liramlu, thick, densely dashed},
  p1l2our/.style={p1l2our, thick, solid},
  p1l23q3/.style={p1l23q3, thick, densely dashed},
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[border=5pt]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{amsmath}
\pgfplotsset{compat=1.18}

% 定义颜色
\definecolor{p2liour}{RGB}{0,180,0}
\definecolor{p2li3q3}{RGB}{220,0,0}
\definecolor{p2liramsvd}{RGB}{220,0,0}
\definecolor{p2liramlu}{RGB}{255,140,0}
\definecolor{p1l2our}{RGB}{0,180,220}
\definecolor{p1l23q3}{RGB}{0,0,0}

\begin{document}
\begin{tikzpicture}

% 图例
\begin{axis}[
  at={(0,0.95\textwidth)},
  anchor=north west,
  width=0.95\textwidth,
  height=0.2\textwidth,
  hide axis,
  xmin=0, xmax=1,
  ymin=0, ymax=1,
  legend style={
    draw=black,
    fill=white,
    legend columns=2,
    legend cell align=left,
    font=\footnotesize
  },
  legend entries={P2LI our, P2LI 3Q3, {P2LI \textit{Ram.}+SVD}, {P2LI \textit{Ram.}+LU}, P1L2 our, P1L2 3Q3},
]
\addplot[p2liour, thick] coordinates {(0,0) (0.2,0)};
\addplot[p2li3q3, thick] coordinates {(0,0) (0.2,0)};
\addplot[p2liramsvd, thick, densely dashed] coordinates {(0,0) (0.2,0)};
\addplot[p2liramlu, thick, densely dashed] coordinates {(0,0) (0.2,0)};
\addplot[p1l2our, thick] coordinates {(0,0) (0.2,0)};
\addplot[p1l23q3, thick, densely dashed] coordinates {(0,0) (0.2,0)};
\end{axis}

% 旋转稳定性图
\begin{axis}[
  at={(0,0.7\textwidth)},
  anchor=north west,
  width=0.47\textwidth,
  height=0.65\textwidth,
  xlabel={$\log_{10}$ of rotation error},
  ylabel={Frequency},
  title={Rotation stability},
  title style={at={(0.5,1.02)}, anchor=south},
  xmode=log,
  ymin=0, ymax=15000,
  ytick={0,5000,10000,15000},
  yticklabels={0,0.5,1,1.5},
  after title={$\times 10^4$},
  grid=both,
  grid style={line width=0.1pt, draw=gray!10},
  minor grid style={line width=0.05pt, draw=gray!5},
  xmin
