# loopforge

把模糊工作流锻造成可维护、可验证、可复用的 AI-agent workflow loop。

## 适合做什么

- 从成功案例、聊天记录、prompt、草稿或工作历史里提炼可复用 loop。
- 创建 `loop-spec-v1` YAML/JSON。
- 同时输出一份给人复制使用的模块化 Loop Prompt。
- 审查已有 loop：`Ready`、`Repair needed`、`Not actually a loop`。
- 区分 loop、goal、SOP、checklist、cron job、一次性任务和系统动力学 feedback loop。

## 不适合做什么

- 查找官方 Loop Library 已发布条目。
- 直接执行 loop。
- 只写 `/goal` 指令。
- 做泛泛的增长飞轮或系统反馈环分析。

## 默认输出

生成 loop 时默认输出两部分：

```text
## Loop Spec
<loop-spec-v1 YAML/JSON>

## Loop Prompt
<可复制给 agent 直接运行的一份模块化提示词>
```

除非用户明确要求 machine-only output，否则不要只给 YAML。

## 快速使用

```text
用 loopforge 把这个工作流变成可复用 loop spec 和提示词：
<贴上你的流程、prompt、运行记录或成功案例>
```

## 校验

```bash
python3 loopforge/scripts/lint_loop_spec.py --self-test
python3 loopforge/scripts/lint_loop_spec.py --profile runnable path/to/spec.yaml
```

`template` profile 允许声明过的占位符；`runnable` profile 要求可直接运行，不能有未替换占位符。
