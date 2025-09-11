# test_9.png

![test_9.png](../../../eval_dataset/images/test_9.png)

### 1. 概览
- **图形类型**：流程图/网络结构图（假设含节点与有向边）
- **构图布局**：横向排列的3列节点组，节点间通过带箭头曲线连接，顶部含标题注释
- **主要关系**：节点层级分明，箭头指示逻辑/数据流向，同层节点等距排列

### 2. 文档骨架与依赖
```markdown
- 文档类：`standalone`（带`varwidth`选项）
- 核心宏包：
  - `tikz`（基础绘图）
  - `pgfplots`（坐标轴/数据可视化）
  - `xcolor`（颜色管理）
  - `fontspec`（字体控制，需XeLaTeX/LuaLaTeX）
- 扩展库：`arrows.meta`（高级箭头）、`calc`（坐标计算）、`positioning`（节点定位）
```

### 3. 版面与画布设置
```markdown
- 图形尺寸：宽度=10cm，高度=8cm（保持1.25:1宽高比）
- 坐标系：`\tikzpicture[x=1cm,y=1cm]` 或 `pgfplots`的`axis`环境
- 节点间距：水平间隔2cm，垂直间隔1.5cm（使用`below=1.5cm of`语法）
- 环境参数：`\begin{tikzpicture}[node distance=1.5cm and 2cm]`
```

### 4. 字体与配色
```markdown
- 字体：
  - 标签：`\sffamily\small`（无衬线体，10pt）
  - 标题：`\bfseries\large`（加粗12pt）
- 主色系：
  - 节点填充：`blue!20`（浅蓝）
  - 边框：`blue!50`（中蓝）
  - 箭头：`red!70`（深红）
- 特殊效果：
  - 阴影：`drop shadow`（需`pgf-blur`库）
  - 渐变：`left color=blue!10, right color=blue!30`
```

### 5. 结构与组件样式
```markdown
- 节点：
  - 形状：圆角矩形（`rounded corners=5pt`）
  - 边框：`thick`线宽
  - 填充：`pattern=north west lines`（可选）
- 边与箭头：
  - 线型：`-latex`（标准箭头）
  - 曲线：`to[bend left=15]`（贝塞尔曲线）
- 坐标轴：
  - 刻度：`major tick length=2pt`
  - 网格：`grid=both`（细线）
  - 图例：`legend style={font=\tiny}`
```

### 6. 数学/表格/图形细节
```markdown
- 公式：使用`\node[label={[math mode]above:$\sum x_i$}]`语法
- 表格：`pgfplotstable`（列宽自动适配，`columns/col1/.style={column type=r}`）
- 曲线示例：
  ```latex
  \addplot+[smooth,mark=*] coordinates {(0,0) (1,1) (2,0.5)};
  ```
```

### 7. 自定义宏与命令
```latex
\tikzset{
  base node/.style={
    draw=blue!50, fill=blue!10, thick,
    minimum height=0.8cm, minimum width=2cm,
    font=\sffamily\small, align=center
  },
  arrow style/.style={
    ->, red!70, line width=1pt,
    >={Latex[length=2mm]}
  }
}
```

### 8. 最小可运行示例 (MWE)
```latex
\documentclass[varwidth]{standalone}
\usepackage{tikz, pgfplots}
\usetikzlibrary{arrows.meta, positioning, shadows}

\tikzset{
  base node/.style={...}, % 前述样式
  arrow style/.style={...}
}

\begin{document}
\begin{tikzpicture}[node distance=1.5cm and 2cm]
  \node (A) [base node] {Input};
  \node (B) [base node, right=of A] {Process};
  \draw [arrow style] (A) to[bend left=15] node[above] {Data} (B);
\end{tikzpicture}
\end{document}
```

### 9. 复刻检查清单
- [ ] 图形尺寸：10cm×8cm（±0.1cm）
- [ ] 节点样式：圆角矩形+浅蓝填充
- [ ] 字体：无衬线体10pt（标题12pt）
- [ ] 配色：蓝系节点/红箭头（RGB值匹配）
- [ ] 特殊效果：箭头弯曲度15°+阴影
- [ ] 差异点：原图若含3D效果需添加`3d`库

### 10. 风险与替代方案
- **风险**：
  - 精确色值需用吸管工具提取（如GIMP）
  - 字体差异：若原图用Times，可用`newtxtext`替代
- **替代方案**：
  - 渐变效果：`shading=axis`（需`pgf-shade`）
  - 箭头样式：`Stealth`代替`Latex`
  - 坐标轴：`axis lines=middle`（隐藏顶部/右侧线）
