# test_10.png

![test_10.png](../../../eval_dataset/images/test_10.png)

以下为针对所示科研绘图（4 根量子比特导线、左侧 R_y 门、内部“楼梯式”受控门组、虚线框并标注“× D”表示重复单元）的 LaTeX/TikZ 重构指导。

1. 概览
- 图形类型：量子电路（Quantum circuit）。
- 构图布局：
  - 4 条水平量子导线（从上到下等距）。
  - 每条导线左侧各有一个单比特旋转门 R_y(θ_i) 的矩形门框。
  - 中部到右侧由若干列两比特受控操作构成“楼梯式”连接（相邻导线之间交替出现控制点/靶标 ⊕ 等）。
  - 整个子电路被虚线、圆角边框包围，并在右下角标注“× D”，表示该子电路重复 D 次。
- 主要元素关系：
  - R_y(θ_1…θ_4) 分别作用在 4 条导线上。
  - 之后有三列相邻线之间的耦合操作（CNOT/受控变体的阶梯），最右侧一列包含顶线上靶标 ⊕，在下两线出现实心控制点（图中似有一个空心控制点，可能为“0 控制”）。
  - 无坐标轴、无图例，黑白为主。

2. 文档骨架与依赖
- 文档类：standalone（便于直接生成单个图）。
- 核心宏包：
  - tikz
  - quantikz（基于 TikZ 的量子电路绘图宏包，最贴合该图）
  - xcolor（若需颜色或灰度）
  - amsmath（门内数学公式）
- TikZ 库：若只用 quantikz 无需额外库；如用原生 TikZ 重绘，可用 fit、calc、arrows.meta，但本文首选 quantikz。

3. 版面与画布设置
- 图形尺寸建议：
  - 宽度约 6–7 cm；高度由 4 根导线和行距决定，约 3.5–4.5 cm。
- 坐标与纵横比：由量子电路矩阵布局控制，无需显式坐标轴。
- 间距与对齐：
  - 行距 row sep ≈ 1.1–1.3em（等距四线）。
  - 列距 column sep ≈ 1.4–1.7em（使门与受控连线留有呼吸感）。
  - 线宽 line width ≈ 0.8 pt（与示图接近）。
- 环境参数（quantikz）建议：
  - \begin{quantikz}[row sep=1.2em, column sep=1.6em, line width=0.8pt]
  - 使用 \gategroup（quantikz 提供）绘制虚线圆角分组框。

4. 字体与配色
- 字体：
  - 门内公式使用数学字体（默认 Computer Modern 即可）：R_y(\theta_i)。
  - 若论文需 Times 系：可加载 newtxtext/newtxmath。
- 颜色：
  - 主色：黑色（线、门框、控制点、⊕）。
  - 分组框：黑色虚线。若需弱化，可设为 gray!60。
- 特效：
  - 虚线与圆角：style={dashed, rounded corners, inner xsep=..., inner ysep=...}。
  - 通常无透明度/阴影。

5. 结构与组件样式
- 节点（门）：
  - 形状：直角矩形，细边框，无填充。
  - 门标签：数学模式，建议 \gate{R_y(\theta_i)}。
- 连线与符号：
  - 导线：水平直线，线宽 0.8 pt。
  - 控制点：\ctrl{<偏移>}（实心），\octrl{<偏移>}（空心/0 控制）。
  - 靶标：\targ{}（带 ⊕ 的圆）。
  - 竖线自动由控制与靶标连接生成。
- 分组框与标签：
  - \gategroup[wires=4, steps=5, style={dashed, rounded corners, inner xsep=6pt, inner ysep=4pt}, label style={label position=right, anchor=west}, label={$\times D$}]{}

6. 数学/表格/图形细节
- 公式排版：
  - 在 \gate 内直接写数学：\gate{R_y(\theta_1)}。
  - 若需统一符号大小，可用 \mathit 或 \mathrm：\gate{$R_y(\theta_1)$}。
- 本图无表格/坐标轴；曲线图不涉及。

