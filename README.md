# n8n 工作流转 Claude Code Skills

从 n8n 工作流模板转换而来的 14 个业务技能，可直接在 Claude Code 中使用。

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

## 安装方法

### 方法一：一键安装所有 skills
```bash
./install.sh
```

### 方法二：手动安装单个 skill
```bash
cp -r <skill-name> ~/.claude/skills/
```

## 使用方法

安装后，在 Claude Code 中直接说触发词即可使用，例如：
- "帮我分析这个竞品"
- "生成一个LinkedIn帖子"
- "检查这个网站的SEO"

## 依赖的 MCP 服务

部分 skills 需要以下 MCP 服务（可选）：
- **jimeng-mcp-server**: 图片/视频生成
- **playwright**: 网页自动化操作

## License

MIT
