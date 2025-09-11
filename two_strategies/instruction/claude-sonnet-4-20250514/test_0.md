# test_0.png

![test_0.png](../../../eval_dataset/images/test_0.png)

# LaTeX/TikZ 重构指导：Borel 有界函数韦恩图

## 1. 概览

**图形类型**：韦恩图（Venn Diagram）
**构图布局**：两个椭圆形集合的交集图，展示 Borel 有界函数的分类
**主要元素关系**：
- 左侧蓝色椭圆：Eulerian sources
- 右侧粉色椭圆：Lagrangian sources associated to a given λ
- 中间紫色交集区域：包含数学表达式
- 整体被矩形框包围，顶部有标题

## 2. 文档骨架与依赖

```latex
\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{amssymb}
\usetikzlibrary{shapes.geometric, positioning, fit}
```

**核心宏包**：
- `tikz`：绘图核心
- `amsmath, amssymb`：数学符号支持
- `shapes.geometric`：椭圆形状
- `positioning`：相对定位
- `fit`：自适应边框

## 3. 版面与画布设置

**图形尺寸**：约 8cm × 5cm
**坐标系范围**：(-4, -2.5) 到 (4, 2.5)
**椭圆参数**：
- 左椭圆：x半径 2.2，y半径 1.5，中心 (-1.2, 0)
- 右椭圆：x半径 2.2，y半径 1.5，中心 (1.2, 0)

```latex
\begin{tikzpicture}[scale=1, every node/.style={font=\small}]
```

## 4. 字体与配色

**字体设置**：
- 标题：`\normalsize\bfseries`
- 集合标签：`\small`
- 数学表达式：`\scriptsize`

**配色方案**：
- 蓝色椭圆：`blue!30` (填充), `blue!80` (边框)
- 粉色椭圆：`red!20!orange!30` (填充), `red!60!magenta` (边框)
- 紫色交集：`blue!40!red!60` (填充)
- 边框：`black, thick`

## 5. 结构与组件样式

**椭圆样式**：
```latex
\tikzset{
    ellipse/.style={ellipse, minimum width=4.4cm, minimum height=3cm, thick},
    left ellipse/.style={ellipse, fill=blue!30, draw=blue!80},
    right ellipse/.style={ellipse, fill=red!20!orange!30, draw=red!60!magenta},
    intersection/.style={fill=blue!40!red!60, opacity=0.7}
}
```

**文本样式**：
```latex
\tikzset{
    title/.style={font=\normalsize\bfseries, align=center},
    label/.style={font=\small, align=center},
    math/.style={font=\scriptsize, align=center}
}
```

## 6. 数学/表格/图形细节

**数学表达式**：在交集区域使用 `\scriptsize` 字体
```latex
\node[math] at (0, 0) {$+\S$ ?? $+\S$ ??};
```

**标签定位**：
- "Eulerian sources"：左下方
- "Lagrangian sources associated to a given λ"：右下方，分两行
- "Broad sources"：交集区域下方

## 7. 自定义宏与命令

```latex
% 定义颜色
\definecolor{leftcolor}{RGB}{173, 216, 230}
\definecolor{rightcolor}{RGB}{255, 182, 193}
\definecolor{intersectcolor}{RGB}{147, 112, 219}

% 定义样式宏
\tikzset{
    venn ellipse/.style={ellipse, minimum width=4.4cm, minimum height=3cm, thick},
    left set/.style={venn ellipse, fill=leftcolor, draw=blue!80},
    right set/.style={venn ellipse, fill=rightcolor, draw=red!60!magenta}
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{amssymb}
\usetikzlibrary{shapes.geometric, positioning, fit}

\begin{document}
\begin{tikzpicture}[scale=1, every node/.style={font=\small}]
    
    % 定义颜色
    \definecolor{leftcolor}{RGB}{173, 216, 230}
    \definecolor{rightcolor}{RGB}{255, 182, 193}
    \definecolor{intersectcolor}{RGB}{147, 112, 219}
    
    % 绘制左椭圆 (Eulerian sources)
    \node[ellipse, minimum width=4.4cm, minimum height=3cm, 
          fill=leftcolor, draw=blue!80, thick] (left) at (-1.2, 0) {};
    
    % 绘制右椭圆 (Lagrangian sources)
    \node[ellipse, minimum width=4.4cm, minimum height=3cm, 
          fill=rightcolor, draw=red!60!magenta, thick] (right) at (1.2, 0) {};
    
    % 交集区域 (需要手动绘制或使用clip)
    \begin{scope}
        \clip (-1.2, 0) ellipse (2.2cm and 1.5cm);
        \fill[intersectcolor, opacity=0.7] (1.2, 0) ellipse (2.2cm and 1.5cm);
    \end{scope}
    
    % 数学表达式在交集中心
    \node[font=\scriptsize] at (0, 0.2) {$+\S$ ?? $+\S$ ??};
    \node[font=\scriptsize, color=gray] at (0, -0.3) {Broad sources};
    
    % 标签
    \node[font=\small, color=blue!80] at (-2.2, -1.8) {Eulerian sources};
    \node[font=\small, color=red!60!magenta, align=center] at (2.2, -1.8) 
          {Lagrangian sources\\associated to a given $\lambda$};
    
    % 外框和标题
    \node[fit={(left) (right)}, draw=black, thick, 
          inner xsep=0.5cm, inner ysep=0.8cm] (frame) {};
    \node[above=0.1cm of frame.north, font=\normalsize\bfseries] 
          {Borel, bounded functions};
    
\end{tikzpicture}
\end{document}
```

## 9. 复刻检查清单

- [ ] **图形尺寸**：8cm × 5cm，椭圆重叠适当
- [ ] **椭圆形状**：两个相同大小的椭圆，适度重叠
- [ ] **配色方案**：蓝色(左)、粉橙色(右)、紫色(交集)
- [ ] **字体层次**：标题粗体、标签正常
