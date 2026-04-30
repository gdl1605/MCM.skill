# Contributing Guide

Thank you for improving this skill package.

## Scope of contribution

Please contribute in one of these scopes:

- Documentation clarity and templates in `contest-skill/references/*`
- Distill rules in `contest-skill/references/distill/*`
- Metadata/metadata-quality improvements in `contest-skill/SKILL.md`
- Packaging/docs improvements in root docs (`README`, `LICENSE`, `NOTICE`, `SECURITY`, `CHANGELOG`)

## Before changing

1. Keep changes small and scoped to one stage (problem typing, model selection, validation, writing, packaging).
2. If a change affects output shape, update the corresponding reference contract.
3. Ensure Chinese default language requirements are preserved.
4. Prefer evidence-backed changes: cite rule sources from `contest-skill/references/distill/evidence-map.md` when updating strategy rules.
5. Label new modeling or writing rules with an evidence tier: `高频共性`, `中频经验`, `低频个例`, or `弱证据`.

## Open-source boundaries

- Do not commit contest statements, official attachments, datasets, answer workbooks, full papers, or large verbatim excerpts.
- Do not commit private paths, local machine paths, credentials, API keys, or `.env` files.
- Do not add case-specific project scripts unless they are generalized into reusable `contest-skill/assets/` or `contest-skill/scripts/` assets.
- If you add a new packaged path in `SKILL.md` or `references/*.md`, make sure that file is included in `contest-skill/`.

## Style

- Keep markdown clean and avoid unrelated refactors.
- Avoid adding file bloat; keep the package minimal and reusable.
- Use structured outputs (tables/checklists) for stage contracts.

## PR checklist

- [ ] `README.md` remains accurate for the included files.
- [ ] Core references still coherent with `SKILL.md`.
- [ ] No changes that break dependency paths in this package.
- [ ] Sensitive or non-open data paths are not introduced.
- [ ] New strategy rules include an evidence tier.
- [ ] Output-shape changes are reflected in `contest-skill/references/output-contracts.md`.
- [ ] `python3 scripts/check_package_paths.py` passes from the repository root.

## Testing

No automated tests are required for docs-only changes.
For pipeline changes, provide a short smoke-run example and expected artifact path list.
For release preparation, run the smoke prompts in `docs/evals/smoke-prompts.md` and compare against `docs/evals/expected-behavior.md`.
