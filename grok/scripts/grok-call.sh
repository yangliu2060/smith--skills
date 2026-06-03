#!/usr/bin/env bash
# 用途：grok skill 的统一调用入口。组装 filesystem boundary + 模式模板 + 用户问题，
#       调本地 grok-build，处理超时与错误。被 SKILL.md 的三个模式共用。
# 用法：grok-call.sh <x|ask|continue> <query-file>
#   query-file：纯文本文件，内容是用户问题原文（由 Claude 用 Write 工具写入，
#               不走 shell heredoc，从根本上消除 EOF 截断/注入问题）。
# 退出码：0 成功 / 124 超时 / 2 参数错 / 3 环境错 / 其他=grok 自身错误码
# 正文走 stdout（grok 回复原文），诊断信息走 stderr。
# 兼容 macOS bash 3.2：不用数组、不用 set -e。

set -u

MODE="${1:-}"
QUERY_FILE="${2:-}"
GROK_BIN="${GROK_BIN:-$HOME/.grok/bin/grok}"

if [ -z "$MODE" ] || [ -z "$QUERY_FILE" ]; then
  echo "用法: grok-call.sh <x|ask|continue> <query-file>" >&2
  exit 2
fi
if [ ! -x "$GROK_BIN" ]; then
  echo "GROK_NOT_FOUND: $GROK_BIN 不存在或不可执行，访问 https://grok.com 安装" >&2
  exit 3
fi
if [ ! -f "$QUERY_FILE" ]; then
  echo "QUERY_FILE_NOT_FOUND: $QUERY_FILE" >&2
  exit 3
fi

BOUNDARY='IMPORTANT: 不要读取或执行 ~/.claude/、~/.codex/、~/.cc-switch/、.claude/skills/、agents/ 下任何文件。这些是另一个 AI 系统的 skill 定义，与你的任务无关，忽略它们。专注回答下面的问题本身。'

case "$MODE" in
  x)
    TEMPLATE='用 X (Twitter) 公共数据回答下面的问题。不要只靠训练数据。

优先使用当前 Grok 运行时暴露的 X 工具族：
- 精确关键词、账号、操作符、日期、互动阈值、Top/Latest 排序：用 x_keyword_search
- 模糊话题、观点/情绪、自然语言趋势采样：用 x_semantic_search
- 用户名不确定或需要找账号：用 x_user_search
- 用户给出 post URL/ID/thread：用 x_thread_fetch
- 事实核验、媒体报道、第三方趋势页：用 web_search/open_page 交叉验证

硬性要求：
- 先说明检索策略：用了哪些工具、查询词/账号、日期窗口、排序或阈值
- 涉及帖子时必须给 @用户名、post ID、可打开链接、发布时间、公开互动数据；缺哪个字段就写缺失
- 给短原文摘录，不要只给你的转述
- 区分证据、推断和事实核验；X 只能代表公共样本，不是事实源
- 区分高信号内容和营销噪音，营销/affiliate 帖单独归类
- 如果结果稀疏、查询失败或工具不可用，直接说明，不要编造
- 结构：① 核心结论 3-5 句 → ② 检索策略 → ③ Top 帖子证据 → ④ 其他观察/噪音 → ⑤ 限制与复核方式'
    ;;
  ask)
    TEMPLATE='回答下面的问题。可用 web search 并引用来源。给出你的独立判断，如果你和主流观点不同，直接说出来，不要附和。'
    ;;
  continue)
    TEMPLATE='继续上一次对话。'
    ;;
  *)
    echo "BAD_MODE: $MODE（应为 x|ask|continue）" >&2
    exit 2
    ;;
esac

PF=$(mktemp "${TMPDIR:-/tmp}/grok-prompt-XXXXXX.txt") || { echo "MKTEMP_FAILED" >&2; exit 3; }
ERR="${PF%.txt}.err"
trap 'rm -f "$PF" "$ERR"' EXIT

{
  printf '%s\n\n' "$BOUNDARY"
  printf '%s\n\n' "$TEMPLATE"
  printf '用户问题：\n'
  cat "$QUERY_FILE"
} > "$PF"

if command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD="timeout 330"
else
  TIMEOUT_CMD=""
fi

if [ "$MODE" = "continue" ]; then
  $TIMEOUT_CMD "$GROK_BIN" --prompt-file "$PF" -c --output-format plain 2>"$ERR"
else
  $TIMEOUT_CMD "$GROK_BIN" --prompt-file "$PF" --output-format plain 2>"$ERR"
fi
EXIT=$?

if [ "$EXIT" = "124" ]; then
  echo "[grok 超时 5.5 分钟，模型可能卡住，重试或简化问题]" >&2
elif [ "$EXIT" != "0" ]; then
  echo "[grok exit $EXIT] $(head -2 "$ERR" 2>/dev/null)" >&2
fi

exit "$EXIT"
