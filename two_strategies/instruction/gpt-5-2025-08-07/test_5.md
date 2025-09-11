# test_5.png

![test_5.png](../../../eval_dataset/images/test_5.png)

下面给出针对所示科研绘图（二维坐标图，含散点、水平基准线与内嵌图例）的完整 LaTeX/PGFPlots 重构指南。示例尽量贴近外观，但对无法从图像唯一确定的数值给出可调参数与替代方案。

1. 概览
- 图形类型：二维坐标图（PGFPlots），含少量散点和一条水平参考线。
- 构图布局：
  - x 轴：Time to obtain the sparse trainable network (hrs)，范围约 0–7。
  - y 轴：Test accuracy (%)，范围约 55–90，水平虚线网格。
  - 绘制要素：两个散点（蓝色圆点、绿色菱形），一条黑色粗水平线（Unpruned Accuracy）。
  - 图例：置于图内右上区域，白底黑框，二维布局（2 列 × 2 行），条目依次为 IMP（三角形红色）、SynFlow（蓝色空心圆）、SNIP（绿色菱形空心）、Unpruned Accuracy（黑色实线）。
- 主要元素关系：散点分布在左侧靠近 x≈0，黑色水平线位于 y≈75–77 附近，网格仅在 y 方向显示虚线。

2. 文档骨架与依赖
- 文档类：standalone（便于独立编译与尺寸控制）。
- 核心宏包：tikz、pgfplots、xcolor。
- PGFPlots 版本：建议 compat=1.18 或更新。
- TikZ/PGFPlots 库：无强制需求；若需更精细的箭头或后续扩展，可加载 arrows.meta（本图不必需）。

3. 版面与画布设置
- 建议图形尺寸：宽 11.5–12 cm，高 3.6–4.2 cm（原图为“扁宽”比例，约 3:1）。
- 坐标系范围与比例（可调）：
  - xmin=0, xmax=7
  - ymin=55, ymax=90
  - 纵横比由 width/height 控制，无需固定 aspect ratio。
- 刻度与网格：
  - xtick 距离 1（0,1,…,7）
  - ytick 以 5 为步长（55,60,…,90）
  - ymajorgrids，虚线、浅灰色。
- 对齐与间距：
  - axis lines=box（四边框）
  - 外侧刻度，tick 长度适中（3pt 左右）
  - 图例放置在坐标系相对位置 at={(0.6,0.85)} 附近，anchor=west，可根据需要微调。
- 环境参数：使用 axis 环境；xlabel、ylabel 正常放置，ylabel 竖排。

4. 字体与配色
- 字体建议：
  - 默认 Computer Modern 已可；若需更“期刊化”观感可用 Times 系列（newtxtext,newtxmath）。
  - 轴标签与刻度：\footnotesize 或 \small；图例 \small。
- 颜色（建议近似值，HTML 十六进制）：
  - SynFlow（蓝）：#1F77B4
  - SNIP（绿）：#2CA02C
  - IMP（红）：#D62728
  - 网格线：gray!65（或 #A6A6A6）
  - 轴线/文字：黑色
- 透明度与阴影：本图无。若需，可用 opacity 或 shadings（不建议本图使用）。

5. 结构与组件样式
- 节点/标记（marks）：
  - SynFlow：空心圆 mark=o，蓝色描边，白填充，线宽≈1pt，mark size≈3–3.2pt。
  - SNIP：空心菱形 mark=diamond*（白填充，绿色描边），线宽≈0.9–1pt，mark size≈3–3.2pt。
  - IMP：实心上三角 mark=triangle*，红色填充与描边，size≈3pt；仅出现在图例中（图中未见对应点）。
- 线条：
  - Unpruned Accuracy：黑色，thick（≈1.1–1.3pt），水平线贯穿全宽。
  - 网格：仅 y 方向，dashed，浅灰。
- 坐标轴：
  - axis lines=box；tick 对外；major tick length=3pt。
  - legend：draw=black, fill=white, legend columns=2, transpose legend（按行填充），cell align=left，内边距略小（legend style 内可调 inner sep）。

6. 数学/表格/图形细节
- 本图无公式与表格；坐标轴长标签可直接使用换行或正常空格。
- 曲线/散点/参考线核心 PGFPlots 片段：
  - 散点：\addplot[only marks,<样式>] coordinates {(x,y)};
  - 水平线：\addplot[<线型>] coordinates {(xmin,y0) (xmax,y0)}; y0 为基准精度值。
- 刻度数值格式：默认 fixed；无需科学计数法。

7. 自定义宏与命令
- 建议封装样式，便于复用与统一风格：
  - 颜色：SynBlue、SnipGreen、ImpRed
  - 数据系列样式：synflow, snip, imp, unpruned
  - 轴样式：myaxis（统一尺寸、网格、刻度、图例风格）

