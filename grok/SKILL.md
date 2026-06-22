---
name: grok
description: |
  Grok CLI 包装器：让 Claude 调用本地 grok-build 获取 X (Twitter) 实时内容。
  X 模式必须优先驱动 Grok 原生 X 工具族：x_keyword_search、x_semantic_search、
  x_user_search、x_thread_fetch；必要时再用 web_search/open_page 交叉验证。
  返回带 @用户名、点赞/浏览数、链接、时间的真实帖子。复用用户已登录的 grok.com 订阅，
  调用零额外成本（不像 MCP 方案要 xAI API key 按 token 付费）。
  三种模式：x（X 实时抓取，主力）、ask（把 Grok 当独立第二意见）、continue（续接追问）。
  当用户需要真实 X/Twitter 实时数据时使用，例如：
  问问 grok X 上在聊什么、让 grok 搜 X 上对某事的实时讨论、grok 看看 @某账号最近发了什么、
  X 上现在怎么说、X 实时热点、X 实时趋势、ask grok what X is saying about、
  grok 第二意见、consult grok。
  排除（不要触发本 skill）：写 X 推文 → 用 x-twitter-writer；大规模历史语料采集 →
  用 x-sousuo；泛网络调研 → 用 smart-research。本 skill 的差异点是 Grok 对公共 X 搜索
  工具有原生路径，适合可复核的 X 话语采样；不是 firehose，也不是事实裁判。
  没有"公共 X 搜索 / X 实时反馈 / thread 上下文"诉求时不要用它。
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# /grok — Claude 调用 Grok

主战场是 **X (Twitter) 公共搜索与实时话语采样**。x 模式要把任务显式交给 Grok 的 X 工具族：

- `x_keyword_search`：精确关键词、账号操作符、日期、互动阈值、Top/Latest 排序
- `x_semantic_search`：自然语言话题、模糊趋势、观点/情绪采样
- `x_user_search`：用户或账号发现
- `x_thread_fetch`：已知 post URL/ID/thread 的上下文抓取
- `web_search` / `open_page`：事实核验、媒体报道、第三方趋势页补充

次要场景：把 Grok 当独立第二意见用。复用 grok.com 订阅，零额外成本（vs MCP 方案要 xAI API
key 按 token 付）。

> **诚实声明**：这个 skill 通过 Grok CLI 发 prompt，不能像 REST Responses API 那样在请求体里
> 强制声明 `tools: [{type: "x_search"}]`。它能做的是把工具选择、证据字段和输出格式写进 prompt，
> 让 Grok 在当前运行时暴露这些 X 工具时优先使用。它不是 firehose，也不能看 DM、私有账号、
> 个人级点赞/书签。

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

- **x**（主力）：要公共 X 数据、实时反馈、限定时间窗采样、账号近期动态、具体 thread 上下文。
  触发：`/grok x`、"X 上 ..."、"推特上 ..."、"X 热点/趋势"、"grok 看看 @某账号"、
  "抓这条 X thread"。脚本模板已强制 X 工具选择、证据链接、post ID、时间戳、互动数据和限制说明。
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
- 写 X 推文 → x-twitter-writer
- 大规模历史语料抓取、批量导出、定时采集 → x-sousuo
- 泛网络调研、论文/新闻/网页为主 → smart-research
- 只要读本地代码或改文件 → Claude 自己做，别绕道 grok

## 已知限制

- 每次调用冷启动 3-5s + 抓 X 思考时间，单次可能 30s-2min，属正常
- grok-build 是固定模型，不支持调思考深度（传 `--effort` 会报 400，脚本已不传）
- X 搜索是公共索引采样，不是全量 firehose
- X 精确互动数（赞/浏览/转发/回复/书签）可能缺字段，缺失时必须说明
- X 数据不能单独当事实源；涉及事实判断时必须用网页来源交叉验证
