# grok-skill

Let Claude Code call your local **Grok Build** CLI for **public X (Twitter) search and real-time discourse sampling**. X mode now explicitly asks Grok to prefer its native X tool family: `x_keyword_search`, `x_semantic_search`, `x_user_search`, and `x_thread_fetch`, with `web_search` / `open_page` for cross-checking. Outputs must include @用户名、post ID、链接、时间、互动数据、短原文摘录和限制说明。复用你的 grok.com 订阅,零额外成本(不像 MCP 方案要 xAI API key)。

## Why this exists

Claude 自己也能调 Tavily / WebSearch 搜 X,但 X 任务真正需要的是可复核的公共话语采样: 精确关键词、账号限定、日期窗口、thread 上下文、互动数据和原文链接。这个 skill 把 grok-build 包装成 Claude Code 的工作流入口,让 "X 上现在怎么说" 变成一次带检索策略和证据字段的 Grok 调用,而不是让 Claude 自己拼工具或拿训练数据糊弄你。

> **诚实声明**: 这个 skill 通过 Grok CLI 发 prompt,不能像 xAI REST Responses API 那样在请求体里强制声明 `tools: [{ "type": "x_search" }]`。它能做的是把工具选择、证据字段和输出格式写进 prompt,让 Grok 在当前运行时暴露这些 X 工具时优先使用。它不是 firehose,也不能看 DM、私有账号、个人级点赞或书签。

替代方案对比:

| 方案 | 成本 | X 抓取链 | 启动延迟 |
|------|------|---------|----------|
| **这个 skill(包装本地 grok)** | 0(复用 grok.com 订阅) | ✅ Prompt 强制优先用 Grok X 工具族并输出证据字段 | 30s-2min |
| Grok MCP server(`grok-mcp` 等) | xAI API key 按 token 付费 | ✅ 类似(走 xAI API) | <1s |
| Claude + Tavily / Exa 自己拼 | API key 付费 + 你的拼装时间 | ⚠️ 工具有,排序/过滤要自己写 | <1s |
| Claude 训练数据 | 0 | ❌ 截止日期之前 | 0 |

## Real demo output

> 用户问:"最近 24 小时 X 上关于 Claude Code 的最高互动帖子是哪条?"

Grok 通过本 skill 返回(部分):

> **@_catwu** · 2026-05-28 17:42 GMT(约 18 小时前)
> 互动:**6,290 likes,658 retweets**(抓取瞬间精确值)
> 链接:`https://x.com/_catwu/status/2060054180379689074`
> 核心:Anthropic 工程师官宣 Claude Code 动态工作流(dynamic workflows),支持数百并行 sub-agents,内部案例 <10 分钟并行处理数百 A/B test flags。

带 post ID + 精确互动数 + 链接 + 时间 + 原文摘录 + 语义摘要,这是普通 web 搜索 API 给不了的。

## Requirements

- macOS 或 Linux
- [Grok Build CLI](https://grok.com) 装在 `~/.grok/bin/grok` 并已 `grok login`
- `bash`(>= 3.2 也行,macOS 自带兼容)
- `timeout`(macOS 装 `brew install coreutils`,Linux 一般自带)
- [Claude Code](https://claude.com/claude-code) 或任何加载 Anthropic Skills 的客户端

## Install

本 skill 是 [smith--skills](https://github.com/yangliu2060/smith--skills) 仓库的一部分。三种安装方式:

### Option A:仓库 install.sh(批量装多个 skill)

```bash
git clone https://github.com/yangliu2060/smith--skills.git
cd smith--skills && ./install.sh
```

### Option B:symlink(推荐,便于跟踪上游更新)

```bash
git clone https://github.com/yangliu2060/smith--skills.git ~/code/smith--skills
mkdir -p ~/.claude/skills
ln -s ~/code/smith--skills/grok ~/.claude/skills/grok
```

### Option C:只 copy grok 子目录

```bash
git clone https://github.com/yangliu2060/smith--skills.git
cp -r smith--skills/grok ~/.claude/skills/
```

### 验证安装

打开 Claude Code,直接说话:

```
问问 grok,X 上这两天对 Claude Code 的真实反馈
```

如果 Claude 触发 `grok` skill、写 query 文件、调脚本、转达 grok 回复,就装好了。

## Usage

三种触发方式 —— 自然语言即可,不必打 slash command:

| 场景 | 触发示例 | 模式 |
|------|---------|------|
| **X 公共搜索 / 实时话语采样(主力)** | "问问 grok,X 上对 Opus 4.8 的真实反馈,给 post ID 和链接" | `x` |
| **第二意见 / 通用问答** | "grok 第二意见:sqlite 做向量库后端靠谱吗" | `ask` |
| **续接追问** | "继续问 grok,那换 duckdb 呢" | `continue` |

也可以直接调脚本(脚本独立可用,不依赖 Claude):

```bash
echo "X 上最近怎么评价 cursor 的新版本" > /tmp/q.txt
bash ~/.claude/skills/grok/scripts/grok-call.sh x /tmp/q.txt
```

退出码语义化:`0` 成功 / `124` 超时 / `2` 参数错 / `3` 环境错 / 其他 = grok 自身错误。

## Design principles

1. **零额外成本** — 复用你已付费的 grok.com 订阅,不要求 xAI API key
2. **防注入** — 用户问题走 `Write 落盘 → cat 读入`,不经 shell heredoc;`EOF`/`$VAR`/反引号/`rm -rf` 等特殊字符全部当数据处理(已用 fake-grok 验证)
3. **filesystem boundary** — 每次自动告诉 grok 不要读 Claude 的 skill 文件,避免浪费 token
4. **bash 3.2 兼容** — macOS 自带 bash 也能跑,不依赖数组/关联数组
5. **退出码语义化** — 让脚本可以被其他自动化串联

## Known limits

- 单次调用 30s-2min(grok 抓 X + 思考慢)
- grok-build 模型固定,不支持 `--effort`(传了会报 400,脚本已不传)
- X 搜索是公共索引采样,不是全量 firehose
- X 精确互动数可能缺字段,缺失时必须说明
- X 数据不能单独当事实源;涉及事实判断时必须用网页来源交叉验证
- 续接靠 grok `-c` 标志(最近 session),跨工作目录不保证命中

## How it was built

本 skill 走完了完整的 [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) TDD 流程:

- ✅ 真实 X 搜索端到端验证(拿到 @MarioNawfal、@_catwu 等带精确互动数的真实帖子)
- ✅ heredoc 注入漏洞独立修复(用假 grok 测试 `EOF`/`$VAR`/反引号无注入,无截断)
- ✅ 三模式 DRY 重构(统一收敛到 `scripts/grok-call.sh`,SKILL.md 从 162 行降到 107 行)
- ✅ 20 条 trigger eval 自动优化 description(10 正例 + 10 near-miss 边界)

## License

MIT — see [LICENSE](./LICENSE)

## Acknowledgments

- **xAI / Grok team** — 出 grok-build CLI 这个低门槛高质量入口
- **Anthropic** — Claude Code & Skills 框架
- **[skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator)** — TDD 方法论 + description 自动优化
