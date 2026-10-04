# Playbook Hunt content handoff

This folder can be shared without the app repository. It contains authored content and templates, not user submissions, reports, evidence, or database exports.

## Files

- `playbooks/`: three complete authored examples: lower your internet bill, find cheaper car insurance, and plan seven days in Japan. They are marked `tested: false`. A published content status means visible content, not a verified result.
- `use_cases_and_kits.yaml`: starter catalog referencing only the supplied playbooks, with all eight categories.
- `playbook_template.yaml`: blank authoring template. Fill required fields before validation; do not import the blank template itself.
- `playbook_example_lower-your-internet-bill.yaml`: valid filled example, also present in playbooks/. Do not import it twice.
- `catalog_plan.yaml`: broader planned catalog, including unwritten playbooks. Keep as planning material, not the initial import catalog. The target is about 48 playbooks; only three are supplied here.

## Copy into a new app

Copy playbooks/*.yaml to content/playbooks/, the starter use_cases_and_kits.yaml to content/use_cases_and_kits.yaml, and the template/example files to content/templates/. Build the importer and validator using P3. Import only content/playbooks/*.yaml and the starter catalog.

## Content rules

- Never author tried counts, success percentages, savings statistics, or fake reports. New imports start with empty statistics.
- At most two inputs may be required. Every input key must match a {{key}} in the prompt and every placeholder must reference an input. Keys are lowercase and unique. The creator UI generates keys automatically; YAML authors supply them explicitly.
- Choice inputs need choices. Keep optional-input explanations in content where useful; do not force creators to edit technical metadata.
- Curated YAML import currently uses 3–5 non-empty steps. The separate creator-submission form accepts 1–5 completed steps; do not reintroduce the three-step minimum into creation.
- Keep tested false until a real test supports the claim. The blank template defaults to false.
- Only add real source URLs. Use sources: [] when none are supplied.
- Outcome type selects the report measurement: monthly/yearly/one-time money, hours, or binary outcome. It is not an outcome statistic.
- No preview images are supplied for these playbooks. Leave preview_image empty instead of inventing evidence.

The examples have been checked against the current content schema. Blank templates and the broader catalog plan are intentionally not ready-to-import content.
