# Gen_Eval_Tikz

## 注意
- 请大家在本地运行前，一定要先
```bash 
git pull
```
  - 然后可以尝试切分支操作
  - 不然merge起来太费劲了

- 请大家一定注意本地内容，不要一股脑 `git add .` 尽量确定好哪些要提交再提交
- 请大家尽可能写清楚 commit 的内容，方便后续回退、查看

# GitHub 使用小建议

## 分支管理

-   **主分支保护**：禁止直接推送到 `master/main`，所有改动通过 Pull
    Request (PR)。
-   **分支命名规范**：
    -   `feat/xxx` 新功能
    -   `fix/xxx` 修 bug
    -   `docs/xxx` 文档
    -   `refactor/xxx` 重构
-   每个功能/bugfix 建独立分支，避免多人同时操作同一分支。

## 提交规范

-   提交前先执行：

    ``` bash
    git pull --rebase
    ```

    避免产生无意义的合并提交。

-   提交信息要清晰、简洁：

        feat(parser): 支持新语法
        fix(ci): 修复 Ubuntu runner 权限问题

-   避免一次性 `git add .`，建议选择性提交：

    ``` bash
    git add <file1> <file2>
    ```

## Pull Request 建议

-   **小步提交**，方便代码 review。
-   PR 描述里写明：
    -   改动目的
    -   主要改动点
    -   测试方法
-   合并方式推荐 **Squash and merge**，保持历史整洁。

## 代码质量

-   添加 `.gitignore`，避免提交虚拟环境、临时文件、大文件：

        __pycache__/
        .venv/
        *.log
        .env
        data/*

-   使用 `pre-commit` 钩子自动检查格式 / lint：

    ``` bash
    pip install pre-commit
    pre-commit install
    ```

## 安全与配置

-   **不要提交密钥 / 密码**，使用 `.env` 文件并添加到 `.gitignore`。
-   可以在仓库启用 **Secret Scan** 或 `git-secrets` 工具。
-   使用 **GitHub Actions** 做自动化测试，保证每个 PR 能跑通。

## 日常操作小技巧

-   查看提交记录（简洁模式）：

    ``` bash
    git log --oneline --graph --decorate
    ```

-   撤销上一次提交但保留代码：

    ``` bash
    git reset --soft HEAD~1
    ```

-   找回误删的提交：

    ``` bash
    git reflog
    ```