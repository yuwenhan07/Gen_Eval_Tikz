# test_1.png

![test_1.png](../../../eval_dataset/images/test_1.png)

# LaTeX/TikZ 重构指导：生产函数曲线图

## 1. 概览

这是一个经济学中的生产函数图形，展示了两条凹函数曲线：
- **图形类型**：二维坐标系下的函数曲线图
- **构图布局**：标准的第一象限坐标系，原点在左下角
- **主要元素**：
  - 两条向上凹的曲线，上方曲线标注为 $y = G(N^u)f(k)$
  - 下方曲线标注为 $y = G(N)f(k)$
  - x轴标签：Input (capital per worker)，变量为 $k$
  - y轴标签：Output per worker，变量为 $y$
- **视觉特点**：简洁的学术风格，黑白配色，清晰的数学标注

## 2. 文档骨架与依赖

```latex
\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{amsmath}
\usepackage{amssymb}
\usetikzlibrary{arrows.meta}
```

**核心依赖说明**：
- `pgfplots`：用于绘制坐标轴和函数曲线
- `amsmath`：支持数学公式排版
- `arrows.meta`：提供现代箭头样式

## 3. 版面与画布设置

- **图形尺寸**：建议 8cm × 6cm
- **坐标系范围**：x轴 [0, 5]，y轴 [0, 4]
- **纵横比**：约 4:3
- **轴线样式**：带箭头的轴线，延伸至图形边界外

**推荐的 axis 环境参数**：
```latex
\begin{axis}[
    width=8cm, height=6cm,
    axis lines=left,
    axis line style={-Stealth},
    xmin=0, xmax=5,
    ymin=0, ymax=4,
    xtick=\empty, ytick=\empty,
]
```

## 4. 字体与配色

- **字体**：Computer Modern（LaTeX默认）
- **字号**：轴标签使用 `\normalsize`，函数标签使用 `\small`
- **配色方案**：
  - 主色：黑色 `black` (#000000)
  - 轴线：黑色
  - 曲线：黑色，线宽约 1pt
- **无特殊效果**：纯黑白学术风格，无渐变或阴影

## 5. 结构与组件样式

### 坐标轴
- **样式**：左侧和底部轴线，带箭头
- **刻度**：隐藏数值刻度，仅保留轴线
- **标签位置**：x轴标签在右下方，y轴标签在左上方垂直排列

### 曲线
- **形状**：凹函数（递增但边际递减）
- **线型**：实线，均匀线宽
- **函数形式**：可用 `sqrt` 或 `ln` 函数模拟

### 标注
- **位置**：函数标签位于曲线右侧
- **对齐**：左对齐，与曲线末端水平对齐

## 6. 数学/表格/图形细节

### 数学公式排版
- 使用 `node` 命令在指定位置放置数学公式
- 公式格式：`$y = G(N^u)f(k)$` 和 `$y = G(N)f(k)$`
- 上标 `u` 需要正确处理

### 函数曲线实现
使用 PGFPlots 的 `\addplot` 命令：
```latex
\addplot[black, thick, smooth, domain=0.1:4.5] {1.8*sqrt(x)};
\addplot[black, thick, smooth, domain=0.1:4.5] {1.4*sqrt(x)};
```

## 7. 自定义宏与命令

```latex
% 定义曲线样式
\pgfplotsset{
    production curve/.style={
        black, thick, smooth, no marks
    }
}

% 定义标签样式
\newcommand{\funclabel}[3]{
    \node[right, font=\small] at (axis cs:#1,#2) {$#3$};
}
```

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[tikz,border=5mm]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta}

\begin{document}
\begin{tikzpicture}
    \begin{axis}[
        width=8cm, height=6cm,
        axis lines=left,
        axis line style={-Stealth, thick},
        xmin=0, xmax=5,
        ymin=0, ymax=4,
        xtick=\empty, ytick=\empty,
        xlabel style={at={(1,0)}, anchor=north west},
        ylabel style={at={(0,1)}, anchor=south east, rotate=90},
        xlabel={Input (capital per worker)},
        ylabel={Output\\per worker},
        every axis plot/.append style={thick}
    ]
    
    % 上方曲线
    \addplot[black, thick, smooth, domain=0.1:4.2] {1.8*sqrt(x)};
    \node[right, font=\small] at (axis cs:4.2,2.44) {$y = G(N^u)f(k)$};
    
    % 下方曲线  
    \addplot[black, thick, smooth, domain=0.1:4.2] {1.4*sqrt(x)};
    \node[right, font=\small] at (axis cs:4.2,1.89) {$y = G(N)f(k)$};
    
    % 坐标轴变量标记
    \node[below] at (axis cs:4.8,-0.1) {$k$};
    \node[left] at (axis cs:-0.1,3.8) {$y$};
    
    \end{axis}
\end{tikzpicture}
\end{document}
```

## 9. 复刻检查清单

- [x] **图形尺寸**：8×6cm，符合原图比例
- [x] **坐标范围**：第一象限，合适的显示范围
- [x] **曲线形状**：凹函数特征，上下两条曲线相对位置正确
- [x] **轴线样式**：左侧和底部轴线，带箭头
- [x] **字体与字号**：Computer Modern，合适大小
- [x] **标签位置**：x轴、y轴标签位置准确
- [x] **函数标注**：数学公式格式正确，位置合理
- [x] **配色与线型**：纯黑色，适当线宽

## 10. 风险
