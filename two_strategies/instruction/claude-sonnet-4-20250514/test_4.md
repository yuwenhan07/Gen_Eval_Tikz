# test_4.png

![test_4.png](../../../eval_dataset/images/test_4.png)

# 科研绘图 LaTeX/TikZ 重构指导

## 1. 概览

这是一个展示混合逻辑模型（Mixed logit models）与HAVAN框架关系的概念图。图形类型为**流程示意图**，包含：
- 上半部分：三个正态分布曲线，分别表示"异质性偏好"、"x相关偏好"和"z相关偏好"
- 中间：红色弧形箭头连接，表示混合逻辑模型估计过程
- 下半部分：蓝色弧形箭头和文字说明HAVAN框架的作用
- 整体布局为垂直层次结构，体现了模型间的逻辑关系

## 2. 文档骨架与依赖

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{amsmath}
\usepackage{xcolor}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, decorations.pathreplacing}
\pgfplotsset{compat=1.18}
```

**关键依赖说明：**
- `arrows.meta`: 自定义箭头样式
- `positioning`: 节点相对定位
- `shapes.geometric`: 椭圆等几何形状
- `decorations.pathreplacing`: 弧形装饰线
- `pgfplots`: 绘制正态分布曲线

## 3. 版面与画布设置

- **图形尺寸**: 约 12cm × 8cm
- **坐标系**: 使用相对坐标，以中心为原点
- **层次间距**: 垂直间距约2.5cm，水平间距约3.5cm
- **建议参数**:
```latex
\begin{tikzpicture}[scale=1, 
    node distance=2.5cm and 3.5cm,
    every node/.style={align=center}]
```

## 4. 字体与配色

**字体设置：**
- 主标题：`\small\color{red}`
- 分布标签：`\footnotesize`
- 变量符号：`\small` 数学模式
- 框架说明：`\small\color{blue}`

**配色方案：**
- 红色文字：`red` 或 `RGB(220,20,60)`
- 蓝色文字：`blue` 或 `RGB(0,100,200)`
- 曲线颜色：`black`
- 背景：`white`

## 5. 结构与组件样式

**正态分布曲线：**
```latex
% 使用 pgfplots 绘制标准正态分布
\begin{axis}[
    width=2.5cm, height=2cm,
    axis lines=none,
    domain=-3:3,
    samples=50
]
\addplot[thick, black] {exp(-x^2/2)/sqrt(2*pi)};
\end{axis}
```

**弧形箭头：**
```latex
\draw[red, thick, ->] (start) to[bend right=30] (end);
\draw[blue, thick, ->] (start) to[bend left=30] (end);
```

**节点样式：**
```latex
\tikzset{
    dist/.style={rectangle, minimum width=2.5cm, minimum height=2cm},
    label/.style={font=\footnotesize, below}
}
```

## 6. 数学/表格/图形细节

**数学符号处理：**
- 变量符号使用 `$x_{ijt}$`, `$z_{ijt}$` 格式
- 希腊字母使用标准LaTeX命令
- 在TikZ节点中：`node {$x_{ijt}$}`

**分布曲线绘制：**
使用解析函数 `exp(-x^2/2)/sqrt(2*pi)` 绘制标准正态分布

## 7. 自定义宏与命令

```latex
% 定义常用样式
\tikzset{
    rdarrow/.style={red, thick, ->, >=Stealth},
    blarrow/.style={blue, thick, ->, >=Stealth},
    distplot/.style={black, thick, domain=-2.5:2.5, samples=40},
    redtext/.style={font=\small, color=red, align=center},
    bluetext/.style={font=\small, color=blue, align=center, text width=8cm}
}

% 正态分布绘制宏
\newcommand{\normaldist}[3]{
    \begin{scope}[shift={(#1)}]
    \begin{axis}[
        width=2.5cm, height=2cm,
        axis lines=none,
        domain=-2.5:2.5
    ]
    \addplot[distplot] {exp(-x^2/2)/sqrt(2*pi)};
    \end{axis}
    \node[label, below=0.3cm] at (0,-1) {#2};
    \node[right=0.5cm] at (1.5,0) {#3};
    \end{scope}
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{amsmath}
\usepackage{xcolor}
\usetikzlibrary{arrows.meta, positioning, decorations.pathreplacing}
\pgfplotsset{compat=1.18}

\tikzset{
    rdarrow/.style={red, thick, ->, >=Stealth},
    blarrow/.style={blue, thick, ->, >=Stealth},
    redtext/.style={font=\small, color=red, align=center},
    bluetext/.style={font=\small, color=blue, align=center, text width=8cm}
}

\begin{document}
\begin{tikzpicture}[node distance=2.5cm and 3.5cm]

% 绘制三个正态分布
\foreach \x/\label/\var in {0/Heterogeneous\\preferences/, 4/x-related\\preference/$x_{ijt}$, 8/z-related\\preference/$z_{ijt}$} {
    \begin{scope}[shift={(\x,3)}]
        \begin{axis}[
            width=2.5cm, height=2cm,
            axis lines=none,
            domain=-2.5:2.5,
            samples=40
        ]
        \addplot[thick, black] {exp(-x^2/2)/sqrt(2*pi)};
        \end{axis}
        \node[below=0.3cm, font=\footnotesize, align=center] at (0,-1) {\label};
        \ifx\var\empty\else
            \node[right=0.8cm, font=\small] at (1.3,0) {\var};
        \fi
    \end{scope}
}

% 上方红色标题和箭头
\node[redtext] at (4,5.5) {Mixed logit models estimate\\constituent mixing distribution parameters};
\draw[rdarrow] (2,4.8) to[bend right=20] (6,4.8);

% 下方蓝色文字和箭头
\node[bluetext] at (4,0) {HAVAN Framework directly relates model inputs\\to distributional parameters of aggregate observables-related preferences};
\draw[blarrow] (
