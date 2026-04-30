# Expected Behavior

This file defines the minimum behavior expected from Contest Skill during smoke checks.

## Language

- Contest-facing outputs default to Chinese.
- English is allowed for file names, variable names, code identifiers, and user-requested English output.

## Structure

Key stages must produce structured outputs, such as tables, decision cards, numbered plans, or fixed blocks.
Loose prose alone is insufficient for:

- problem splitting
- subproblem typing
- primary/backup route selection
- preprocessing design
- data inspection
- execution planning
- validation planning
- final answer artifact drafting
- writing sprint packaging
- final review

## Modeling Route

The skill should:

- identify the deliverable before naming models
- prefer explainable contest-safe baselines first
- provide backup routes for high-risk or decision-heavy questions
- avoid treating low-evidence methods as defaults
- connect upstream analysis, prediction, ranking, or classification outputs to downstream decisions when the problem is chained

## Data And Artifacts

The skill should ask for or define:

- data grain, primary keys, and time axis
- target provenance, including proxy targets
- repeated measurements or hierarchical structures
- schema for answer workbooks, recommendation tables, ranking tables, prediction tables, or classification tables
- at least one final answer artifact before paper polishing

## Validation

The skill should include at least one validation route matched to the task type:

- ranking stability for evaluation tasks
- naive or recent-history baseline for prediction tasks
- feasibility and sensitivity checks for optimization tasks
- error inspection and feature interpretation for classification tasks
- diagnostics or robustness checks for statistical/process models

## Writing

The skill should convert results into Chinese contest-paper material only after result tables, figures, or validation notes exist.
Writing packages should include:

- abstract material pool
- figure/table mapping
- result explanation by question
- back-to-question conclusion sentence
- limitations or robustness notes when relevant
