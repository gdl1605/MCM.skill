# Smoke Prompts

Use these prompts as lightweight release checks before publishing a new version of mcm.skill.
They are not benchmark datasets and do not require private contest materials.

## 1. Fresh Problem Split

```text
Use $mcm to analyze this modeling contest problem. Please split the problem, identify each subproblem type, give primary and backup routes, and list the first deliverables.

Problem summary:
A city wants to optimize shared-bike deployment. It provides station-level daily rentals, weather, holidays, and maintenance records. Question 1 asks for usage patterns. Question 2 asks for next-week station demand forecasts. Question 3 asks for a relocation plan under truck-capacity and labor constraints. Question 4 asks what extra data should be collected.
```

Expected behavior:

- Output is in Chinese unless the prompt explicitly requests English.
- Includes a full-problem split table.
- Identifies statistical analysis, prediction, optimization, and open recommendation components.
- Gives a primary route and explains whether each question needs a backup route.
- Lists first deliverables, including at least one final answer artifact table.

## 2. Single-Question Route Selection

```text
用 $mcm 只处理问题三：基于各站点未来一周预测需求，在车辆容量、调度次数和人工成本约束下制定共享单车调度方案。请给出主方案、备选方案、预处理表和验证计划。
```

Expected behavior:

- Recognizes the task as an optimization/decision problem with prediction as upstream input.
- Defines decision variables, objective, and constraints before naming algorithms.
- Provides a backup or robustness route because the question is decision-heavy.
- Produces a structured validation table, not only prose.

## 3. Writing From Results

```text
用 $mcm 根据这些结果写论文材料：问题二已经导出 station_demand_forecast.csv，问题三已经导出 relocation_plan.csv 和 sensitivity_summary.csv。请生成摘要素材池、图表映射、每问结果解释和结论句。
```

Expected behavior:

- Does not invent unsupported numerical values.
- Builds a four-field abstract material pool: 背景、方法、结果、特点.
- Maps result tables/figures to paper sections.
- Gives result-to-question conclusion sentences in Chinese.
- Mentions validation or sensitivity evidence when interpreting the relocation plan.

## 4. Review Existing Work

```text
用 $mcm 检查我当前的建模方案：我已经做了预测模型和几张趋势图，但还没有最终推荐表，也没有灵敏度分析。请输出 P0/P1/P2 缺口和修补顺序。
```

Expected behavior:

- Uses a review/audit posture.
- Flags missing final answer artifact as a P0 or high-priority gap.
- Flags missing robustness or sensitivity analysis.
- Produces a repair order instead of only general advice.
