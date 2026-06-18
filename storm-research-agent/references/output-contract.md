# Output Contract

## Language

Default to Chinese unless the user asks for English.

Use English only when explicitly requested.

For bilingual output:

1. Write 中文版 first.
2. Write English version second.
3. Keep claims, sources, confidence scores, risks, and the final decision identical across both versions.
4. Do not make the English version more generic, more optimistic, or less evidence-bound.

Keep technical terms such as STORM, Practitioner, Academic, Skeptic, Economist, Historian, peer review, and `needs verification` when they improve precision. Explain them in Chinese when needed.

## File Paths

When the current project has a `03_analysis/` directory or the user asks for files, save to one of:

```text
03_analysis/YYYY-MM-DD-storm-{short-topic}-zh.md
03_analysis/YYYY-MM-DD-storm-{short-topic}-en.md
03_analysis/YYYY-MM-DD-storm-{short-topic}-bilingual.md
```

Choose the suffix from the language mode.

## Completion Report

Report:

- Input sources
- Output path
- Whether Feishu was modified
- Whether an X draft or publish staging package was created
- Whether anything was published
- Verification performed

Default for Feishu, X draft, staging, and publish is “no” unless explicitly requested.

## Quality Bar

A valid result must include:

- Source chain or explicit `needs verification` labels
- 5 perspectives
- At least 3 contradictions
- At least 1 blind spot
- Confidence scores
- A final decision card
- Chinese-first output for Chinese audiences
- Mirrored claims when bilingual output is requested
