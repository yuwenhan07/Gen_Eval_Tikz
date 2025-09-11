# test_22.png

![test_22.png](../../../eval_dataset/images/test_22.png)

```latex
% 1. 概览
% 此图是一个网络结构，由若干节点和边组成，呈现出两个子图，每个子图包含连接不同节点的多条线。左侧子图是一个点状对称结构，右侧子图则为一个矩形连接分布结构。主要元素包括节点、实线和虚线边。

\documentclass{standalone}

% 2. 文档骨架与依赖
% 使用 TikZ 库绘制该网络图。需要 arrows.meta 库以便更好地控制箭头样式。

\usepackage{tikz}
\usetikzlibrary{arrows.meta}

\begin{document}

% 3. 版面与画布设置
% 依据图形风格，可设置 \tikzpicture 默认的尺寸，留出适当的周边间距。

\begin{tikzpicture}[node distance=1cm and 1.5cm, >=Stealth]

% 4. 字体与配色
% 使用中等大小字体，默认黑色。

\tikzset{
  every node/.style={circle, draw, inner sep=1.5pt, font=\small},
  edge/.style={draw, thick},
  dashed edge/.style={edge, dash pattern=on 3pt off 3pt}
}

% 5. 结构与组件样式
% 绘制节点并通过不同样式的边连接。

% 左侧子图
\node (x) at (0,0) {$x$};
\node (y) [right=of x] {$y$};
\node (z1) [above=of x] {$z_1$};
\node (z5) [below=of x] {$z_5$};
\node (w) [above=of z1, fill=black!10] {$w$};

\draw[edge] (x) -- (z1) -- (y);
\draw[edge] (x) -- (z5) -- (y);
\draw[edge] (x) -- (y) -- (x);
\draw[dashed edge] (w) -- (x) (w) -- (y);

% 右侧子图
\node (x2) at (4,0) {$x$};
\node (y2) [right=of x2] {$y$};
\node (y1) [above=of x2] {$y_1$};
\node (y5) [below=of x2] {$y_5$};

\draw[edge] (x2) -- (y1) -- (y2);
\draw[edge] (x2) -- (y5) -- (y2);
\draw[edge] (x2) -- (y2);
\draw[edge] (y1) -- (x2);
\draw[edge] (y5) -- (x2);

\end{tikzpicture}

\end{document}

% 6. 数学/表格/图形细节
% 节点通过 \node 放置，公式以 MathJax 格式插入节点中，无需额外配置。

% 7. 自定义宏与命令
% 在提供的 MWE 中，已使用 TikZ 预设定义常用的节点和边样式以提高复用性。

% 8. 最小可运行示例 (见上)

% 9. 复刻检查清单
% - 图形尺寸: 使用 [node distance=1cm and 1.5cm] 确保节点间距
% - 节点/边样式: \tikzset 中定义
% - 字体与字号: 使用 \small
% - 配色与线型: 默认黑色，虚线样式由 dash pattern 实现
% - 与原图的差异点: 确保边的对称性及正确连接

% 10. 风险与替代方案
% - 字体：若系统缺少特定字体，LaTeX 可自动回退至最接近的字体如 Computer Modern
% - 色值：使用 TikZ 默认色值，且可根据物理输出效果进行调整
```
