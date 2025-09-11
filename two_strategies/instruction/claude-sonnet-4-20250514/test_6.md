# test_6.png

![test_6.png](../../../eval_dataset/images/test_6.png)

# 科研绘图 LaTeX/TikZ 重构指导

## 1. 概览

**图形类型**: 网络结构图/二分图，展示了分层的节点连接关系
**构图布局**: 
- 左侧：垂直排列的输入节点 (x₁ ○ 到 x₉ ○)
- 中间：6个垂直椭圆区域，每个包含多个节点
- 底部：水平排列的输出节点 (1-6)
- 连接线：从左侧输入节点到各椭圆区域内节点的映射关系

**主要元素关系**: 这是一个典型的神经网络或分类系统示意图，显示输入特征到隐藏层/分类器的映射。

## 2. 文档骨架与依赖

```latex
\documentclass[tikz,border=3mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usepackage{amssymb}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, fit}
```

**核心宏包说明**:
- `tikz`: 绘图核心
- `shapes.geometric`: 椭圆形状
- `arrows.meta`: 现代箭头样式
- `positioning`: 节点定位
- `fit`: 椭圆边界拟合

## 3. 版面与画布设置

**建议参数**:
- 图形尺寸: 约 12cm × 8cm
- 坐标系: 相对定位，使用 `positioning` 库
- 节点间距: 垂直 0.6cm，水平 1.8cm
- 椭圆宽度: 1.2cm，高度: 6cm

```latex
\begin{tikzpicture}[
    scale=1,
    node distance=0.6cm and 1.8cm,
    every node/.style={font=\small}
]
```

## 4. 字体与配色

**字体设置**:
- 节点标签: `\small` Computer Modern
- 下标: 数学模式 `$x_i$`

**配色方案**:
- 实心节点: 黑色 `black`
- 空心节点: 白色填充，黑色边框 `fill=white, draw=black`
- 连接线: 黑色 `black`
- 椭圆边框: 黑色 `draw=black, fill=none`

## 5. 结构与组件样式

**节点样式**:
```latex
% 实心节点
filled/.style={circle, fill=black, inner sep=1.5pt, minimum size=3pt}

% 空心节点  
hollow/.style={circle, fill=white, draw=black, inner sep=1.5pt, minimum size=3pt}

% 输入标签节点
input/.style={font=\small}

% 输出标签节点
output/.style={font=\small}
```

**椭圆容器**:
```latex
ellipse/.style={ellipse, draw=black, minimum width=1.2cm, minimum height=6cm}
```

**连接线**:
```latex
connection/.style={draw=black, line width=0.4pt}
```

## 6. 数学/表格/图形细节

**数学符号处理**:
- 输入节点使用数学模式: `$x_1 \circ$, `$x_2 \circ$`, etc.
- 下标正确渲染: `$x_{i} \circ$`

**节点分布**:
- 每个椭圆内包含 9个节点，与输入节点数量对应
- 节点在椭圆内垂直等间距分布

## 7. 自定义宏与命令

```latex
% 定义样式
\tikzset{
    filled/.style={circle, fill=black, inner sep=1.5pt, minimum size=3pt},
    hollow/.style={circle, fill=white, draw=black, inner sep=1.5pt, minimum size=3pt},
    input/.style={font=\small},
    output/.style={font=\small},
    ellipse/.style={ellipse, draw=black, minimum width=1.2cm, minimum height=6cm},
    connection/.style={draw=black, line width=0.4pt}
}

% 批量创建输入节点的宏
\newcommand{\inputnode}[2]{\node[input] (x#1) at #2 {$x_{#1} \circ$};}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[tikz,border=3mm]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\usetikzlibrary{shapes.geometric, positioning, fit}

\begin{document}
\begin{tikzpicture}[
    node distance=0.6cm and 1.8cm,
    filled/.style={circle, fill=black, inner sep=1.5pt, minimum size=3pt},
    hollow/.style={circle, fill=white, draw=black, inner sep=1.5pt, minimum size=3pt},
    input/.style={font=\small},
    output/.style={font=\small},
    connection/.style={draw=black, line width=0.4pt}
]

% 输入节点
\foreach \i in {1,...,9} {
    \node[input] (x\i) at (0, {4.8-0.6*(\i-1)}) {$x_{\i} \circ$};
}

% 椭圆区域和内部节点
\foreach \col in {1,...,6} {
    % 创建椭圆内的节点
    \foreach \row in {1,...,9} {
        \pgfmathsetmacro\ypos{4.8-0.6*(\row-1)}
        \pgfmathsetmacro\xpos{1.8*\col}
        
        % 根据位置决定节点类型（这里简化处理，实际需要根据原图调整）
        \ifnum\row<6
            \node[filled] (n\col\row) at (\xpos, \ypos) {};
        \else
            \node[hollow] (n\col\row) at (\xpos, \ypos) {};
        \fi
    }
    
    % 创建椭圆边界
    \node[ellipse, fit={(n\col1) (n\col9)}] (ellipse\col) {};
}

% 连接线（示例连接，需要根据原图调整）
\foreach \i in {1,...,9} {
    \foreach \col in {1,...,6} {
        % 连接到对应行的节点
        \draw[connection] (x\i) -- (n\col\i);
    }
}

% 底部标签
\foreach \i in {1,...,6} {
    \node[output] at ({1.8*\i}, -0.8) {\i};
}

% 底部标签说明
\foreach \i in {1,...,6} {
    \node[output] at ({1.8*\i}, -1.6) {\i};
}

\end{tikzpicture}
\end{document}
```

## 9. 复刻检查清单

- [x] **图形尺寸**: 横向约12cm，纵向约8cm
- [x] **节点样式**: 实心黑点和空心圆点
- [x] **字
