# test_4.png

![test_4.png](../../../eval_dataset/images/test_4.png)

以下是针对该科研绘图的完整 LaTeX/TikZ 重构指导：

### 1. 概览
- **图形类型**：流程图。
- **构图布局**：包含两个正态分布曲线和文字说明，中间用箭头连接。
- **主要元素关系**：包括两个正态曲线，代表不同偏好，之间用加号连接，带有箭头及解释说明。

### 2. 文档骨架与依赖
- **文档类**：推荐使用 `standalone` 以便轻松集成到其他文档中。
- **核心宏包**：`TikZ`, `xcolor`。
- **特定功能**：需要 TikZ 的 `arrows.meta` 和 `decorations.pathreplacing` 库用于箭头和曲线装饰。

### 3. 版面与画布设置
- **尺寸**：宽度 `10cm`。
- **节点与元素的间距**：适中保持视觉清晰。
- **环境参数**：`\begin{tikzpicture}[scale=1]`，保证整体尺寸合适。

### 4. 字体与配色
- **字体**：默认字体 `\sffamily`。
- **主色**：蓝色 `#0000FF`，红色 `#FF0000`。
- **辅助色**：黑色 `#000000`。

### 5. 结构与组件样式
- **节点**：无边框，文本居中。
- **箭头**：使用 `stealth` 风格，曲线带装饰效果。
- **坐标轴**：使用自定义绘制，简单线条表示。

### 6. 数学/表格/图形细节
- **公式排版**：使用 `\( ... \)` 包裹数式，如 `\(x_{ijt}\)`。

### 7. 自定义宏与命令
- 创建箭头样式命令和色彩定义以便复用。

### 8. 最小可运行示例 (MWE)
```latex
\documentclass{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, decorations.pathreplacing}
\begin{document}

\begin{tikzpicture}[scale=1]
    % Colors
    \definecolor{myblue}{RGB}{0, 0, 255}
    \definecolor{myred}{RGB}{255, 0, 0}

    % Normal distributions
    \draw plot[smooth, tension=1] coordinates { (0,0) (0.5,1) (1,0)};
    \node at (-0.5, -0.2) {Heterogeneous preferences};

    \draw plot[smooth, tension=1] coordinates { (3,0) (3.5,1) (4,0)};
    \node at (3.5, -0.2) {\( x\text{-related preference} \)};

    \draw plot[smooth, tension=1] coordinates { (6,0) (6.5,1) (7,0)};
    \node at (6.5, -0.2) {\( z\text{-related preference} \)};

    % Equation
    \node at (1.5, 0.5) {=};
    \node at (5, 0.5) {+};

    % Arrows
    \draw[myred, thick, ->, shorten >=2pt, shorten <=4pt] (2,0.7) to[out=90,in=90] (5,0.7);
    \node[myred, above] at (3.5, 1.2) {Mixed logit models estimate};
    \node[myred, above] at (3.5, 0.9) {constituent mixing distribution parameters};

    \draw[myblue, thick, ->, decorate, decoration={zigzag}] (7,-0.5) to[out=-100,in=-80] (0.8,-1.5);
    \node[myblue, below] at (3.5, -1.8) {HAVAN Framework directly relates model inputs};
    \node[myblue, below] at (3.5, -2.1) {to distributional parameters of aggregate observables-related preference};
\end{tikzpicture}

\end{document}
```

### 9. 复刻检查清单
- 图形尺寸、坐标范围。
- 节点/边样式，包括箭头装饰。
- 字体与字号。
- 配色与线型。
- 特殊效果如箭头装饰。

### 10. 风险与替代方案
- **不确定因素**：精确色值和字体，可能因系统不同略有差异。
- **替代方案**：使用系统默认色和字体，如 `Computer Modern`，接近色替代可使用 `blue` 代替 `#0000FF`，`red` 代替 `#FF0000`。
