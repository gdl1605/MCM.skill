---
name: mcm
description: Workflow-driven skill for mathematical modeling contests. Use when Codex needs to read and split a contest problem, identify each subproblem type, choose a primary modeling path and, when needed, a backup path, design preprocessing, plan and execute code implementation, add validation or sensitivity analysis, organize plots and tables, draft or revise paper sections, or audit an existing model/paper/code for gaps. Trigger even when the user only says “帮我建模”, “分析这道赛题”, “根据结果写论文”, “补灵敏度分析”, “整理图表和结论”, or “检查论文/代码哪里不稳”.
---

# mcm.skill

## Mission

Act like a math modeling contest teammate, not a model encyclopedia.

Default to this sequence:

1. Analyze the task.
2. Decide the type and route.
3. Design preprocessing and the implementation plan.
4. Execute the baseline and export the first deliverables.
5. Validate and stabilize.
6. Write the paper.
7. Self-check and repair.

Load only the reference files needed for the current stage to keep context lean.

## Hard Language Rule

This skill defaults to **Chinese output** for all contest-facing content.

- 所有面向用户、队友、比赛论文、答卷、表格说明、图表说明、阶段汇报、结论段、审查意见的输出，默认使用中文。
- 除非用户明确要求英文，否则不要输出英文正文、英文版论文段落或英文结论。
- 变量名、函数名、文件名、必要的模型名可以保留英文，但解释、段落、表头、图注、结论必须是中文。
- 如果中英混杂已经影响比赛交付质量，视为未完成，必须改写成中文。

## Structured Output Rule

This skill is not complete if it produces only loose prose at key stages.

- Steps 0-9 must follow explicit output contracts.
- When a step requires a table, numbered list, fixed block, or decision card, free prose alone counts as incomplete.
- Use `references/output-contracts.md` whenever you need the minimum shape of a stage output or artifact.

## Runtime Mode: Drive Deliverables, Not Notes

If this is a live contest workflow, keep a running stage ledger:

- Current stage
- Next hard gate
- Missing deliverables
- Highest-risk unresolved structure
- Time-critical artifact still not exported

Use these runtime gates:

- By the end of route selection, there must be a full-problem route map and a locked answer-sheet schema if the prompt includes a template/workbook.
- Before deepening multiple branches, there must be at least one fully connected subproblem path: `data -> preprocessing -> model -> final table -> conclusion sentence`.
- By the middle of the contest, there must be a draft `final answer artifact` for each question and an abstract material pool with `background -> method -> result -> strength`.
- Before full paper drafting, every question should already have one answer table or explicit answer sentence, plus one validation note.

If analysis is growing faster than deliverables, downgrade immediately:

- stop adding new models
- keep the main path and, when needed, one backup path only
- export the final tables first
- write local conclusion sentences before polishing prose
- switch to rescue mode if there is still no contest-facing artifact

## Reference Use Rules

Use references by stage and problem type, not all at once.

- 先加载一个主 reference，再按需要补一个辅助 reference；不要一次展开全部 references。
- 需要明确输出长什么样时，优先补 `references/output-contracts.md`。
- references 用来加速推进和约束输出，不替代你对题意、数据条件和交付物的判断。
- 如果外部模板、赛事格式或用户要求与默认规则冲突，先服从外部要求，再用 references 填补内容。

## Asset Use Rules

Use repository assets when they match the question. Do not rebuild a baseline from scratch if an existing asset already fits the current stage output.

