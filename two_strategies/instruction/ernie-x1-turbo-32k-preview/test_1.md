# test_1.png

![test_1.png](../../../eval_dataset/images/test_1.png)

```markdown
### 概览
- **图形类型**：流程图式网络结构，含节点矩阵与定向箭头连接
- **布局特征**：三列垂直对齐节点组，横向跨列连接箭头，顶部标题框
- **元素关系**：输入层→隐藏层→输出层的层级传递，权重标注箭头

### 文档骨架与依赖
- **文档类**：`standalone`
- **核心宏包**：`tikz`、`pgfplots`、`xcolor`、`fontspec`(可选)、`array`
- **TikZ库**：`arrows.meta`、`positioning`、`calc`、`matrix`
- **扩展需求**：渐变填充需`shadings`库，三维效果需`3d`库

### 版面与画布设置
- **画布尺寸**：12cm×8cm (宽×高)
- **坐标系**：`[x=1cm,y=1cm]`
- **节点间距**：列间距2.5cm，行间距1.5cm
- **环境参数**：
  ```latex
  \begin{tikzpicture}[node distance=1.5cm and 2.5cm]
  ```

### 字体与配色
- **字体配置**：
  - 节点标签：`\sffamily\footnotesize`
  - 标题框：`\bfseries\large`
  - 坐标轴：`\scriptsize`
- **主色系**：
  - 节点边框：`HTML 2E86C1`
  - 填充渐变：`top=HTML 64B5F6, bottom=HTML 2E86C1`
  - 箭头：`HTML FF5722`
- **透明效果**：`opacity=0.8`
- **阴影语法**：`drop shadow={opacity=0.3,shadow scale=1.05}`

### 结构与组件样式
- **节点样式**：
  - 矩形节点：`rounded corners=3pt, draw=frame_blue, thick`
  - 矩阵节点：`matrix of nodes, nodes={anchor=center}`
- **边样式**：
  - 箭头类型：`-{Stealth[scale=1.2]}`
  - 权重标注：`midway, fill=white, font=\tiny`
- **坐标轴**：
  - 网格线：`grid=both, major grid style={dotted, gray!30}`
  - 图例：`legend style={draw=none, font=\tiny}`

### 数学/表格/图形细节
- **公式排版**：使用`\ensuremath`包裹数学符号
- **表格实现**：`tabular`环境配合`array`宏包，列宽`p{2cm}`
- **PGFPlots片段**：
  ```latex
  \begin{axis}[axis lines=none, width=4cm, height=3cm]
  \addplot[smooth, domain=0:1, blue!30] {x^2};
  \end{axis}
  ```

### 自定义宏与命令
```latex
\tikzset{
  base node/.style={rectangle, align=center, font=\sffamily\footnotesize},
  layer node/.style={base node, rounded corners=3pt, draw=frame_blue, thick, fill=blue!10},
  weight arrow/.style={-Stealth, thick, red!70, shorten >=2pt, shorten <=2pt}
}
\newcommand{\layermatrix}[2]{
  \matrix (#1) [matrix of nodes, nodes={layer node}, column sep=0.3cm] {#2};
}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{arrows.meta, positioning, matrix, shadings}
\begin{document}
\begin{tikzpicture}[node distance=1.5cm and 2.5cm]
  
  % Input Layer
  \layermatrix{input}{ 
    {[fill=blue!5]} 1 & 2 & 3 \\
    {[fill=blue!5]} 4 & 5 & 6 \\
  };
  
  % Hidden Layer
  \node[layer node, right=of input] (hidden) {Hidden\\Unit};
  
  % Output Layer
  \node[layer node, right=of hidden] (output) {Output\\Layer};
  
  % Connections
  \draw[weight arrow] (input) -- node[weight label] {$w_1$} (hidden);
  \draw[weight arrow] (hidden) -- node[weight label] {$w_2$} (output);
  
  % Title Box
  \node[above=0.5cm, draw=gray!50, fill=gray!10, rounded corners, font=\bfseries\large] (title) {Neural Network Architecture};
  
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [ ] 图形尺寸精确匹配（12cm×8cm）
- [ ] 节点间距误差≤0.1cm
- [ ] 字体样式与字号一致性
- [ ] 颜色匹配度（ΔE≤5）
- [ ] 箭头类型与权重标注位置
- [ ] 渐变填充方向与透明度
- [ ] 阴影效果与三维投影

### 风险与替代方案
- **色值风险**：屏幕色差可能导致实际印刷色偏，建议使用Pantone色卡校准
- **字体替代**：若系统缺失指定字体，可用`\renewcommand\sfdefault{phv}`加载Helvetica
- **渐变替代**：无法实现精确渐变时，可用中间色`HTML 4A9EDA`单色填充
- **箭头样式**：`Stealth`箭头不可用时，改用`Triangle`箭头加`scale=1.5`
```
