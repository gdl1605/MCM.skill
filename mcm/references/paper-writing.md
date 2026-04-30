# Paper Writing

Serves `SKILL.md` Step 8: convert modeling outputs into contest-ready paper content.

Call this file when:

- You already have a model route or final results.
- You need to draft abstract, problem analysis, results, or conclusion.
- You need to rewrite technical output into paper language.

## Hard Language Rule

- 默认用中文写比赛论文、答卷、图注、表注、摘要素材池和审查意见。
- 除非用户明确要求英文，否则不要生成英文版正文。
- 变量名和文件名可保留英文，但段落、表头、结论句必须是中文。

## Asset Hooks

- 从零起稿时，先参考 `assets/paper-template/paper_skeleton.md`。
- 单问已有稳定结果表时，先用 `assets/paper-template/section_fill_blanks.md` 起草本问结果块。
- 第一版稳定结果出现后，立刻用 `assets/paper-template/abstract_pool_template.md` 填四栏摘要素材池。
- 若当前题已有 `assets/xlsx-schema/` 下的 schema，正文结论优先围绕 schema 中的最终答卷支撑列来写，不要围绕临时中间列写结论。

## Default Structure: Recommended, Not Mandatory

Use this order as the default reference for high-scoring Chinese contest papers:

1. Abstract
2. Problem restatement
3. Problem analysis
4. Assumptions and notation
5. Data description / preprocessing
6. Model building and solving by question
7. Result analysis
8. Model evaluation and extension
9. Conclusion
10. References
11. Appendix if needed

External requirements override the default structure:

- If the contest, school, teacher, or template gives a required format, follow that first.
- If the task is a short report, presentation outline, workbook explanation, or other non-standard deliverable, adapt the section set to that format.
- Use the default structure only when no stronger external format exists.

Keep the core body around this chain:

`problem -> model -> result -> interpretation -> back to prompt`

For decision or classification questions, do not stop there. Add a final answer block:

`problem -> model -> result -> interpretation -> final recommendation/判定表 -> back to prompt`

## Abstract Material Pool First

Do not wait until the final writing sprint to invent the abstract.

Start a small four-column pool as soon as the first stable result appears:

- Background: contest scenario and overall task
- Method: module or model used for each question
- Result: the most decision-relevant outputs
- Strength: robustness, interpretability, template-ready delivery, or practical value

If this pool does not exist yet, build it before polishing the abstract. If the repository already has `assets/paper-template/abstract_pool_template.md`, fill that template first instead of freehanding the pool.

## Schema-To-Text Hook

When a schema file exists for the current problem:

- keep table names and key columns consistent between the exported result table, the final answer artifact, and the paper text
- let正文优先解释 schema 中的最终答卷支撑列，例如 `replenishment_kg`、`selling_price_yuan_per_kg`、`recommendation`、`label`、`priority`、`expected_benefit`
- treat temporary analysis-only columns as appendix or validation material unless they also appear in the final answer artifact

可直接套用的中文句式：

- “由表 x 中的 `date`、`category_name` 与 `replenishment_kg` 可见，……。”
- “根据表 x 的 `priority`、`data_item` 与 `expected_benefit`，优先建议……。”

## Minimal Writing Output Contracts

Do not let writing stop at “we can draft later”. At minimum, output:

- one structure decision:
  - 默认建模论文结构
  - 或外部格式优先说明
- one abstract material pool
- one result block per question
- one conclusion sentence per question

### Minimal section template by question

```text
[问题编号]
1. 本问要回答什么：
2. 使用了什么模型/规则：
3. 得到了什么结果表/图：
4. 结果说明了什么：
5. 因此对题目应给出的结论是：
```

## Abstract Formula

Use this four-part structure:

1. Background and task
2. Method by question or by module
3. Key results
4. Model strengths or usefulness

### Stable abstract pattern

- Sentence 1-2: state the contest scenario and the overall task.
- Sentence 3 onward: name each main module and what it solves.
- Final middle sentences: report the most decision-relevant results.
- Final sentence: state robustness, interpretability, or practical value.

Do:

- Tie each model to a question.
- Include at least one concrete result.
- End with something the judges can trust.

Do not:

- Repeat the problem statement without methods.
- List model names without roles.
- Claim the result is “good” without evidence.

## Section Templates

## 1. Problem Restatement

Write:

