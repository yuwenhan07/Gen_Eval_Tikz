# test_12.png

![test_12.png](../../../eval_dataset/images/test_12.png)

# LaTeX/TikZ 重构指导：稀疏性模式可视化图

## 1. 概览

图像展示了四种不同的稀疏性模式可视化，通过网格矩阵表示。图像分为2×2布局，每个子图有一个标题，分别是：
- 左上：Random Sparsity（随机稀疏性）
- 右上：Block Random Sparsity（块随机稀疏性）
- 左下：Random Column Sparsity（随机列稀疏性）
- 右下：Block Random Column Sparsity（块随机列稀疏性）

每个子图是一个方形网格，其中灰色单元格表示非零元素，白色单元格表示零元素。

## 2. 文档骨架与依赖

```latex
\documentclass[border=5pt]{standalone}
\usepackage{tikz}
\usepackage{xcolor}
```

## 3. 版面与画布设置

- 总图宽度：约12cm
- 高度：约12cm
- 每个子图是一个10×10的网格矩阵
- 子图之间有适当间距

## 4. 字体与配色

- 标题：使用黑体，约10-12pt
- 网格填充：
  - 非零元素：中灰色 (RGB: 180,180,180 或 gray!40)
  - 零元素：白色 (white)
- 网格线：黑色 (black)

## 5. 结构与组件样式

- 网格：由10×10个小方格组成
- 网格线：细黑线
- 标题：位于每个子图上方中央位置

## 6. 数学/表格/图形细节

- 每个网格单元的大小相同，约为0.3-0.4cm
- 网格线宽度约为0.5pt

## 7. 自定义宏与命令

为提高代码复用性，定义以下样式：
- 网格单元样式
- 不同稀疏模式的填充函数

## 8. 最小可运行示例 (MWE)

```latex
\documentclass[border=5pt]{standalone}
\usepackage{tikz}

\begin{document}

\begin{tikzpicture}[
    cell/.style={
        draw,
        minimum size=0.4cm,
        inner sep=0pt,
        outer sep=0pt
    },
    filled/.style={
        cell,
        fill=gray!40
    },
    empty/.style={
        cell,
        fill=white
    },
    title/.style={
        font=\bfseries,
        anchor=south
    }
]

% 定义随机数种子，确保每次编译结果一致
\pgfmathsetseed{12345}

% 常量定义
\def\gridsize{10} % 10x10网格
\def\blocksize{3} % 块大小
\def\sparsity{0.2} % 稀疏率（非零元素比例）

% Random Sparsity
\node[title] at (5*0.4, 11*0.4) {Random Sparsity};
\foreach \i in {0,...,\numexpr\gridsize-1\relax} {
    \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
        \pgfmathrandom{0}{100}
        \pgfmathsetmacro{\randval}{int(\pgfmathresult)}
        \ifnum\randval<20
            \node[filled] at (\i*0.4, \j*0.4) {};
        \else
            \node[empty] at (\i*0.4, \j*0.4) {};
        \fi
    }
}

% Block Random Sparsity
\node[title] at (15*0.4, 11*0.4) {Block Random Sparsity};
\foreach \i in {0,...,\numexpr\gridsize-1\relax} {
    \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
        \pgfmathrandom{0}{100}
        \pgfmathsetmacro{\randblock}{int(\pgfmathresult)}
        \pgfmathtruncatemacro{\blocki}{int(\i/\blocksize)}
        \pgfmathtruncatemacro{\blockj}{int(\j/\blocksize)}
        \pgfmathsetmacro{\inblock}{mod(\blocki*3+\blockj, 4) == 0 ? 1 : 0}
        \ifnum\randblock<30
            \ifnum\inblock=1
                \node[filled] at ({(\i+10)*0.4}, \j*0.4) {};
            \else
                \node[empty] at ({(\i+10)*0.4}, \j*0.4) {};
            \fi
        \else
            \node[empty] at ({(\i+10)*0.4}, \j*0.4) {};
        \fi
    }
}

% Random Column Sparsity
\node[title] at (5*0.4, 0*0.4-0.8) {Random Column Sparsity};
\foreach \i in {0,...,\numexpr\gridsize-1\relax} {
    \pgfmathrandom{0}{100}
    \pgfmathsetmacro{\randcol}{int(\pgfmathresult)}
    \ifnum\randcol<30
        \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
            \node[filled] at (\i*0.4, {(\j-12)*0.4}) {};
        }
    \else
        \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
            \node[empty] at (\i*0.4, {(\j-12)*0.4}) {};
        }
    \fi
}

% Block Random Column Sparsity
\node[title] at (15*0.4, 0*0.4-0.8) {Block Random Column Sparsity};
\foreach \i in {0,...,\numexpr\gridsize-1\relax} {
    \pgfmathtruncatemacro{\blocki}{int(\i/\blocksize)}
    \pgfmathrandom{0}{100}
    \pgfmathsetmacro{\randcol}{int(\pgfmathresult)}
    \ifnum\randcol<40
        \ifnum\blocki=1
            \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
                \node[filled] at ({(\i+10)*0.4}, {(\j-12)*0.4}) {};
            }
        \else
            \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
                \node[empty] at ({(\i+10)*0.4}, {(\j-12)*0.4}) {};
            }
        \fi
    \else
        \foreach \j in {0,...,\numexpr\gridsize-1\relax} {
            \node[empty] at ({(\i+10)*0.4}, {(\j-12)*0.4}) {};
        }
    \fi
}

\end{tikzpicture}

\end{document}
```

## 9. 复刻检查清单

- ✅ 图形尺寸：2×2布局，每个子图为10×10网格
- ✅ 节点样式：网格单元为方形，灰色填充表示非零元素
- ✅