7. 自定义宏与命令
- 建议封装常用样式与门：
  - \newcommand{\rygate}[1]{\gate{$R_y(#1)$}}
  - 用 tikzset 统一线宽与分组框样式：
    - \tikzset{mywire/.style={line width=0.8pt}}
    - \tikzset{mygroup/.style={dashed, rounded corners, inner xsep=6pt, inner ysep=4pt}}
  - 在 quantikz 里可通过可选参数传入 line width=0.8pt，一般即可。

8. 最小可运行示例 (MWE)
说明：
- 下例尽量复刻：4 根导线；每线左侧 R_y；中间三列相邻耦合；最右一列在顶线为 ⊕，在第 3、4 线为控制点；整个块用虚线圆角框并在右下标注“× D”。
- 图中有一个空心控制点的可能性不完全确定，已在注释中给出可切换为 \octrl 的位置。

```latex
\documentclass[border=2pt]{standalone}
\usepackage{amsmath}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{quantikz} % Quantum circuits on TikZ

% 可选：统一线宽
\tikzset{every picture/.style={line width=0.8pt}}

\begin{document}
\begin{quantikz}[row sep=1.2em, column sep=1.6em]
% 1st row (top wire)
\lstick{} &
  \gate{$R_y(\theta_1)$}
  % 分组框从本单元开始，跨 4 根线、向右 5 列
  \gategroup[wires=4,steps=5,
    style={dashed, rounded corners, inner xsep=6pt, inner ysep=4pt},
    label style={label position=right, anchor=west},
    label={$\times D$}]{}
  & \ctrl{1} & \qw      & \qw      & \targ{} & \qw \\
% 2nd row
\lstick{} &
  \gate{$R_y(\theta_2)$}
  & \targ{} & \ctrl{1} & \qw      & \qw     & \qw \\
% 3rd row
\lstick{} &
  \gate{$R_y(\theta_3)$}
  & \qw     & \targ{}  & \ctrl{1} & \ctrl{-2} & \qw \\
% 4th row (bottom wire)
\lstick{} &
  \gate{$R_y(\theta_4)$}
  & \qw     & \qw
  % 若需要“0 控制”（空心），可将下一行的 \targ{} 改为 \octrl{-1} 或将本行的 \ctrl{-1} 改为 \octrl{-1}
  & \targ{} % ← 若想匹配图中疑似空心控制点，可替换为 \octrl{-1}
  & \ctrl{-3} & \qw
\end{quantikz}
\end{document}
```

可选变体（两个位置的“0 控制”）：
- 若希望在倒数第二列让最底线为“空心控制点”，把该列的 \targ{} 改为 \octrl{-1}，同时相应连线仍自动绘制。
- 如果中部阶梯某处需要空心控制，将对应的 \ctrl{<偏移>} 换成 \octrl{<偏移>} 即可。

9. 复刻检查清单
- 图形尺寸与间距
  - 宽度 6–7 cm；row sep ≈ 1.2em；column sep ≈ 1.6em；线宽 0.8 pt。
- 节点/边样式
  - 门为细边矩形；控制点为实心圆；空心控制用 \octrl；靶标 ⊕ 用 \targ。
- 字体与字号
  - 门内数学字体；与正文统一时选 newtxmath 或默认 Computer Modern。
- 配色与线型
  - 主体黑色；分组框 dashed、rounded corners；可调 inner xsep/ysep 控制留白。
- 特殊效果
  - 仅虚线与圆角；无阴影/透明度。
- 与原图的差异点
  - 中部某个符号可能为“空心控制点（0 控制）”或靶标，视原文语义选择 \octrl 或 \targ。
  - 具体列距/行距可能需微调以匹配原图比例。

10. 风险与替代方案
- 不确定因素
  - 精确色值：原图为黑白，若包含不同灰度需现场采样或用 gray!x 近似。
  - 字体差异：不同论文模板可能要求 Times/Helvetica；门内公式粗细会随之变化。
  - 个别符号判读：空心控制 vs 靶标的判读可能受分辨率影响。
- 替代方案
  - 字体：默认 Computer Modern → 若需 Times 系，加载 newtxtext,newtxmath。
  - 颜色：黑色 → 可用 gray!70 降低分组框权重。
  - 宏包：若不使用 quantikz，可用原生 TikZ 自绘（节点+路径）或 Qcircuit；但 quantikz 最省力且语义清晰。

说明
- 上述 MWE 的门序与连接遵循图像的主观可辨结构（R_y 门 + 楼梯式耦合 + 右端顶线靶标与下两线控制）。如需严格一一对应，请据原始论文中该模块的具体定义，调整 \ctrl / \octrl / \targ 的位置与列数（只需在示例中增删列即可）。
