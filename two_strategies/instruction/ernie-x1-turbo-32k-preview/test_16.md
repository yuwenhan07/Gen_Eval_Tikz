# test_16.png

![test_16.png](../../../eval_dataset/images/test_16.png)

```markdown
### 概览
- **图形类型**：流程图式网络结构，含矩形节点与有向箭头连接
- **布局特征**：纵向分层排列，节点间水平/斜向对齐，存在主从关系
- **主要元素**：6个矩形节点（3层×2列），带方向箭头连接，顶部标题框

### 文档骨架与依赖
```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{positioning, arrows.meta, shadows, calc}
\usepackage{xcolor}
\usepackage{fontspec} % 如需自定义字体
```

### 版面与画布设置
```latex
\begin{tikzpicture}[
  node distance=1.2cm and 2cm,
  scale=1,
  transform shape,
  every node/.style={inner sep=3mm, outer sep=2pt}
]
% 坐标系范围建议：x=[0,12], y=[0,8]
```

### 字体与配色
- **字体**：主标题 \Large\sffamily\bfseries，节点标签 \small\sffamily
- **主色系**：
  - 标题框：HTML #2E86C1
  - 节点A：HTML #3498DB
  - 节点B：HTML #2980B9
  - 箭头：HTML #2C3E50
- **渐变示例**：
  ```latex
  \shade[left color=blue!30, right color=blue!10] 
  ```

### 结构与组件样式
```latex
\node[draw=blue!50, fill=blue!10, rounded corners=4pt, 
      minimum width=3cm, minimum height=1.2cm, 
      drop shadow] (node1) {Process Step A};
      
\draw[-{Stealth[length=3mm]}, line width=1.2pt, color=darkgray] 
  (node1) -- (node2);
```

### 数学/表格/图形细节
- **公式节点**：
  ```latex
  \node[math mode] {$ E = mc^2 $};
  ```
- **表格嵌入**：
  ```latex
  \node[anchor=center] {\begin{tabular}{ccc}
    \toprule
    A & B & C \\
    \midrule
    1 & 2 & 3 \\
    \bottomrule
  \end{tabular}};
  ```

### 自定义宏与命令
```latex
\tikzset{
  main node/.style={
    rounded corners=4pt,
    draw=#1!50,
    fill=#1!10,
    minimum width=2.5cm,
    font=\sffamily\small
  },
  title box/.style={
    fill=blue!20,
    draw=blue!50,
    minimum height=1cm,
    font=\sffamily\Large\bfseries
  }
}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{positioning, arrows.meta, shadows}
\begin{document}
\begin{tikzpicture}[
  node distance=1.5cm and 2cm,
  every node/.style={inner sep=4pt},
  box/.style={
    draw=#1, thick, fill=#1!10, rounded corners=4pt,
    minimum width=3cm, minimum height=1.2cm,
    drop shadow, font=\sffamily\small
  }
]

% Title Box
\node[box=blue!50, minimum height=1.5cm, 
      font=\sffamily\Large\bfseries] (title) {Research Framework};

% First Layer
\node[below=of title, box=blue!50] (A) {Input Data};
\node[right=of A, box=blue!30] (B) {Preprocessing};

% Second Layer
\node[below=of A, box=green!50] (C) {Model Training};
\node[right=of C, box=green!30] (D) {Validation};

% Arrows
\draw[-{Stealth[length=3mm]}, thick] 
  (A) edge (C) 
  (B) edge (D);
\draw[-{Stealth}, thick, color=red!70] 
  (title) -- ++(0,-2) -- (A.north);

% Annotation
\node[anchor=south west, font=\tiny] at (current bounding box.south east) 
  {Fig. 1: Research workflow with bidirectional connections};
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [ ] 图形尺寸 12cm×8cm
- [ ] 节点圆角半径 4pt
- [ ] 箭头类型 Stealth 长度 3mm
- [ ] 主色系准确度 ±10% ΔE
- [ ] 阴影偏移 2pt
- [ ] 字体大小层级匹配

### 风险与替代方案
- **颜色风险**：显示器校准差异可能导致色值偏差，建议使用Pantone色卡对应值
- **字体替代**：若系统无Source Sans Pro，可用TeX Gyre Heros替代
- **尺寸容差**：允许±5%的节点间距调整空间
- **阴影方案**：无原生阴影支持时，可用双线描边模拟
```
