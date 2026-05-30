---
name: grok
description: |
  Grok CLI 包装器 — 让 Claude 调本地 grok-build 获取 X (Twitter) 实时内容。
  grok-build CLI 内部把 X 抓取工作流（Tavily / Firecrawl / Playwright / opencli 等工具 +
  相关性排序 + 互动加权 + 营销噪音过滤 + 结构化输出）整合好了，开发者不用自己拼。
  返回带 @用户名、点赞/浏览数、链接、时间的真实帖子。复用用户已登录的 grok.com 订阅，
  调用零额外成本（不像 MCP 方案要 xAI API key 按 token 付费）。
  三模式：x（X 实时抓取，主力）、ask（把 Grok 当独立第二意见）、continue（续接追问）。
  Use this skill when the user wants REAL-TIME X/Twitter data, e.g.:
  问问 grok X 上在聊什么、让 grok 搜 X 上对某事的实时讨论、grok 看看 @某账号最近发了什么、
  X 上现在怎么说、X 实时热点、X 实时趋势、ask grok what X is saying about、
  grok 第二意见、consult grok。
  排除（不要触发本 skill）：写 X 推文 → 用 x-twitter-writer；非实时的历史 X 检索 →
  用 x-sousuo；泛网络调研 → 用 smart-research。本 skill 的差异点是 grok 把 X 抓取工作流
  调通了 + 复用订阅零成本，**不是**独家数据通道（grok 内部用的也是 web 工具）；
  没有"实时 X 抓取"诉求时不要用它。
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# /grok — Claude 调用 Grok

主战场是 **X (Twitter) 实时内容**。grok-build CLI 内部用 Tavily / Firecrawl / Playwright /
opencli 等工具实时抓 X，配上相关性排序、互动加权、营销噪音过滤、结构化输出 —— 整套工作
流已经调好。对开发者来说 = 现成的 X 抓取专家，省去自己拼工具栈的事。次要场景：把 Grok
当独立第二意见用。复用 grok.com 订阅，零额外成本（vs MCP 方案要 xAI API key 按 token 付）。

> **诚实声明**：grok-build CLI 不是 xAI 内部 firehose API，它内部走的也是上面那些 web 工具。
> 本 skill 的价值是"省事 + 省钱"，不是"独家数据通道"。

所有调用逻辑（filesystem boundary、模式模板、超时、错误处理、临时文件清理）都收敛在
`scripts/grok-call.sh` 一个脚本里。本 skill 只负责：识别模式 → 写 query 文件 → 调脚本 →
转达结果。

## 怎么调用（三步，所有模式通用）

1. **用 Write 工具**把用户问题原文写入临时文件，如 `/tmp/grok-q-<时间戳>.txt`。
   为什么用 Write 而不是 shell heredoc：用户问题里若含 `EOF`、`$`、反引号、`rm -rf`
   这类字符，heredoc 会被截断或触发命令注入。Write 把问题当纯数据落盘，脚本再 `cat`
   读入，全程不经 shell 解析，从根上杜绝这个问题。

2. 运行脚本，`<mode>` 取 `x` / `ask` / `continue`：

   ```bash
   bash ~/.cc-switch/skills/grok/scripts/grok-call.sh <mode> /tmp/grok-q-<时间戳>.txt
   ```

   脚本会自动拼好 filesystem boundary + 对应模式模板 + 用户问题，调 grok（超时 330s），
   跑完自清理临时文件。它还自带前置检查：grok 不存在退出码 3，参数错退 2，超时退 124。

3. stdout 即 grok 回复，**原样转给用户**，不要二次总结或改写风格。保留 @用户名、
   互动数据、链接。按下面格式包一层：

   ```
   ━━━ Grok 回复 ━━━
   <grok stdout 原文>
   ━━━━━━━━━━━━━━━━
   ```

## 三个模式怎么选

解析用户输入决定 `<mode>`，模糊时用 AskUserQuestion 确认：

- **x**（主力）：要 X 实时数据。触发：`/grok x`、"X 上 ..."、"推特上 ..."、"X 热点/趋势"、
  "grok 看看 @某账号"。脚本模板已强制 Live Search + 结构化输出（核心结论 → Top 帖子 →
  其他观察）+ 互动数据标注。
- **ask**：通用问答 / 第二意见，非 X 场景。触发：`/grok` 后跟普通问题、"grok 第二意见"、
  "consult grok"。脚本模板开放 web search，要 grok 给独立判断、不附和。
- **continue**：续接最近一次 grok 对话追问。触发："继续问 grok"、"接着问"。脚本带 `-c`，
  query 文件只放追问内容即可。注意 `-c` 续接的是当前工作目录最近的 session，跨目录不保证命中。

## 错误处理（脚本退出码）

- `0` 成功 — stdout 是 grok 回复
- `124` 超时（5.5 分钟）— 提示用户重试或简化问题
- `3` 环境错 — grok 没装（提示去 https://grok.com 安装）或 query 文件丢失
- `2` 参数错 — mode 不对或缺 query 文件
- 其他 — grok 自身错误码，stderr 有诊断头两行

脚本把诊断信息写 stderr、正文写 stdout，所以 stdout 永远是干净正文。

## 何时不该用本 skill

- 单纯查代码、改文件 → 用 Claude 自己，别绕道 grok
- 需要多轮深聊（5+ 回合）→ 直接进 grok TUI（终端跑 `grok` 不带参数）更顺手
- 只要 1-2 条特定帖子且非实时 → Claude 用 Tavily/Exa 也够
- 写 X 推文 → x-twitter-writer；非实时历史检索 → x-sousuo；泛调研 → smart-research

## 已知限制

- 每次调用冷启动 3-5s + 抓 X 思考时间，单次可能 30s-2min，属正常
- grok-build 是固定模型，不支持调思考深度（传 `--effort` 会报 400，脚本已不传）
- X 精确互动数（赞/浏览）因反爬有时抓不全，grok 会退化用"传播广度"做 proxy 并说明
