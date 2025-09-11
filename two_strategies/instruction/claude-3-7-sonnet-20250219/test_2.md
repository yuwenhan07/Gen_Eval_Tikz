# test_2.png

![test_2.png](../../../eval_dataset/images/test_2.png)

# LaTeX/TikZ 重构指导：神经网络连接示意图

## 1. 概览

这是一个神经网络连接示意图，展示了两层神经元之间的连接关系。图中包含两组垂直矩形表示神经元，每组左侧有标记（$\tilde{w}_1$、$\tilde{w}_2$等），神经元之间通过实线和虚线箭头连接，表示权重连接（$w_1$）。整体布局对称，使用了简洁的黑白线条风格。

## 2. 文档骨架与依赖

```latex
\documentclass[tikz, border=10pt]{standalone}
\usepackage{tikz}
\usepackage{amsmath} % 用于数学符号
\usetikzlibrary{arrows.meta} % 箭头样式
\usetikzlibrary{positioning} % 相对位置
\usetikzlibrary{calc} % 坐标计算
```

## 3. 版面与画布设置

- 图形尺寸：约 8cm × 5cm
- 节点间距：水平方向约 1cm，垂直方向保持对齐
- 建议使用相对坐标定位，确保神经元垂直排列

```latex
\begin{tikzpicture}[
    scale=1,
    every node/.style={font=\normalsize},
    neuron/.style={rectangle, draw, minimum width=0.3cm, minimum height=2cm},
    weight label/.style={font=\normalsize},
]
```

## 4. 字体与配色

- 所有文本使用数学模式，标签为斜体（如 $w_1$、$\tilde{w}_1$）
- 颜色：全黑线条和文本（RGB: 0,0,0）
- 无渐变、透明度或阴影效果

## 5. 结构与组件样式

- 神经元：垂直长方形，黑色细边框，无填充
- 权重标记：水平短线，位于神经元中部
- 连接线：
  - 实线：直线连接，黑色，中等粗细
  - 虚线：短划线样式，黑色，中等粗细
- 弧线：平滑曲线，黑色，无箭头

## 6. 数学细节

- 数学标记使用 $\tilde{w}_1$、$\tilde{w}_2$、$w_1$ 等带有下标的符号
- 波浪符号（tilde）用于部分权重标记
- 所有标签位于神经元左侧或连接线中部

## 7. 自定义宏与命令

```latex
\tikzset{
    neuron/.style={rectangle, draw, minimum width=0.3cm, minimum height=2cm},
    neuron weight/.style={draw, line width=0.5pt, minimum width=0.5cm},
    connection/.style={draw, -},
    dashed connection/.style={draw, dashed}
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[tikz, border=10pt]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta}
\usetikzlibrary{positioning}
\usetikzlibrary{calc}

\begin{document}
\begin{tikzpicture}[
    neuron/.style={rectangle, draw, minimum width=0.3cm, minimum height=2cm},
    neuron weight/.style={draw, line width=0.5pt, minimum width=0.5cm},
    connection/.style={draw, -},
    dashed connection/.style={draw, dashed}
]

% 第一组神经元（左侧）
\node[neuron] (n11) at (0,0) {};
\node[neuron] (n12) at (1,0) {};

% 第一组权重标记
\node (w11) at (-0.7,0) {$\tilde{w}_1$};
\draw (n11.west) -- ++(-0.5,0);
\draw (n11.west) ++(0,0) -- ++(0,0.1);
\draw (n11.west) ++(0,-0.1) -- ++(0,-0.1);
\draw (n11.west) ++(-0.5,0) -- ++(0,0.1);
\draw (n11.west) ++(-0.5,-0.1) -- ++(0,-0.1);

% 第二组神经元（中间）
\node[neuron] (n21) at (3.5,0) {};
\node[neuron] (n22) at (4.5,0) {};
\node[neuron] (n23) at (5.5,0) {};

% 第二组权重标记
\node (w21) at (3.0,0) {$\tilde{w}_2$};
\draw (n21.west) -- ++(-0.5,0);
\draw (n21.west) ++(0,0) -- ++(0,0.1);
\draw (n21.west) ++(0,-0.1) -- ++(0,-0.1);
\draw (n21.west) ++(-0.5,0) -- ++(0,0.1);
\draw (n21.west) ++(-0.5,-0.1) -- ++(0,-0.1);

\node (w22) at (4.0,0) {$\tilde{w}_2$};
\draw (n22.west) -- ++(-0.5,0);
\draw (n22.west) ++(0,0) -- ++(0,0.1);
\draw (n22.west) ++(0,-0.1) -- ++(0,-0.1);
\draw (n22.west) ++(-0.5,0) -- ++(0,0.1);
\draw (n22.west) ++(-0.5,-0.1) -- ++(0,-0.1);

% 第三组神经元（右侧）
\node[neuron] (n31) at (7.5,0) {};
\node[neuron] (n32) at (8.5,0) {};

% 第三组权重标记
\node (w31) at (7.0,0) {$\tilde{w}_1$};
\draw (n31.west) -- ++(-0.5,0);
\draw (n31.west) ++(0,0) -- ++(0,0.1);
\draw (n31.west) ++(0,-0.1) -- ++(0,-0.1);
\draw (n31.west) ++(-0.5,0) -- ++(0,0.1);
\draw (n31.west) ++(-0.5,-0.1) -- ++(0,-0.1);

% 连接线
\draw[connection] (n12) -- node[above, sloped] {$w_1$} (n21);
\draw[dashed connection] (n23) -- node[above, sloped] {$w_1$} (n31);

% 顶部弧线连接
\draw[connection] (n11) to[bend left=30] (n32);

% 中间弧线连接
\draw[connection] (n21) to[bend left=30] (n23);

\end{tikzpicture}
\end{document}
```

## 9. 复刻检查清单

- ✓ 图形尺寸与比例：保持了原图的长宽比和整体布局
- ✓ 神经元
