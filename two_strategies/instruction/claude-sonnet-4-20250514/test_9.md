# test_9.png

![test_9.png](../../../eval_dataset/images/test_9.png)

# LaTeX/TikZ 科研绘图重构指导

## 1. 概览

此图为一个**神经网络架构流程图**，展示了两个并行的多层感知机(MC)链式结构：
- **图形类型**：网络架构框图，包含节点、连接线和数学标记
- **构图布局**：上下双层并行结构，左侧输入，右侧汇聚输出
- **主要元素**：矩形节点(MC)、有向连接线、交叉连接、求和节点、数学标签

## 2. 文档骨架与依赖

```latex
\documentclass[border=5mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{amssymb}
\usetikzlibrary{positioning, arrows.meta, calc, shapes.geometric}
```

**核心依赖说明**：
- `tikz`：基础绘图
- `positioning`：相对定位
- `arrows.meta`：现代箭头样式
- `calc`：坐标计算
- `shapes.geometric`：几何形状（圆形求和节点）

## 3. 版面与画布设置

- **图形尺寸**：约 12cm × 8cm
- **坐标系**：相对定位，节点间距 2.5cm（水平）× 2cm（垂直）
- **对齐方式**：网格对齐，垂直居中
- **画布参数**：
```latex
\begin{tikzpicture}[
    node distance=2.5cm and 2cm,
    >=Stealth
]
```

## 4. 字体与配色

- **字体族**：Computer Modern（LaTeX默认）
- **节点标签**：`\normalsize` MC
- **数学标签**：`\small` 斜体变量名
- **输入标签**：`\normalsize` 正体
- **配色方案**：
  - 节点边框：黑色 `black`
  - 节点填充：白色 `white`
  - 连接线：黑色 `black`
  - 背景：透明

## 5. 结构与组件样式

### 节点样式
```latex
% MC节点
mc/.style={
    rectangle,
    draw=black,
    fill=white,
    minimum width=1.2cm,
    minimum height=0.8cm,
    font=\normalsize
}

% 求和节点
sum/.style={
    circle,
    draw=black,
    fill=white,
    minimum size=0.8cm,
    font=\large
}
```

### 连接线样式
```latex
% 主连接线
main/.style={->, thick, black}

% 交叉连接线
cross/.style={->, black}
```

## 6. 数学/表格/图形细节

- **数学标记**：使用 `$i_{V_c}$, $i_{V_{c2}}$` 等斜体变量
- **下标处理**：多字符下标用 `{}` 包围
- **特殊符号**：求和符号 `$\oplus$`
- **省略号**：使用 `$\cdots$`

## 7. 自定义宏与命令

```latex
% 定义MC节点宏
\newcommand{\mcnode}[2]{\node[mc] (#1) {MC};}

% 定义标签宏
\newcommand{\edgelabel}[3]{\path (#1) -- (#2) node[midway, above, font=\small] {$#3$};}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[border=5mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usetikzlibrary{positioning, arrows.meta, calc, shapes.geometric}

\begin{document}
\begin{tikzpicture}[
    node distance=2.5cm and 2cm,
    >=Stealth,
    % 节点样式
    mc/.style={
        rectangle,
        draw=black,
        fill=white,
        minimum width=1.2cm,
        minimum height=0.8cm,
        font=\normalsize
    },
    sum/.style={
        circle,
        draw=black,
        fill=white,
        minimum size=0.8cm,
        font=\large
    },
    % 连接线样式
    main/.style={->, thick, black},
    cross/.style={->, black},
    label/.style={font=\small}
]

% 上层MC链
\node[mc] (mc1) {MC};
\node[mc, right=of mc1] (mc2) {MC};
\node[mc, right=of mc2] (mc3) {MC};
\node[right=1cm of mc3, font=\normalsize] (dots1) {$\cdots$};
\node[mc, right=1cm of dots1] (mc4) {MC};

% 下层MC链
\node[mc, below=3cm of mc1] (mc5) {MC};
\node[mc, right=of mc5] (mc6) {MC};
\node[mc, right=of mc6] (mc7) {MC};
\node[right=1cm of mc7, font=\normalsize] (dots2) {$\cdots$};
\node[mc, right=1cm of dots2] (mc8) {MC};

% 输入标签
\node[left=1cm of mc1] (vc) {$V_c$};
\node[left=1cm of mc5] (vh) {$V_H$};

% 求和节点
\node[sum, right=3cm of mc4] (sum1) {$\oplus$};

% 输出
\node[right=1.5cm of sum1] (output) {$\hat{y}$};

% 主连接线（上层）
\draw[main] (vc) -- (mc1);
\draw[main] (mc1) -- (mc2) node[midway, above, label] {$i_{V_c}$};
\draw[main] (mc2) -- (mc3) node[midway, above, label] {$i_{V_{c2}}$};
\draw[main] (mc3) -- (dots1);
\draw[main] (dots1) -- (mc4);

% 主连接线（下层）
\draw[main] (vh) -- (mc5);
\draw[main] (mc5) -- (mc6) node[midway, above, label] {$i_{V_H}$};
\draw[main] (mc6) -- (mc7) node[midway, above, label] {$i_{V_{H2}}$};
\draw[main] (mc7) -- (dots2);
\draw[main] (dots2) -- (mc8);

% 交叉连接
\draw[cross] (mc1) -- (mc6) node[midway, above right, label] {$i_{c1}$};
\draw[cross] (mc2) -- (mc7) node[midway, above right, label] {$i_{V_{c2}}$};
\draw[cross] (mc5) -- (mc2) node[midway, below right, label] {$i_{H1}$};
\draw[cross] (mc6) -- (mc3) node[midway, below right, label] {$i_{V_{H2}}$};

% 输出连接
\draw[main] (mc4) -- (sum1) node[midway, above, label] {$i_{V_c}$};
\draw[main] (mc
