# 构建与发布

本站使用 MkDocs Material 构建静态 HTML，通过 GitHub Actions 发布到 GitHub Pages。

## 本地预览

以下命令在仓库根目录运行。构建依赖与教程示例依赖分开管理：站点使用 `requirements-docs.txt`，任务管理器仅使用标准库。
为统一站点构建和完整教程验证，建议使用 Python 3.14。

=== "Windows PowerShell"

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
    .\.venv\Scripts\python.exe -m mkdocs serve
    ```

=== "macOS / Linux"

    ```shell
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements-docs.txt
    .venv/bin/python -m mkdocs serve
    ```

浏览器访问 `http://127.0.0.1:8000/`，修改 Markdown 或样式后自动刷新。已有 `.venv` 时直接使用，无需重复创建。

## 目录约定

```text
.
├── .github/workflows/pages.yml  # 检查、构建与部署
├── docs/
│   ├── index.md                # 站点首页
│   ├── tutorial/               # 00—22 章，正文的唯一来源
│   ├── assets/stylesheets/     # 站点样式
│   ├── examples.md             # 源码与合订版下载入口
│   ├── deployment.md           # 本文
│   └── validation.md           # 教程内容验证记录
├── examples/                   # 可执行示例与测试
├── scripts/
│   ├── build_book.py           # 合订版生成器
│   ├── site_hooks.py           # 构建时加入源码下载和合订版
│   ├── verify_site.py          # 构建产物、链接、子路径检查
│   └── verify_tutorial.py      # 教程内容验证器
├── main.py                     # 原有学习脚本
├── mkdocs.yml                  # 导航、主题与 Markdown 配置
├── requirements-docs.txt       # 站点构建依赖
└── README.md                   # 仓库说明与维护入口
```

`site/` 是自动生成的发布目录，`Python完整教程.md` 是自动生成的本地合订版，两者均不需要提交。
示例和脚本在构建时加入站点下载资源，不需要手动向 `docs/` 复制源码。

## 开启 GitHub Pages

1. 将项目提交到 GitHub 仓库的默认分支。
2. 打开仓库 **Settings → Pages → Build and deployment**。
3. 将 **Source** 设置为 **GitHub Actions**。
4. 默认分支每次 push 自动检查和发布；也可在 **Actions → Build and deploy documentation → Run workflow** 手动触发。
5. 首次部署完成后，在 Pages 设置或工作流的 `github-pages` 环境中查看实际网址。

工作流自动识别默认分支，兼容 `main`、`master` 或其他名称。PR 执行教程测试与站点构建检查，部署仅在默认分支执行。
如仓库为私有，请确认账户计划支持 Pages，以及仓库允许使用 Actions 和对应部署环境。

配置遵循 [GitHub Pages 官方自定义工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 仓库子路径与自定义域名

工作流通过 `actions/configure-pages` 获取实际站点地址并传入 `SITE_URL`，支持普通项目站点的 `/仓库名/` 前缀、用户站点和已配置的自定义域名。
页面链接和资源使用相对地址。仓库源码无需填写固定的 GitHub 用户名或仓库名。

本地模拟带路径前缀的构建：

```powershell
$env:SITE_URL = 'https://example.github.io/python-study01/'
python -m mkdocs build --strict
python -B scripts/verify_site.py --base-url $env:SITE_URL
```

使用自定义域名时，在仓库 Pages 设置中配置域名和 DNS，再重新运行工作流。

## 维护与验证

- 修改正文：编辑 `docs/tutorial/` 中对应章节；新增章节时同步更新 `mkdocs.yml` 导航。
- 修改首页：编辑 `docs/index.md`；样式集中在 `docs/assets/stylesheets/extra.css`。
- 修改示例：编辑根目录 `examples/`；构建会自动更新站点中的下载文件。
- 修改主题或构建依赖：更新 `requirements-docs.txt` 后执行严格构建和页面检查。

```shell
python -B scripts/build_book.py
python -B -m unittest discover -s examples -p "test_*.py" -v
python -B scripts/verify_tutorial.py
python -m mkdocs build --strict
python -B scripts/verify_site.py
```

完整教程验证需要 Python 3.14+。严格构建会把缺失链接、导航错误等警告视为失败；构建产物检查还会验证静态资源、章节数量、源码下载、搜索索引与本地锚点。
