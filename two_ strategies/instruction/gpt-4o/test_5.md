# test_5.png

![test_5.png](../../../eval_dataset/images/test_5.png)

1. 概览
- 图像为坐标图，主要显示“Test accuracy (%)”与“Time (hrs)”的关系。
- 坐标图上有多个数据点及其对应标签。
- 含图例区分不同数据集。

2. 文档骨架与依赖
- 文档类推荐 `standalone`。
- 核心宏包：`TikZ`, `PGFPlots`。
- 特定功能：`arrows.meta` 用于箭头样式。

3. 版面与画布设置
- 图形尺寸：宽 10cm，高 4cm。
- 坐标系范围：x 轴从 0 到 7，y 轴从 50 到 90。
- 使用 `axis` 环境，建议 `width=10cm, height=4cm`。

4. 字体与配色
- 字体：`\small` 大小。
- 主色：蓝色 `rgb:red,1;green,0;blue,0`，绿色 `rgb:red,0;green,1;blue,0`，红色 `rgb:red,1;green,0;blue,0`。
- 图例背景为白色。

5. 结构与组件样式
- 节点标注居中，边框矩形。
- 边与箭头：实线，`thick`。
- 坐标轴： `grid=both`，包含网格线。

6. 数学/表格/图形细节
- 使用 `\addplot` 添加曲线及点。
- 用 `legend` 指定图例。

7. 自定义宏与命令
- 可用 `\newcommand` 简化颜色设置和箭头样式。

8. 最小可运行示例 (MWE)
```latex
\documentclass{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.17}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
    xlabel={Time to obtain the sparse trainable network (hrs)},
    ylabel={Test accuracy (\%)},
    xmin=0, xmax=7,
    ymin=50, ymax=90,
    ytick={50,55,60,65,70,75,80,85,90},
    xtick={0,1,2,3,4,5,6,7},
    grid=both,
    legend pos=north west,
    legend style={draw=black, fill=white},
    width=10cm, height=4cm
]

\addplot[
    color=blue,
    mark=triangle*,
    ]
    coordinates {(0.5,60) (2,75)};
\addlegendentry{IMP}

\addplot[
    color=red,
    mark=diamond*,
    ]
    coordinates {(1,55)};
\addlegendentry{SNIP}

\addplot[
    color=green,
    mark=square*,
    ]
    coordinates {(2.5,65)};
\addlegendentry{SynFlow}

\addplot[
    thick,
    black
    ]
    coordinates {(0,70) (7,70)};
\addlegendentry{Unpruned Accuracy}

\end{axis}
\end{tikzpicture}
\end{document}
```

9. 复刻检查清单
- 图形尺寸和坐标范围：宽 10cm，高 4cm，范围准确。
- 节点/边样式：已定义为 `thick`。
- 字体与字号：`\small`。
- 配色与线型：使用 `rgb` 定义。
- 特殊效果：无渐变、阴影。

10. 风险与替代方案
- 色值不准确可用近似 `xcolor` 替代。
- 字体差异可用默认 `Computer Modern`。
