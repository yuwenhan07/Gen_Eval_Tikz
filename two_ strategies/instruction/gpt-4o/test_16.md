# test_16.png

![test_16.png](../../../eval_dataset/images/test_16.png)

1. **概览**
   - 图像类型为“表格网络结构”，由多个矩阵组成，每个矩阵表示不同的集群 (C1, C2, C3, C4)。
   - 布局为一个大矩形内嵌长方形矩阵，每个矩阵使用网格划分，包含数字标识。
   - 右侧有附加标注；图底部显示时间相关指标。

2. **文档骨架与依赖**
   - 文档类：`standalone`
   - 核心宏包：`TikZ`, `xcolor`, `amsmath`, `booktabs`
   - TikZ 库：`matrix` 用于创建矩阵结构。

3. **版面与画布设置**
   - 建议尺寸：宽度 14cm，高度 12cm。纵横比接近 1:1。
   - 节点间距较小，主要以紧凑结构为主。
   - 使用 `\tikzpicture` 环境。

4. **字体与配色**
   - 字体：默认 Computer Modern，字体大小为 `\small`。
   - 主颜色为黑色；灰色用于阴影填充（约 #CCCCCC）。

5. **结构与组件样式**
   - 矩阵节点：方形，边框线，白色填充。
   - 右侧小矩形：仅边框。
   - 箭头：标准 TikZ 线型，细线，使用 `{}` 样式。

6. **数学/表格/图形细节**
   - 矩阵使用 `matrix` 环境，元素间距较小。
   - 列宽均匀，使用 `bmatrix` 格式，`booktabs` 提高线条质量。

7. **自定义宏与命令**
   - 创建节点和边样式宏，用于多次使用 `\node` 和 `\draw`。

8. **最小可运行示例 (MWE)**
   ```latex
   \documentclass{standalone}
   \usepackage{tikz}
   \usepackage{amsmath}
   \usetikzlibrary{matrix}

   \begin{document}
   \begin{tikzpicture}
     \matrix[matrix of nodes, nodes in empty cells,
             nodes={draw, minimum size=5mm, anchor=center},
             row sep=0mm, column sep=0mm] (m) {
       |[draw=none, right delimiter=\}|] & & 1 & & & & & & 11 & & 12 & & |[draw=none, right delimiter=\}|] & 17 & 18\\
       |[draw=none, right delimiter=\}|] & & 2 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 3 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 4 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       \\
       |[draw=none, right delimiter=\}|] & & 5 & & & & & & 11 & & 12 & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 6 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 7 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 8 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       \\
       |[draw=none, right delimiter=\}|] & & 9 & & & & & & 11 & & 12 & & |[draw=none, right delimiter=\}|] &\\
       |[draw=none, right delimiter=\}|] & & 10 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 11 & & & & & & & & 11 & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 12 & & & & & & & & 12 & & |[draw=none, right delimiter=\}|] & \\
       \\
       |[draw=none, right delimiter=\}|] & & 13 & & & & & & 11 & & 12 & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 14 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 15 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
       |[draw=none, right delimiter=\}|] & & 16 & & & & & & & & & & |[draw=none, right delimiter=\}|] & \\
     };

     \node[anchor=west] at (m-9-16.east) {\(\begin{array}{l}
       \text{Upper half of } C_3 \\
       \text{Lower half of } C_3 \\
     \end{array}\)};
   
     \node[anchor=north] at ([xshift=5mm]m-16-1.south) {\(t\)};
     \node[anchor=north] at ([xshift=30mm]m-16-1.south) {\(t^2\)};
   \end{tikzpicture}
   \end{document}
   ```

9. **复刻检查清单**
   - **图形尺寸**：宽 14cm，高 12cm。
   - **节点/边样式**：方形节点，标准箭头。
   - **字体与字号**：Computer Modern，\small。
   - **配色与线型**：黑色，细线，灰色阴影。
   - **特殊效果**：无。

10. **风险与替代方案**
    - 因不完全了解精确色值，灰色填充可用 `gray!50` 替代。
    - 字体可使用默认 Computer Modern 如不匹配，可选用 Times 替代。
