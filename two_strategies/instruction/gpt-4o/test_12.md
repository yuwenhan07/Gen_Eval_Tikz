# test_12.png

![test_12.png](../../../eval_dataset/images/test_12.png)

以下是针对该科研绘图的 LaTeX/TikZ 重构指导：

### 1. 概览
- **图表类型**: 整体为矩阵热图，布局呈2x2网格。
- **构图布局**: 每个子图是一个 10x10 的方形矩阵，矩阵中的单元格以不同的灰度表示稀疏性。
- **主要元素关系**: 每个热图上方有标题，说明稀疏性的种类。

### 2. 文档骨架与依赖
- **推荐文档类**: `standalone`。
- **核心宏包**: `tikz`, `xcolor`。
- **特定功能**: 需要 `matrix` 和 `shapes` 库用于绘制矩阵和填充颜色。

### 3. 版面与画布设置
- **图形尺寸**: 每个子图建议大小为 4 cm x 4 cm。
- **节点间距与对齐**: 方阵节点均匀排列。
- **环境参数**: 使用 \verb|tikzpicture| 环境。

### 4. 字体与配色
- **标签字体**: `\small\sffamily\bfseries`。
- **主色与辅助色**: 黑白渐变（灰阶），主要使用 `black!20` - `black!80`。
- **渐变处理**: 无需渐变，只需跨灰度。

### 5. 结构与组件样式
- **节点**: 矩阵元素为正方形，边框黑色，填充为不同灰度。
- **边与箭头**: 不涉及箭头。
- **坐标轴**: 无坐标轴，只有方格线。

### 6. 数学/表格/图形细节
- **无公式或表格**。
- **矩阵表示**: 使用 `matrix` 环境定义每个子图的矩阵结构。

### 7. 自定义宏与命令
- 参数化定义节点样式和颜色，以便复用。

### 8. 最小可运行示例 (MWE)
```latex
\documentclass{standalone}
\usepackage{tikz}
\usetikzlibrary{matrix}

\begin{document}
\begin{tikzpicture}
    % Define styles
    \tikzset{matrix cell/.style={draw, minimum size=0.4cm, anchor=center}}
    
    % Top-left matrix
    \matrix[matrix of nodes, nodes={matrix cell}] (m1) at (0,0) {
        \node[fill=black!20] {}; & \node[fill=black!40] {}; & \node[fill=black!60] {}; & \node[fill=black!80] {}; & ...  \\
        ... \\
    };
    \node[above=of m1.north, yshift=-0.5cm] {\small\sffamily\bfseries Random Sparsity};
    
    % Top-right matrix
    \matrix[matrix of nodes, nodes={matrix cell}] (m2) at (5,0) {
        \node[fill=black!20] {}; & \node[fill=black!40] {}; & ...  \\
        ...
    };
    \node[above=of m2.north, yshift=-0.5cm] {\small\sffamily\bfseries Block Random Sparsity};

    % Bottom-left matrix
    \matrix[matrix of nodes, nodes={matrix cell}] (m3) at (0,-5) {
        \node[fill=black!40] {}; & \node[fill=black!60] {}; & ...  \\
        ...
    };
    \node[below=of m3.south, yshift=0.5cm] {\small\sffamily\bfseries Random Column Sparsity};
    
    % Bottom-right matrix
    \matrix[matrix of nodes, nodes={matrix cell}] (m4) at (5,-5) {
        \node[fill=black!50] {}; & \node[fill=black!70] {}; & ...  \\
        ...
    };
    \node[below=of m4.south, yshift=0.5cm] {\small\sffamily\bfseries Block Random Column Sparsity};

\end{tikzpicture}
\end{document}
```

### 9. 复刻检查清单
- **图形尺寸**: 检查子图大小及间距。
- **节点/边样式**: 确保矩形正方形，且边框可见。
- **字体与字号**: 检查标签字体符合要求。
- **配色与线型**: 灰度填充是否正确。
- **特殊效果**: 不涉及渐变。

### 10. 风险与替代方案
- **色值差异**: 灰度可能因显示器不同略有差异。
- **字体替代**: 若没有 `sans-serif`，则使用 `Computer Modern`。
- **近似色**: 灰度可简化为 `grayscale` 环境中预定义色。
