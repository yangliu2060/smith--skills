# grok-skill

Let Claude Code call your local **Grok Build** CLI to pull **real-time X (Twitter) firehose** data —带 @用户名、点赞/浏览数、时间的真实帖子。复用你的 grok.com 订阅,零额外成本。

## Why this exists

Claude / Tavily / generic web search 拿不到 X 的实时 firehose。Grok 与 X 同属 xAI 生态,对 X 公开帖文有**原生实时访问 + 互动加权排序**。这个 skill 把 grok-build CLI 包装成 Claude Code 的工作流入口,让 "X 上现在怎么说" 一句话变成结构化抓取 —— 而不是让 Claude 拿训练数据糊弄你。

替代方案对比:

| 方案 | 成本 | X 实时性 | 启动延迟 |
|------|------|---------|----------|
| **这个 skill(包装本地 grok)** | 0(复用 grok.com 订阅) | ✅ firehose | 30s-2min |
| Grok MCP server(`grok-mcp` 等) | xAI API key 按 token 付费 | ✅ 同上 | <1s |
| Tavily / Exa search | API key 付费 | ⚠️ 滞后第三方索引 | <1s |
| Claude 训练数据 | 0 | ❌ 截止日期之前 | 0 |

## Real demo output

> 用户问:"最近 24 小时 X 上关于 Claude Code 的最高互动帖子是哪条?"

Grok 通过本 skill 返回(部分):

> **@_catwu** · 2026-05-28 17:42 GMT(约 18 小时前)
> 互动:**6,290 likes,658 retweets**(抓取瞬间精确值)
> 链接:`https://x.com/_catwu/status/2060054180379689074`
> 核心:Anthropic 工程师官宣 Claude Code 动态工作流(dynamic workflows),支持数百并行 sub-agents,内部案例 <10 分钟并行处理数百 A/B test flags。

带精确互动数 + 链接 + 时间 + 语义摘要 —— 这是普通 web 搜索 API 给不了的。

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
| **X 实时抓取(主力)** | "问问 grok,X 上对 Opus 4.8 的真实反馈" | `x` |
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
- X 精确互动数偶尔抓不全,grok 会退化用"传播广度"做 proxy 并说明
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