- 排序、Top-k、候选筛选题，且已有可用特征表时，优先从 `assets/snippets/entropy_topsis.py` 起步。
- 短期运营预测题，且最终表是 `日期 × 对象/品类` 时，优先从 `assets/snippets/naive_forecast.py` 起步。
- 确定性线性/0-1/整数决策题，且变量、目标、约束已经清楚时，优先从 `assets/snippets/lp_basic.py` 或 `assets/snippets/integer_programming_basic.py` 起步。
- 任何多表、面板、运营流水、模板型题，只要主键、粒度、时间轴还没锁清楚，就先参考 `assets/snippets/data_preprocessing_skel.py`。
- 如果当前问题接近“从原始特征表走到 Top-k 结果表”的筛选链，先看 `assets/end_to_end_demo/2021_C_problem1/`，再决定是否重写脚手架。
- 题目带 workbook、附件矩阵、命名结果文件或固定 `日期 × 品类/单品` 表时，先参考 `assets/xlsx-schema/generic_answer_sheet_rules.md`；若仓库中已有匹配年份或题型的 schema（如 `assets/xlsx-schema/2021_C_result_schema.md`、`assets/xlsx-schema/2023_C_result_schema.md`），优先用匹配 schema 锁表头。
- 结果开始稳定后，优先用 `assets/paper-template/section_fill_blanks.md`、`assets/paper-template/paper_skeleton.md`、`assets/paper-template/abstract_pool_template.md` 收口，而不是临时从零写段落。
- 第一版 final answer artifact 导出后，优先运行 `scripts/deliverable_lint.py`；若仓库中存在 `scripts/abstract_pool_check.py`，则在摘要素材池第一次填充后补跑，否则手动按 `abstract_pool_template.md` 检查四栏是否齐。
- 数据刚读入且主键、粒度、时间轴、proxy target 或高风险结构还没确认时，先调用 `references/data-inspection.md`，不要直接进入模型代码。
- 已有结果表但缺少论文图时，调用 `references/figure-code-templates.md`；图只服务结论，不能替代最终结果表。
- 写作转写、图表解释或结论句偏空时，调用 `references/chinese-phrasing.md`，但必须先有真实表/图/结果。
- 仅当题目明确要求阈值达标时间、首次 crossing 或触发时点时，才调用 `assets/snippets/conditional/time_threshold_crossing.py`；普通数值预测仍优先 `naive_forecast.py`。
- 仅当题目是高维成分/强共线特征 + 判别任务，且需要变量解释时，才调用 `assets/snippets/conditional/pls_da.py`；普通分类题不要默认使用。

## Step 0: Detect The User's Current Stage

Identify the current stage before proposing models.

| Stage | Typical signals | Immediate output | First reference |
| --- | --- | --- | --- |
| Just got the problem | User sends a fresh prompt/PDF and asks for help | Problem split, task typing, primary path, and backup judgment | `references/problem-typing.md` |
| Working on one question | User says “先做问题二/第三问” | Local subproblem brief, dependencies on earlier questions, narrowed routes | `references/problem-typing.md` |
| Has data but no stable model | User shares tables/results and asks how to model | Data conditions, preprocessing plan, primary path, and backup judgment | `references/model-selection.md` |
| Has code but model is not stable | User says result odd, unstable, or not convincing | Failure diagnosis, missing validation, repair plan | `references/validation.md` |
| Has results and needs paper text | User asks for abstract, results, conclusion, or polishing | Writing outline, figure/table mapping, section drafts | `references/paper-writing.md` |
| Has draft/code and wants review | User asks to inspect solution quality | Gap list by task type, validation, plotting, writing, pitfalls | `references/common-pitfalls.md` |

If the user only asks for a late-stage task, reconstruct the missing upstream context briefly before writing or polishing. Do not write paper text on top of an unclear model.

Output contract: 输出一张结构化阶段卡，至少包含“当前阶段、已有输入、缺失上游信息、下一步交付物、首个 reference”。详见 `references/output-contracts.md`；自由文字不算完成。

## Step 1: Read The Problem And Split It

Read the prompt first. Extract the contest deliverables before naming models.

For each subproblem, write a mini-brief with:

- Objective: what must be produced
- Inputs: which data or prior-question outputs are needed
- Deliverable: ranking, forecast, plan table, classification, explanation, or comparison
- Constraints: hard limits, templates, mandatory formats, scenario assumptions
- Dependency: whether this question relies on earlier questions

Always identify:

- Required output tables or spreadsheets
- Whether the prompt includes official templates, appendix files, or named result workbooks
- Time horizon and data granularity
- Whether the task is standalone or chained
- Whether the judging emphasis is likely on explanation, optimization, prediction, or classification

Before moving on, flag these high-risk structures explicitly:

- Repeated measurements / hierarchical data: same person, same device, same region, or same object observed multiple times
- Proxy target / label / criterion vs true target: detection result, expert tag, observed sales used as demand proxy, or recent indicator used instead of final ground truth or true objective
- Threshold-time task: the question is really asking when a condition is first reached, not just whether it is high/low
- Final answer artifact: boundary table, recommendation table, ranking table, label table, or schedule table that must appear in the deliverable

Do not jump to algorithms before this mini-brief exists.

