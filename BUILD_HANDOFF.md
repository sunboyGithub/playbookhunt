# Build Playbook Hunt without the original app repository

Share the following files/folders together. The existing playbookhunt_app repository is not required and should be left out.

## Share list

1. AGENTS.md — current project brief, stack, ranking/privacy rules, and agreed scope.
2. playbookhunt_prompt/ — ordered coding prompts, execution plan, tracker, and background references.
3. playbookhunt_design/ — current UI decisions, historical visual frames, and brand assets with source/license notes.
4. playbookhunt_content_templates/ — three authored starter playbooks, a matching starter catalog, blank template, filled example, and broader catalog plan.
5. This BUILD_HANDOFF.md file.

A recipient builds a new implementation from these materials. This is a specification/content handoff, not a runnable copy of the existing application or a guarantee of an identical implementation.

## Start here

Read AGENTS.md, then playbookhunt_design/CURRENT_DESIGN.md and the content README. Run P0 onward from playbookhunt_prompt/playbookhunt_coding_agent_prompts.md, one prompt at a time, in a new app workspace. P12c/P12d contain the final feedback/request designs. Phase 2 requires a separate decision.

Set up the new workspace with:
- A copy of AGENTS.md at its root.
- Original PNG frames copied to docs/design/, plus CURRENT_DESIGN.md in that folder.
- assets/muse-avatar.png copied to docs/brand/muse-avatar.png and, during implementation, public/brand/muse-avatar.png.
- assets/agents/ copied with its license and README to public/brand/agents/ during implementation.
- Content copied according to playbookhunt_content_templates/README.md.

Copy the prompt folder into the new workspace documentation if desired, and adjust relative paths to match the new structure. No absolute path from the original author's machine is required. Runtime source files, database migrations, tests, CI, and deployment configuration are work to implement using the prompts; they are not bundled here.

## Resolve differences

Current user instructions and AGENTS.md take priority. The latest coding prompts and CURRENT_DESIGN.md describe final behavior. The execution plan, tracker, reference notes, and original mockups contain historical proposals; they must not override the later decisions. Numbers in mockups are illustrative. The main prompt's reference to a local commit is provenance, not an artifact the recipient needs.

## Accounts and content

The recipient supplies their own domain, service accounts, credentials, legal review, and real-world testing. The target is about 48 curated playbooks across eight categories; this package supplies only three authored, untested examples. catalog_plan.yaml includes unwritten ideas. Do not fabricate missing playbooks or outcomes to meet a target.

Share only the listed package. Do not include playbookhunt_app/, environment files, session logs, database backups, user reports, evidence uploads, or test-results screenshots. Retain asset licenses and source acknowledgments.