8. 最小可运行示例 (MWE)
说明：
- 其中数值为近似占位。请根据原始数据微调两个散点坐标与水平线数值 \unprunedacc；图例位置 at= 可细调以匹配原图。
- 保留 legend-only 的 IMP 条目以复刻图例外观。

```latex
\documentclass[tikz,border=2pt]{standalone}
\usepackage{pgfplots}
\usepackage{xcolor}
% \usepackage{newtxtext,newtxmath} % 可选：若需 Times 风格，解除注释
\pgfplotsset{compat=1.18}

% ---- Colors ----
\definecolor{SynBlue}{HTML}{1F77B4}
\definecolor{SnipGreen}{HTML}{2CA02C}
\definecolor{ImpRed}{HTML}{D62728}

% ---- Styles ----
\pgfplotsset{
  myaxis/.style={
    width=11.8cm,
    height=3.9cm,
    xmin=0, xmax=7,
    ymin=55, ymax=90,
    axis lines=box,
    tick align=outside,
    major tick length=3pt,
    xtick distance=1,
    ytick={55,60,65,70,75,80,85,90},
    ymajorgrids,
    grid style={gray!65, dashed},
    xlabel={Time to obtain the sparse trainable network (hrs)},
    ylabel={Test accuracy (\%)},
    label style={font=\small},
    tick label style={font=\footnotesize},
    legend style={
      draw=black, fill=white,
      font=\small,
      legend columns=2,
      transpose legend,
      at={(0.60,0.86)}, % 依据需要微调
      anchor=west,
      cells={anchor=west},
      /tikz/every even column/.style={column sep=7pt}
    }
  },
  synflow/.style={only marks, mark=o, mark size=3.2pt, line width=1pt, draw=SynBlue, fill=white},
  snip/.style={only marks, mark=diamond*, mark size=3.2pt, line width=0.9pt, draw=SnipGreen, fill=white},
  imp/.style={only marks, mark=triangle*, mark size=3pt, draw=ImpRed, fill=ImpRed},
  unpruned/.style={black, thick}
}

% ---- Adjustable numbers ----
\pgfmathsetmacro{\unprunedacc}{76.0} % 水平基准线的 y 值（请据实调整）

\begin{document}
\begin{tikzpicture}
  \begin{axis}[myaxis]

    % Legend-only entry for IMP (appears in legend, not plotted in axes)
    \addlegendimage{imp}
    \addlegendentry{IMP}

    % SynFlow point (blue open circle) -- approximate coordinates
    \addplot[synflow] coordinates {(0.6,70)};
    \addlegendentry{SynFlow}

    % SNIP point (green open diamond) -- approximate coordinates
    \addplot[snip] coordinates {(0.15,57)};
    \addlegendentry{SNIP}

    % Unpruned Accuracy horizontal line
    \addplot[unpruned] coordinates {(0,\unprunedacc) (7,\unprunedacc)};
    \addlegendentry{Unpruned Accuracy}

  \end{axis}
\end{tikzpicture}
\end{document}
```

9. 复刻检查清单
- 图形尺寸与纵横比：width≈11.8 cm, height≈3.9 cm；是否与原图“扁宽”外观一致。
- 坐标范围与刻度：x: 0–7（步长 1）；y: 55–90（步长 5）；仅 y 方向网格、虚线、浅灰。
- 节点/边样式：蓝色空心圆、绿色空心菱形、红色实心三角（仅图例）；水平黑线粗细是否匹配。
- 字体与字号：轴标签 \small，刻度 \footnotesize，图例 \small；Times 或 CM 是否与原图一致。
- 配色与线型：蓝/绿/红近似值是否匹配；网格灰度与虚线样式是否匹配。
- 图例：白底黑框，2 列，条目顺序与排版（IMP | SynFlow / SNIP | Unpruned Accuracy）是否一致；位置是否合适。
- 特殊效果：无渐变与阴影；坐标轴边框为 box。
- 与原图差异点：散点确切坐标和水平线精确 y 值可能存在偏差；图例位置需微调；字体家族或字重可能略有差异。

10. 风险与替代方案
- 不确定因素：
  - 精确散点坐标与水平线 y 值无法从静态图像唯一反推。
  - 原图所用字体、精确颜色与线宽不可完全确认。
  - 图例的精确锚点与内边距可能有微差。
- 可接受替代：
  - 字体：默认 Computer Modern；若期刊要求 Times，启用 newtxtext,newtxmath。
  - 颜色：使用给定 HTML 色值近似；也可改用 xcolor 的 preset（e.g., RoyalBlue, ForestGreen, BrickRed）。
  - 线宽与标记尺寸：通过 thick/semithick 或 line width=⟨pt⟩ 细调。
  - 图例位置：通过 at={(..,..)} 与 anchor=.. 微调；必要时使用 legend pos=north east 并配合 xshift/yshift。
  - 若需更严谨地避免“臆造”，可将散点与水平线的 y 值提为命令参数或从外部数据表读入（\addplot table），方便后期替换为真实数据。
