# Playbook Hunt — Coding Agent Prompts

Companion to `playbookhunt_execution_plan.md`. Prompts are ordered; run them one at a time.

After the P12-v2 baseline, run **P12c — Tester feedback**, then **P12d — Request a playbook page**, before Phase 2. These follow-ups are now implemented locally through P12d (commit 3398a0f); they were not part of P12-v2. The prompts below describe the final agreed behavior for future agents. Multi-agent activation remains deferred.

## How to use
0. For a new independent build, read `../BUILD_HANDOFF.md` and create your own empty app workspace. The original `playbookhunt_app` repository is not part of this handoff and is not needed. Copy the parent AGENTS.md, design assets/references, and starter content using the handoff guide, then run coding sessions inside your new workspace. Configure your own Supabase, Vercel, Resend, PostHog, and Sentry accounts. Repository creation and publishing are separate actions requiring the project owner's instruction.
1. Run **P0** first. It creates `AGENTS.md` (the project brief). Every later prompt tells the agent to read it.
2. Use **one prompt per session / PR**. Review the PR against its acceptance criteria before moving on.
3. If the agent drifts, paste the relevant section of `playbookhunt_execution_plan.md` (ranking spec, data model, homepage v2).
4. Update `AGENTS.md` when decisions change so later prompts inherit them.
5. First read `../playbookhunt_design/CURRENT_DESIGN.md` (or your copied design folder). The historical design frames are copied to `docs/design/`; point the agent to the matching PNG (or attach it) when running P4–P8: Frame 1 → P4, Frame 2 → P5, Frame 3 → P6, Frame 4 → P7, Frame 5 → P8, Frames 8–9 (sign-in, My playbooks) → P8, Frame 6 (card system) and Frames 7a–7b (mobile) → every UI prompt.

Every prompt includes these standard working rules; some prompts add task-specific verification and delivery constraints:

> **Working rules:** Read `AGENTS.md` first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run `pnpm lint`, `pnpm typecheck`, and `pnpm test` and fix failures before finishing. Summarize what you built, what you verified, and anything left open.

---

## P0 — Project brief (`AGENTS.md`)

```text
Create a file AGENTS.md at the repo root containing the project brief below, verbatim but cleaned up as Markdown. Also create CLAUDE.md that just says "See AGENTS.md". Do not write any other code.

# Playbook Hunt — Project Brief

Name: Playbook Hunt. Domain: playbookhunt.com (NEXT_PUBLIC_SITE_URL=https://playbookhunt.com). Social handle: @playbookhunt. The brand is agent-neutral; the product is Muse-first for launch.

## What we are building

A search-first website where people find AI-agent "playbooks" (prompt + inputs + steps) for a real task, try them in their AI agent, and report whether they worked. The differentiator is REAL-WORLD OUTCOME DATA, not a big prompt library.

Core loop: Task → Discover → Try → Report → Aggregate → Rank → Discover again.

Example card: "Lower your internet bill — 1,247 tried · 68% worked (n=412) · Median $18/mo · Verified 3 days ago · Tested with Muse".

## v1 scope

In: target ~48 curated playbooks across 8 categories (the shared starter pack currently contains 3 authored, untested examples); homepage; search/filters; /playbooks, /categories + category pages, /kits + starter kit pages, /use-cases/[slug] pages (homepage Popular Use Cases); playbook detail with Save and Share; try flow with agent picker; sign-in (Google, Facebook, email link) with pending-action resume; Save + My playbooks (/me: Saved / Tried / Reported); outcome reports with optional evidence and optional Muse referral code; follow-up emails; stats & ranking; admin/moderation; playbook requests; Create a playbook form that goes to admin review; analytics; SEO; /how-we-verify page; private tester feedback via footer/report-success, with an admin Feedback queue.

Out (phase 2): public creator profiles, Inspired-by claims/thanks, creator referral links on playbooks, comments, votes.

## Stack

Next.js (App Router, RSC, Server Actions, TypeScript strict), Tailwind CSS + shadcn/ui, Supabase (Postgres, Auth, Storage, RLS), Resend (email), PostHog (analytics), Sentry, Vercel. pnpm. Vitest + Playwright. zod for validation. cmdk for the ⌘K palette.

## Categories

personal-finance 💰, travel-booking ✈️, travel-planning 🗺️, shopping 🛍️, small-business 🏢, productivity ⚡, health 🏥, creativity 🎨.

## Agents

Data-driven (agents table) with capabilities (info, web_actions, phone_calls) and status (active / coming_soon / hidden):

- muse: active, primary, recommended, preselected.
- chatgpt-dots: display name "ChatGPT"; legacy internal identifier retained for compatibility. Status coming_soon (greyed), not selectable in v1.
- grok-bot: display name "Grok"; legacy internal identifier retained for compatibility. coming_soon (greyed).
- manus: coming_soon (greyed).
- instinct, Claude and Gemini: not listed (status hidden).

In the UI, Muse is the only selectable agent for now; all coming_soon agents render as greyed, disabled chips with no extra labels or explanations. "Open in <agent>" URL templates are config; if prefill support is not verified, copy the prompt and open the agent's home page instead.

## Design system

- Light theme. Background #FAF9F6, cards white, border #E7E5E0, radius 12–16px, generous whitespace.
- Accent (primary CTA) #FF5A1F. Outcome colors: worked #16A34A, partly #F59E0B, didn't #DC2626.
- Muse blue #2A66DE (soft #E8EFFC, dark text #1D4FB8, line #C3D4F5), sampled from the Muse logo. Use it for everything Muse: the word "Muse" in the hero headline, the Muse agent chip, and the "Open in Muse" button. Wherever Muse appears as an agent, show the official Muse avatar (/public/brand/muse-avatar.png, the fluffy character, circular crop) inside a Meta-blue ring (#0081FB, ~14% of the radius).
- Font: Inter or Geist; monospace for prompt blocks.
- One PlaybookCard component in three densities: rich (preview image, category tag top-left, badge, title, promise, evidence lines, agent chips, creator avatar, hover "Try"), compact (title, agent icons +N, evidence line, avatar), row (rank #, icon, title+promise, tags, right-side evidence box).
- Below the report threshold, show "Early · N reports" instead of a percentage.

## Ranking rules (non-negotiable)

- Evidence score = 0.55·WilsonLowerBound(success) + 0.20·outcomeStrength + 0.15·recency + 0.10·usage. Weights in config.
- Success: worked=1, partly=0.5, didn't=0. Reports weighted by trust (email verified, evidence approved, account age) and decayed with a 60-day half-life. Author's own, rejected and outlier reports weigh 0.
- Show % only when report_count >= 20; show median only when amount_n >= 10.
- "Proven to work" requires >= 20 reports and >= 3 evidence-approved reports.
- Trending is a separate score from recent tries/reports (48h half-life over 7 days).
- Votes, referral links, referral codes, credits and follower counts NEVER affect ranking.
- Optional Muse referral codes on reports are displayed only on verified reports, one per user, labeled as a referral, with a link to Muse's official referral terms.

## Creation and requests

Keep creation focused on the task: no public creator-name field or live attribution line in the form. Retain existing P10b author credit; public profiles and further attribution work are deferred. /request is a public, dedicated task-request page using the same protected submission flow as empty search results. The dedicated page requires Topic (an icon grid with two columns on mobile and naturally wrapping chips on wider screens), Goal (a matching-purpose dropdown), and a task; every goal list includes Something else. Use the form heading “What would you like AI to help with?” without a separate introductory paragraph. Omit the privacy helper on this page; show concise send errors only after failure and dismiss them when editing. Email remains optional. Topic changes clear the purpose but preserve typed text. Store readable topic/purpose context with the request for admin review; no sign-in required. Keep compact empty-search requests working.

## Data integrity

Never fabricate stats. Seed data has empty stats. Numbers in wireframes are illustrative only.

## Privacy

Evidence uploads go to a private bucket, visible only to the uploader and admins. Encourage redaction. No PII in analytics events. Tester feedback and optional reply emails are admin-only; store pathname context without query strings/fragments. Feedback uses rate limiting, Turnstile, and idempotent server submissions, and never affects ranking.

## Footer

Keep the shared footer compact: How we verify / Request / Create / Privacy / Terms / Feedback. Three columns and two rows on mobile, one wrapping row on desktop; preserve 44px touch targets and omit the tagline. Mobile-menu labels and report-success Send feedback remain descriptive.

## Conventions

- src/app for routes, src/components (ui/ = shadcn), src/lib (supabase, ranking, analytics, validation), src/server (server actions/queries), supabase/migrations, content/playbooks/*.yaml, scripts/.
- Server-side data access through typed query functions in src/server; no Supabase calls from client components except auth.
- All tables have RLS. Admin checks happen server-side.
- Accessible (keyboard, labels, contrast AA), responsive down to 360px.
- Mobile parity (match Frames 7a/7b): every desktop feature exists on mobile with the same copy, rules and states. Header → logo, search icon, ☰ menu (Sign in or avatar, Playbooks, Starter kits, Categories, + Create a playbook, Report a result, footer links). Popular Use Cases shows 2 tiles + peek + arrow. Detail: Save ☆ and Share ↗ icon buttons in the top bar, Works with (Muse + greyed agents), copy toast above a sticky "Try this playbook / Report" bar. Try, Report, Sign-in and Share open as bottom sheets; My playbooks uses stacked cards. Every UI prompt must ship desktop and mobile together and include a Playwright check at 390×844.
- Keep dependencies minimal; ask before adding a major one.

## Build-package references

This parent folder is a standalone specification and content package; the existing app repository is not required or included in the handoff. Read BUILD_HANDOFF.md first. Run the prompts in playbookhunt_prompt/playbookhunt_coding_agent_prompts.md in order in your own new app workspace.

Use playbookhunt_design/CURRENT_DESIGN.md for current UI decisions; older PNG/HTML frames illustrate the original design and do not override this brief or the updated prompts. Use playbookhunt_content_templates/playbooks/ for the three authored starter playbooks, and its README for template and catalog instructions. Never treat the planned catalog as finished or tested content.

For installed Next.js versions, read the relevant framework documentation before implementation. Use client navigation for internal links, including the home logo; avoid blank-page/full-page skeleton flashes, and verify delayed transitions in a production build on desktop and mobile.
```

