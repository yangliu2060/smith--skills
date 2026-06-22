#!/usr/bin/env python3
"""Lightweight Loop Spec v1 linter.

This is intentionally text-first: it catches missing contract fields without
adding a YAML dependency.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "spec_version",
    "kind",
    "status",
    "name",
    "purpose",
    "use_when",
    "do_not_use_when",
    "inputs",
    "authority",
    "state",
    "round",
    "next_action_rule",
    "working_signal",
    "acceptance_gate",
    "terminal_states",
    "outputs",
    "provenance",
]

ROUND_FIELDS = ["observe", "choose", "act", "verify", "record"]
TERMINAL_FIELDS = ["success", "clean_noop", "blocked", "approval_required", "exhausted", "stagnated"]

PLACEHOLDERS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"<[^>\n]+>",
    r"\[[^\]\n]+\]",
    r"待定",
    r"待补充",
]

VAGUE = [
    r"keep trying",
    r"until satisfied",
    r"until it feels good",
    r"make sure it works",
    r"as needed",
    r"看情况",
    r"直到满意",
    r"感觉可以",
]

PRIVATE_LEAKS = [
    r"/Users/[A-Za-z0-9._-]+",
    r"C:\\Users\\",
    r"/home/[A-Za-z0-9._-]+",
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"\b(api[_-]?key|token|secret|password)\b\s*[:=]",
    r"\binternal\b.*\bdomain\b",
]


def has_field(text: str, field: str) -> bool:
    return bool(re.search(rf"(?m)^\s*{re.escape(field)}\s*:", text))


def load_json_if_possible(path: Path, text: str) -> dict | None:
    if path.suffix.lower() != ".json":
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def lint_text(text: str, source: str, profile: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def error(message: str) -> None:
        findings.append({"level": "error", "source": source, "message": message})

    def warning(message: str) -> None:
        findings.append({"level": "warning", "source": source, "message": message})

    for field in REQUIRED_FIELDS:
        if not has_field(text, field):
            error(f"missing required field `{field}`")

    for field in ROUND_FIELDS:
        if not has_field(text, field):
            error(f"missing round field `{field}`")

    for field in TERMINAL_FIELDS:
        if not has_field(text, field):
            error(f"missing terminal state `{field}`")

    if not re.search(r"spec_version\s*:\s*1\b", text):
        error("`spec_version` must be 1")

    if not re.search(r"kind\s*:\s*agent-workflow-loop\b", text):
        error("`kind` must be agent-workflow-loop")

    if not re.search(r"status\s*:\s*(draft|provisional|tested|published)\b", text):
        error("`status` must be draft, provisional, tested, or published")

    for pattern in VAGUE:
        if re.search(pattern, text, re.IGNORECASE):
            error(f"dangerously vague instruction matched `{pattern}`")

    for pattern in PRIVATE_LEAKS:
        if re.search(pattern, text, re.IGNORECASE):
            error(f"possible private leak matched `{pattern}`")

    if re.search(r"\b(must|required)\b.{0,40}\bAskUserQuestion\b", text, re.IGNORECASE):
        error("runtime-specific AskUserQuestion cannot be mandatory")

    if re.search(r"Loop Library|Forward Future|catalog\.json", text, re.IGNORECASE):
        if not re.search(r"https?://", text):
            warning("external Loop Library reference should include a source URL")

    if profile == "runnable":
        for pattern in PLACEHOLDERS:
            if re.search(pattern, text, re.IGNORECASE):
                error(f"unresolved placeholder matched `{pattern}`")
    else:
        undeclared = [
            pattern for pattern in PLACEHOLDERS
            if re.search(pattern, text, re.IGNORECASE) and "parameters:" not in text
        ]
        if undeclared:
            warning("template placeholders found but no `parameters` field declares them")

    return findings


def lint_file(path: Path, profile: str) -> list[dict[str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [{"level": "error", "source": str(path), "message": f"cannot read file: {exc}"}]

    data = load_json_if_possible(path, text)
    if data is not None:
        text = "\n".join(f"{key}:" for key in data.keys()) + "\n" + text

    return lint_text(text, str(path), profile)


def self_test() -> int:
    good = """
spec_version: 1
kind: agent-workflow-loop
status: tested
name: Source proof loop
purpose: Verify source-backed claims.
use_when: Evidence changes the next action.
do_not_use_when: The user only needs a static checklist.
parameters: {}
inputs: []
authority:
  may_read: []
  may_write: []
  must_ask_before: []
state:
  stores: []
  update_rule: Record source and decision.
round:
  observe: Read the source.
  choose: Continue, revise, stop, or escalate based on evidence.
  act: Change one claim.
  verify: Re-read source and compare.
  record: Save source URL and decision.
next_action_rule: If proof is weak, gather another source; if contradicted, revise; if proven, stop.
working_signal: More claims have direct evidence.
acceptance_gate: All key claims cite real sources.
terminal_states:
  success: Evidence passes.
  clean_noop: No claims need changes.
  blocked: Source unavailable.
  approval_required: Needs private source.
  exhausted: Round cap reached.
  stagnated: No improvement after two rounds.
outputs: []
provenance:
  sources: []
  generated_at: 2026-06-22
"""
    bad = "name: Bad\nround:\n  act: keep trying until satisfied\n"
    if lint_text(good, "good", "runnable"):
        print("self-test failed: good spec produced findings", file=sys.stderr)
        return 1
    if not any(item["level"] == "error" for item in lint_text(bad, "bad", "runnable")):
        print("self-test failed: bad spec produced no errors", file=sys.stderr)
        return 1
    print("Loop spec lint self-test passed.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lint Loop Spec v1 files.")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--profile", choices=["template", "runnable"], default="runnable")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return self_test()

    if not args.files:
        parser.error("provide at least one spec file or --self-test")

    findings: list[dict[str, str]] = []
    for raw in args.files:
        findings.extend(lint_file(Path(raw), args.profile))

    if args.format == "json":
        print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
    else:
        for item in findings:
            print(f"{item['level']}: {item['source']}: {item['message']}", file=sys.stderr)
        if not findings:
            print("Loop spec lint passed.")

    return 1 if any(item["level"] == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
