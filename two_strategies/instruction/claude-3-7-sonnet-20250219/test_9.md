# test_9.png

![test_9.png](../../../eval_dataset/images/test_9.png)

# LaTeX/TikZ 图像重构指导

## 1. 概览

这是一个流程图，展示了两个并行处理路径（上下两行）的信号流向，每行包含多个标记为"MC"的方框模块。两条路径之间有交叉连接的箭头，最终在右侧通过一个加法节点（⊕符号）合并输出。图中包含多个标签（如 $i_{\mathcal{L}}$, $i\mathcal{V}_{\mathcal{L}}$ 等）用于标识不同的信号路径。

## 2. 文档骨架与依赖

```
\documentclass[border=10pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, fit, shapes.misc}
```

核心宏包：
- `tikz`：绘制整个流程图
- 需要的 TikZ 库：
  - `arrows.meta`：自定义箭头样式
  - `positioning`：节点相对定位
  - `calc`：计算节点位置
  - `fit`：创建包围节点的框
  - `shapes.misc`：用于绘制加号符号

## 3. 版面与画布设置

- 图形尺寸：约 12cm × 6cm
- 节点间距：水平方向约 1cm，垂直方向约 3cm
- 建议的环境参数：
  ```
  \begin{tikzpicture}[
    node distance=1cm and 3cm,
    auto
  ]
  ```

## 4. 字体与配色

- 字体：默认的 LaTeX 数学字体（用于标签的斜体数学符号）
- 字号：正常文档字号
- 颜色：纯黑色线条和文字

## 5. 结构与组件样式

- MC 节点：方形，黑色边框，无填充，居中对齐文本
- 大框：矩形，黑色边框，包含多个 MC 节点
- 箭头：直线箭头，中等粗细
- 标签：使用数学模式，放置在箭头上方或箭头旁
- 加号节点：圆形节点，内部带有 ⊕ 符号

## 6. 数学细节

- 标签使用数学模式，包含下标和花体字符
- 主要标签包括：$\mathcal{V}_\mathcal{L}$, $\mathcal{V}_\mathcal{H}$, $i_{\mathcal{L}}$, $i\mathcal{V}_{\mathcal{L}}$, $i_{\mathcal{H}_1}$, $i\mathcal{V}_{\mathcal{H}_2}$ 等
- 最终输出标记为 $\hat{i}$

## 7. 自定义宏与命令

```latex
\tikzset{
  mc/.style={draw, minimum size=0.8cm, inner sep=2pt},
  container/.style={draw, inner sep=10pt},
  arrow/.style={-{Stealth[scale=1.2]}, thick},
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[border=10pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, calc, fit, shapes.misc}

\begin{document}
\begin{tikzpicture}[
  node distance=1.2cm,
  mc/.style={draw, minimum size=0.8cm, inner sep=2pt},
  container/.style={draw, inner sep=10pt},
  arrow/.style={-{Stealth[scale=1.2]}, thick},
]

% 上行节点
\node[mc] (mc1) {MC};
\node[mc, right=of mc1] (mc2) {MC};
\node[mc, right=of mc2] (mc3) {MC};
\node[right=0.5cm of mc3] (dots1) {$\cdots$};
\node[mc, right=0.5cm of dots1] (mc4) {MC};

% 上行容器
\node[container, fit={(mc1) (mc2) (mc3) (dots1) (mc4)}] (upper) {};

% 下行节点
\node[mc, below=3cm of mc1] (mc5) {MC};
\node[mc, right=of mc5] (mc6) {MC};
\node[mc, right=of mc6] (mc7) {MC};
\node[right=0.5cm of mc7] (dots2) {$\cdots$};
\node[mc, right=0.5cm of dots2] (mc8) {MC};

% 下行容器
\node[container, fit={(mc5) (mc6) (mc7) (dots2) (mc8)}] (lower) {};

% 输入标签
\node[left=1cm of upper.west] (vl) {$\mathcal{V}_\mathcal{L}$};
\node[left=1cm of lower.west] (vh) {$\mathcal{V}_\mathcal{H}$};

% 连接箭头
\draw[arrow] (vl) -- (upper.west);
\draw[arrow] (vh) -- (lower.west);

% 上行内部连接
\draw[arrow] (mc1) -- node[above] {$i_\mathcal{L}$} (mc2);
\draw[arrow] (mc2) -- node[above] {$i\mathcal{V}_\mathcal{L}$} (mc3);
\draw[arrow] (mc3) -- (dots1);
\draw[arrow] (dots1) -- (mc4);

% 下行内部连接
\draw[arrow] (mc5) -- node[above] {$i_{\mathcal{H}_1}$} (mc6);
\draw[arrow] (mc6) -- node[above] {$i\mathcal{V}_{\mathcal{H}_2}$} (mc7);
\draw[arrow] (mc7) -- (dots2);
\draw[arrow] (dots2) -- (mc8);

% 交叉连接
\draw[arrow] (mc1) -- node[sloped, above] {$i_\mathcal{L}$} (mc6);
\draw[arrow] (mc5) -- node[sloped, above] {$i_{\mathcal{H}_1}$} (mc2);
\draw[arrow] (mc2) -- node[sloped, above] {$i\mathcal{V}_\mathcal{L}$} (mc7);
\draw[arrow] (mc6) -- node[sloped, above] {$i\mathcal{V}_{\mathcal{H}_2}$} (mc3);

% 输出部分
\node[circle, draw, right=2cm of $(upper.east)!0.5!(lower.east)$] (sum) {$\oplus$};
\node[right=1cm of sum] (output) {$\hat{i}$};

% 输出连接
\draw[arrow] (upper.east) -- node[sloped, above] {$i\mathcal{V}_\mathcal{L}$} (sum);
\draw[arrow] (lower.east) -- node[sloped, above] {$i\mathcal{V}_\mathcal{H}$} (sum);
\draw[arrow] (sum) -- (output);

\end{tikzpicture}
\end{document}
```

## 9. 复