- One short scenario sentence
- One data source sentence
- One line per question explaining the real deliverable
- If the prompt provides a workbook, template, or named result file, name that output object explicitly here

Avoid:

- Long background retelling
- Copy-paste from the prompt

## 2. Problem Analysis

Write:

- What type each question is
- Which questions are upstream vs downstream
- Why the chosen workflow is reasonable

Useful pattern:

- “Question 1 is essentially a ranking task, so we first construct…”
- “Question 2 depends on Question 1, so we restrict the candidate set and then optimize…”

## 3. Assumptions

Write only assumptions that the later model actually uses.

Good assumptions:

- Noise reduction
- Stable-operating simplifications
- Parameter-treatment conventions
- Feasibility assumptions aligned with constraints

Bad assumptions:

- Empty clichés such as “ignore external factors” with no later consequence

## 4. Model Building And Solving

For each question, keep this order:

1. State what the model must solve
2. Define the variables or indicators
3. Write the objective / rule / relation
4. State the constraints or decision logic
5. Explain the solving method
6. Present the result in contest language

If the question asks for a scheme, timing, grouping, or判定方法, end the subsection with:

- one final answer sentence
- one compact table containing the recommended boundary / timing / label rule
- one sentence explaining why judges should trust this recommendation

If the question is open-ended recommendation or data-collection advice, end the subsection with:

- one prioritized table such as `data item -> use -> benefit`
- one sentence explaining which items are most urgent

Do not open with equations before the reader knows what they do.

## 5. Result Analysis

For each result block:

1. Point to the table or figure
2. State the observed pattern
3. Explain what it means
4. Tie it back to the original question
5. State the final deliverable object if the question requires a recommendation, ranking, label, or timing rule

For decision-heavy tasks, add:

5. State the final recommended scheme explicitly, not just the trend behind it

Good pattern:

- “From Table x, the top suppliers remain stable across…”
- “Figure y shows that profit improves under…”
- “This means the proposed plan better satisfies…”

### Standard Chinese result-to-answer pattern

Use a contest-facing ending sentence such as:

- “综上，针对问题 x，建议采用……方案，详见表 x。”
- “因此，可将……判定为……，完整结果见表 x。”
- “由此得到的排序结果表明……应优先……，见表 x。”
- “综合收益与风险后，最终推荐……，对应策略表见表 x。”

## 6. Model Evaluation And Extension

Cover:

- Why the route works
- Where it may fail
- Which assumptions or parameters matter most
- How the model could be extended later

Avoid generic praise such as “the model is simple and practical”.

## 7. Conclusion

Summarize by question, not by method.

Good pattern:

- “For Question 1, we obtained…”
- “For Question 2, we proposed…”
- “For Question 3, the analysis shows…”

Do not rewrite the abstract.

For each question, the conclusion should still answer “so what should be done / adopted / judged” in one line.

If a formal template file exists, the conclusion should also tell the reader which result table/workbook contains the full answer.

## Useful Transition Patterns

### Problem-analysis transitions

- “The core of Question x is to quantify…”
- “Since Question y depends on Question x, we first… and then…”
- “This task is essentially a constrained decision problem.”

### Model-introduction transitions

- “To characterize the relation between…”
- “Under the constraint that…, we maximize/minimize…”
- “Considering the data exhibit…, we adopt…”

### Result transitions

- “The results show that…”
- “Compared with the baseline…”
- “This indicates that…”

### Figure-table transitions

- “As shown in Figure x, …”
- “From Table x and Figure y together, …”
- “The heatmap further confirms that…”

## Result Language And Figure Citation

Prefer:

- “shows”
- “indicates”
- “suggests”
- “is significantly higher/lower than”
- “remains stable within”
- “is sensitive to”

Avoid:

- “挺好”
- “效果非常不错”
- “很厉害”
- “大概说明”
- abstract lines with no concrete result

## Direct-Use vs Adapt-Before-Use

These are usually safe to reuse almost directly:

- Section ordering
- Abstract structure
- Result paragraph order
- Formal verbs for trends, comparisons, and conclusions

These usually need adaptation before use:

- Any sentence containing problem-specific nouns
- Any sentence containing numeric conclusions
- Assumptions tied to a specific contest setting
- Claims about robustness or innovation

If a sentence depends on the current task’s object, data, or result, rewrite it before putting it into the paper.
