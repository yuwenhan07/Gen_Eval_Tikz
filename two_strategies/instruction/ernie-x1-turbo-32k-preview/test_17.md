# test_17.png

![test_17.png](../../../eval_dataset/images/test_17.png)

```markdown
### 1. 概览
- **图形类型**：流程图（含矩形节点、带箭头连接线、分层布局）
- **构图布局**：纵向三层结构（输入层→处理层→输出层），左右对称分布
- **主要元素**：
  - 顶部/底部矩形框（输入/输出节点）
  - 中间菱形决策节点
  - 带箭头连接线（实线/虚线区分逻辑路径）
  - 节点间垂直/水平对齐网格

### 2. 文档骨架与依赖
```latex
\documentclass[tikz,border=2mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, shadows}
\usepackage{xcolor}
\definecolor{primary}{HTML}{1f77b4}
\definecolor{secondary}{HTML}{ff7f0e}
```

### 3. 版面与画布设置
```latex
\begin{tikzpicture}[
  node distance=1.5cm and 2cm,
  scale=1,
  every node/.style={scale=1},
  show background rectangle,
  inner frame sep=5mm
]
% 坐标系范围：x(0,12) y(0,8)
% 画布尺寸：12cm×8cm
```

### 4. 字体与配色
- **字体**：
  - 节点标签：\sffamily\small
  - 坐标轴标题：\bfseries\large
- **主色**：
  - 蓝色：`#1f77b4` (primary)
  - 橙色：`#ff7f0e` (secondary)
- **特殊效果**：
  ```latex
  \tikzset{
    shadowed/.style={drop shadow={opacity=0.3}},
    gradient/.style={left color=primary!30, right color=primary!70}
  }
  ```

### 5. 结构与组件样式
```latex
% 节点样式
\tikzset{
  rect/.style={rectangle, draw=primary, thick, fill=primary!10, 
              minimum width=2cm, minimum height=1cm, align=center},
  decision/.style={diamond, draw=secondary, thick, 
                  fill=secondary!10, aspect=1.5, align=center},
  arrow/.style={-{Stealth[length=3mm]}, thick}
}

% 坐标轴配置
\begin{axis}[
  axis lines=middle,
  xlabel=$x$, ylabel=$y$,
  grid=both,
  legend style={at={(0.95,0.95)}, anchor=north east}
]
```

### 6. 数学/表格/图形细节
- **公式排版**：
  ```latex
  \node at (3,4) {$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$};
  ```
- **PGFPlots示例**：
  ```latex
  \addplot[domain=-3:3, samples=100, smooth]{x^2};
  ```

### 7. 自定义宏与命令
```latex
\newcommand{\inputnode}[2]{
  \node[rect, shadowed] (#1) {#2};
}
\newcommand{\decisionnode}[2]{
  \node[decision, gradient] (#1) {#2};
}
```

### 8. 最小可运行示例 (MWE)
```latex
\documentclass[tikz,border=2mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, shadows}
\begin{document}
\begin{tikzpicture}[node distance=1.5cm and 2cm]
  % 输入层
  \inputnode{in1}{Input 1};
  \inputnode{in2}[below=of in1]{Input 2};
  
  % 决策节点
  \decisionnode{dec1}[right=of in2]{Decision?};
  
  % 输出层
  \node[rect, right=of dec1] (out1) {Output};
  
  % 连接线
  \draw[arrow] (in1) -- (dec1);
  \draw[arrow, dashed] (in2) -- (dec1);
  \draw[arrow] (dec1) -- node[above]{Yes} (out1);
  \draw[arrow] (dec1.south) -- ++(0,-1) node[below]{No};
  
  % 坐标轴示例
  \draw[thick] (0,0) -- (5,0) node[below]{$x$};
  \draw[thick] (0,0) -- (0,4) node[left]{$y$};
\end{tikzpicture}
\end{document}
```

### 9. 复刻检查清单
- [ ] 图形尺寸：12cm×8cm
- [ ] 坐标范围：x(0,12) y(0,8)
- [ ] 节点样式：矩形/菱形+阴影+渐变
- [ ] 字体：无衬线体，标题加粗
- [ ] 配色：蓝/橙主色+30%透明度
- [ ] 特殊效果：箭头长度3mm，网格线间距1cm
- [ ] 差异点：原图阴影角度可能不同

### 10. 风险与替代方案
- **不确定因素**：
  - 精确色值可能需调整（建议使用Pantone色卡匹配）
  - 字体渲染差异（LaTeX默认CM与Adobe字库差异）
- **替代方案**：
  - 字体：Times New Roman替代默认CM
  - 颜色：使用PGFPlots内置色图代替自定义RGB
  - 阴影：使用fill opacity替代drop shadow
```
