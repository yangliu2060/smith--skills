# Smith Skills

自用/精选的 Claude Code / Codex Skills 仓库，覆盖内容创作、客户服务、市场调研、SEO 优化、Agent workflow loop 设计、Grok X 实时抓取、Claude headless review 等场景。

## Skills 列表

### 营销与内容创作
| Skill | 描述 |
|-------|------|
| [video-creator](./video-creator/) | AI 视频创作：生成脚本、调用视频/浏览器工具、整理发布报告 |
| [viral-post-creator](./viral-post-creator/) | 病毒式社交帖子生成：从主题生成文案、配图方向和平台发布建议 |
| [linkedin-post-creator](./linkedin-post-creator/) | LinkedIn 帖子创作：围绕品牌背景、主题和反馈循环打磨职业化内容 |
| [cold-email-personalizer](./cold-email-personalizer/) | 冷邮件个性化：读取线索数据，生成结构化、可批量处理的个性化邮件 |

### 客户服务
| Skill | 描述 |
|-------|------|
| [email-assistant](./email-assistant/) | 智能邮件助手：摘要、分类、知识库查询、回复草稿和审核 |
| [ecommerce-support](./ecommerce-support/) | 电商客服：识别意图，处理订单查询、推荐、投诉和工单创建 |

### 市场调研
| Skill | 描述 |
|-------|------|
| [storm-research-agent](./storm-research-agent/) | 中文优先的 STORM 多视角调研：证据包、矛盾地图、盲点分析和决策卡 |
| [social-trend-monitor](./social-trend-monitor/) | 社交趋势监控：发现多平台趋势、排序热度并生成趋势报告 |
| [influencer-evaluator](./influencer-evaluator/) | 网红评估：解析公开账号数据，输出评分、等级和合作建议 |
| [competitor-price-monitor](./competitor-price-monitor/) | 竞品价格监控：跟踪竞品价格变化、促销信号和异常波动 |
| [competitor-research](./competitor-research/) | 竞品全网调研：收集竞品公开信息，输出定位、卖点、渠道和机会判断 |

### SEO与内容优化
| Skill | 描述 |
|-------|------|
| [seo-analyzer](./seo-analyzer/) | SEO 分析：检查页面结构、技术指标、内容质量和优化建议 |
| [geo-content-optimizer](./geo-content-optimizer/) | GEO 内容优化：让内容更适合 AI 搜索、引用和答案生成 |
| [ai-readability-audit](./ai-readability-audit/) | AI 可读性审计：检查内容是否易被 AI 抽取、理解和引用 |
| [youtube-video-analyzer](./youtube-video-analyzer/) | YouTube 视频分析：提取字幕/信息，生成摘要、结构和可复用洞察 |

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

## 依赖的 MCP 服务

部分 skills 需要以下 MCP 服务（可选）：
- **jimeng-mcp-server**: 图片/视频生成
- **playwright**: 网页自动化操作

## License

MIT
