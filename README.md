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
   tags: [notes]
   lang: zh-CN
   description: 一句话摘要，可选。
   draft: false
   ---

   正文写在这里。
   ```

3. 提交并推送到 `main`，GitHub Actions 自动构建发布。

文章地址由 `slug` 决定，例如 `/my-note/`。发布后不要随意修改；需要修改时可以在 front matter 添加 `aliases: [/旧地址/]`。`draft: true` 的文章不发布，未来日期的文章默认也不发布。使用 `<!--more-->` 可指定摘要截断位置。

图片放在 `static/images/`，在文章中使用 `![说明](/images/example.jpg)`。关于页编辑 `content/about.md`；站名、简介和联系方式编辑 `hugo.toml`。

网页界面统一使用英文，只有文章标题和内容（包括正文摘要和目录）允许使用中文。标签、文章元信息及站点介绍应使用英文；中文文章可在 front matter 中添加 `lang: zh-CN` 标记正文语言。项目文档和日常交流仍可使用中文。

## 本地预览（可选）

从 [Hugo Releases](https://github.com/gohugoio/hugo/releases/tag/v0.169.0) 安装 **Hugo 0.169.0 标准版**即可，不需要 Extended、Go 或 npm。二进制放在仓库以外或系统 PATH 中。

```sh
hugo server -D       # http://localhost:1313/，包括草稿
hugo --gc --minify --panicOnWarning
python3 scripts/check-site.py  # 可选的构建产物检查，需要 Python 3
```

请在项目根目录运行预览命令，或通过 `hugo server -D --source /项目绝对路径` 指定目录，否则 Hugo 找不到模板和配置。文章预览地址为 `http://localhost:1313/baby/`。

孕期文章的图表由 `content/posts/baby.md` 中的 `charts` 数据生成；使用 `pregnancy-chart` shortcode 绘制内联 SVG，`pregnancy-diagram` 绘制带来源的科普示意图。鼠标、触控和键盘交互使用原生 JavaScript；禁用脚本仍可读图和展开数据表。报告转录与聊天估算必须分开标注，范围值不得写成精确测量，不提交原始报告或对话资料。Apple 字体优先使用设备已有的 San Francisco、苹方及 SF Mono，不分发字体文件。

发布前可额外检查孕期文章：

```sh
hugo --buildDrafts --destination /tmp/qpg93-baby-preview --minify --panicOnWarning
python3 scripts/check-pregnancy.py /tmp/qpg93-baby-preview
```

该检查覆盖图表结构、数据和基础隐私规则，不代替医学核对或浏览器实测。无需安装浏览器；不要为测试下载 Playwright、Chromium 等工具。`draft: true` 只阻止网页发布，不能隐藏公开仓库中的源码。

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

新版使用系统字体、响应式布局、系统深浅色及手动主题切换、客户端搜索、标签归档和 sitemap。页面不展示 RSS 入口或订阅区块，但保留 `/feed.xml` 以兼容已有订阅。默认不加载第三方统计、评论、远程脚本或字体。旧版没有启用的 Disqus/Gitalk 不再保留；历史代码仍可从 Git 提交记录找回。原 LICENSE 保留。

Hugo 的分页地址为 `/page/2/`，不再使用 Jekyll 的 `/page2/`；当前原站仅一篇文章，没有需要迁移的第二页。
