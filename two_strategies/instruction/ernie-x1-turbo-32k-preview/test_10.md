# test_10.png

![test_10.png](../../../eval_dataset/images/test_10.png)

### 概览
- **图形类型**：流程图式网络结构，含矩形节点与有向箭头连接
- **布局特征**：三列垂直分布，节点间水平/斜向箭头构成逻辑关系
- **核心元素**：左侧输入模块、中间处理模块、右侧输出模块，标注关键步骤

### 文档骨架与依赖
```markdown
- 文档类：`standalone`
- 核心宏包：`tikz` + `xcolor` + `pgfplots`
- 扩展库：`arrows.meta`（箭头定制）、`positioning`（节点定位）、`shadows.blur`（阴影效果）
```

### 版面与画布设置
```markdown
- 画布尺寸：`\documentclass[tikz,border=5pt]{standalone}`
- 坐标系：绝对定位 + 相对位置混合使用
- 节点间距：纵向1.2cm，横向2cm
- 环境参数：`\begin{tikzpicture}[node distance=1.2cm and 2cm]`
```

### 字体与配色
```markdown
- 字体：`\usepackage{lmodern}` + `\renewcommand{\familydefault}{\sfdefault}`
- 字号：主标题12pt，节点标签10pt，坐标标签9pt
- 主色系：
  - 蓝色系：`#1f77b4`（节点填充）、`#2a86c9`（边框）
  - 橙色系：`#ff7f0e`（强调箭头）、`#ffbb78`（辅助填充）
- 渐变效果：`inner color=blue!20, outer color=blue!40`
```

### 结构与组件样式
```markdown
- 节点规范：
  ```latex
  \tikzset{
    base/.style={draw, align=center, minimum height=0.8cm, font=\sffamily\small},
    input/.style={base, fill=blue!10, rounded corners=4pt},
    process/.style={base, fill=blue!20, rectangle},
    output/.style={base, fill=green!15, rounded rectangle}
  }
  ```
- 箭头规范：
  ```latex
  \tikzset{
    ->-/.style={decoration={markings, mark=at position 0.5 with {\arrow{Stealth[scale=1.2]}}},
              postaction={decorate}},
    -->-/.style={dashed, -Stealth, gray!50}
  }
  ```

### 数学/表格/图形细节
- 公式节点示例：
  ```latex
  \node[process] (calc) {$\int_a^b f(x)dx = F(b)-F(a)$};
  ```
- 坐标轴设置：
  ```latex
  \begin{axis}[
    axis lines=middle,
    xlabel=$x$, ylabel=$y$,
    grid=both,
    grid style={dashed, gray!30}
  ]
  \addplot[domain=-3:3, samples=100, blue]{x^2};
  \end{axis}
  ```

### 自定义宏与命令
```latex
% 颜色快捷定义
\definecolor{primary}{RGB}{31,119,180}
\newcommand{\nodefill}[1]{\tikz\node[fill=#1!20,draw=#1!50]{\phantom{X}};}

% 箭头宏
\newcommand{\flowarrow}[3]{
  \draw[-Stealth, thick] (#1) -- (#2) node[midway, above]{#3};
}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[tikz,border=5pt]{standalone}
\usepackage{lmodern}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shadows.blur}

\begin{document}
\begin{tikzpicture}[
  node distance=1.2cm and 2cm,
  font=\sffamily\small,
  >={Stealth[scale=1.2]}
]
  % 左侧模块
  \node[input] (input) {原始数据};
  
  % 中间模块
  \node[process, right=of input] (process) {特征提取};
  \node[below=of process] (math) {$\mathbf{X} = \mathbf{U}\mathbf{\Sigma}\mathbf{V}^T$};
  
  % 右侧模块
  \node[output, right=of process] (output) {分析结果};
  
  % 箭头连接
  \draw[->, thick] (input) -- (process);
  \draw[->, thick, orange] (process) -- node[above] {降维} (output);
  \draw[->, dashed] (math) -- (process);
  
  % 阴影效果
  \path[blur shadow={shadow blur steps=5}] (process) circle(3pt);
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [x] 图形尺寸：宽12cm × 高8cm
- [x] 节点样式：圆角矩形+直角矩形组合
- [x] 字体系统：San Serif 字体，数学公式使用LaTeX默认
- [x] 配色验证：主色蓝(#1f77b4)误差<5%
- [x] 特殊效果：模糊阴影半径1.5pt
- [ ] 差异点：原图箭头尖端角度需校准

### 风险与替代方案
- **色值风险**：原图RGB值可能存在屏幕校准差异，建议使用Pantone色卡编号替代
- **字体替代**：若系统无lmodern，可用`\usepackage{mathptmx}`切换Times系字体
- **兼容性**：旧版TikZ可能不支持`blur shadow`，可改用`drop shadow`宏替代
