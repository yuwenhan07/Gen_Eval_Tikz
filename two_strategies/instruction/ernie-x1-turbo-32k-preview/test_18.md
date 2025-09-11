# test_18.png

![test_18.png](../../../eval_dataset/images/test_18.png)

```markdown
### 概览
- **图形类型**：三维曲面坐标图 + 颜色映射条 + 坐标轴标注
- **构图布局**：三维曲面占据主区域，右侧垂直颜色条，坐标轴标注在三维空间中倾斜显示
- **主要元素关系**：曲面高度与颜色映射关联，坐标轴标注与曲面网格线对齐

### 文档骨架与依赖
- **文档类**：`standalone`
- **核心宏包**：`pgfplots`（三维绘图）、`xcolor`（颜色控制）、`tikz`（底层绘图）
- **TikZ库**：`3d`、`perspective`、`calc`（三维坐标计算）

### 版面与画布设置
- **图形尺寸**：宽=12cm，高=8cm
- **坐标系范围**：x=[-3,3], y=[-3,3], z=[0,3]
- **画布参数**：`\begin{tikzpicture}[perspective={p={(10,5,5)},q={(0,10,0)}}]`
- **节点间距**：颜色条与主图间距=5mm，坐标轴标签与轴间距=3mm

### 字体与配色
- **字体**：`\sffamily\footnotesize`（无衬线小脚注字体）
- **主色**：`#1f77b4`（曲面基础色），辅助色`#ff7f0e`（高亮网格线）
- **渐变/透明度**：曲面使用`shader=interp`平滑着色，透明度`opacity=0.8`

### 结构与组件样式
- **节点**：坐标轴标签使用`anchor=south west`对齐
- **边与箭头**：网格线`line width=0.3pt`，坐标轴箭头`->`样式
- **坐标轴**：刻度标签`tick label style={font=\tiny}`，网格线`grid=major`

### 数学/图形细节
- **曲面公式**：`z = exp(-x^2-y^2)*sin(2*x)*cos(3*y)`
- **PGFPlots核心片段**：
  ```latex
  \addplot3[
    surf,
    domain=-3:3,
    samples=50,
    colormap/viridis,
    shader=interp
  ] {exp(-x^2-y^2)*sin(2*x)*cos(3*y)};
  ```

### 自定义宏与命令
```latex
% 颜色映射条样式
\pgfplotsset{colorbar style={
    title={$z$},
    width=2mm,
    ytick={0,1,2,3},
    yticklabels={0,1,2,3}
}}

% 坐标轴样式
\pgfplotsset{every axis/.append style={
    axis line style={line width=0.6pt},
    tick align=outside
}}
```

### 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}
\usepgfplotslibrary{colormaps,3d}

\begin{document}
\begin{tikzpicture}[perspective={p={{10,5,5}},q={0,10,0}}]
\begin{axis}[
    view={45}{30},
    xlabel={$x$}, ylabel={$y$}, zlabel={$z$},
    xmin=-3, xmax=3,
    ymin=-3, ymax=3,
    zmin=0, zmax=3,
    grid=both,
    grid style={line width=0.2pt, draw=gray!30},
    axis lines=box,
    axis line style={line width=0.7pt},
    tick align=outside,
    tick label style={font=\tiny},
    colormap/viridis,
    colorbar,
    colorbar style={
        title={$z$},
        width=2mm,
        ytick={0,1,2,3},
        yticklabels={0,1,2,3}
    }
]
\addplot3[
    surf,
    domain=-3:3,
    samples=50,
    shader=interp,
    opacity=0.8
] {exp(-x^2-y^2)*sin(2*x)*cos(3*y)};
\end{axis}
\end{tikzpicture}
\end{document}
```

### 复刻检查清单
- [x] 图形尺寸：12cm×8cm
- [x] 坐标范围：x/y/z=[-3,3]/[-3,3]/[0,3]
- [x] 节点样式：坐标轴标签对齐正确
- [x] 配色方案：viridis色图匹配
- [x] 特殊效果：曲面平滑着色+透明度
- [x] 差异点：原图网格线密度需调整`samples`参数

### 风险与替代方案
- **色值风险**：原图可能使用非标准色图，建议使用`colormap/viridis`作为标准替代
- **字体替代**：若原图字体不可用，使用`\sffamily`无衬线字体族替代
- **三维视角**：原图视角可能需微调`view={45}{30}`参数匹配
- **网格密度**：`samples`参数可根据原图细节调整（50为推荐起始值）
```
