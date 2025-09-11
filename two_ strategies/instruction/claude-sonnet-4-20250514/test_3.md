# test_3.png

![test_3.png](../../../eval_dataset/images/test_3.png)

# 图像到 LaTeX 复刻指导：有向图/状态转换图

## 1. 概览

### 图形类型与构图
- **图形类型**：有向图/状态转换图，展示节点间的转换关系
- **构图布局**：对角线布局，从左上到右下呈阶梯状排列
- **主要元素**：
  - 状态节点：$q_0, q_1, q_k, q_{k+p}, q_{k+2p}, q_{k+3p}$
  - 转换边：实线箭头和虚线箭头
  - 边标签：字母 $a, c, d$ 等
  - 等式标注：右侧的数学表达式

## 2. 文档骨架与依赖

### 推荐文档类与宏包
```latex
\documentclass[border=5mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{amssymb}
```

### 所需 TikZ 库
```latex
\usetikzlibrary{
    arrows.meta,
    positioning,
    calc
}
```

## 3. 版面与画布设置

### 图形尺寸与坐标系
- **建议尺寸**：约 8cm × 6cm
- **坐标系范围**：相对定位，无需指定具体数值范围
- **节点间距**：水平间距 2.5cm，垂直间距 1.2cm

### TikZ 环境参数
```latex
\begin{tikzpicture}[
    node distance=1.2cm and 2.5cm,
    >=Stealth
]
```

## 4. 字体与配色

### 字体设置
- **节点标签**：默认数学字体，正常大小
- **边标签**：较小字体，建议 `\small` 或 `\footnotesize`
- **等式标注**：正常数学字体

### 配色方案
- **节点**：无填充，黑色边框
- **实线箭头**：黑色 (#000000)
- **虚线箭头**：黑色虚线
- **文本**：黑色 (#000000)

## 5. 结构与组件样式

### 节点样式
```latex
\tikzset{
    state/.style={
        circle,
        draw,
        minimum size=0.8cm,
        inner sep=2pt
    }
}
```

### 边与箭头样式
```latex
\tikzset{
    solid edge/.style={
        ->,
        thick
    },
    dotted edge/.style={
        ->,
        dotted,
        thick
    }
}
```

## 6. 数学/表格/图形细节

### 数学表达式处理
- 节点中的下标使用 `$q_0$, $q_1$` 等
- 右侧等式使用独立的文本节点
- 边标签直接使用字母，如 `$a$, $c$, $d$`

## 7. 自定义宏与命令

```latex
% 状态节点宏
\newcommand{\statenode}[3]{
    \node[state] (#1) at #2 {$#3$};
}

% 带标签的边宏
\newcommand{\labelededge}[4][solid edge]{
    \draw[#1] (#2) -- node[midway, above, sloped, font=\small] {$#4$} (#3);
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[border=5mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}

\usetikzlibrary{arrows.meta, positioning, calc}

\begin{document}
\begin{tikzpicture}[
    node distance=1.2cm and 2.5cm,
    >=Stealth,
    state/.style={
        circle,
        draw,
        minimum size=0.8cm,
        inner sep=2pt
    },
    solid edge/.style={
        ->,
        thick
    },
    dotted edge/.style={
        ->,
        dotted,
        thick
    }
]

% 状态节点
\node[state] (q0) at (0,0) {$q_0$};
\node[state] (q1) at (1.5,-0.8) {$q_1$};
\node[state] (qk) at (3,-1.6) {$q_k$};
\node[state] (qkp) at (4.5,-2.4) {$q_{k+p}$};
\node[state] (qk2p) at (6,-3.2) {$q_{k+2p}$};
\node[state] (qk3p) at (7.5,-4) {$q_{k+3p}$};

% 实线箭头
\draw[solid edge] (q0) -- node[midway, above left, font=\small] {$a$} (q1);
\draw[solid edge] (q1) -- node[midway, above left, font=\small] {$a$} (qk);
\draw[solid edge] (qk) -- node[midway, above left, font=\small] {$d$} (qkp);
\draw[solid edge] (qkp) -- node[midway, above left, font=\small] {$c/d$} (qk2p);
\draw[solid edge] (qk2p) -- node[midway, above left, font=\small] {$c$} (qk3p);

% 虚线箭头
\draw[dotted edge] (q1) -- node[midway, below right, font=\small] {$a$} (qk);
\draw[dotted edge] (qk) -- node[midway, below right, font=\small] {$a$} (qkp);
\draw[dotted edge] (qkp) -- node[midway, below right, font=\small] {$a$} (qk2p);
\draw[dotted edge] (qk2p) -- node[midway, below right, font=\small] {$a$} (qk3p);

% 左侧标签
\node at (-0.8,-0.5) {$c$};
\node at (-0.3,-1.3) {$c$};

% 右侧等式
\node[anchor=west] at (8.5,-1.6) {$= q$};
\node[anchor=west] at (8.5,-2.4) {$= q$};
\node[anchor=west] at (8.5,-3.2) {$= q$};

% 最右侧节点
\node at (8,-4.8) {$c$};
\node at (8.8,-4.8) {$c$};

\end{tikzpicture}
\end{document}
```

## 9. 复刻检查清单

### 必检项目
- [ ] **图形尺寸**：整体比例协调
- [ ] **节点位置**：对角线阶梯布局正确
- [ ] **箭头样式**：实线与虚线区分明确
- [ ] **标签位置**：边标签位于适当位置
- [ ] **字体大小**：边标签相对较小
- [ ] **线条粗细**：箭头线条适中粗细
- [ ] **数学符号**：下标正确显示

### 细节对
