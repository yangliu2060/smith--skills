# Smith Skills

自用/精选的 Claude Code / Codex Skills 仓库，包含 n8n 工作流迁移、自研调研与内容工具、Agent workflow loop 设计、Grok X 实时抓取、Claude headless review 等。

## Skills 列表

### 营销与内容创作
| Skill | 描述 | 原始模板 |
|-------|------|---------|
| [video-creator](./video-creator/) | AI视频创作（jimeng MCP + Playwright） | [#10358](https://n8n.io/workflows/10358) |
| [viral-post-creator](./viral-post-creator/) | 病毒式社交帖子生成器 | [#8756](https://n8n.io/workflows/8756) |
| [linkedin-post-creator](./linkedin-post-creator/) | LinkedIn帖子创作 | [#6979](https://n8n.io/workflows/6979) |
| [cold-email-personalizer](./cold-email-personalizer/) | 冷邮件个性化 | [#6089](https://n8n.io/workflows/6089) |

### 客户服务
| Skill | 描述 | 原始模板 |
|-------|------|---------|
| [email-assistant](./email-assistant/) | 智能邮件助手（支持RAG知识库） | [#2852](https://n8n.io/workflows/2852) |
| [ecommerce-support](./ecommerce-support/) | 电商客服（Playwright自动化） | [#3480](https://n8n.io/workflows/3480) |

### 市场调研
| Skill | 描述 | 原始模板 |
|-------|------|---------|
| [storm-research-agent](./storm-research-agent/) | 中文优先的 STORM 多视角调研 Agent：证据包、矛盾地图、盲点分析、决策卡，支持中英文输出 | 自研 / Yao-style Production |
| [social-trend-monitor](./social-trend-monitor/) | 社交趋势监控 | [#8450](https://n8n.io/workflows/8450) |
| [influencer-evaluator](./influencer-evaluator/) | 网红评估 | [#7256](https://n8n.io/workflows/7256) |
| [competitor-price-monitor](./competitor-price-monitor/) | 竞品价格监控 | [#8963](https://n8n.io/workflows/8963) |
| [competitor-research](./competitor-research/) | 竞品全网调研 | [#2354](https://n8n.io/workflows/2354) |

### SEO与内容优化
| Skill | 描述 | 原始模板 |
|-------|------|---------|
| [seo-analyzer](./seo-analyzer/) | SEO分析助手 | [#5303](https://n8n.io/workflows/5303) |
| [geo-content-optimizer](./geo-content-optimizer/) | GEO内容优化（AI搜索友好） | [#8768](https://n8n.io/workflows/8768) |
| [ai-readability-audit](./ai-readability-audit/) | AI可读性审计 | [#4151](https://n8n.io/workflows/4151) |
| [youtube-video-analyzer](./youtube-video-analyzer/) | YouTube视频分析 | [#2679](https://n8n.io/workflows/2679) |

### 工具
| Skill | 描述 |
|-------|------|
| [skill_auditor](./skill_auditor/) | Claude Skills 安全审计工具 |
| [loopforge](./loopforge/) | 把模糊工作流锻造成可维护的 AI-agent workflow loop：同时输出 `loop-spec-v1` YAML/JSON 和可复制 Loop Prompt |
| [claude-review](./claude-review/) | Codex 驱动 Claude 做 headless 评审（plan / 架构 / 文档 / work-log），自动链式调用 `plan-eng-review`。安装到 `~/.codex/skills/` |
| [grok](./grok/) | 让 Claude 调本地 Grok Build CLI 抓 X (Twitter) 实时 firehose 内容（带 @用户名/互动数/链接的真实帖子）。复用 grok.com 订阅零额外成本。三模式：x 实时抓取 / ask 第二意见 / continue 续接 |

## 安装方法

### 方法一：一键安装推荐 skills
```bash
./install.sh
```

安装脚本只安装常用推荐列表，不等于仓库里的全部 skill。

### 方法二：手动安装单个 skill
```bash
cp -r <skill-name> ~/.claude/skills/
```

## 使用方法

安装后，在 Claude Code 中直接说触发词即可使用，例如：
- "帮我分析这个竞品"
- "生成一个LinkedIn帖子"
- "检查这个网站的SEO"
- "用 STORM 调研这个选题是否值得写"
- "用 loopforge 把这个工作流变成可复用 loop spec 和提示词"
- 为来实现和n8n的工作节点相同,有些skill绕路远路,建议可以依据需要修改

## 依赖的 MCP 服务

部分 skills 需要以下 MCP 服务（可选）：
- **jimeng-mcp-server**: 图片/视频生成
- **playwright**: 网页自动化操作

## License

MIT
