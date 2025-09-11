# test_15.png

![test_15.png](../../../eval_dataset/images/test_15.png)

### 概览
- **图形类型**：流程图（含矩形节点与箭头连接）
- **布局特征**：纵向排列，节点间等距垂直对齐，箭头带方向标记
- **核心关系**：输入→处理→输出三级结构，箭头标注流程类型（如“计算”“验证”）

### 文档骨架与依赖
```latex
\documentclass[crop,12pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shadows}
\usepackage{xcolor}
\usepackage{booktabs}
```
- **特殊功能依赖**：`arrows.meta`库定制箭头样式，`shadows`库添加阴影效果

### 版面与画布设置
```latex
\begin{tikzpicture}[
    node distance=1.5cm and 2cm,
    scale=1.0,
    every node/.style={scale=0.9}
]
```
- **画布尺寸**：自动适配内容（standalone特性）
- **坐标系范围**：隐式通过节点位置确定，建议使用`[xshift=2cm]`等相对定位
- **对齐控制**：`above=of`和`right=of`实现精确垂直/水平对齐

### 字体与配色
- **字体设置**：`\sffamily`无衬线体，字号12pt，正常粗细
- **主色系**：
  - 节点填充：`blue!20`（浅蓝）
  - 边框色：`blue!50`
  - 箭头色：`red!70`
- **特殊效果**：
  ```latex
  \tikzset{
    shadowed/.style={drop shadow, fill=white, draw=black},
    gradient/.style={left color=blue!10, right color=blue!30}
  }
  ```

### 结构与组件样式
```latex
% 节点样式
\tikzstyle{block} = [
  rectangle, 
  rounded corners,
  minimum width=3cm, 
  minimum height=1cm,
  gradient,
  shadowed,
  align=center
]

% 箭头样式
\tikzset{
  flow/.style={
    -Stealth,
    line width=1pt,
    red!70
  }
}
```
- **坐标轴配置**：流程图无需坐标轴，若需网格可添加`grid=major`

### 数学/表格/图形细节
- **公式嵌入**：节点内使用`$E=mc^2$`直接排版
- **表格集成**：
  ```latex
  \node[block] (table) {
    \begin{tabular}{ccc}
      \toprule
      A & B & C \\
      \midrule
      1 & 2 & 3 \\
      \bottomrule
    \end{tabular}
  };
  ```

### 自定义宏与命令
```latex
\newcommand{\procnode}[3]{
  \node[block, #1] (#2) {#3};
}

\newcommand{\flowarrow}[3]{
  \draw[flow] (#1) -- node[above] {#3} (#2);
}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[crop,12pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shadows}
\usepackage{booktabs}

\begin{document}
\begin{tikzpicture}[node distance=1.5cm]
  \tikzstyle{block} = [rectangle, rounded corners, minimum width=3cm, 
                      minimum height=1cm, fill=blue!20, draw=blue!50,
                      drop shadow, align=center]
  \tikzset{flow/.style={-Stealth, line width=1pt, red!70}}
  
  \node[block] (A) {输入数据};
  \node[block, below=of A] (B) {计算过程};
  \node[block, below=of B] (C) {验证结果};
  
  \draw[flow] (A) -- node[right] {流程1} (B);
  \draw[flow] (B) -- node[right] {流程2} (C);
  
  % 添加表格节点
  \node[block, right=of A] (T) {
    \begin{tabular}{cc}
      \toprule
      参数 & 值 \\
      \midrule
      X & 10 \\
      Y & 20 \\
      \bottomrule
    \end{tabular}
  };
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [ ] 图形尺寸与原图比例一致
- [ ] 节点间距垂直/水平对齐
- [ ] 字体使用无衬线体且字号统一
- [ ] 配色方案匹配原图色值
- [ ] 箭头线宽与样式一致
- [ ] 阴影效果与透明度设置

### 风险与替代方案
- **色值不确定性**：若原图RGB值无法精确获取，可使用`blue!30`等近似色阶
- **字体兼容性**：系统默认字体差异可通过`\usepackage{mathptmx}`切换Times字体
- **阴影效果**：部分编译环境可能不支持`drop shadow`，可改用`fill=gray!20`替代