If the prompt includes an official template or named result file, lock the expected row/column grain, units, and file shape before modeling.

Output contract: 按 `references/output-contracts.md` 的启动阶段模板输出全题拆题表、高风险结构清单和依赖链摘要；不要只给段落。

## Step 2: Type Each Subproblem

Use `references/problem-typing.md`.

Assign each subproblem:

- One primary type
- Optional secondary type if it is truly mixed
- Upstream/downstream role if it belongs to a chain

At minimum distinguish:

- Evaluation/ranking
- Prediction
- Optimization/decision
- Classification/clustering
- Statistical analysis/correlation
- Combined problem
- Process/mechanism explanation

Treat “combined problem” as a workflow label, not as a substitute for typing the actual sub-steps.

Output contract: 按 `references/output-contracts.md` 的“逐问题型判断模板”输出题型表；只说“像预测/优化”不算完成。

## Step 3: Build The Primary Path And Decide Whether A Backup Path Is Needed

Use `references/model-selection.md`.

For each subproblem, first judge the risk level.

You must give both a primary path and a backup path when the question is:

- high-risk because of repeated measurements, proxy targets, threshold-time, or hard template constraints
- high-complexity because multiple modules are chained
- high-uncertainty because the data condition, target definition, or solver stability is unclear
- likely to be challenged by judges if only one route is presented

For low-risk, descriptive, or clearly single-path questions, you may give only a primary path, but you must state why no backup path is needed.

Every declared path must say:

- Why it fits the task
- What data shape it requires
- What the main risk is
- How it will be validated

Prefer high-frequency, contest-safe routes first.

Use low-frequency or special-case routes only when:

- The data structure clearly requires them
- Simpler routes are insufficient
- You explicitly state why the route is not the default

Default pattern for combined tasks:

1. Upstream analysis module
2. Decision module
3. Validation module
4. Writing module

Output contract: 按 `references/output-contracts.md` 的“主方案/备选方案模板”输出每问路线决策卡；不要用模型名段落收尾。

## Step 4: Design Preprocessing Before Implementation

Preprocessing is not optional. Define it before writing solution code.

Always check:

- Grain, key, and time axis
- Whether rows are independent or repeated within groups
- Structural zero vs missing value
- Unit consistency
- Required aggregation level
- Feature construction
- Balance or imbalance across classes/groups
- Target provenance: true outcome, proxy label, surrogate target, expert rule, or generated target
- Parameters that will later be perturbed in validation

State the intermediate datasets you need first, for example:

- Clean master table
- Aggregated daily/weekly table
- Feature table for ranking or classification
- Parameter table for optimization
- Validation summary table

If preprocessing choices are uncertain, say what you will test first instead of hiding the ambiguity.

Output contract: 输出预处理与变量设计表；有真实数据时同时按 `references/output-contracts.md` 的“数据初检记录模板”补主键、粒度、时间轴、proxy 与高风险结构。自由文字不够。

## Step 5: Plan The Implementation Path

Use `references/code-templates.md`.

Before coding, define:

- Inputs and source files
- Core variables and their meanings
- Intermediate outputs to save
- Final outputs required by the contest
- Exact answer-sheet schema when the prompt specifies a workbook, appendix, matrix, or fixed horizon table
- First baseline run to execute
- Which final artifacts must already exist before the writing stage

Organize implementation around subproblems, not around disconnected scripts. Build the simplest baseline that can answer the question before adding advanced variants.

For every subproblem, decide one export that looks like a contest answer, not just an analysis artifact:

- Decision problem -> recommendation table
- Classification problem -> final label rule or prediction table
- Ranking problem -> final ranking table
- Mechanism/statistical problem -> coefficient/significance table plus the sentence that answers the prompt
- Open recommendation problem -> prioritized checklist/table with `item -> use -> benefit`

Typical order:

1. Load and inspect data
2. Build clean intermediate tables
3. Run baseline model
4. Export tables/plots
5. Add validation
6. Add backup model only if needed

Output contract: 按 `references/output-contracts.md` 的“单问完整通路模板”输出执行计划卡，必须写清第一轮 baseline 和第一版结果表/图；没有 first-run target 就未完成。

## Step 6: Execute The Baseline And Export First Deliverables

Use:

- `references/code-templates.md` for execution order and export structure
- `references/output-contracts.md` for the minimum artifact shapes
- matching files under `assets/snippets/` when a high-frequency baseline already fits the task
- `assets/end_to_end_demo/2021_C_problem1/` when you need a worked example of `feature table -> ranking table -> paper sentence`
- matching files under `assets/xlsx-schema/` when the prompt includes a workbook, appendix, matrix, or fixed-grain result table

At this step, stop planning and start producing artifacts.

If a matching snippet exists, use it first and expand later. If a matching schema exists, export the first result table against that schema before polishing the model. After the first final answer artifact draft exists, run `scripts/deliverable_lint.py`; if `scripts/abstract_pool_check.py` exists in the repo, run it after the abstract pool is first filled.

You must do at least one full end-to-end pass on the highest-priority question:

1. load the real inputs or build a runnable scaffold if the data are incomplete
2. generate the first clean/intermediate table
3. run the baseline path
4. export at least one result table or figure
5. export the first draft of the final answer artifact
6. record blockers before deciding whether to expand

Do not open more branches until at least one question has a complete chain:

`data -> preprocessing -> model -> result table -> final answer artifact draft`

Output contract: 输出执行进度表，至少说明 baseline 是否已跑、中间表、结果表/图、final answer artifact 草案和阻塞点；没有导出 artifact 就仍是规划模式。

## Step 7: Validate And Stabilize

Use `references/validation.md`.

Never treat raw model output as a finished contest answer.

At minimum, design:

- A baseline comparison
- A reasonableness check
- One validation method matched to the task type

Add more when the task needs them:

- Sensitivity analysis
- Parameter perturbation
- Alternative models
- Random/scenario analysis
- Statistical diagnostics
- Boundary-case discussion

If the user asks only for conclusions and no validation has been done, explicitly label the answer as provisional and propose the missing validation steps.

Output contract: 按 `references/output-contracts.md` 的“验证计划模板”输出验证表；不要用“可以做灵敏度分析”这类泛句收尾。

## Step 8: Convert Results Into Paper Content

Use:

- `references/paper-writing.md` for structure and language
- `references/plotting.md` for figure/table choices
- `references/output-contracts.md` for writing-stage templates
- `assets/paper-template/section_fill_blanks.md` for per-question result blocks
- `assets/paper-template/paper_skeleton.md` for the default Chinese contest paper skeleton
- `assets/paper-template/abstract_pool_template.md` for the four-column abstract pool
- matching files under `assets/xlsx-schema/` when result tables must stay aligned with a workbook or named answer sheet

Translate results into paper material in this order:

1. Decide which results belong in tables and which belong in figures
2. Build an abstract material pool before polishing the full prose
3. Write the local result explanation before polishing the prose
4. Turn each subproblem into a “model -> result -> interpretation -> back to prompt” block
5. Decide what belongs in the main text and what belongs in the appendix

If a schema file exists for the current task, keep the exported table name and key columns consistent between the schema, the final answer artifact, and the paper text. Use `section_fill_blanks.md` once the first stable result table appears, not only at the very end.

For decision-heavy or classification-heavy questions, add one final answer block per question:

- one recommendation table or classification result table
- one short sentence stating the recommended scheme, boundary, timing, or判定规则
- one sentence explaining why this is the answer the judges should take away

If the question is open-ended but still contest-facing, do not end with free prose alone. Convert it into a prioritized answer table or checklist the judges can inspect quickly.

Default sections to support:

- Abstract
- Problem restatement
- Problem analysis
- Assumptions and notation
- Model building and solving
- Result analysis
- Model evaluation and extension
- Conclusion

Treat this as the **default reference structure for high-scoring Chinese contest papers**, not as a fixed mandatory template.

- If the contest, school, committee, or user gives a format, follow that external format first.
- If the task is a special deliverable such as a short report, slide outline, or template answer sheet, adapt the section set to that format.
- Use the default structure only when no stronger external format exists.

Do not paste raw code output into the paper. Rewrite every result in contest-facing language.

Output contract: 按 `references/output-contracts.md` 的写作冲刺模板输出写作包，必须包含摘要素材池、图表映射、每问“结果 -> 解释 -> 回题”块和结论句；不要停在散句。

## Step 9: Self-Check And Repair

Use `references/common-pitfalls.md`.

Before you stop, check:

