# test_8.png

![test_8.png](../../../eval_dataset/images/test_8.png)

以下是基于所给图片的“图像到 LaTeX/TikZ 复刻”完整指导。目标是复刻一个单块系统框图：左侧输入线标注 |f⟩（上方）与 Inputs（下方），中间矩形块标注 M(L)，右侧输出线标注 L|f⟩ = |f′⟩（上方）与 Outputs（下方）。无箭头，细线，黑白配色。

1. 概览
- 图形类型：简洁的单块框图（系统/算子示意）。
- 布局：
  - 水平居中矩形块，左右各有一条水平连线。
  - 上方为数学标签（ket 记号），下方为文字说明（Inputs/Outputs）。
- 元素关系：
  - 左线 → 方块 → 右线（仅连线，无箭头）。
  - 方块内为算子名 M(L)（数学斜体）。
  - 右侧上方为变换关系 L|f⟩ = |f′⟩，L 为粗体。

2. 文档骨架与依赖
- 推荐文档类：standalone（便于独立编译与裁边）。
- 宏包：
  - tikz（主绘图）
  - amsmath, amssymb（数学排版）
  - xcolor（若需定义颜色）
- TikZ 库：
  - positioning（便捷定位）
  - calc（可选，便于坐标计算）
  - arrows.meta（可选；本图不需要箭头，但若后续扩展可用）
- 若希望快速使用 bra-ket 记号，也可选 physics 或 braket。为最小依赖，下文用自定义宏 \ket。

3. 版面与画布设置
- 建议整体尺寸：宽约 10 cm，高约 4 cm（与原图观感接近）。
- 坐标系与纵横比：
  - 以 x=1cm, y=1cm 设定，矩形块中心置于 (0,0)。
  - 左右连线端点建议在 x=±4.0，y=0。
- 方块尺寸：宽约 3.2 cm，高约 2.0 cm（即半宽 1.6、半高 1.0）。
- 标签间距与对齐：
  - 线上数学标签：在线段中点，above=4pt。
  - 线上文字标签：在线段中点，below=4pt。
  - 线、方块居中对齐。
- \tikzpicture 参数：建议 font=\small 统一字号；baseline 用于与外部文字对齐（可选）。

4. 字体与配色
- 字体：
  - 数学：默认 Computer Modern（standalone + amsmath 即可）。
  - 正文（Inputs/Outputs）：默认 Roman；与数学风格协调。
- 颜色：
  - 纯黑：black（#000000）。
  - 本图无渐变、透明或阴影；如需轻微变体，可使用 line width 与 gray!xx，但原图为纯黑细线。
- 若需统一更接近 Times 风格：可改用 newtxtext,newtxmath 或使用 LuaLaTeX/XeLaTeX + unicode-math。

5. 结构与组件样式
- 节点（方块）：
  - 形状：矩形，细边框，无填充。
  - 边框粗细：line width=0.4pt（与默认细线接近）。
  - 内部文字：$M(L)$（数学模式，斜体）。
- 连线：
  - 水平直线，无箭头。
  - 粗细：line width=0.4pt。
- 标签：
  - 线上方数学标签：左段 $\ket{f}$；右段 $\mathbf{L}\ket{f}=\ket{f'}$。
  - 线下方文字标签：左段 Inputs；右段 Outputs。
  - 字号建议 \small，保持清爽。

6. 数学/表格/图形细节
- 公式在节点中排版：
  - 直接用数学模式 $...$，或令对应节点样式 font=\small 以统一字号。
- bra-ket 记号：
  - 自定义 \ket 宏：\newcommand{\ket}[1]{\lvert #1\rangle}
  - 右侧的 f′ 用 f' 即可。
- 本图无坐标轴/legend/表格/曲线，不需要 PGFPlots。

7. 自定义宏与命令
- 建议封装样式与常用宏，便于复用：
  - \newcommand{\ket}[1]{\lvert #1\rangle}
  - 样式：
    - block/.style={draw, line width=.4pt, minimum width=\blockW, minimum height=\blockH}
    - portline/.style={line width=.4pt}
    - lab/.style={font=\small}
    - mathlab/.style={font=\small}

8. 最小可运行示例 (MWE)
```latex
\documentclass[tikz]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usetikzlibrary{positioning,calc}

% Bra-ket (避免额外依赖)
\newcommand{\ket}[1]{\lvert #1\rangle}

\begin{document}
\begin{tikzpicture}[x=1cm,y=1cm, font=\small]
  % -- 尺寸参数 --
  \def\blockW{3.2cm}
  \def\blockH{2.0cm}
  \def\xL{-4.0}   % 左端 x
  \def\xR{ 4.0}   % 右端 x
  \def\halfW{1.6} % 方块半宽
  \def\halfH{1.0} % 方块半高

  % -- 方块 --
  \draw[line width=.4pt] (-\halfW,-\halfH) rectangle (\halfW,\halfH);
  \node at (0,0) {$M(L)$};

  % -- 左右连线与标签 --
  % 左线段：(-4,0) 到 (-1.6,0)
  \draw[line width=.4pt] (\xL,0) -- (-\halfW,0)
    node[midway, above=4pt] {$\ket{f}$}
    node[midway, below=4pt] {Inputs};

  % 右线段：(1.6,0) 到 (4,0)
  \draw[line width=.4pt] (\halfW,0) -- (\xR,0)
    node[midway, above=4pt] {$\mathbf{L}\ket{f}=\ket{f'}$}
    node[midway, below=4pt] {Outputs};
\end{tikzpicture}
\end{document}
```

9. 复刻检查清单
- 图形尺寸、坐标范围：
  - 整体约 10×4 cm；端点 x=±4，方块半宽/半高 1.6/1.0。
- 节点/边样式：
  - 方块细边、无填充；连线为 0.4pt 水平直线、无箭头。
- 字体与字号：
  - 节点与标签 font=\small；数学为默认 CM。
- 配色与线型：
  - 纯黑；无渐变、透明、阴影。
- 特殊效果：
  - 无；若画质偏淡，可将 line width 调至 0.5–0.6pt。
- 与原图的差异点（可能）：
  - 字体家族与粗细（若原始图用 Times/其他数学字体）。
  - 线粗与具体间距微差；右侧 L 的粗体程度可能略不同。

10. 风险与替代方案
- 字体不确定性：
  - 若需 Times 风格：使用 \usepackage{newtxtext,newtxmath}，或 Xe/LuaLaTeX + \setmainfont 与 \setmathfont。
- 粗体 L 显示差异：
  - 若 \mathbf 不够醒目，可用 \boldsymbol{L} 或 \pmb{L}；或切换更粗的数学字体。
- 精确尺寸与色值：
  - 原图仅黑白；若需要更「淡」的线，可用 draw=black!80。
- 兼容性：
  - 代码对 pdfLaTeX 足够；若改用系统字体（Times/TeX Gyre）则用 XeLaTeX/LuaLaTeX。
- 可维护性：
  - 将尺寸参数（\blockW, \blockH, \xL, \xR）置于宏，便于后续统一调整。
