# qpg93 的个人博客

[网站](https://qpg93.github.io/) · Hugo 静态博客，无 Node.js、npm、Ruby、主题子模块或第三方字体依赖。

## 日常写作：不需要安装任何工具

1. 在 `content/posts/` 新建 Markdown 文件，例如 `my-note.md`。
2. 填写文章信息和正文：

   ```markdown
   ---
   title: 我的新文章
   date: 2026-11-13
   slug: my-note
   tags: [随笔]
   description: 一句话摘要，可选。
   draft: false
   ---

   正文写在这里。
   ```

3. 提交并推送到 `main`，GitHub Actions 自动构建发布。

文章地址由 `slug` 决定，例如 `/my-note/`。发布后不要随意修改；需要修改时可以在 front matter 添加 `aliases: [/旧地址/]`。`draft: true` 的文章不发布，未来日期的文章默认也不发布。使用 `<!--more-->` 可指定摘要截断位置。

图片放在 `static/images/`，在文章中使用 `![说明](/images/example.jpg)`。关于页编辑 `content/about.md`；站名、简介和联系方式编辑 `hugo.toml`。

## 本地预览（可选）

从 [Hugo Releases](https://github.com/gohugoio/hugo/releases/tag/v0.169.0) 安装 **Hugo 0.169.0 标准版**即可，不需要 Extended、Go 或 npm。二进制放在仓库以外或系统 PATH 中。

```sh
hugo server -D       # http://localhost:1313/，包括草稿
hugo --gc --minify --panicOnWarning
python3 scripts/check-site.py  # 可选的构建产物检查，需要 Python 3
```

构建结果在 `public/`，已加入忽略列表，不提交到仓库。升级 Hugo 时同时更新工作流内固定版本与本说明。

## GitHub Pages 一次性设置

仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。推送后在 Actions 查看 `Deploy Hugo to GitHub Pages`。Pull Request 只构建检查，不部署。

如需隐藏仓库首页的 Contributors 模块，可在仓库首页右侧 About 的齿轮设置中取消勾选 Contributors。这与网站页面无关，无需改写 Git 历史。

## 目录

```text
content/          Markdown 文章和关于页
layouts/         项目自有模板，不依赖外部主题
static/          原样发布的 CSS、JavaScript、图片及归档资源
archetypes/      新文章模板（hugo new content posts/my-note.md）
scripts/         构建结果检查
hugo.toml        网站配置
.github/         构建和部署工作流
```

## 迁移说明

原文章 `/init/`、关于页 `/about/`、标签页 `/tags/`（含 `#notice` 锚点）、`/images/favicon.ico`、`/archives/ysc.json`、RSS `/feed.xml` 和搜索索引 `/search.json` 地址保留。原始文章日期、正文与归档资源保留。

新版使用系统字体、响应式布局、系统深浅色及手动主题切换、客户端搜索、标签归档、RSS 和 sitemap。默认不加载第三方统计、评论、远程脚本或字体。旧版没有启用的 Disqus/Gitalk 不再保留；历史代码仍可从 Git 提交记录找回。原 LICENSE 保留。

Hugo 的分页地址为 `/page/2/`，不再使用 Jekyll 的 `/page2/`；当前原站仅一篇文章，没有需要迁移的第二页。
