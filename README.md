# Contest Skill

Contest Skill is a Chinese mathematical modeling contest skill for Codex-style AI agents.
It packages a contest workflow from problem reading to paper writing, with reusable
references, output contracts, code snippets, answer-table schemas, and writing templates.

The goal is practical contest execution: split the problem, identify subproblem types, choose
primary and backup routes, inspect data, build a baseline, export first deliverables, validate
results, and convert stable outputs into Chinese paper sections.

## What It Does

- Reads a contest problem and splits it into subproblems.
- Classifies each subproblem as ranking, prediction, optimization, classification, statistical analysis, process explanation, or a combined workflow.
- Recommends contest-safe primary routes and backup routes.
- Forces early data inspection around grain, keys, time axis, proxy targets, repeated measurements, and answer-table schema.
- Provides reusable baseline snippets for ranking, forecasting, optimization, preprocessing, threshold-time tasks, and structured classification.
- Provides output contracts for route selection, execution plans, validation, final answer artifacts, and writing packages.
- Helps draft Chinese modeling-paper sections from actual result tables, figures, and validation notes.

## What It Does Not Do

- It does not include contest statements, attachments, datasets, full papers, or official answer workbooks.
- It is not an automatic award-winning solver.
- It does not replace contest rules, academic integrity requirements, or human verification.
- It does not turn low-evidence methods such as deep learning, CVaR, or compositional transforms into default choices.

## Installation

Copy the skill folder into your Codex skills directory:

```bash
cp -R contest-skill ~/.codex/skills/contest-skill
```

Then invoke it explicitly with `$contest-skill`, or let Codex trigger it when the task is clearly about mathematical modeling contests.

## Example Prompts

```text
Use $contest-skill to analyze this modeling contest problem and produce a Chinese executable workflow.
```

```text
用 $contest-skill 帮我拆解这道赛题，判断每问题型，并给出主模型、备选模型和验证方案。
```

```text
用 $contest-skill 检查我当前的模型和论文草稿，指出 P0/P1/P2 缺口。
```

```text
用 $contest-skill 根据这些结果表写摘要素材池、图表映射和每问结论句。
```

## Folder Layout

```text
contest-skill-open/
├── README.md
├── LICENSE
├── NOTICE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── scripts/
│   └── check_package_paths.py
├── contest-skill/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── assets/
│   │   ├── end_to_end_demo/
│   │   ├── paper-template/
│   │   ├── snippets/
│   │   └── xlsx-schema/
│   ├── scripts/
│   │   └── deliverable_lint.py
│   └── references/
│       ├── code-templates.md
│       ├── common-pitfalls.md
│       ├── chinese-phrasing.md
│       ├── data-inspection.md
│       ├── figure-code-templates.md
│       ├── model-selection.md
│       ├── output-contracts.md
│       ├── plotting.md
│       ├── problem-typing.md
│       ├── validation.md
│       ├── paper-writing.md
│       └── distill/
└── docs/
    └── evals/
        ├── expected-behavior.md
        └── smoke-prompts.md
```

## Usage Model

- 默认中文输出（除非用户明确要求英文）。
- Skill 调用时优先使用最小上下文：按阶段调用对应 `references/*.md`。
- 输出优先级：可交付产物 > 过程解释。
- 在关键阶段使用 `references/output-contracts.md` 强制结构化输出。

## Package Contents

- `contest-skill/SKILL.md`: Core workflow and trigger instructions.
- `contest-skill/references/`: Stage-specific playbooks and output contracts.
- `contest-skill/references/distill/`: Distilled modeling and writing rules.
- `contest-skill/assets/snippets/`: Lightweight baseline code assets.
- `contest-skill/assets/paper-template/`: Chinese paper skeleton and section templates.
- `contest-skill/assets/xlsx-schema/`: Answer-table schema anchors.
- `contest-skill/assets/end_to_end_demo/`: Minimal ranking-to-table demo.
- `contest-skill/scripts/deliverable_lint.py`: Lightweight delivery completeness check.

## Evidence Policy

The skill is distilled from recurring modeling and writing patterns observed across recent
mathematical modeling contest materials and excellent-paper examples. Conclusions are labeled
by evidence strength:

- `高频共性`: repeated across multiple strong examples; suitable as a default rule.
- `中频经验`: stable in some examples; suitable as a candidate route.
- `低频个例`: appears in a narrow setting; should not become a default.
- `弱证据`: useful as a caution or inspiration only.

Evidence labels such as `2021-C066` are compact identifiers for summarized patterns. This
package does not redistribute the underlying papers or contest attachments.

## Minimal Integration Idea

This package can be used in two ways:

1. as a direct `.agents/skills` drop-in (same relative paths)
2. as a standalone repo copy, then wire into your Codex plugin/runtime by your own plugin manifest

## Runtime Notes

The snippets are intentionally lightweight and meant as contest baselines. Depending on which
assets you use, Python packages such as `pandas` and `matplotlib` may be needed. Optimization
or classification extensions may require additional libraries chosen by the user or agent.

## Optional Dependencies

The core skill instructions are Markdown and do not require Python packages. Optional runtime
assets may need common scientific Python libraries:

```bash
pip install pandas matplotlib
```

Some user-extended optimization, classification, or statistical workflows may also use packages
such as `scipy`, `scikit-learn`, `statsmodels`, or a linear/integer programming solver. Install
those only when a specific contest workflow needs them.

## Package Checks

Before publishing a release, run:

```bash
python3 scripts/check_package_paths.py
```

This checks that package-local references inside `contest-skill/` resolve within the packaged
skill folder, and that common private or non-packaged path markers are not present elsewhere.

## Files In This Package

- Open-source metadata files: `README.md`, `LICENSE`, `NOTICE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`
- Core skill logic: `contest-skill/SKILL.md`, `contest-skill/agents/openai.yaml`
- Reference playbooks: `contest-skill/references/*`
- Runtime assets: `contest-skill/assets/*`
- Minimal delivery lint: `contest-skill/scripts/deliverable_lint.py`
- Distill knowledge base: `contest-skill/references/distill/*`
- Package path check: `scripts/check_package_paths.py`

## Note

This package includes the runtime assets explicitly referenced by `SKILL.md`. Keep the package focused on reusable
contest assets; do not add private contest data, full papers, or case-specific project scripts.