---

## P1 — Scaffold the app

```text
Goal: Scaffold the Playbook Hunt Next.js app per AGENTS.md.

Requirements:
- Next.js latest stable, App Router, TypeScript strict, src/ directory, pnpm.
- Tailwind + shadcn/ui initialized. Add components: button, card, badge, input, dialog, sheet, tabs, select, checkbox, dropdown-menu, toast/sonner, skeleton, avatar, tooltip, command.
- Design tokens from AGENTS.md in the Tailwind theme / CSS variables (background, card, border, accent, muse blue, worked/partly/didnt, radius). Inter or Geist via next/font.
- Supabase: @supabase/ssr helpers for server components, server actions, middleware (session refresh), and a browser client. Env vars in .env.example: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, RESEND_API_KEY, NEXT_PUBLIC_POSTHOG_KEY, SENTRY_DSN, NEXT_PUBLIC_SITE_URL. Validate env with zod at startup.
- App shell: header (logo "Playbook" + "Hunt" with "Hunt" in the orange accent, nav: Playbooks, Starter kits, Categories; search trigger showing "⌘K"; "+ Create a playbook" button (requires sign-in → /create); "Report a result" button; Sign in, or the avatar menu when signed in), shared compact footer used on every page (How we verify, Request → /request, Create → /create, Privacy, Terms; P12c adds Feedback). Use three columns on mobile, natural wrapping on wider screens, 44px touch targets, and no tagline. Keep descriptive labels in the mobile menu. Placeholder pages for all routes: /, /search, /playbooks, /categories, /c/[slug], /kits, /k/[slug], /use-cases/[slug], /p/[slug], /create, /request, /how-we-verify, /login, /me, /admin.
- Scaffold in place inside the existing repo and keep `docs/` untouched. Copy `docs/brand/muse-avatar.png` → `public/brand/muse-avatar.png` and `docs/content-templates/*` → `content/templates/`.
- Tooling: ESLint, Prettier, Vitest (with one sample test), Playwright (with one smoke test that loads /), scripts: dev, build, lint, typecheck, test, test:e2e.
- Supabase CLI config (supabase/ folder) for local development.
- README with setup steps (local Supabase, env, dev server).

Acceptance criteria:
- pnpm dev renders the shell with correct colors/fonts on the placeholder homepage.
- pnpm lint, typecheck, test, test:e2e all pass.
- No secrets committed.

Out of scope: database schema, real pages.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P2 — Database schema, RLS, types

```text
Goal: Create the Supabase schema for Playbook Hunt v1 (plus the phase-2 referral table stub).

Tables (snake_case, uuid PKs, created_at/updated_at where sensible):
- profiles(id = auth.users.id, handle unique, display_name, avatar_url, role enum('user','admin') default 'user', created_at) + trigger to create a profile on signup.
- categories(id, slug unique, name, emoji, description, sort)
- agents(id, slug unique, display_name, vendor, prompt_format text, launch_url_template text null, home_url text, capabilities text[] (info|web_actions|phone_calls), status enum('active','coming_soon','hidden'), sort)
- playbooks(id, slug unique, title, promise, category_id fk, status enum('draft','published','archived'), who_for, who_not_for, time_min int, time_max int, outcome_type enum('money_monthly','money_yearly','money_once','time_hours','binary'), outcome_unit text, required_capability enum('info','web_actions','phone_calls') default 'info', report_fields jsonb (e.g. provider options), followup_days int default 7, preview_image_url, primary_agent_id fk, author_id fk profiles null, current_version_id fk null, last_verified_at timestamptz null, search_tsv tsvector generated from title/promise/who_for + category name via trigger, timestamps)
- playbook_versions(id, playbook_id, version int, prompt_template text, changelog text, created_at; unique(playbook_id, version))
- playbook_inputs(id, version_id, key, label, help, why_it_helps, type enum('text','textarea','select','number','money','zip','provider_picker','date'), options jsonb, required bool, sort) — content validation: at most 2 required inputs per playbook.
- playbook_steps(id, version_id, sort, body)
- playbook_agents(playbook_id, agent_id, tested bool, notes; pk both)
- playbook_sources(id, playbook_id, platform enum('x','threads','reddit','rednote','other'), handle, url, title)
- collections(id, slug unique, title, blurb, illustration_url, is_featured, sort); collection_items(collection_id, playbook_id, sort)
- use_cases(id, slug unique, title, description, gradient_from, gradient_to, sort); use_case_items(use_case_id, playbook_id, sort)
- try_events(id, playbook_id, version_id, agent_id, user_id null, device_id text, action enum('started','copied','opened'), created_at)
- outcome_reports(id, playbook_id, version_id, user_id, agent_id, result enum('worked','partly','didnt'), amount numeric null, unit text null, hours_saved numeric null, time_spent_bucket enum('lt15','15_30','30_60','1_2h','2h_plus') null, provider text null, region text null, note text null, referral_code text null, status enum('pending','approved','rejected') default 'approved', is_verified bool default false, is_outlier bool default false, weight numeric default 1, created_at; unique(user_id, version_id))
- report_evidence(id, report_id, storage_path, kind enum('image','pdf'), review_status enum('pending','approved','rejected'))
- followups(id, user_id, playbook_id, try_event_id, due_at, sent_at null, completed_at null)
- playbook_requests(id, query, email null, user_id null, created_at)
- saves(user_id, playbook_id, created_at; pk both)
- playbook_stats(playbook_id pk, tried_count, report_count, worked, partly, didnt, success_rate_raw, wilson_lb, median_amount, p25, p75, amount_n, last30_success, evidence_score, trending_score, last_report_at, updated_at)
- referral_links(id, playbook_id, creator_id, agent_id, url, label, created_at) — phase 2, no UI.

Indexes: GIN on search_tsv, pg_trgm GIN on title, btree on foreign keys, (playbook_id, created_at) on try_events and outcome_reports.

RLS:
- Public read: categories, agents, published playbooks and their versions/inputs/steps/agents/sources, collections, playbook_stats.
- outcome_reports: public read of approved rows but EXCLUDING user_id (expose via a view `public_reports` with display name/initial only); insert by authenticated user for self; update/delete own within 24h; admin all.
- report_evidence + storage bucket 'evidence' (private): owner + admin only. Bucket 'previews' public read, admin write.
- try_events: insert by anyone (anon allowed with device_id); read admin only.
- followups, saves: owner only. playbook_requests: insert anyone, read admin.
- Admin = profiles.role = 'admin', via a SECURITY DEFINER helper is_admin().

Also:
- Seed SQL for categories (8 from AGENTS.md, each with an icon) and agents (muse active with capabilities ['info','web_actions','phone_calls']; chatgpt-dots (display name ChatGPT), grok-bot (display name Grok), manus coming_soon; instinct, claude, gemini hidden).
- Generate TypeScript types to src/lib/database.types.ts and add a pnpm script db:types.
- src/server/queries/*.ts typed query helpers: getPublishedPlaybookBySlug, listPlaybooks(filters), getCategory, getCollection.

Acceptance criteria:
- supabase db reset applies cleanly locally.
- RLS tests (SQL or Vitest against local Supabase): anon cannot read user_id on reports, cannot read evidence, cannot insert reports; a user cannot insert a second report for the same version.
- Types generated and used by query helpers.

Out of scope: UI, ranking computation (P9).

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.

Also: (1) put the categories and agents seed in a migration so prod gets them; (2) leave agent URLs null (not verified yet); (3) use column grants so users can't set status/is_verified/is_outlier/weight on reports or role on profiles; (4) add tags text[] to playbooks and include tags in search_tsv (the YAML template has tags); (5) run DB tests via a separate pnpm test:db (pgTAP, supabase test db); (6) Docker and local Supabase are already running.
```

---

## P3 — Playbook content pipeline

```text
Goal: Let us author playbooks as YAML files and import them into Supabase.

Requirements:
- content/playbooks/<slug>.yaml schema (zod in src/lib/content/schema.ts):
  slug, title, promise, category (slug), status, who_for, who_not_for, time: {min, max}, outcome: {type, unit}, followup_days, primary_agent, agents: [{slug, tested, notes}], preview_image (path under content/previews/ or URL), inputs: [{key, label, help, type, options?, required}], prompt (multiline, uses {{key}} placeholders that must match inputs), steps: [string], sources: [{platform, handle, url, title}], changelog.
- content/use_cases_and_kits.yaml: use_cases (slug, title, description, gradient [c1,c2], sort, playbooks), starter_kits (slug, title, blurb, illustration, featured, playbooks), categories (slug, name, icon). Templates live in content/templates/ (copied from docs/content-templates/ in P1) — use them as the schema source of truth. Playbook YAML may also list use_cases and tags.
- scripts/import-content.ts (pnpm content:import):
  - Validates all files; fails with clear messages (file, field).
  - Upserts playbooks by slug. If prompt/inputs/steps changed, creates a new playbook_version (version+1, changelog) and sets current_version_id; otherwise no new version.
  - Uploads preview images to the 'previews' bucket.
  - Upserts collections and items. Creates an empty playbook_stats row for new playbooks.
  - Dry-run flag prints the diff.
- pnpm content:validate runs validation only (use in CI).
- Add 3 example playbooks drawn from the wireframes (stats empty!):
  1. lower-your-internet-bill (personal-finance, money_monthly, inputs: latest bill, plan name & speed, customer tenure; steps: paste bill → review offers → call/chat with script → log result; who_for: US home internet customers paying > $60/month, 6+ months with the same provider; who_not_for: people on promo pricing).
  2. cheaper-car-insurance (personal-finance, money_yearly).
  3. plan-7-days-in-japan (travel-planning, time_hours).
- Seed content from the templates in content/templates/ (copy them into content/): playbook_example_lower-your-internet-bill.yaml as a real playbook, and use_cases_and_kits.yaml for use cases, starter kits and categories. Items that reference playbook slugs not yet written are skipped with a warning (not an error), so pages render with whatever content exists.

Acceptance criteria:
- Import is idempotent (second run makes no changes).
- Changing a prompt creates version 2 and keeps version 1.
- Unit tests for schema validation and placeholder/input matching.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P4 — Homepage v2 and PlaybookCard system

```text
Goal: Build the homepage and the shared PlaybookCard component. The attached homepage wireframe is the baseline; the section order below extends it.

PlaybookCard (src/components/playbook-card/*), one component with density prop 'rich' | 'compact' | 'row':
- rich: preview image (16:9, rounded, lazy), category tag top-left over image, badge (New / Verified), title, promise (1 line clamp), evidence line 1 "1,247 tried · 68% worked (n=412)", evidence line 2 "Median $18/mo · verified 3d ago", agent chips, creator avatar; on hover/focus show a "Try" button (links to try flow) — on touch devices the button is always visible.
- compact: title (2-line clamp), agent icons with +N, one evidence line, creator avatar.
- row: rank number, category emoji/icon, title + promise, tags, right-side evidence box ("68% worked" large, "n=412" small).
- Threshold logic via a shared formatter src/lib/stats/format.ts: if report_count < 20 show "Early · N reports"; hide median if amount_n < 10; format money by outcome_type ($/mo, $/yr), time as "3 hrs saved"; relative "verified 3d ago". Unit test the formatter.

Homepage sections (server-rendered, data from playbook_stats + playbooks). Match Frame 1 in the Design Frames tab:
1. Hero: H1 "What do you want Muse to do?" with "Muse" in Muse blue; subline "Proven playbooks with real results"; large search input → /search?q=; default placeholder "Save $100 on internet bill", then rotating ("Plan my Japan trip", "Find a cheaper flight", "Research my competitors") with reduced-motion support; counter from real data ("48 playbooks · 3,210 real results reported" — hide the results part when zero); quick links "Best results 2026 · Trending · Recently verified".
2. Category chips (from categories table, each with its icon).
3. "Popular Use Cases" carousel (Zapier style): exactly 4 tiles visible on desktop (2 on mobile), labels centered horizontally and vertically, diagonal gradient backgrounds with a soft light streak (gradient pairs in config), scroll-snap, right arrow button (left arrow appears once scrolled), the next tile peeks and fades out under the arrow, and nothing renders to the right of the arrow (overflow hidden at the container edge); page dots below; keyboard accessible.
4. "Proven to work": 3 rich cards, only playbooks meeting the eligibility rule (>=20 reports, >=3 evidence-approved); if fewer than 3 qualify, label the row "Recently verified" and fill from that.
5. "Top playbooks this week": numbered list of 5 rows by evidence_score.
6. "Trending [category] playbooks": inline switcher chip showing the category icon + name + ▾; switches category client-side (server action); 6 compact cards.
7. "Starter kits": featured collections; each card's right third is the collection illustration (collections.illustration_url, palette-matched), left two-thirds title, 2-line blurb, playbook count.
8. Category explorer: left list with counts, right grid of 6 compact tiles.
9. "Tried an AI playbook? Report your result." block: collage of 3 recent approved outcomes, a Muse-blue note "Bonus: add your Muse referral code to a verified report. If people join Muse with it, you could earn up to 1B Muse tokens.*" (*copy + link come from config pointing to Muse's official terms; hide the note if the config is empty), and a CTA to a report picker.
10. Shared compact footer used on every page: How we verify · Request · Create · Privacy · Terms. P12c adds Feedback (the dialog and report-success entry point still say Send feedback). Final layout: three columns/two rows on mobile, naturally wrapping links on wider screens, 44px touch targets, no tagline or large gaps between rows. Request links to /request; Create links to /create. Keep descriptive mobile-menu labels. Implement the working feedback submission flow in P12c.

⌘K command palette (cmdk): opens from header and ⌘K/Ctrl+K; searches playbooks by title (server action with pg_trgm), shows categories and quick actions (Report a result, Request a playbook).

States: sensible empty states. Keep the current page visible during navigation until the homepage data is ready, including when clicking the PlaybookHunt logo. Homepage sections sharing the same data request should appear together; do not wrap each in a skeleton fallback or add a root loading screen that flashes across every route. Reserve localized loading placeholders for genuinely independent content. Responsive at 360/768/1280. Lighthouse accessibility >= 95.

Acceptance criteria:
- With only the 3 example playbooks and no reports, the page renders without errors and shows "Early · 0 reports" style evidence.
- Playwright test: homepage loads, search submits to /search?q=, ⌘K opens and navigates to a playbook.
- Playwright navigation regression: in a production build, on desktop and mobile (390×844), navigate through Playbooks, Starter kits, Categories, and the header logo back home. Delay destination responses and verify the current content stays visible until the destination is ready. Observe the whole transition, including after releasing the response, so brief blank-page or skeleton flashes fail the test. Extend this check as P5 replaces placeholder routes with real pages.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P5 — Search, results, category & starter-kit pages

```text
Goal: Build /search, /playbooks, /categories, /c/[slug], /kits, /k/[slug], /use-cases/[slug].

Search backend (src/server/search.ts):
- Query parsing: websearch_to_tsquery on search_tsv, plus pg_trgm similarity on title for typos; combine rank = ts_rank + similarity.
- Keyword → category map (src/lib/search/category-keywords.ts, e.g. bill/bills/internet/phone/insurance/save → personal-finance; flight/hotel/airline → travel-booking; trip/itinerary/japan → travel-planning; doctor/lab/insurance claim → health). If text matching returns < 3 results, add the mapped category's top playbooks and show "Matched: "bills" → Personal finance". If still empty, show popular playbooks + the Request form. Search must never dead-end.
- Add a small synonyms map (e.g. "bill" ↔ "bills", "cheap" ↔ "cheaper/save", "trip" ↔ "itinerary/travel", "comcast/xfinity/verizon/att" → internet/phone bill) applied before querying.
- Filters: category, agent (Muse selectable; coming_soon agents listed greyed and disabled; hidden agents not shown), outcome type group (save_money = money_*, save_time = time_hours, plan/research/create via category mapping), verified within 30 days, min reports (0/20/100), time to complete (<15 / 15–60 / 60+ min).
- Sort: best_evidence (default: evidence_score desc, then text rank), most_tried, highest_outcome (median_amount normalized per year, only amount_n>=10), recently_verified, trending.
- Pagination: cursor or page param, 24 per page.

UI:
- URL is the source of truth for all filters/sort (shareable). Use searchParams in the server component; client filter controls update the URL.
- Top: search input (prefilled), outcome-type filter pills (All · Save money · Save time · Plan · Research · Create) with inline search, result count.
- Left filter sidebar on desktop, bottom sheet on mobile.
- View toggle: cards (compact PlaybookCard grid) / list (row density).
- Empty state: "No playbooks yet for '<q>'", related categories, popular playbooks, and a Request this playbook form (inserts into playbook_requests; optional email; Turnstile or honeypot anti-spam).
- /c/[slug]: category header (emoji, name, description, playbook count), same results component pre-filtered.
- /k/[slug]: starter kit header (illustration, title, blurb), ordered playbook list (row density), "Try the whole kit" not needed in v1.
- Header nav destinations: Playbooks → /playbooks (the results page with no query, all published playbooks, sorted Best evidence); Starter kits → /kits (grid of all kits: illustration, title, blurb, count); Categories → /categories (grid of 8 category tiles with icon, description and playbook count → /c/[slug]).
- /use-cases/[slug]: opened from the homepage Popular Use Cases tiles. Header with the tile gradient, title and one-line description, then the results component limited to the use case's playbooks (curated list, cross-category), with the usual filters/sort. Empty state: "We're testing playbooks for this" + Request form.
- Track analytics events (via a thin src/lib/analytics.ts wrapper, no-op if PostHog key missing): search {q_length, filters}, filter_changed, card_click {slug, position}.

Acceptance criteria:
- Searching "comcast" finds lower-your-internet-bill; "japan itinerary" finds plan-7-days-in-japan; typo "insurence" finds cheaper-car-insurance; "lower my bills" and "save money" return Personal finance playbooks via the category map; a nonsense query shows popular playbooks + Request form.
- Unit tests for query building and synonyms; Playwright test for filter → URL → results.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P6 — Playbook detail page

```text
Goal: Build /p/[slug] matching the attached playbook-detail wireframe.

Layout (two columns desktop, single column mobile with sidebar content moved under the header):
Main column:
1. Breadcrumb: Home / <Category> / <Title>.
2. Title (H1), promise, chips: category · "Tested with Muse" (avatar) · "<time_min> to <time_max> min". Top-right of the header: "☆ Save" and "↗ Share" buttons. Save toggles the saves row (★ Saved, Muse blue when saved) and shows a toast "Saved to My playbooks · View saved →"; if signed out it opens the sign-in modal with the title "Sign in to save this playbook" and completes the save after sign-in (see P8 auth rules).
3. Stat tiles (3): Tried (tried_count) · Worked (% with "n = X reports", or "Early · X reports") · Median saved (value with "n = X with amounts", or hidden/"Not enough data").
4. Outcome preview image (if present) with caption "Example result (redacted)".
5. Who this is for / Who this is NOT for.
6. What you'll need: list of inputs with icons by type.
7. The playbook: prompt block (monospace, collapsed to ~4 lines with "Show full prompt"), Copy prompt button (logs try_event 'copied') that switches to "✓ Copied" for 3s and shows a toast "Copied! Paste it into Muse." with the secondary line "Want it filled in with your details? Try this playbook →" (the last part is a link that opens the Try sheet); numbered steps line. "What you'll need" marks each input Required / Optional (with why_it_helps).
8. What happened for others: stacked bar worked/partly/didn't with percentages + "Last 30 days: X%"; "Filter:" chips Provider ▾ (company the reporter dealt with; options from playbook.report_fields), Agent ▾, Result ▾ (worked/partly/didn't); list of recent approved reports showing time spent and agent (result badge, amount, relative date, agent, "Verified" if evidence approved, evidence thumbnail only if the reporter marked it public — v1: never show evidence publicly, show a "Evidence reviewed" tag instead); "Show all reports" pagination; filters by agent, outcome, provider.
9. "Did it work for you?" card with Report your result button.
10. Related playbooks: 3 compact cards (same category, then same collection).
Share: a "Share" button next to the title opens a share sheet (desktop popover, mobile native Web Share API when available) with X, Instagram, Threads, Facebook, WhatsApp, TikTok and Copy link. Use web intent URLs for X/Facebook/Threads/WhatsApp; Instagram and TikTok have no web share URL, so they use the native sheet on mobile and copy-link + toast on desktop. Log share {channel}.
Sidebar (sticky on desktop):
- "Verified N days ago" badge (from last_verified_at; hide if null).
- Primary button "Try this playbook" (opens try flow sheet from P7; for now link to /p/[slug]/try).
- "Works with" block: Muse highlighted in Muse blue with the Muse avatar, "Calls and chats for you · X% worked (n)"; below it one row of greyed, disabled chips for coming_soon agents (ChatGPT, Grok, Manus). No "Coming soon"/"Script only" labels or explanations.
- "Playbook by": use "Playbook Hunt team" for team-authored curated content; approved P10b community submissions show the author’s public-safe display name, or the existing “Community contributor” fallback if absent. Never expose an email address or misattribute community content to the team. Further attribution UI is deferred; do not add a creator-name field or live credit line to /create.
- "Inspired by": list of playbook_sources with platform icon, handle, type, external link (rel="noopener nofollow ugc"); line "Their idea helped N people try this." Thank/Claim buttons are phase 2 — do not render.
- "Good to know": provider/region caveat text (from playbook field or default) + "Last changed: <changelog of current version> <date>".

SEO: generateMetadata (title, description = promise), OG image via next/og showing title + evidence line, JSON-LD HowTo (steps). Do NOT emit AggregateRating in v1 (a success % is not a star rating). Canonical URL. ISR revalidate 300s + on-demand revalidation hook for stats refresh.

Acceptance criteria:
- Page renders for all 3 example playbooks with empty stats (Early states everywhere, bar hidden with "No reports yet — be the first").
- With fixture stats (a test seed), all tiles/bars render correct numbers; thresholds respected.
- Accessibility: headings order, bar has text alternative, buttons labeled.
- Playwright: copy prompt writes to clipboard and fires the try event. Check all three existing playbook detail pages on desktop and 390×844 mobile: ChatGPT/Grok/Manus have logos and remain disabled; Instinct is absent. Test detail pages independently from the Try sheet, including after agent visibility changes.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P7 — Try flow and agent picker

```text
Goal: The "Try this playbook" experience.

Requirements:
- Try UI as a right-side Sheet on desktop / full-screen on mobile, opened from detail page and hover Try on cards; also reachable at /p/[slug]/try.
- Step 1 — Pick your agent: Muse as a large preselected card (Muse blue, Muse avatar, "Recommended", capability + evidence line). Below it one row of greyed, disabled chips (ChatGPT, Grok, Manus) with no labels. Before activating another agent, verify its destination and support it consistently in creation, Try, and Report; a display-name change alone must not enable it. Remember the last choice in localStorage.
- Step 2 — Your details: form generated from playbook_inputs of the current version using reusable field components (provider_picker as chips, money, zip with numeric keyboard, date, textarea). Show "Only <X> is required · stays in your browser". Optional fields show "optional · <why_it_helps>". Internet-bill example: Provider* (Xfinity, Spectrum, AT&T, Verizon, T-Mobile, Cox, Other), Monthly price (optional), ZIP (optional · finds local offers), Latest bill lines (optional · most accurate). Unfilled optional slots are removed from the prompt or shown as [label]. Never send input values to our server or analytics (privacy) — all templating happens client-side.
- Step 3 — Your prompt: rendered prompt_template with {{key}} replaced (unfilled keys shown highlighted as [label]). Per-agent formatting via src/lib/agents/format.ts (e.g. plain text for all by default; hooks to add agent-specific preambles later).
- Actions: "Copy prompt" (primary; switches to "✓ Copied") and "Open in Muse" (Muse-blue button with the Muse avatar; only uses a prefill URL if agents.launch_url_template is verified, otherwise copy + open agents.home_url; template gets the URL-encoded prompt; if the prompt exceeds a safe URL length, copy first and open the agent home). Do not hardcode provider URLs in components; they live in the agents table and must be verified by us before enabling.
- Below the prompt, show "Steps to use the playbook" as a simple bullet list of the creator's instructions. Helper: "Use these instructions as you work through the playbook." Do not show checkboxes or imply that progress input is required.
- Logging: insert try_events ('started' on sheet open with an agent selected, 'copied', 'opened'), with user_id if signed in, else an anonymous device_id cookie (random uuid, httpOnly not required, no PII). Debounce duplicate 'started' per session.
- If signed in: create a followups row due_at = now + followup_days (one per user/playbook while open). If not signed in: after the first copy, show a one-time dismissible card "Save this prompt and get a reminder?" with a single "Sign in" button (opens the SignInModal with reason="reminder") and "Not now" (remember dismissal). Never block copying behind sign-in.
- Mobile: the Try UI is a full-height bottom sheet with stacked fields and large tap targets; add a Playwright mobile-viewport test (iPhone 13) for fill → copy.
- After copy/open: show "Did it work? Come back and report your result" with a Report button.

Acceptance criteria:
- Template rendering unit tests (filled, unfilled, special chars, long prompt).
- Try events recorded correctly for anon and signed-in users (integration test against local Supabase).
- No input values appear in network requests to our backend (test by asserting the server action payloads).

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P8 — Auth, outcome reporting, evidence, follow-ups

```text
Goal: Let users sign in, report outcomes in under 30 seconds, and get reminded to report.

Auth (match Frame 8):
- Supabase Auth with Google, Facebook (Facebook Login = the Meta option available to websites) and email magic link. No Apple login. Sign-in and sign-up are the same step (a new email creates the account).
- One reusable <SignInModal reason="save|report|create|reminder"> with context titles: "Sign in to save this playbook" / "Sign in to report your result" / "Sign in to create a playbook" / "Sign in to get a reminder". Buttons: Continue with Google, Continue with Facebook (Facebook blue #1877F2), "or", email field + "Email me a sign-in link"; fine print "New here? This creates your free account, no password needed…". "Check your email" state with Resend / Use a different email; link expires in 15 minutes.
- When sign-in is required: Save, Report, Create a playbook, reminders. Never required for browsing, search, opening playbooks, Try, Copy prompt or Open in Muse. After the first copy, the Try sheet shows one dismissible soft card (P7).
- Pending action resume: store {action, playbookId, returnTo, scrollY} in sessionStorage before auth; after the callback, return to the same page/scroll and complete the action automatically, then toast (e.g. "Saved · View saved →"). Closing the modal cancels only the pending action.
- Header when signed in: avatar menu (name/email, My playbooks, Create a playbook, Settings & reminders, Sign out).
- /me = "My playbooks" (match Frame 9): tabs Saved (n) · Tried (n) · Reported (n); category filter chips; sort (Recently saved / Best evidence); cards show ★ toggle (unsave), evidence line, "Saved X ago", an "Updated since you saved" badge when the playbook's current version is newer than the save, and "Did it work? Report" on playbooks the user tried but hasn't reported. Empty state: "No saved playbooks yet. Tap ☆ Save on any playbook to keep it here." + "Browse Proven to work". Reports tab allows edit within 24h / delete. Private to the user (RLS).

Report form (dialog from detail page + /p/[slug]/report; requires sign-in):
1. Result: three large buttons Worked / Partly / Didn't (required).
2. Agent used (prefilled from last try, changeable).
3. Amount saved (optional) with unit from outcome_unit (e.g. $/mo or $/yr); for time_hours playbooks ask "Hours saved" instead. Numeric validation and sane max. Match the field to the playbook outcome: internet bill and car insurance collect money saved; Japan planning collects hours saved. Collecting both is a separate enhancement, not part of this prompt.
3b. How long did it take you? (optional chips: < 15 min, 15–30 min, 30–60 min, 1–2 hrs, 2 hrs+).
4. Provider you dealt with / region (optional, shown when the playbook defines them — add optional `report_fields` to the YAML schema/DB as jsonb, e.g. provider select for internet bill).
5. Note (optional, 500 chars).
5c. Your Muse referral code (optional, Muse-blue box): a 6-character input (letters and numbers, e.g. GT09WC) with light-grey placeholder "e.g. GT09WC" that disappears on typing, auto-uppercase, validated with /^[A-Z0-9]{6}$/, helper text "6 characters, letters and numbers. Your code may appear with your verified report on this playbook. Display and placement are not guaranteed."; eligible for display only when the report is verified; one active code per user; text links to Muse's official referral terms from config; never used in ranking.
6. Evidence (optional): a clearly outlined upload area with a visible "Choose image or PDF" button; show the selected filename and Change/Remove controls. Image/PDF, max 5MB, uploaded to the private 'evidence' bucket via signed upload URL only when submitting; strip EXIF on client. Require "I've hidden account numbers and personal info" when uploading and reset that confirmation when the file changes. Explain that evidence is private to the uploader and reviewers.
- Expand "Redaction tips" inline, without navigation or unmounting the form. Opening/closing tips must preserve result, amount, time, provider, note, referral code, and file selection.
- Use consistent, smaller muted "(optional)" labels and "(required)" for Did it work?; keep field labels and units readable. Avoid repeated dot-separated required/optional text. The agent defaults to Muse; user-entered optional fields can remain blank.
- Submit via server action: validates with zod, enforces one report per user per current version (friendly message offering to edit), rate limit (e.g. 10 reports/day/user), inserts report with status 'approved' unless flagged (amount above playbook cap → 'pending' + is_outlier), marks matching followups completed, triggers stats refresh (P9 function) for that playbook, revalidates the playbook page.
- P12c adds a secondary "Send feedback" entry point to this success screen; keep it separate from submitting an outcome report.
- Success screen: "Thanks! Your result is in.", a share sheet (same component as the detail page: X, Instagram, Threads, Facebook, WhatsApp, TikTok, Copy link), and a "Try next" suggestion. Only "Did it work?" is required on the whole form.
- Analytics: report_opened, report_submitted {result, has_amount, has_evidence} (no amounts or notes in analytics).

Follow-ups:
- Scheduled job (Vercel Cron hitting a protected route, or pg_cron + edge function) every hour: find followups due and not sent, send Resend email "Did <playbook> work for you?" with three one-click links (worked/partly/didn't) that open the report form preselected (signed token, expires in 14 days); mark sent_at. Unsubscribe link and a profile setting to disable reminders.

Acceptance criteria:
- Full flow works locally: sign in → try → report → stats update → page shows the report.
- Duplicate report blocked; edit within 24h works; evidence not publicly accessible (test anonymous fetch of the storage path fails).
- Email template renders (React Email) and cron route rejects requests without the secret.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.

Local authentication acceptance:

Configure Supabase redirects for the actual development origin, including localhost ports 3000 and 3001.
Preserve the browser’s origin after authentication, including when Next binds to 0.0.0.0.
Test an actual email magic-link flow through local Mailpit in Playwright, including callback, session cookies, and authenticated navigation. Password-based test sessions alone are insufficient.
Document restarting local Supabase after auth configuration changes without resetting its data.
```

---

## P9 — Stats aggregation and ranking

```text
Goal: Compute playbook_stats and ranking scores exactly per the spec in AGENTS.md.

Implement in TypeScript (src/lib/ranking/*) as pure functions with exhaustive unit tests, and call them from a server-side job that reads raw data and writes playbook_stats. (Alternatively mirror in SQL, but the TS module is the source of truth and must be tested.)

Functions:
- reportWeight(report, reporter, playbook): 1.0 × (email verified ? 1 : 0.5) × (evidence approved ? 1.5 : 1) × (account age < 1 day ? 0.5 : 1); 0 if status rejected, is_outlier, or reporter is the playbook author.
- decay(ageDays, halfLife=60) = 0.5^(ageDays/halfLife).
- successValue: worked 1, partly 0.5, didnt 0.
- wilsonLowerBound(p, n, z=1.96) handling n=0 → 0.
- outcomeStrength(playbook, categoryPeers): percentile of median amount (money normalized to per-year: monthly×12, once as-is) among category peers with amount_n>=5; 0.5 if not computable; time_hours compared only with time_hours peers.
- recency(lastVerifiedAt, halfLife=60).
- usage(tried, maxTried) = log10(1+tried)/log10(1+maxTried).
- evidenceScore = w.wilson·wilson + w.outcome·outcome + w.recency·recency + w.usage·usage with weights from src/config/ranking.ts (defaults 0.55/0.20/0.15/0.10).
- trendingScore(events, now): Σ over events in last 7 days of (try 1, report 3) × 0.5^(ageHours/48).
- outlier detection: once amount_n>=10, flag amount > Q3 + 3·IQR; also any amount > playbook cap.
- aggregate(playbook, reports, tries): tried_count (distinct users/devices with a 'started' event), report_count, worked/partly/didnt counts, success_rate_raw, wilson_lb (weighted), median/p25/p75/amount_n (approved, non-outlier), last30_success, last_report_at, evidence_score, trending_score, eligibility flags (show_rate: report_count>=20, show_median: amount_n>=10, strongest_eligible: report_count>=20 && evidence_approved>=3), badges (verified_recent: last_verified_at within 30d, high_success: wilson>=0.6, top_saver: top 10% outcome in category, most_tried: top 10% tried).

Job:
- refreshPlaybookStats(playbookId) (called after report submit/approve) and refreshAllStats() (cron every 15 min for trending + nightly full). Writes playbook_stats, revalidates affected pages/tags.
- Add columns needed for flags/badges to playbook_stats via migration.

Required test scenarios (fixtures):
1. Playbook A: 500 tries, 30 reports, 40% worked vs Playbook B: 100 tries, 40 reports, 80% worked with evidence → B ranks above A.
2. 5 reports all worked → show_rate false; Wilson low; ranks below a 60-report 70% playbook.
3. Author's own reports and outliers do not change stats.
4. Old reports (1 year) count much less than recent ones.
5. Referral links/votes present in data have zero effect (assert score identical with and without them).
6. Trending favors a playbook with a burst of tries in the last 48h over one with steady old traffic.

Acceptance criteria: all tests pass; homepage/search ordering reflects evidence_score after refresh.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P10 — Admin and moderation

```text
Goal: An /admin area for the founder to run the site.

Access: only profiles.role='admin' (server-side check in layout + every server action). Seed script to promote an email to admin.

Pages:
- Dashboard: counts (published playbooks, tries 7d, reports 7d, pending reports, pending evidence, open requests), top playbooks by evidence_score and trending.
- Reports queue: filter by status/outlier/has evidence/playbook; actions approve, reject (with reason), mark verified; bulk actions; each action triggers refreshPlaybookStats.
- Evidence viewer: signed URL preview (short expiry), approve/reject evidence; approving sets report is_verified and may update playbook last_verified_at if result=worked.
- Playbooks: list with status, stats, last verified; edit core fields (title, promise, who for/not for, status, preview image) — prompt/inputs/steps edits create a new version with a required changelog; "Mark verified now" button sets last_verified_at; preview as public.
- Collections: create/edit starter kits, reorder items (drag or up/down), toggle featured.
- Requests inbox: list playbook_requests grouped by similar query (pg_trgm), mark as planned/done.
- Use cases: create/edit Popular Use Cases (title, description, gradient, sort, ordered playbook list).
- Submissions: queue of "Create a playbook" drafts (see P10b): preview, request changes (comment emailed to the author), approve → publish as a playbook with the author credited, reject.
- Audit log table (admin_actions: admin_id, action, target, payload, created_at) written by every admin action.

Acceptance criteria:
- Non-admins get 404 on /admin routes and server actions reject them (tests).
- Approving/rejecting a report updates stats and the public page.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.

Document signing in with an existing local account, promoting that exact email, and opening /admin. Test the complete magic-link → promoted account → admin dashboard flow.
```

---

## P10b — Create a playbook

```text
Goal: Let signed-in creators submit a playbook for review through a simple form designed for ordinary people. Public creator profiles and creator referral links/codes stay in phase 2.

Creator experience rules:
- Use “Create a playbook” in navigation without a beta label. Explain on the form: “We review submissions before publishing.”
- Address the creator directly. "The user" means the person who will use the published playbook. Avoid ambiguous "they" and unnecessary technical terms.
- Creators name the information a user will provide; they do not enter their own answers in those field definitions. Generate internal keys automatically.
- Keep the form short: show one user input, a prefilled Step 1, and an empty optional Step 2 initially; reveal further fields only when added. A complete submission needs one or two required user inputs and at least one instruction.
- Use the content template's storage structure, but follow the creator-facing requirements below instead of copying technical YAML fields into the form. These requirements replace the earlier three-step minimum and mandatory explanations for optional inputs.

Access and core fields:
- "+ Create a playbook" in the header and "Create a playbook" in the avatar menu lead to /create. Signed-out users get SignInModal reason="create" and return to the form after sign-in. Creating and saving drafts require sign-in.
- /create is a single-page form: outcome-first title, one-sentence promise, category, who it is for / who should skip, estimated completion time, result measured, user inputs, prompt, steps to use the playbook, testing experience, and an optional inspiration source.
- Explain "Estimated time to complete": the overall time someone needs to follow the playbook, including their own actions. Minimum 10 / maximum 20 displays as "10 to 20 min". Validate minimum >= 0 and maximum >= minimum.
- "Result measured" selects the outcome type (task completed, money saved per month/year/once, or hours saved); it does not record a claimed amount or populate public stats.
- Testing is Muse-only for launch, with the official Muse avatar. "What result did you get?" is free-text reviewer notes. Keep those notes private; never turn them into reports, savings statistics, or site verification.
- Label the source field "Inspired by post (optional)". Hint: "Paste a link to the post that inspired this playbook—for example, on X, Rednote, Threads, or Reddit." Accept valid http/https links from other sites too.

Form organization:
- Six numbered sections: "1. Describe the task", "2. Time and expected result", "3. User inputs", "4. Write the prompt", "5. Steps to use the playbook", "6. Your experience".
- Provide compact, wrapping section links at the top for jumping within the single-page form. Moving between sections preserves all entries; explain that an unfinished draft can be saved and completed later.

User inputs:
- Section helper: "What information will someone need to use your playbook?"
- Explain: "Create the fields the person using your playbook will fill in. Name the information needed—for example, ‘Internet provider’—rather than entering your own answer. Mark one or two as required."
- Label each group "User input 1", "User input 2", etc. Ask only for "Input name", "How will the user enter this information?", choices when applicable, and a Required checkbox.
- Answer formats: Short text, Long text, Provider choices, Dropdown choices, Money, Number, ZIP code, Date. Choice inputs show "Choices (one per line)".
- Provide "Add user input" and "Remove user input N" controls. Start with one required input; additional inputs default to optional. Allow at most two required inputs.
- Do not expose a Placeholder key field or ask creators to satisfy a lowercase-key pattern. Generate unique internal keys such as input_1_placeholder. Preserve valid existing keys and keep references consistent when editing drafts.
- Do not show or require "Why it helps" in this creator form. Existing optional help metadata may remain in storage for imported content.

Prompt editor:
- Label: "Prompt to use in Muse". Use an ordinary editable textarea; internal templates still use {{key}} so the Try flow can substitute user answers.
- Generate an example from the current title and user inputs directly inside the textarea, styled as readable grey text. It must be real editable content that can be submitted as-is, not an HTML placeholder that disappears without becoming a value. Do not add a separate example panel.
- Keep the generated example synchronized with title/input changes until the creator edits the prompt. Clicking an untouched example selects it for easy replacement. After editing, preserve the creator's wording through other field changes, autosave, and reload; do not overwrite it with a regenerated example.
- Provide buttons below the textarea that match the numbered fields above: "Insert user input 1: Internet provider", "Insert user input 2: Internet plan". Before a name is entered, use "Insert user input N". Update button labels when input names change.
- Each button inserts the corresponding internal placeholder at the text cursor. Creators should not need to type placeholder syntax themselves.
- Every placeholder must match a defined input and every defined input must be used. Explain missing references with input names and their Insert buttons. Show the rendered prompt with sample answers in the full playbook preview instead of adding another live-preview panel to the form.

Steps to use the playbook:
- Describe the whole workflow, from preparing details to checking the result, not only follow-ups after sending the prompt.
- Show "Step 1 (required)" prefilled with "Enter your details, then copy the prompt into Muse." This is real editable content, styled grey while unchanged, usable without typing. Focusing the untouched default selects it for easy replacement.
- Show an empty "Step 2 (optional)" with a grey HTML placeholder: "Example: Review Muse’s response and confirm the details before taking action." This example is only a hint, not a saved instruction.
- "Add step" reveals additional optional fields up to five total. "Remove last step" is disabled when only the initial two fields remain. Do not pre-render Step 3.
- Require a non-empty Step 1 for submission; the default satisfies it. Omit blank optional steps from the materialized version. Incomplete drafts may be saved.
- When reopening older drafts, preserve every written instruction; trim unused trailing fields beyond the initial two and provide the default first step if it is blank. A task-specific imported step such as "Paste your redacted renewal summary" is not a universal default.

Actions, autosave and validation:
- Button order: "Submit for review" → "Preview playbook" → "Save draft", on desktop and mobile.
- Autosave incomplete drafts privately to the signed-in account. Save draft must work without satisfying submission requirements.
- Show visible saving/saved/error feedback near the actions, including confirmation after a manual save. Protect against stale concurrent edits and late autosaves reverting a submitted status.
- Validate with a strict schema on the server; client validation helps guide the creator. Reject supplied statistics, author identity, publication status, or other privileged fields.
- Display clear messages next to each invalid field, highlight it, and focus the first invalid field on submission. Identify specific missing inputs/instructions; never show a concatenated dump of regex or schema errors. Use accessible labels and error associations.

Preview playbook:
- Open a private dialog from the current in-memory form, without requiring completion, saving first, submitting, or publishing it. Show missing information clearly for incomplete drafts.
- Include title, promise, category, time estimate, audience, user inputs, rendered prompt, instructions, Muse, author credit, and inspiration source where present. Keep private reviewer notes out of the public-facing preview.
- Provide desktop/mobile layout controls and an accessible close/back-to-editing action. The preview must fit a 390×844 viewport.
- Reuse the Try input controls for sample answers. Filling them updates the rendered prompt; unfilled slots show readable input names. Sample answers stay in preview-local state, never in draft storage, backend requests, or analytics. Changing preview layout preserves sample answers while the preview remains open.
- Clearly identify the preview as a draft and show an Early/no-reports state rather than fabricated outcome data. Returning to editing preserves the creator's form values.

Storage and review:
- Save incomplete content in private owner-scoped draft storage associated with a draft playbooks row. Only the author and admins can read drafts and testing notes; all tables have RLS.
- Submit atomically as a playbooks row with status='in_review' and authenticated author_id, with normal versions/inputs/steps like imported content. Keep public stats empty.
- Add "My submissions" to /me with drafts, review status, reviewer feedback, and links to continue editing or view a published playbook.
- Reuse the P10 admin queue for approve / request changes / reject. Admin preview includes the private testing notes. Approval publishes with author credit in "Playbook by". Use a public-safe display name or the existing “Community contributor” fallback, never an email address. Do not add a creator-name field or live attribution line to the form; further attribution UI is deferred.
- Submitted/published content is protected from author draft writes. Requested changes let the author revise and resubmit a new version without destroying version history. Feedback links return to the correct draft through sign-in.
- Author's own reports are excluded from all stats by P9; add a focused regression test. Creator referral codes/support links remain phase 2 and never affect ranking.

Acceptance criteria:
- Signed-out header click → real sign-in → form; save/reload restores the draft; submit → admin queue → approve → public page with author credit and Early state.
- Creating an input requires no key or help-text entry. Automatic keys are unique, examples use the correct inputs, and numbered Insert buttons stay aligned with field names.
- The in-box example is usable directly; editing it prevents later regeneration from overwriting it, including after reload. Inserting an input at the cursor uses its correct reference.
- Six section links navigate without losing edits. Step 1 starts with the editable default and Step 2 is empty/optional; Add reveals Step 3 and Remove restores the two-field minimum. Submission without editing the default publishes exactly one step; blank optional instructions never appear publicly.
- Invalid or missing prompt references, missing required content, and more than two required inputs are blocked with field-level messages and focus handling. The same incomplete form can still be saved as a draft.
- Preview opens an incomplete unsaved form without creating/submitting it, reflects current edits, fills the prompt from sample answers, and returns to editing without data loss. Assert that sample answers do not appear in backend request bodies or stored drafts.
- Test ownership, stale draft writes, locked review states, and revision/resubmission behavior against local Supabase without resetting existing user data.
- Playwright covers desktop and 390×844 mobile: authoring, manual/autosave, input insertion, instruction controls, preview layout/sample answers/keyboard dismissal, submission and approval.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Run the relevant local Supabase and desktop/mobile Playwright checks. Summarize what you built, what you verified, and anything left open.
```

---

## P11 — Analytics, SEO, performance, trust pages

```text
Goal: Instrumentation, discoverability, and speed.

Analytics:
- PostHog via src/lib/analytics.ts (client + server capture). Outbound agent links (Open in Muse, future agents) append configurable attribution params (e.g. utm_source=playbookhunt&utm_medium=playbook&utm_campaign=<slug>) and fire open_in_agent {agent, slug}; this is the hook for future partner/referral revenue, no billing code in v1. Events: page_view, save_toggled, share {channel}, sign_in_started {reason, method}, sign_in_completed {reason, method}, create_submitted, use_case_view, search, filter_changed, card_click, playbook_view, try_started, copy_prompt, open_in_agent, report_opened, report_submitted, followup_sent, followup_clicked, playbook_requested. No PII, no prompt inputs, no amounts/notes. Respect Do Not Track; cookie consent banner for EU visitors (simple).
- A funnel doc in docs/analytics.md: search → playbook_view → try_started → report_submitted.

SEO:
- sitemap.xml (playbooks, categories, kits), robots.txt, canonical URLs, OG images (next/og) for home/category/kit/playbook, JSON-LD (WebSite with SearchAction on home, HowTo on playbooks, BreadcrumbList).
- Descriptive titles: "<Title> — AI playbook with real results | Playbook Hunt".

Trust pages:
- /how-we-verify: explains testing, what "worked" means, thresholds (why % hidden under 20 reports), weighting, decay, that votes/referrals never affect rank, evidence privacy, how to report problems. Written in plain language (Wirecutter tone).
- /privacy and /terms placeholders with TODO markers for legal review; health/finance disclaimer component used on relevant category pages and playbooks.

Performance:
- Lighthouse >= 90 performance, >= 95 accessibility on home and detail (mobile). next/image everywhere, font subsetting, no layout shift, cache headers, ISR/tag revalidation.
- Sentry for server/client errors.

Acceptance criteria: Lighthouse report committed to docs/; sitemap validates; events visible in PostHog dev project.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P12 — QA, hardening, production launch

```text
Goal: Make v1 production-ready.

- Playwright E2E suite covering: homepage → search → filter → detail → try (copy) → sign in (use Supabase test user / magic link bypass in test env) → report with amount → stats refreshed → report visible; request a playbook from empty search; signed-out Save → sign-in modal → returns to the page and the playbook appears in /me Saved; Create a playbook → admin approves → playbook published; homepage Popular Use Case tile → /use-cases/[slug]; header links → /playbooks, /kits, /categories; mobile viewport Try sheet; admin approves an outlier report.
- Rate limiting on server actions and API routes (Upstash Ratelimit or a Postgres-based limiter): search, try events, reports, requests, auth.
- Bot protection: Cloudflare Turnstile on report and request forms.
- Error and not-found pages styled to the design system; global error boundary with Sentry.
- Security review: RLS audit script listing tables without RLS; verify no service-role key usage in client bundles; CSP headers; input sanitization for notes (render as text); external links rel attributes.
- Data: backup policy notes; evidence retention job (delete evidence files 180 days after review, keep report).
- CI (GitHub Actions): install, lint, typecheck, unit tests, content:validate, build, E2E against a preview deployment.
- docs/launch-checklist.md: env vars in Vercel, Supabase prod project, auth redirect URLs, Resend domain, PostHog prod key, admin account, content import, stats refresh cron, smoke test.

P12-v2 regression checklist (production build, desktop and 390×844 mobile):
- Create: six numbered sections and jump links preserve entries; automatic input keys, matching Insert buttons, and editable in-box prompt example work; field-level errors identify the exact problem while incomplete drafts still save.
- Create steps: prefilled editable Step 1 plus empty optional Step 2; Add/Remove controls; default-only submission publishes one instruction with no blank steps.
- Action order: Submit for review → Preview playbook → Save draft. Preview uses current unsaved values and returns without data loss; sample answers remain local.
- Try: steps appear as bullets, with no progress checkboxes.
- Report: Amount saved/Hours saved follows the outcome type; Provider you dealt with and consistent optional labels; visible upload control, selected filename, Change/Remove, and private evidence submission.
- Open/close inline Redaction tips after filling the report and choosing a file; all entries and selection remain intact. Verify referral copy does not promise display or placement.
- Agents: ChatGPT/Grok/Manus labels and logos, Muse-only selection, Instinct hidden. Check all three seeded detail pages as well as search filters and Try sheets; a cached detail page must not retain a hidden agent after a configuration update.
- Preserve navigation regression coverage for header links and the logo back home; no blank/skeleton flicker.
- Run lint, typecheck, unit tests, build, and relevant E2E checks. Keep local results separate from deployed-preview/CI verification; never mark external acceptance complete from local checks alone.

After implementing P12c/P12d, extend docs/launch-checklist.md and the preview smoke tests with their feedback and request-page acceptance criteria. These follow-ups are not part of the already completed P12-v2 baseline.

Acceptance criteria: CI green; E2E suite passes against preview; checklist complete.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## P12c — Tester feedback

> Approved pre-public-test follow-up. Run after P12-v2. This is product feedback, separate from outcome reports and ranking.

```text
Goal: Give public testers a simple way to report a problem or suggest an improvement.

Requirements:
- Add a “Feedback” link-style button to the shared footer and “Send feedback” to the report-success screen. Keep the footer compact: How we verify / Request / Create / Privacy / Terms / Feedback; three columns and two rows on mobile, a wrapping row on desktop, no tagline, 44px touch targets. Retain descriptive mobile-menu labels.
- Open an accessible dialog on desktop and bottom sheet on mobile.
- Fields: “What would you like to tell us?” (required, maximum 2,000 characters), Type: Problem / Suggestion (optional), and “Email for a reply” (optional).
- Allow signed-out feedback. Do not require an account or attachment.
- Show: “Please leave out personal or sensitive information.”
- Attach the current page pathname as context. Exclude query strings, prompt inputs, report notes, amounts, and evidence.
- Preserve entered text if submission fails. Prevent duplicate submissions and show a clear success confirmation.
- Store feedback privately using server-side validation, rate limiting, and the project’s existing bot-protection patterns.
- Add an admin-only Feedback queue with New / Reviewed / Resolved statuses.
- All new tables must have RLS. Only admins can read/manage feedback; submissions go through a protected server action.
- Render feedback as text. Never include feedback contents or email addresses in analytics.
- Keep this small: no attachments, email notifications, or external support service. Feedback must never affect playbook statistics or ranking.
- Update AGENTS.md and docs/launch-checklist.md to reflect the implemented feedback flow.

Acceptance criteria:
- Signed-out and signed-in users can submit from both entry points.
- Submitted feedback appears in the admin queue with the correct page context.
- Errors identify the relevant field and preserve the form.
- Test validation, admin authorization, rate limiting, and duplicate-submit prevention.
- Playwright covers desktop and 390×844 mobile, including keyboard access and dismissal.
- Existing report submission and success behavior remain functional.

Working rules:
Read AGENTS.md first. Inspect existing patterns and propose a short plan listing files to create/modify before coding. Keep changes scoped to this prompt. Add meaningful tests for logic and authorization. Run pnpm lint, pnpm typecheck, pnpm test, and relevant database/Playwright checks; fix failures. Do not reset existing user data. Summarize what you built, what you verified, and anything left open. Do not commit, push, or deploy unless requested.
```

---

## P12d — Request a playbook page

> Replaces the reverted creator-name form work. Retain existing P10b attribution; do not add creator-name fields, public profiles, or live author-credit lines to the creation form.

```text
Goal: Give visitors a simple dedicated page where they can request a playbook for a real task.

Inspect first:
- Reuse the existing RequestForm, requestPlaybook server action, private request storage, and admin Requests queue. Do not introduce a second request system.

Requirements:
- Replace the /request placeholder with a responsive page titled “Request a playbook”, linked from the shared footer.
- Omit the paragraph under the page title. Use form heading “What would you like AI to help with?”, “Topic” for the icon choices, and “Goal” for the purpose dropdown. Keep two topics per row on mobile only; from 640px upward, let chips wrap naturally to fit the available width.
- Label the text field “Tell us a little more”, the email field “Email (optional)”, and the submit button “Send request”. Keep all choices and fields on one compact page.
- On /request require topic, purpose, and task (3–500 characters); do not label topic/purpose optional. Email for a reply stays optional. Allow signed-out requests.
- Topic chips retain icons: 🛍️ Shopping, 🎨 Creativity, 🗺️ Travel planning, ✈️ Travel booking, 💰 Personal finance, ⚡ Productivity, 🏢 Small business, 🏥 Health, 💬 Something else. Do not preselect choices.
- Show matching purposes in a required Goal dropdown, with Something else in every list. Disable it until a topic is selected and show a blank selection prompt. Shopping: Find the best deals / Negotiate a price / Track prices or availability / Find products for my style. Creativity: Generate images / Create videos / Turn an image into a video / Brainstorm ideas. Travel planning: Plan a trip / Find activities / Plan a trip budget. Travel booking: Compare flights or trains / Find accommodation / Compare transport. Personal finance: Lower bills / Compare insurance / Plan a budget / Track stocks / Research investments. Productivity: Research a topic / Organize information / Plan my week. Small business: Research competitors / Write marketing content / Create social content / Optimize operations / Handle routine admin. Health: Prepare for an appointment / Organize health information.
- Changing topic clears the selected purpose without deleting typed text. Use an accessible required Topic radio group and native Goal select; tailor text hints to the purpose, never submit examples automatically. Validate topic/purpose pairing server-side and store readable context in the existing request text for admins. These are requested goals, not promises of supported agent capabilities or investment returns.
- Provide concrete examples such as comparing phone plans for a family or planning vegetarian meals on a budget. Do not pre-submit example text as the user’s request.
- Omit the privacy helper paragraph on /request to keep it compact. Use reply emails only to follow up on the request. Show a brief error only after a failed send (“Request not sent. Please try again.”); dismiss the message when editing while retaining field validation.
- Preserve topic/purpose/task/email after validation or submission errors. Disable submission while sending and show a clear success confirmation.
- Explain that requests help prioritize future testing, without promising publication dates or a reply to every request.
- Include a secondary Create a playbook link for people who already tried a task.
- Preserve server validation, rate limiting, Turnstile/honeypot protection, privacy, and the existing admin workflow. Do not send task text or email addresses to analytics.
- Keep empty-search request forms working. No attachments, new notification service, creator-name fields, or ranking changes.
- Update AGENTS.md and docs/launch-checklist.md with the implemented flow.

Acceptance criteria:
- Footer → /request → signed-out submission → admin Requests queue works.
- Topic icons render two per row on mobile (360px and 390×844), and wrap naturally on desktop. Goal dropdown, examples, validation, optional email, preserved entries, and success state work at all sizes.
- Footer uses short labels with two mobile rows; Request opens /request and Feedback remains keyboard accessible.
- Existing search request and Create a playbook flows remain functional; creation has no public creator-name field.
- Verify local protections and explicitly document remaining deployed Turnstile checks.

Working rules:
Read AGENTS.md first. Inspect existing patterns and propose a short file-level plan before coding. Keep changes scoped to this prompt. Add meaningful tests for changed logic. Run pnpm lint, pnpm typecheck, pnpm test, and relevant database/Playwright checks; fix failures. Do not reset existing user data. Summarize what changed, verification, and anything left open. Do not commit, push, or deploy unless requested.
```

---

# Phase 2 prompts (after beta)

Tester feedback and the dedicated Request a playbook page are approved follow-ups in P12c/P12d above. Creator-name form work was reverted after usability feedback. Retain existing P10b attribution; further attribution UI and public profiles remain deferred. Coordinated ChatGPT/Grok/Manus activation and possible Helpful feedback remain discussion proposals, not approved implementation scope. Muse remains the only selectable agent. Likes/upvotes, comments, public creator profiles, creator referral links, and Inspired-by claims remain deferred. Votes and referrals must never affect ranking. Run Phase 2 prompts only when separately requested.

## P13 — Creator profiles and playbook submissions

> The v1 slice (Create a playbook beta form + review queue) is P10b. This phase-2 prompt adds public creator profiles and featured creators on top of those existing flows.

```text
Goal: Let anyone submit a playbook and have a public creator profile.

- Reuse the P10b /create form and review queue (no new submission form; public name/profile design belongs in this phase).
- Add: multi-step polish for /create, image upload for the preview, and a public profile link on approved playbooks.
- /u/[handle] creator profile (n8n/Notion style): avatar, bio, links, playbooks list (row density), aggregate stats: playbooks published, total tries, average weighted success across playbooks with >= 20 reports (hide otherwise).
- Homepage "Featured creators" row and a "Become a creator" CTA block (Notion style).
- Author's own reports remain excluded from stats (already in P9) — add a test.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

## P14 — Inspired-by credits: Thank and Claim

```text
Goal: Credit original social creators and let them claim.

- On the detail sidebar "Inspired by" block: "Thank them" (signed-in users; one per user per source; shows count) and "Claim credit".
- Claim flow: creator signs in, selects the source, we give a verification code to place in their X/Threads/Reddit/小红书 bio or a post; admin verifies manually (v1) → source linked to the creator profile.
- Notify: admin tool to generate a message to the original creator ("Your idea helped 1,247 people try this") with a link to claim.
- Thanks and claims are never inputs to ranking (add test).

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

## P15 — Referral links and useful-votes

```text
Goal: Optional creator referral links and "useful" votes, both isolated from ranking.

- Creators can attach one referral link per agent per playbook (referral_links table). Displayed in the sidebar under "Playbook by" as a clearly labeled "Referral link" with a disclosure tooltip, visually separate from Try/Open-in buttons. Admin can disable any link.
- "Useful" votes on playbooks (votes table, one per user); show count on detail page only.
- Tests: evidence_score and ordering are byte-identical with and without referral links and votes present; referral links never appear on cards or in search results.

Working rules: Read AGENTS.md first. Propose a short plan (files to create/modify) before coding. Keep changes scoped to this prompt. Add tests for logic. Run pnpm lint, pnpm typecheck, and pnpm test and fix failures before finishing. Summarize what you built, what you verified, and anything left open.
```

---

## Bonus — Content-authoring prompt (for a general AI assistant, not the coding agent)

```text
You are helping me turn an AI-agent use case I found on social media into a structured Playbook Hunt playbook.

Source post: <paste text + link + handle>
My test notes: <what I entered, what the agent did, the result, time taken, $ saved if any>

Produce a YAML file matching this schema: slug, title (outcome-first, ≤ 6 words, e.g. "Lower your internet bill"), promise (one sentence), category (one of personal-finance, travel-booking, travel-planning, shopping, small-business, productivity, health, creativity), status: draft, who_for, who_not_for, time {min, max} in minutes, outcome {type: money_monthly|money_yearly|money_once|time_hours|binary, unit}, followup_days, primary_agent: muse, agents [{slug, tested, notes}], inputs [{key, label, help, type, required}], prompt (uses {{key}} placeholders for every input; clear role, goal, constraints, output format; ask the agent to cite sources for prices/offers), steps (3–5 short imperative steps ending with "Log the result"), sources [{platform, handle, url, title}], changelog: "Initial version".

Rules: rewrite in your own words (don't copy the post), no medical/legal/financial guarantees, include a safety caveat for health/finance, keep the prompt under 250 words.
```