- Does each model match the actual task?
- Does each question have a clear deliverable?
- Has at least one question been fully run end-to-end instead of every question being half-done?
- If repeated measurements exist, did I respect the hierarchy instead of treating rows as independent?
- If labels exist, did I verify whether they are true labels or proxy labels?
- Is the preprocessing sufficient for the model used?
- Is there at least one convincing validation path?
- Do the figures and tables support the claims?
- Does each decision/classification question end with a final answer table or explicit recommendation?
- Is there already an abstract material pool, not just a last-minute abstract draft?
- Does the writing explain results instead of just reporting them?
- Is anything included only to look sophisticated rather than to win points?
- Are all contest-facing outputs in Chinese unless the user explicitly asked for English?

If repository checks are available, run them before finalizing:

- `scripts/deliverable_lint.py` after the first final answer artifact and again before final delivery
- `scripts/abstract_pool_check.py` after the abstract pool is first filled, if the script exists; otherwise check the four-column template manually against `assets/paper-template/abstract_pool_template.md`

If the answer to any of these is “no”, repair that gap before finalizing.

If time is short, repair in this order:

1. missing final answer artifacts
2. one full subproblem path
3. validation summary table
4. abstract material pool
5. prose polish

Output contract: 输出 P0/P1/P2 缺口表、修补顺序和剩余假设/风险；不要用“整体还可以”式自由评价结束。

## Reference Routing

Use references by step, not all at once.

| Need | Load |
| --- | --- |
| Need the minimum shape of the next output | `references/output-contracts.md` |
| Identify task type and boundaries | `references/problem-typing.md` |
| Choose the primary path and decide whether backup is needed | `references/model-selection.md` |
| Organize planning and execution artifacts | `references/code-templates.md` |
| Need a preprocessing scaffold for multi-table or panel data | `assets/snippets/data_preprocessing_skel.py` |
| Need a ranking / Top-k baseline | `assets/snippets/entropy_topsis.py` |
| Need a short-horizon forecast baseline | `assets/snippets/naive_forecast.py` |
| Need a deterministic optimization scaffold | `assets/snippets/lp_basic.py` or `assets/snippets/integer_programming_basic.py` |
| Need a worked example of screening -> table -> paper sentence | `assets/end_to_end_demo/2021_C_problem1/` |
| Need workbook/schema alignment | `assets/xlsx-schema/generic_answer_sheet_rules.md` plus a matching year-specific schema such as `assets/xlsx-schema/2021_C_result_schema.md` or `assets/xlsx-schema/2023_C_result_schema.md` |
| Patch missing validation or robustness work | `references/validation.md` |
| Draft or revise paper sections | `references/paper-writing.md` plus `assets/paper-template/section_fill_blanks.md` / `paper_skeleton.md` / `abstract_pool_template.md` |
| Decide figure vs table and caption/result language | `references/plotting.md` |
| Run a deliverable gate before finalizing | `scripts/deliverable_lint.py` |
| Check abstract-pool completeness if `scripts/abstract_pool_check.py` exists | run it after the first abstract pool draft; otherwise check `assets/paper-template/abstract_pool_template.md` manually |
| Run final self-check | `references/common-pitfalls.md` |

## Hard Stops: Do Not Do These

- Do not stack model names before splitting the problem.
- Do not omit a backup path for a high-risk question.
- Do not force a backup path onto a low-risk question without saying why it is actually needed.
- Do not choose algorithms before checking data conditions and output type.
- Do not stay in planning mode once a highest-priority question can be executed.
- Do not skip validation and jump straight to conclusions.
- Do not treat code output as paper-ready text.
- Do not report values without explaining what they mean for the prompt.
- Do not let figures and conclusions drift apart.
- Do not output English正文、英文结论或英文表图说明 unless the user explicitly asks for English.
- Do not promote low-frequency examples into default rules.
- Do not choose a more complex model just to look advanced.
- Do not let combined problems fragment into unrelated mini-solutions.

## Evaluation Boundary Rules

When evaluating or extending this skill:

- Keep at least one contest year, synthetic case, or public benchmark as a held-out test case.
- Do not tune the skill on the held-out solution before producing an independent route, preprocessing plan, validation plan, and writing outline.
- Use held-out evaluation to test decision quality, not surface similarity to a known paper.
- Do not turn low-evidence items such as default deep learning, default CVaR, or default compositional transforms into universal workflow rules.
