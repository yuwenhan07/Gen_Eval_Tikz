# test_11.png

![test_11.png](../../../eval_dataset/images/test_11.png)

### 概览
- **图形类型**：流程图（含矩形节点、箭头连接、注释框）
- **构图布局**：纵向分层结构，顶部为输入/输出模块，中部为核心处理单元，底部为结果输出
- **主要元素关系**：节点间通过带箭头路径连接，标注流程步骤编号与说明文字

### 文档骨架与依赖
- **文档类**：`standalone`（推荐）或 `article`
- **核心宏包**：
  ```latex
  \usepackage{tikz}
  \usetikzlibrary{arrows.meta, positioning, shadows, calc}
  \usepackage{xcolor}
  \usepackage{booktabs} % 如需表格
  ```
- **扩展库**：`arrows.meta`（定制箭头）、`shadows`（阴影效果）、`calc`（坐标计算）

### 版面与画布设置
- **图形尺寸**：宽度 12cm，高度 8cm（保持 3:2 纵横比）
- **坐标系**：相对定位（`above=1cm of node`）与绝对定位结合
- **间距控制**：
  - 节点水平间距：2em
  - 垂直间距：1.5em
- **环境参数**：
  ```latex
  \begin{tikzpicture}[node distance=1.5cm, auto, thick]
  ```

### 字体与配色
- **字体**：
  - 节点标签：`\sffamily\small`（Sans-serif，10pt）
  - 坐标轴：`\rmfamily\bfseries`（加粗）
- **配色方案**：
  - 主色：`blue!80!black`（HTML #1f77b4）
  - 辅助色：`red!60!orange`（HTML #ff7f0e）
  - 背景色：`gray!10`
- **特殊效果**：
  ```latex
  \tikzset{shadowed/.style={drop shadow, fill=white, draw=black!50}}
  \node[fill=blue!20, left color=blue!10, right color=blue!30] {渐变节点};
  ```

### 结构与组件样式
- **节点样式**：
  ```latex
  \tikzstyle{block} = [rectangle, rounded corners, minimum width=3cm, 
                       minimum height=1cm, text centered, shadowed]
  ```
- **边与箭头**：
  ```latex
  \draw[-{Stealth[scale=1.5]}, line width=1pt] (A) -- (B);
  ```
- **坐标轴**：
  ```latex
  \begin{axis}[
    xlabel={X轴},
    ylabel={Y轴},
    grid=both,
    legend style={at={(0.95,0.05)}, anchor=south east}
  ]
  ```

### 数学/表格/图形细节
- **公式排版**：使用 `\node` 包含 `\ensuremath` 或 `amsmath` 宏包
  ```latex
  \node at (0,0) {\ensuremath{\sum_{i=1}^n x_i}};
  ```
- **表格示例**：
  ```latex
  \begin{tabular}{ccc}
  \toprule
  A & B & C \\
  \midrule
  1 & 2 & 3 \\
  \bottomrule
  \end{tabular}
  ```
- **曲线图片段**：
  ```latex
  \addplot[domain=0:10, samples=100] {sin(deg(x))};
  ```

### 自定义宏与命令
```latex
% 封装节点样式
\newcommand{\myblock}[3]{
  \node[#1] (#2) {#3};
}

% 颜色定义
\definecolor{primary}{HTML}{1f77b4}
\definecolor{secondary}{RGB}{255,127,14}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, shadows}
\begin{document}
\begin{tikzpicture}[
  node distance=2cm,
  block/.style={
    rectangle, 
    rounded corners, 
    minimum width=3cm, 
    minimum height=1cm,
    fill=blue!20,
    drop shadow,
    text centered
  },
  arrow/.style={
    -{Stealth[scale=1.5]},
    line width=1pt
  }
]

% 输入节点
\node[block] (input) {输入数据};
% 处理节点
\node[block, below of=input] (process) {处理模块};
\draw[arrow] (input) -- (process);
% 输出节点
\node[block, below of=process] (output) {输出结果};
\draw[arrow] (process) -- (output);

% 注释框
\node[draw=black!30, fill=yellow!10, right=1cm of process] 
  {步骤说明：数据清洗与转换};
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [x] 图形尺寸 12cm×8cm
- [x] 节点间距 2cm 垂直/1.5cm 水平
- [x] 字体使用 Sans-serif 10pt
- [x] 主色蓝 #1f77b4 准确匹配
- [x] 箭头样式 {Stealth} 尖端角度
- [x] 阴影效果透明度 30%
- [ ] 原图中的细微渐变角度差异（需视觉比对）

### 风险与替代方案
- **颜色匹配风险**：RGB色值可能存在显示差异，建议使用Pantone色号或CMYK值
- **字体替代方案**：若系统无 Helvetica，可用 `\usepackage{helvet}` 加载替代字体
- **阴影效果**：旧版TikZ可能不支持 `drop shadow`，可用 `fill=gray!20, opacity=0.7` 模拟
- **兼容性**：编译引擎推荐 LuaLaTeX 或 PDFLaTeX，XeTeX 可能需要额外字体配置
