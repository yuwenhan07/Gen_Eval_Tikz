# test_4.png

![test_4.png](../../../eval_dataset/images/test_4.png)

```markdown
### 概览
- **图形类型**：流程图式网络结构图，含分层节点与定向连接箭头
- **构图布局**：三层垂直布局（输入层/隐藏层/输出层），水平对称分布
- **主要元素**：矩形节点（带标签）、带箭头连接线、分组框、注释文本

### 文档骨架与依赖
```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{arrows.meta, positioning, fit, backgrounds}
\usepackage{xcolor}
\usepackage{fontspec} % 如需特定字体
```
- **核心扩展**：arrows.meta（箭头定制）、positioning（节点定位）、fit（分组框）

### 版面与画布设置
```latex
\begin{tikzpicture}[
    node distance=1.5cm and 2cm, % 垂直/水平间距
    scale=1.2, % 整体缩放
    every node/.style={inner sep=4pt, outer sep=2pt}
]
```
- **画布尺寸**：默认自动适配内容，建议设置`[scale=1.2]`
- **坐标系**：隐式笛卡尔坐标系，原点(0,0)位于左下
- **对齐方式**：基线对齐，分组框使用fit库自动调整

### 字体与配色
- **字体**：主标签\scriptsize（9pt），注释\tiny（7pt），Sans Serif族
- **主色系**：
  - 节点边框：`blue!70!black`
  - 填充色：`blue!10`（输入层），`green!10`（隐藏层）
  - 箭头：`red!60`
- **渐变示例**：`\shade[left color=blue!10, right color=blue!30]`

### 结构与组件样式
- **节点**：
  ```latex
  \node[draw, rectangle, rounded corners, fill=blue!10] (node1) {Input 1};
  ```
- **连接线**：
  ```latex
  \draw[-{Stealth[scale=1.2]}, thick, red!60] (node1) -- (node2);
  ```
- **分组框**：
  ```latex
  \node[draw, dashed, fit=(node1)(node2), inner sep=8pt] (group1) {};
  ```

### 数学/表格/图形细节
- **公式集成**：使用`$\int_0^1 f(x)dx$`直接在节点文本中嵌入
- **表格示例**：
  ```latex
  \node[anchor=center] {\begin{tabular}{c|c} 1 & 2 \\ \hline 3 & 4 \end{tabular}};
  ```

### 自定义宏与命令
```latex
\tikzset{
  base_node/.style={draw, rectangle, rounded corners, minimum width=1.8cm},
  input_node/.style={base_node, fill=blue!10},
  hidden_node/.style={base_node, fill=green!10},
  arrow_red/.style={-{Stealth[scale=1.2]}, thick, red!60}
}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usetikzlibrary{arrows.meta, positioning, fit}
\begin{document}
\begin{tikzpicture}[node distance=1.5cm and 2cm]
  % Input layer
  \node[draw, rectangle, fill=blue!10] (in1) {Input 1};
  \node[draw, rectangle, fill=blue!10, right=of in1] (in2) {Input 2};
  
  % Hidden layer
  \node[draw, rectangle, fill=green!10, below=of in1] (hid1) {Hidden};
  \draw[-{Stealth[scale=1.2]}, thick, red!60] (in1) -- (hid1);
  \draw[-{Stealth[scale=1.2]}, thick, red!60] (in2) -- (hid1);
  
  % Output layer
  \node[draw, rectangle, below=of hid1] (out) {Output};
  \draw[-{Stealth[scale=1.2]}, thick, red!60] (hid1) -- (out);
  
  % Grouping
  \node[draw, dashed, inner sep=8pt, fit=(in1)(in2)] {};
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [x] 图形尺寸：自动适配内容，缩放比例1.2
- [x] 节点样式：圆角矩形+填充色+边框
- [x] 箭头类型：Stealth箭头，红色渐变
- [x] 字体系统：Sans Serif，标签9pt
- [x] 特殊效果：分组虚线框
- [ ] 差异点：原图可能含阴影，需添加`drop shadow`选项

### 风险与替代方案
- **色值不确定**：使用近似色`blue!70!black`替代精确CMYK值
- **字体差异**：默认使用Latin Modern，替代Times New Roman需`fontspec`
- **阴影兼容性**：`shadows`库可能增加编译时间，可省略或用`opacity=0.2`替代
```
