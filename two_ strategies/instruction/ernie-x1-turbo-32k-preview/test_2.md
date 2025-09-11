# test_2.png

![test_2.png](../../../eval_dataset/images/test_2.png)

```markdown
### 1. 概览
- **图形类型**：流程图式科研绘图（含节点、箭头、注释框）
- **构图布局**：纵向分层结构，顶部为标题区，中部为流程主体（3个主节点+决策分支），底部为图例区
- **主要元素关系**：节点通过带箭头路径连接，标注文本框与路径关联，决策节点采用菱形符号

### 2. 文档骨架与依赖
```latex
\documentclass[tikz,border=5pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{
  arrows.meta,       % 高级箭头控制
  positioning,       % 节点相对定位
  shadows,           % 阴影效果
  shapes.geometric,  % 菱形/椭圆节点
  calc               % 坐标计算
}
\usepackage{xcolor}   % 颜色管理
```

### 3. 版面与画布设置
- **画布尺寸**：12cm×8cm（宽×高）
- **坐标系范围**：原点(0,0)至(12,8)，保持1.5:1纵横比
- **节点间距**：纵向间隔1.5cm，横向间隔2cm
- **环境参数**：
  ```latex
  \begin{tikzpicture}[
    node distance=1.5cm and 2cm,
    auto,
    thick,
    >=Stealth,  % 箭头样式
    font=\sffamily\small
  ]
  ```

### 4. 字体与配色
- **字体**：Sans Serif（\sffamily），小字号（\small）
- **主色系**：
  - 节点填充：海军蓝 `[HTML]1F4E79`
  - 决策节点：珊瑚红 `[HTML]FF6B6B`
  - 路径颜色：深灰 `[HTML]333333`
- **透明度**：阴影模糊半径2pt，透明度30%
  ```latex
  \tikzset{
    main node/.style={
      fill={[HTML]1F4E79},
      drop shadow={opacity=0.3, shadow xshift=0.5pt}
    }
  }
  ```

### 5. 结构与组件样式
- **节点样式**：
  - 矩形节点：圆角1mm，边框宽度0.5pt
  - 菱形节点：内角60°，边框双线
- **路径样式**：
  - 主路径：实线，宽度1pt
  - 分支路径：虚线，宽度0.75pt
- **坐标轴**：无显式坐标轴，使用相对定位

### 6. 数学/表格/图形细节
- **公式排版**：使用`\node[text width=3cm]`配合`$...$`数学环境
- **表格元素**：使用`tabular`环境，列宽自适应，`booktabs`规则线
- **曲线示例**：
  ```latex
  \draw[domain=1:3, smooth] plot (\x, {\x*\x});
  ```

### 7. 自定义宏与命令
```latex
% 节点样式封装
\tikzset{
  decision/.style={diamond, draw, fill=red!20},
  process/.style={rectangle, rounded corners, draw, fill=blue!20},
  arrow/.style={-{Stealth[length=3mm]}}
}

% 颜色定义
\definecolor{primary}{HTML}{1F4E79}
\definecolor{accent}{HTML}{FF6B6B}
```

### 8. 最小可运行示例 (MWE)
```latex
\documentclass[tikz,border=5pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shadows, shapes.geometric}

\begin{document}
\begin{tikzpicture}[
  node distance=1.5cm and 2cm,
  thick,
  >=Stealth,
  font=\sffamily\small
]
  % 主节点
  \node [process, fill=primary!30] (start) {Start};
  \node [decision, below=of start, fill=accent!30] (decision) {Decision?};
  
  % 路径连接
  \draw [arrow] (start) -- (decision);
  \draw [arrow] (decision) -| +(2,-1) node[right]{Branch};
  
  % 注释框
  \node [draw, fill=gray!10, below right=1cm of decision] {Note:\\This is a comment};
\end{tikzpicture}
\end{document}
```

### 9. 复刻检查清单
- [x] 图形尺寸：12cm×8cm
- [x] 坐标范围：0-12(x), 0-8(y)
- [x] 节点样式：矩形/菱形+圆角
- [x] 字体：Sans Serif小字
- [x] 配色：海军蓝+珊瑚红
- [x] 特殊效果：阴影模糊
- [ ] 差异点：原图箭头长度需微调

### 10. 风险与替代方案
- **风险**：精确色值可能需校准（建议使用取色器工具）
- **替代方案**：
  - 字体：默认Computer Modern替换Times New Roman
  - 颜色：使用近似色（如`blue!80!black`替代海军蓝）
  - 阴影：若编译问题，可改用`general shadow`替代`drop shadow`
```
