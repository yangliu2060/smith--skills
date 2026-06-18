#!/bin/bash
# 将推荐 Skills 安装到 Claude Code skills 目录

SKILLS_DIR="$HOME/.claude/skills"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📦 安装推荐 Skills..."
echo "源目录: $SOURCE_DIR"
echo "目标目录: $SKILLS_DIR"
echo ""

# 确保目标目录存在
mkdir -p "$SKILLS_DIR"

# 要安装的 skills 列表
skills=(
    "storm-research-agent"
    "competitor-price-monitor"
    "youtube-video-analyzer"
    "competitor-research"
    "geo-content-optimizer"
    "ai-readability-audit"
    "grok"
)

for skill in "${skills[@]}"; do
    if [ -d "$SOURCE_DIR/$skill" ]; then
        echo "✅ 安装: $skill"
        cp -r "$SOURCE_DIR/$skill" "$SKILLS_DIR/"
    else
        echo "⚠️ 跳过: $skill (目录不存在)"
    fi
done

echo ""
echo "🎉 安装完成！"
echo ""
echo "已安装的 Skills:"
for skill in "${skills[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "  - $skill"
    fi
done
echo ""
echo "使用方法:"
echo "  - '监控竞品价格' -> competitor-price-monitor"
echo "  - '分析这个YouTube视频' -> youtube-video-analyzer"
echo "  - '调研这个竞品' -> competitor-research"
echo "  - '用 STORM 调研这个选题是否值得写' -> storm-research-agent"
echo "  - 'GEO优化这篇文章' -> geo-content-optimizer"
echo "  - '检查网站AI可读性' -> ai-readability-audit"
echo "  - '问问 grok / X 上...' -> grok（实时 X 抓取，需先装 grok-build CLI 并登录 grok.com）"
