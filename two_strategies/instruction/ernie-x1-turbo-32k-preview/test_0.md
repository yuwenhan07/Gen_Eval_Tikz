# test_0.png

![test_0.png](../../../eval_dataset/images/test_0.png)

```markdown
### 1. 概览
- **图形类型**：流程图（含矩形节点、箭头连接、标注框）
- **布局特征**：水平分层结构，主流程从左至右延伸，子流程垂直分支
- **核心元素关系**：主节点通过带箭头实线连接，辅助说明框通过虚线箭头关联主流程

### 2. 文档骨架与依赖
```latex
\documentclass[tikz]{standalone}
\usepackage{xcolor}
\usetikzlibrary{arrows.meta, positioning, shadows, calc}
```
- **必要扩展**：`arrows.meta`（自定义箭头）、`positioning`（精确定位）、`shadows`（阴影效果）、`calc`（坐标计算）

### 3. 版面与画布设置
```latex
\begin{tikzpicture}[
  node distance=1.5cm and 2cm,
  scale=1.2,
  transform shape,
  every node/.style={align=center}
]
```
- **画布尺寸**：宽度=15cm，高度=8cm
- **坐标系**：原点(0,0)位于左下，x轴范围0-14，y轴范围0-7
- **对齐策略**：主节点水平对齐（`on grid`），子节点垂直居中（`above/below`）

### 4. 字体与配色
- **字体配置**：
  - 节点标签：`\sffamily\small`（10pt）
  - 坐标轴标题：`\bfseries\scriptsize`（9pt加粗）
- **主色系**：
  - 节点边框：`RoyalBlue!80!black`
  - 填充渐变：`top color=SkyBlue!30, bottom color=RoyalBlue!10`
- **辅助色**：
  - 标注框：`BurntOrange!20`（填充）+ `Sepia!50`（边框）
  - 箭头：`DarkGreen!70`（实线）+ `Red!40`（虚线）
- **特殊效果**：
  - 阴影：`drop shadow={opacity=0.3, shadow xshift=2pt}`
  - 透明度：`opacity=0.8`（标注框填充）

### 5. 结构与组件样式
- **节点规范**：
  - 形状：`rectangle`（主流程）、`rounded rectangle`（子流程）、`ellipse`（决策点）
  - 边框：`line width=0.8pt`
  - 填充：双色渐变（`inner color`与`outer color`）
- **边与箭头**：
  - 主流程箭头：`-{Stealth[length=3mm]}`
  - 虚线箭头：`-{Latex[open]..}`
  - 线宽：`very thick`（主流程）、`thin`（虚线）
- **坐标轴**：
  - 刻度：`major tick length=4pt`
  - 网格：`minor grid style=dashed`
  - 图例：`legend style={draw=none, fill=none}`

### 6. 数学/表格/图形细节
- **公式排版**：使用`amsmath`宏包，节点内`$$...$$`环境
- **表格集成**：
  ```latex
  \matrix[table,{column sep=5mm,row sep=3mm}]
  ```
- **曲线示例**（PGFPlots）：
  ```latex
  \begin{axis}[domain=0:10, samples=50]
    \addplot {sin(deg(x))};
  \end{axis}
  ```

### 7. 自定义宏与命令
```latex
\tikzset{
  mainnode/.style={
    draw=RoyalBlue, thick, rounded corners=0.5cm,
    inner sep=10pt, fill=blue!10,
    drop shadow
  },
  arrowstyle/.style={
    -{Stealth[]}, thick, DarkGreen
  }
}
```

### 8. 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{arrows.meta, shadows}
\begin{document}
\begin{tikzpicture}[
  node distance=2cm,
  mainnode/.style={
    draw=RoyalBlue, thick, rounded corners=0.5cm,
    inner sep=10pt, fill=blue!10,
    drop shadow
  },
  arrowstyle/.style={
    -{Stealth[]}, thick, DarkGreen
  }
]
  % 主流程节点
  \node[mainnode] (A) {Input\\Data};
  \node[mainnode, right=of A] (B) {Processing\\Stage};
  \node[mainnode, right=of B] (C) {Output\\Results};
  
  % 箭头连接
  \draw[arrowstyle] (A) -- (B);
  \draw[arrowstyle] (B) -- (C);
  
  % 标注框
  \node[draw=Sepia, fill=BurntOrange!20, dashed, above right=1cm and 0.5cm of B] 
    (D) {Validation\\Check};
  \draw[-{Latex[open]}, thin, Red!40] (B) to[bend left] (D);
\end{tikzpicture}
\end{document}
```

### 9. 复刻检查清单
- [ ] 图形尺寸：15cm×8cm
- [ ] 节点样式：圆角矩形+渐变填充
- [ ] 字体：无衬线体10pt
- [ ] 配色：主色RoyalBlue系+辅助色BurntOrange
- [ ] 特殊效果：阴影+透明度
- [ ] 差异点：原图箭头角度需微调

### 10. 风险与替代方案
- **不确定性**：
  - 精确色值可能需光谱仪校准（建议使用Pantone色卡替代）
  - 字体渲染差异（Linux系统默认CM与Windows Times差异）
- **替代方案**：
  - 字体：`\usepackage{mathptmx}`替代Times New Roman
  - 颜色：近似色替换（如`RoyalBlue`→`#4169E1`）
  - 阴影：`blur shadow`库替代传统阴影
```
