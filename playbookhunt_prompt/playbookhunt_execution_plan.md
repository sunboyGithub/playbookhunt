# Playbook Hunt — Strategy, Design References & Execution Plan

> Find AI workflows that actually work for the task you want to accomplish.
> Core loop: **Task → Discover → Try → Report → Aggregate → Rank → Discover again**

Stack decision: Next.js (App Router, TypeScript) + Supabase (Postgres, Auth, Storage) + Tailwind/shadcn/ui, deployed on Vercel.
v1 scope decision: **core loop only** (curated playbooks, search, detail, try, report, ranking, starter kits, admin). Creator submissions/claims/referrals are phase 2.

---

## Part 1 — Best combined answer (reference research)

### How the two agent answers were merged
- **Answer 2 is the backbone.** It is sharper on what makes this product different: confidence-adjusted success rates, minimum sample thresholds, hiding % until there is enough data, votes/referrals never affecting rank, a per-agent "Try in…" picker, follow-up nudges for outcomes that take days, and Levels.fyi-style "median + n" display.
- **Answer 1 contributes breadth:** full filter/sort list, badges, anti-gaming rules, "who this is NOT for", version history, empty state with "Request a playbook", Wirecutter methodology framing.
- **Dropped from Answer 1:** a homepage trust strip showing one playbook's stats (stats belong on cards), "Download JSON" and too many secondary CTAs, upvotes as a visible ranking input.

### A. Top 5 reference websites

| # | Site | Best for | Borrow | Don't copy |
|---|---|---|---|---|
| 1 | **n8n Workflow Templates** — https://n8n.io/workflows | Workflow discovery, inspectable content, creators | Count in headline, search + category chips, compact cards (title · tool icons +N · verified creator avatar), "Trending [category]" rows, preview-before-use | Dark theme, node-graph complexity, no outcome data |
| 2 | **G2** — https://www.g2.com | Verified outcomes, trust, category browsing | Real-review counter in hero, natural-language search, category list + item grid with (n) counts, "Leave a review" contribution block, minimum-review thresholds, recency | Star ratings (too vague), ad/"Sell on G2" clutter, paid placement |
| 3 | **Product Hunt** — https://www.producthunt.com | Feed/ranked list, community, launch distribution | Numbered ranked list with right-side metric box, ⌘K search, category mega-menu, right rail (events/threads), outcome-based "Awards" | Raw upvotes as ranking; launch-day gamification |
| 4 | **Smithery** — https://smithery.ai | Intent search + "try in my tool" | Client-aware install/try flow → "Try in Muse / Claude / ChatGPT / Gemini" picker that formats the prompt per agent | Developer-only language |
| 5 | **Levels.fyi** — https://www.levels.fyi | Crowdsourced numbers | Median + range + sample size display; ~30-second submission flow | Dense data tables on consumer pages |

Supporting references:
- **Zapier Templates** (https://zapier.com/templates) — calm hero, use-case scroller, featured templates with flow previews, hand-picked "starter kit" collections.
- **Notion Marketplace** (https://www.notion.com/templates) — bento hero, category tiles with counts, list-row agents with usage counts, featured creators, "Become a creator".
- **Glam.ai** (https://glam.ai) — visual-first gallery, hover "Try now", filter pills + inline search.
- **Wirecutter** — "How we tested", "Who this is for / not for", update logs.
- **GitHub / Stack Overflow** — reputation, versioning, accepted answers.
- **Hacker News / Reddit** — time-decayed "hot" ranking (for Trending only).

### B. Recommended design combination

| Surface | Reference |
|---|---|
| Homepage | Zapier/Notion light hero + G2 counter + n8n chips; Product Hunt ranked list; Zapier/Notion collections |
| Search & filters | Smithery intent search + G2 filters + Glam filter pills; Notion list-row / card toggle |
| Playbook cards | n8n compact card + Glam outcome preview & hover Try + evidence stats |
| Playbook detail | n8n inspectability + Zapier one-liner + Wirecutter "who it's for / not for" + change log |
| Try | Smithery per-agent picker |
| Outcome reporting & display | Levels.fyi (median/range/n) + G2 verified badge + G2 "Leave a review" CTA |
| Ranking & trust | G2 thresholds/recency + Wilson confidence + Product Hunt lesson (weight by trust, not raw votes) |
| Creators (phase 2) | n8n/GitHub profiles + Notion featured creators + "Inspired by" credits with Thank/Claim |

### C. Suggested overall UX

**Homepage → Search → Results → Playbook Detail → Try → Report → Ranking**

1. **Homepage** — see Part 2 "Homepage v2".
2. **Search & results**
   - Natural-language search, autocomplete by task/category/outcome/agent, ⌘K palette.
   - Filter pills by outcome type: Save money · Save time · Plan · Research · Create.
   - Filters: agent, category, verified in last 30 days, min reports, outcome type, time to complete.
   - Sort: **Best evidence** (default) · Most tried · Highest median outcome · Recently verified · Trending.
   - Card fields: title, promise, "tried · % worked (n)", median outcome, last verified, agent chips, creator.
   - Empty state: related tasks, popular playbooks, **Request this playbook** form.
3. **Playbook detail** (matches wireframe 2)
   - Breadcrumb, title, one-line promise, chips (category · tested with · time).
   - Stat tiles: Tried · Worked (n reports) · Median saved (n with amounts).
   - Outcome preview image (redacted real result).
   - Who this is for / not for · What you'll need · The playbook (prompt block + Copy + steps) · What happened for others (stacked bar worked/partly/didn't, last-30-days rate, report list with filters) · Did it work for you? · Related playbooks.
   - Sidebar: verified badge, **Try this playbook**, agent picker ("Best results with Muse"), Playbook by, Inspired by (credits), Good to know (change log).
4. **Try**
   - Pick agent → fill required inputs inline (fills `[slots]` in the prompt) → Copy prompt or Open in agent.
   - Log `try_started`; if signed in, schedule a follow-up "Did it work?" email after `followup_days`.
5. **Report** (≤ 30 seconds)
   - Worked / Partly / Didn't · agent (prefilled) · optional amount + unit · provider/region (playbook-specific) · note · optional evidence (private by default).
   - After submit: thank-you, "your report updates the stats", related playbooks.
6. **Ranking** — see Part 3 ranking spec. Votes, referrals and credits never affect rank.

---

## Part 2 — Design patterns from the reference screenshots

| Site | Borrow | Skip | Playbook Hunt use |
|---|---|---|---|
| **Zapier Templates** | Calm light hero (title + one line); horizontal "Use cases" scroller with tinted image tiles; featured templates with category tag top-left + visual flow preview; hand-picked **starter kit** collections with illustration + 2-line blurb | Enterprise nav, B2B jargon | Use-case scroller; **Starter kits** ("Cut your bills kit", "Japan trip kit", "Small-business launch kit") |
| **n8n Templates** | Count in headline; search with category chips underneath; big "learn by doing" feature card; compact cards (title · tool icons +N · verified creator avatar); "Trending [AI ▾] templates" inline category switcher; icon category grid | Dark theme; cards without outcome data | Hero counter; compact card; "Trending [Finance ▾] playbooks"; category grid |
| **Notion Marketplace** | Top tabs (Templates/Skills/Agents/Creators); bento hero (editorial feature + seasonal prompt + top-creator spotlight); category tiles with counts; list-row agents with icon · one-liner · usage count · Free badge; featured creators; "Become a creator" CTA | Paid templates, consultant booking | Seasonal bento hero ("Get ahead of Q4: open enrollment, holiday travel"); list-row view; tiles with counts; creator spotlight (phase 2) |
| **Glam.ai** | Visual-first gallery where the card *shows the result*; hover **Try now** + share; "New" badge; filter pills with inline search; "All tools" grid (image · title · one-liner · arrow) | Dark heavy imagery, pricing pressure, suggestive imagery | **Outcome preview** on cards/detail (redacted bill before/after, itinerary snapshot, report excerpt); hover Try; outcome-type pills |
| **Product Hunt** | Numbered ranked list (icon · tagline · tags · metric box right); ⌘K search; category mega-menu; right rail; "Orbit Awards — powered by what reviewers actually say" | Upvote box as the ranking signal | "Top playbooks this week" list with **"68% worked · n=412"** box instead of upvotes; ⌘K; quarterly **Playbook Hunt Results Awards** computed from outcomes |
| **G2** | Bold declarative hero + real-review counter in accent color; "Ask a question…" search; quick links under search; category list left + item grid right with (n); "Using software? Leave a review." block with review-card collage | Stars, ad clutter | Hero counter ("based on 3,210 real results"); quick links; category explorer; **"Tried an AI playbook? Report your result."** block |

### Homepage v2.1 (section order, updated after design review round 1)
1. Nav: logo "Playbook**Hunt**" ("Hunt" in the orange accent) · Playbooks · Starter kits · Categories · ⌘K search · **+ Create a playbook** · **Report a result** · Sign in (avatar menu when signed in).
2. Hero (light, warm): H1 **"What do you want Muse to do?"** ("Muse" in Muse blue); natural-language search, default placeholder **"Save $100 on internet bill"**, rotating to "Plan my Japan trip", "Find a cheaper flight", "Research my competitors"; counter "48 playbooks · 3,210 real results reported"; quick links "Best results 2026 · Trending · Recently verified".
3. Category chips.
4. **Popular Use Cases** carousel (Zapier style): exactly 4 tiles visible per row on desktop (2 on mobile), text centered, diagonal gradient backgrounds with a soft light streak, right arrow (left arrow appears after scrolling), the 5th tile peeks and fades out under the arrow, nothing is visible to the right of the arrow; page dots underneath.
5. **Proven to work** (renamed from "Strongest results") — 3 rich cards with outcome previews + evidence stats.
6. **Top playbooks this week** — numbered list with evidence box.
7. **Trending [$ Finance ▾] playbooks** — category switcher chip shows the category icon ($ for Finance) plus a ▾ dropdown hint; compact cards.
8. **Starter kits** — cards whose right third is an illustration in the homepage palette (Japan kit: Mount Fuji + torii; Bills kit: bill with a price drop; Small-business kit: storefront).
9. **Category explorer** — left list, right grid of tiles with % worked (n); tiles show playbook counts.
10. **"Tried an AI playbook? Report your result."** + collage of real outcome cards + Muse referral bonus note ("add your Muse referral code to a verified report… up to 1B Muse tokens*", *per Muse's referral terms, never affects rankings).
11. Footer (identical on every page): How we verify · Request a playbook · Create a playbook (beta) · Privacy · Terms.

> Counter numbers must be real. Before there is data, show "48 tested playbooks" only.

### Card anatomy (one `PlaybookCard` component, three densities)
- **Rich** (homepage features): outcome preview image, category tag top-left, New/Verified badge, title, promise, "1,247 tried · 68% worked (n=412)", "Median $18/mo · verified 3d ago", agent chips, creator avatar, hover **Try**.
- **Compact** (n8n style): title, agent/tool icons +N, evidence line, creator avatar.
- **Row** (Notion/Product Hunt style): rank #, icon, title + one-liner, tags, right-side evidence box.
- Below the report threshold, every density shows **"Early · 7 reports"** instead of a percentage.

### Visual direction
- Light theme: warm off-white `#FAF9F6` background, white cards, 1px `#E7E5E0` borders, 12–16px radius, generous whitespace (matches the wireframes, Zapier, Notion).
- One accent color for primary CTAs (orange family, e.g. `#FF5A1F`); semantic outcome colors: worked `#16A34A`, partly `#F59E0B`, didn't `#DC2626`.
- **Muse blue `#2A66DE`** (soft `#E8EFFC`, sampled from the Muse logo) for everything Muse: the word "Muse" in the headline, the Muse agent chip, and the "Open in Muse" button. Wherever Muse appears as an agent, show the **official Muse avatar** (the fluffy character, circular crop).
- Type: a clean geometric sans (e.g. Inter / Geist); monospace for prompt blocks.
- Imagery: illustrations for collections, real (redacted) outcome screenshots for playbooks. No stock photos.

---

## Part 3 — Product & technical specification

### 3.1 Vision & positioning
- Not a prompt library. An **outcome-ranked** directory of AI-agent playbooks.
- Wedge: Muse-tested playbooks for everyday, measurable wins (money saved, hours saved, trips planned).
- Long term: agent-agnostic **recommendation/performance layer** — "which agent + playbook works best for this task?"

### 3.2 Target users & top jobs
- Everyday consumers who want a concrete result (lower a bill, plan a trip) but don't know how to prompt.
- AI-curious power users who want proven workflows and want to share wins.
- Creators on X / Threads / Reddit / 小红书 who post AI use cases (phase 2 supply side).

### 3.3 v1 scope
In: curated playbooks (~48), homepage v2, search/filter, /playbooks, /categories + category pages, /kits + starter kits, /use-cases pages, detail with Save + Share, try flow with agent picker, sign-in (Google, Facebook, email link), Save + My playbooks, outcome reporting + evidence + optional Muse referral code, follow-up email, stats & ranking, admin/moderation, playbook requests, Create a playbook (beta) → admin review, analytics, SEO, "How we verify" page.
Out (phase 2+): public creator profiles, claims/thanks, creator referral links on playbooks, comments, useful-votes, per-agent leaderboards, API.

### 3.4 Routes
| Route | Purpose |
|---|---|
| `/` | Homepage v2 |
| `/search?q=&category=&agent=&outcome=&verified=30d&min=20&sort=` | Search & results |
| `/c/[slug]` | Category page |
| `/k/[slug]` | Starter kit (collection) page |
| `/playbooks` | All playbooks (header "Playbooks"): results page, no query, sorted Best evidence |
| `/kits` | All starter kits (header "Starter kits") |
| `/categories` | All categories (header "Categories") → `/c/[slug]` |
| `/use-cases/[slug]` | Popular Use Case page (homepage tiles): curated cross-category playbook list |
| `/create` | Create a playbook (beta), sign-in required |
| `/p/[slug]` | Playbook detail |
| `/p/[slug]/try` | Try flow (also available as a sheet/modal) |
| `/p/[slug]/report` | Report outcome (also modal) |
| `/request` | Request a playbook |
| `/how-we-verify` | Methodology & ranking transparency |
| `/login`, `/me` | Auth; my tries & reports |
| `/admin/*` | Reports queue, evidence review, playbooks, collections, requests |

### 3.5 Data model (Supabase / Postgres)
- `profiles` — id (= auth user), handle, display_name, avatar_url, role (`user`/`admin`), email_verified, created_at.
- `categories` — slug, name, emoji, description, sort.
- `agents` — slug, display_name (e.g. "ChatGPT · Dots"), vendor, launch_target_url_template (where "Open in" goes; ChatGPT routes to Dots), prompt_format, capabilities (`info`, `web_actions`, `phone_calls`), status (`active`/`coming_soon`/`hidden`), sort.
- `playbooks.required_capability` (`info`/`web_actions`/`phone_calls`) → used to decide which agents can run a playbook. UI (round 2): Muse is the only selectable agent; coming_soon agents (ChatGPT · Dots, Grok-Bot, Manus, Instinct) show as greyed, disabled chips with no labels; Claude and Gemini are hidden.
- `playbooks` — slug, title, promise, category_id, status (`draft`/`published`/`archived`), who_for, who_not_for, time_min, time_max, outcome_type (`money_monthly`/`money_yearly`/`money_once`/`time_hours`/`binary`), outcome_unit, followup_days, preview_image_url, primary_agent_id, author_id, current_version_id, last_verified_at, search_tsv, timestamps.
- `playbook_versions` — playbook_id, version, prompt_template (with `{{slot}}` placeholders), changelog, created_at.
- `playbook_inputs` — version_id, key, label, help, type (`text`/`textarea`/`number`/`money`/`zip`/`provider_picker`/`select`/`date`), options, required (aim for ≤ 1–2 required per playbook), why_it_helps, sort.
- `playbook_steps` — version_id, sort, body.
- `playbook_agents` — playbook_id, agent_id, tested, notes.
- `playbook_sources` — playbook_id, platform (`x`/`threads`/`reddit`/`rednote`/`other`), handle, url, title (Inspired-by credits).
- `collections`, `collection_items` — starter kits.
- `use_cases`, `use_case_items` — homepage Popular Use Cases (slug, title, description, gradient, sort; curated playbook list).
- `try_events` — playbook_id, version_id, agent_id, user_id (nullable), device_id, action (`started`/`copied`/`opened`), created_at.
- `outcome_reports` — playbook_id, version_id, user_id, agent_id, result (`worked`/`partly`/`didnt`), amount, unit, hours_saved, time_spent_bucket, provider, region, note, referral_code (optional; shown only when verified), status (`pending`/`approved`/`rejected`), is_verified, is_outlier, weight, created_at; **unique(user_id, version_id)**.
- `report_evidence` — report_id, storage_path (private bucket), kind, review_status.
- `followups` — user_id, playbook_id, try_event_id, due_at, sent_at, completed_at.
- `playbook_requests` — query, email, user_id, created_at.
- `saves` — user_id, playbook_id, created_at (powers My playbooks › Saved and the "Updated since you saved" badge).
- `playbook_stats` — tried_count, report_count, worked, partly, didnt, success_rate_raw, wilson_lb, median_amount, p25, p75, amount_n, last30_success, evidence_score, trending_score, last_report_at, updated_at.
- Phase 2: `referral_links`, `creator_claims`, `thanks`, `votes`.

### 3.6 Ranking spec
- **Report weight** `w` = 1.0 × (email verified ? 1 : 0.5) × (evidence approved ? 1.5 : 1) × (account age < 1 day ? 0.5 : 1). Weight 0 for: rejected, outlier, the playbook author's own reports.
- **Time decay:** `w_t = w × 0.5^(age_days / 60)`.
- **Success:** worked = 1, partly = 0.5, didn't = 0. `p = Σ(w_t·s) / Σw_t`, `n_eff = Σw_t`.
- **Wilson lower bound** at z = 1.96 on (p, n_eff).
- **Outcome strength:** percentile of median amount within category among playbooks with `amount_n ≥ 5`; money normalized to per-year; neutral 0.5 when missing.
- **Recency:** `0.5^(days_since_last_verified / 60)`.
- **Usage:** `log10(1 + tried) / log10(1 + max_tried)`.
- **Evidence score** = 0.55·Wilson + 0.20·outcome + 0.15·recency + 0.10·usage. Weights live in config and get tuned during beta.
- **Display thresholds:** show % only when `report_count ≥ 20`; show median only when `amount_n ≥ 10`; otherwise "Early · N reports".
- **"Proven to work" eligibility:** ≥ 20 reports and ≥ 3 evidence-approved reports.
- **Trending** (separate): Σ over last 7 days of (try = 1, report = 3) × `0.5^(age_hours / 48)`.
- **Outliers:** amount > Q3 + 3·IQR within the playbook (once `amount_n ≥ 10`) or above a per-playbook cap → flagged for admin.
- **Never in rank:** votes, referral links, credits/thanks, creator follower counts.
- **Badges:** Verified (checked within 30 days), High success (Wilson ≥ 0.6), Top saver (top 10% outcome in category), Recently verified, Most tried.
- **Anti-gaming:** one report per user per version, rate limits per IP/device, outlier detection, evidence required for top placement, author reports excluded, admin moderation queue.

### 3.7 "Last verified" definition
Updated when (a) an admin/tester re-runs the playbook and confirms it still works, or (b) an evidence-approved "worked" report is accepted. Shown as "Verified 3 days ago".

### 3.8 Content operations
1. **Source** — collect ~100 candidate use cases from X, Reddit, Threads, 小红书, AI communities into the Seed Playbooks tracker (link + handle).
2. **Select** — pick 48 (6 per category) that have a measurable outcome and broad appeal.
3. **Test** — run each with Muse at least twice; record inputs, output, result; capture redacted screenshots.
4. **Structure** — write YAML: promise, who for/not for, inputs, prompt template, steps, outcome type, followup_days, sources.
5. **Credit** — link the original post in "Inspired by"; rewrite in your own words; don't copy media without permission.
6. **Publish** — import via script; stats start empty; beta testers generate the first real reports.
7. **Maintain** — re-verify top playbooks monthly; bump version + changelog when the prompt changes.

**Integrity rule:** all displayed numbers come from real tries/reports. No fabricated seed stats. The numbers in the wireframes are illustrative only.

### 3.9 Tech architecture
- Next.js App Router, React Server Components, Server Actions; TypeScript strict.
- Supabase: Postgres (FTS + `pg_trgm`), Auth (magic link + Google), Storage (private evidence bucket, public preview bucket), RLS on all tables, `pg_cron` or Vercel Cron for stats refresh and follow-ups.
- Tailwind + shadcn/ui; `cmdk` for ⌘K; Recharts or plain CSS bars for the outcome bar.
- Email: Resend. Analytics: PostHog. Errors: Sentry. Hosting: Vercel.
- Tests: Vitest (unit, incl. ranking), Playwright (E2E).

### 3.10 Seed categories & candidate playbooks (48)
| Category | Candidates |
|---|---|
| 💰 Personal Finance | Lower your internet bill · Cut your phone bill · Cheaper car insurance · Cancel unused subscriptions · Get a bank fee refunded · Analyze my monthly spending |
| ✈️ Travel – Booking | Cheapest flight to Europe · Rebook a hotel after a price drop · Find award flights with points · Claim flight delay compensation · Best rental car price · Train vs flight comparison |
| 🗺️ Travel – Planning | Plan 7 days in Japan · Weekend city-break itinerary · Family trip with kids · Road trip with stops · Visa & entry checklist · Weather-based packing list |
| 🛍️ Shopping | Compare products before I buy · Find a coupon or price match · Pick the right laptop · Track a price and buy low · Write a return/refund request · Used-car purchase & negotiation |
| 🏢 Small Business | Research my competitors · Marketing plan for my small business · Google Business profile + review replies · Pricing analysis · Find grants & funding · Weekly social content calendar |
| ⚡ Productivity | Inbox triage rules · Weekly plan from my to-dos · Meeting notes → action items · 30-day learning plan · Tailor my resume to a job · Apartment-hunting shortlist |
| 🏥 Health & Medical | Prepare questions for my doctor · Understand my lab results (not medical advice) · Appeal an insurance claim denial · Find an in-network specialist · Meal plan for a goal · Beginner workout plan |
| 🎨 Creativity | Personalized bedtime story · Wedding/birthday speech · Brand name & logo brief · Short video script · Gift ideas finder · Illustrated greeting card |

---

## Part 4 — Phased roadmap

Each phase has exit criteria. Dates are left for you to fill in the tracker.

| Phase | Goal | Key work | Exit criteria |
|---|---|---|---|
| **P0 Foundations** | Ready to build | Name/domain, brand tokens, repo, Supabase + Vercel projects, PostHog/Sentry, `AGENTS.md` | Preview deploy live; design tokens match wireframes |
| **P1 Content sprint** | 48 tested playbooks | Source → select → test → structure → credit | 48 YAML playbooks validated by schema; each tested ≥ 2× with Muse; ≥ 30 with preview images |
| **P2 MVP build** | Full loop in staging | Coding prompts P1–P12 | E2E test passes: search → detail → try → report → stats update → rank changes |
| **P3 Private beta** | Real outcome data | Recruit 50–150 testers; follow-up emails; tune weights and report form | ≥ 10 playbooks with ≥ 20 reports; try→report conversion ≥ 15%; median report time ≤ 45s |
| **P4 Public launch** | Distribution | Product Hunt launch; posts on Reddit/X/Threads/小红书 linking to playbook pages; SEO pages; first Results Awards | ≥ 1,000 tries and ≥ 200 reports in the first month |
| **P5 Creators** | Supply side | Prompts P13–P15: submissions, profiles, Inspired-by Thank/Claim, referral links (labeled, separate) | 20 external playbooks published; ranking unaffected by referrals (tested) |
| **P6 Agent-agnostic & recommendation layer** | Moat | Per-agent success breakdown; "best agent for this task"; embed/API | ≥ 3 agents with ≥ 100 reports each |

---

## Part 5 — Metrics & instrumentation

| Metric | Definition | Event(s) |
|---|---|---|
| **North star: verified outcome reports / week** | Approved reports created in a week | `report_submitted`, admin approve |
| Search → try CTR | Sessions with a search that lead to `try_started` | `search`, `try_started` |
| Try → report conversion | Reports ÷ tries (by signed-in user, 14-day window) | `try_started`, `report_submitted` |
| % playbooks above threshold | Published playbooks with ≥ 20 reports | `playbook_stats` |
| Median time to report | Form open → submit | `report_opened`, `report_submitted` |
| Follow-up response rate | Follow-up emails → reports | `followup_sent`, `report_submitted` |
| D30 return rate | Users returning within 30 days | session |
| Request volume | Playbook requests / week (demand signal) | `playbook_requested` |

---

## Part 6 — Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Cold start: too few reports to show stats | High | High | "Early" state, beta cohort, follow-up emails, founder testing, focus on 10 hero playbooks first |
| Fake or gamed reports | Medium | High | Trust weighting, one report per version, rate limits, outliers, evidence for top placement, moderation |
| PII in bills/evidence | High | High | Private bucket, redaction guidance + blur tool, admin-only access, auto-delete policy |
| Health/financial advice liability | Medium | High | Disclaimers, "prepare questions" framing, no diagnosis playbooks, legal review of health category |
| Playbooks break when agents change | Medium | Medium | Versioning, last-verified date, monthly re-verification, report filters by date |
| Dependence on Muse | Medium | Medium | Agent-agnostic data model from day one; per-agent results |
| Attribution/copyright of social posts | Medium | Medium | Credit + link, rewrite, ask permission for media, takedown process |
| Self-report bias | High | Medium | Show n and "self-reported", medians not means, evidence badges |
| Spam requests/reports | Medium | Low | Captcha (Turnstile), rate limits |

---

## Part 7 — Open questions
1. ~~Final product name and domain~~ Decided: **Playbook Hunt**, playbookhunt.com (see Part 12).
2. Muse deep-link / prompt prefill support — does Muse have a URL scheme or share API?
3. Evidence redaction: manual guidance only, or an in-browser blur tool in v1?
4. Anonymous reports: allowed with lower weight, or sign-in required? (Recommendation: sign-in required for reports, anonymous for tries.)
5. Legal entity, privacy policy, terms before public launch.
6. Chinese-language (小红书) audience: localized pages in v1 or later?

7. Confirm Muse's deep-link / prompt-prefill support, official avatar asset and brand-usage permission, and the exact referral terms (the "up to 1B tokens" claim) before launch.
8. Confirm the official names and links for OpenAI's Dots and Grok's Grok-Bot, and whether either can place phone calls.

---

## Part 8 — Design review round 1: answers & decisions

### Homepage
| # | Question / request | Decision |
|---|---|---|
| A0 | Muse in Facebook blue | Done: `#1877F2` for "Muse" in logo + headline, Muse chip/avatar, "Open in Muse". Orange stays the CTA color. |
| A1–A2 | Headline + placeholder | "What do you want Muse to do?" · placeholder "Save $100 on internet bill". |
| A3–A4 | Popular tasks carousel | Renamed **Popular Use Cases**; 4 visible tiles, centered text, gradient backgrounds, arrow + faded 5th tile, nothing shown right of the arrow. |
| A5 | Better words than "Strongest results" | **"Proven to work"** (chosen). Alternatives: "Most proven", "Top proven playbooks", "Highest success rate", "Works for most people". |
| A6 | Icon after "Finance" | The box was a dropdown arrow that failed to render in v1. Now: category icon ($) before the label + ▾ dropdown hint. Every category gets its own icon. |
| A7 | Starter kit images | Right third is an illustration in the homepage palette (Mount Fuji for Japan, etc.). Frames use drawn placeholders; commission final illustrations in the same palette. |
| A8 | Referral code / 1B tokens in the Report section | Yes, as an optional bonus. Safeguards: referral codes are shown only on verified reports, one code per user, rotated display, labeled as a referral, link to Muse's official terms, and **never** an input to ranking. Confirm the token terms with Muse first. |
| A9 | Footer wording | Unified on every page: **How we verify** (methodology), **Request a playbook** (ask for a task we don't cover, or paste a social post you want tested — replaces "Submit an idea"), **Create a playbook (beta)**, Privacy, Terms. |
| A10 | Can users create playbooks? | Full creator features are phase 2 (P13). Recommended: ship **Create a playbook (beta)** in v1 as a simple form that lands in the admin review queue (no public profiles yet). |

### Playbook detail
| # | Question / request | Decision |
|---|---|---|
| B1 | Are Claude / ChatGPT / Gemini agents? Add Manus, Instinct? | Capabilities are per playbook, not global. General assistants can research, draft and (in some agent modes) act on websites, but for tasks that need a **phone call** (bill negotiation) they are **Script only**: they draft offers and a call script, the user calls. For info/planning playbooks they work fully. Agent lineup: **Muse** (active, recommended); **ChatGPT · Dots** (clicking ChatGPT opens OpenAI's Dots), **Grok-Bot**, **Manus** — greyed **Coming soon** until tested and popular; **Claude, Gemini** — greyed **Script only** for call-based playbooks. "Instinct": not known to me — share a link and it can be added the same way. Agent capabilities change fast; re-verify when testing each playbook. |
| B2 | Copy feedback + nudge | Copy button turns **✓ Copied** + toast "Copied! Paste it into Muse" with a nudge to *Try this playbook* (filled-in prompt) or sign in to save it. Copy is never blocked by sign-in. |
| B3 | Provider / Agent / Output filters | Filters over the report list: **Provider** = company the reporter dealt with (Xfinity, AT&T…), **Agent** = AI agent they used, **Result** (renamed from Outcome) = Worked / Partly / Didn't. Filter fields are per playbook (e.g. Airline for flight playbooks). |
| B4 | Search link at the bottom | Added "Looking for something else?" search box after Related playbooks. |
| B5 | TikTok-style share | Share button → share sheet: X, Instagram, Threads, Facebook, WhatsApp, TikTok, Copy link. X/Facebook/Threads/WhatsApp use web share links; Instagram/TikTok have no web share URL, so use the native share sheet (Web Share API) on mobile and copy-link on desktop. Each playbook has an OG image so shared links look good. |

### Try flow
| # | Question / request | Decision |
|---|---|---|
| C1 | Grey out non-working agents | Yes: Coming soon (Dots, Grok-Bot, Manus) and Script only (Claude, Gemini) are greyed; Muse is highlighted and preselected. |
| C2 | Copy confirmation + sign-in | ✓ Copied state, then a one-time, dismissible "Save this prompt and get a reminder?" card (Google / email link / Not now). No forced pop-up. |
| C3 | Minimize required input | Max 1–2 required fields per playbook; everything else optional with a one-line "why it helps". Internet bill: only Provider is required. |
| C4 | ISP choices + location | Provider picker (Xfinity, Spectrum, AT&T, Verizon, T-Mobile, Cox, Other) + optional ZIP (offers and competitors vary by address; ZIP is enough, no full address). Don't maintain plan catalogs — ask price as a number and let users paste bill lines. |
| C5 | Pre-design forms for other playbooks | Yes: every playbook defines its form in YAML using reusable field types (provider picker per category, ZIP, money, date, airline/airport, duration). |
| C6 | Muse avatar + blue | Done in frames (placeholder avatar; swap for the official asset). |
| C7 | Does Open in Muse work? | Not yet — nothing is built. It works only if Muse supports a deep link / URL that pre-fills a prompt. Until confirmed: copy the prompt and open the Muse app/site. |
| C8 | Mobile | Designed for it: Try opens as a bottom sheet (Frame 7), fields stack, numeric keyboards for price/ZIP, large tap targets. P7 requires a mobile Playwright test. |

### Report result
| # | Question / request | Decision |
|---|---|---|
| R1 | More fields (time) | Added **How long did it take you?** (chips) and Provider; time-type playbooks ask hours saved instead of $. Only "Did it work?" is required. |
| R2 | Social post link | Yes, optional (X, Threads, Instagram, TikTok, Rednote); displayed after moderation, `rel="nofollow ugc"`. |
| R3 | Muse referral code | Yes, optional, in a Muse-blue box; rules as A8. |
| R4 | Share after submit | Yes: success screen is a share sheet + "Try next" suggestion. |

### Search
| # | Question | Decision |
|---|---|---|
| D1 | Is basic search enabled? | Not built yet (design + coding prompt only). P5 now requires: full-text + typo tolerance + synonyms + a **keyword → category map**, so e.g. "lower my bills" always returns Personal finance results; then fall back to popular playbooks, then the Request form. Never a dead end. |

---

## Part 9 — Design review round 2: answers & decisions

Supersedes Part 8 where they differ.

| # | Request | Decision |
|---|---|---|
| 1 | Muse color + avatar | Muse blue is now **`#2A66DE`** (sampled from the Muse logo; soft `#E8EFFC`). The official Muse avatar (fluffy character, circular crop) replaces the placeholder everywhere Muse appears as an agent: chips, Works with, Try card, Open in Muse button, report form. Get written OK from Muse to use the logo color and avatar. |
| 2 | "Create a playbook" button | Yes: **+ Create a playbook** in the header on every page (and in the avatar menu). It requires sign-in; signed-out users get the sign-in modal titled "Sign in to create a playbook". v1 = simple form into the admin review queue. |
| 3 | Sign-in mechanism | See Frame 8. **Never** required to browse, search, open, Try, Copy or Open in Muse. **Required** for Save, Report, Create, and reminders. One modal (Google, Facebook, email magic link); sign-up = sign-in; context-specific title; after sign-in the user returns to the same page and the pending action completes automatically; closing cancels only that action. One soft, dismissible reminder card after the first copy. |
| 4 | Detail page tweaks | Toast second line is now "Want it filled in with your details? **Try this playbook →**". Bottom search section removed (header search covers it). Works with = Muse + greyed chips for ChatGPT · Dots, Grok-Bot, Manus, **Instinct**; Claude, Gemini, "Coming soon", "Script only" and their explanation removed. |
| 5 | Save | **☆ Save** next to Share. Signed in: toggles to ★ Saved (Muse blue) + toast "Saved to My playbooks · View saved →". Signed out: sign-in modal "Sign in to save this playbook", then the save completes. Saved items live in **My playbooks** (Frame 9): tabs Saved / Tried / Reported, category filters, sort, unsave, "Updated since you saved" badge, "Did it work? Report" on tried items, empty state. |
| 6 | Search agent filter | Claude and Gemini removed; ChatGPT · Dots, Grok-Bot, Manus, Instinct listed greyed and not selectable; Muse selectable. |
| 7 | Try flow agents | Same as the detail page: Muse card + one row of greyed disabled chips (ChatGPT · Dots, Grok-Bot, Manus, Instinct); no labels or explanations. |
| 8 | Report form | "Your post about it" section removed (and the field dropped from the data model). |

---

## Part 10 — Design review round 3: answers & decisions

| # | Question / request | Decision |
|---|---|---|
| 1 | What do Playbooks / Starter kits / Categories in the header do? | **Playbooks** → `/playbooks` (every published playbook on the results page, sorted Best evidence, with filters). **Starter kits** → `/kits` (grid of kits → `/k/[slug]`). **Categories** → `/categories` (8 tiles with icon + count → `/c/[slug]`). |
| 2 | What do Popular Use Cases tiles do? | Each opens `/use-cases/[slug]`: gradient header + description, then a curated cross-category playbook list (e.g. Cut monthly bills = internet, phone, subscriptions, insurance, energy) with filters/sort. Content is filled from templates: `playbookhunt/playbookhunt_content_templates/` (YAML) or the **Playbook Intake** and **Use Cases & Kits** tabs in the tracker sheet. |
| 3 | Avatar next to Muse in the search agent filter | Done (Frame 2). |
| 4 | Meta-blue ring around the Muse avatar | Done everywhere: `#0081FB` ring. |
| 5 | Sign in with a Meta account? | Websites can offer **Facebook Login** as the Meta option (I'm not aware of a separate public "Meta account" login for third-party websites). Added **Continue with Facebook** to the sign-in modal (Frame 8); swap to a Meta-branded login later if one becomes available. |
| 6 | Try flow card button | Replaced "Continue with Google / Email me a link" with a single **Sign in** button (opens the full sign-in modal) + "Not now". |
| 7 | Referral code format | 6-character input (e.g. GT09WC): light-grey placeholder "e.g. GT09WC" that disappears when typing, auto-uppercase, validated as 6 letters/numbers. |

---

## Part 11 — Round 4: Apple login, mobile parity, accounts & cost, monetization

### Decisions
| # | Request | Decision |
|---|---|---|
| 1 | Remove Apple login | Removed everywhere. Sign-in = Google, Facebook, or email magic link. |
| 2 | Mobile consistent with web | New Frames 7a (homepage, detail after copy, Try sheet) and 7b (☰ menu, Report sheet, Sign-in sheet, My playbooks) mirror every desktop decision: header links live in the ☰ menu, Save/Share in the detail top bar, same Works with, toast, Try/Report/Sign-in rules, 6-character referral field, greyed agents, Muse avatar with Meta-blue ring. Prompts now require desktop + mobile together with a 390×844 test. |

### Accounts & keys — what each does
Don't paste keys into chat. Keep them in the services' dashboards, in `.env.local` on your machine, and in Vercel's environment settings; the coding agent only needs the variable names (listed in `.env.example`, prompt P1). Never share `SUPABASE_SERVICE_ROLE_KEY`.

| Service | What it does for Playbook Hunt | Free tier (at time of writing) | Paid tier |
|---|---|---|---|
| GitHub | Stores the code and history; runs tests on each change (GitHub Actions) | Free, private repos included | $0 needed |
| Supabase | Database (playbooks, reports, saves), sign-in (Google/Facebook/email), private evidence file storage, scheduled jobs | Free: ~500 MB database, ~1 GB storage, ~50k monthly users; inactive projects pause after ~1 week | Pro ~$25/mo |
| Vercel | Hosts the website, preview link for every change, scheduled tasks | Hobby: free but personal/non-commercial only | Pro ~$20/mo (needed once it earns money) |
| Resend | Sends email: sign-in links and "did it work?" reminders | ~3,000 emails/mo (100/day) | ~$20/mo for ~50k |
| PostHog | Product analytics (search → try → report funnel) | ~1M events/mo | Pay as you go above that |
| Sentry | Error alerts when something breaks | ~5k errors/mo, 1 user | Team ~$26/mo |
| Domain | playbookhunt.com (+ playbookhunt.ai) | — | .com ~$10–20/year; .ai usually more |
| Google / Facebook login apps | Needed for "Continue with Google/Facebook" | Free (Facebook app needs a privacy policy URL and data-deletion instructions to go live) | $0 |

Prices change; confirm on each pricing page before you sign up. Coding-agent subscription costs are not included.

### Estimated running cost
| Scenario | Monthly | 1 month | 3 months | 6 months |
|---|---|---|---|---|
| A. Build + private beta, all free tiers (non-commercial) | ~$0 + domain | ~$10–20 (domain, paid yearly) | ~$10–20 | ~$10–20 |
| B. Public launch (Supabase Pro + Vercel Pro, others free) | ~$45 | ~$55–65 | ~$145–155 | ~$280–290 |
| C. Growing (B + Resend Pro + Sentry Team + some PostHog overage) | ~$90–140 | ~$100–160 | ~$280–440 | ~$550–860 |

Recommendation: stay on A while building and in private beta; move to B at public launch (Supabase free projects pause when idle, and Vercel Hobby doesn't allow commercial use).

### Monetization
| Option | Fit | Notes |
|---|---|---|
| **Agent partner / referral fees** (paid per activated user when people "Open in Muse", later Dots, Grok-Bot…) | **Best fit** | Aligned with the core action and doesn't bias rankings if kept separate. Needs a partner agreement with each agent company. (Muse referral tokens reward the user, not you.) |
| Affiliate / lead-gen on high-intent playbooks (insurance quotes, travel booking, ISP switching) | Good, later | Clearly labeled, never an input to ranking. |
| B2B insights ("which agents actually complete which tasks") | Highest long-term value | Needs large, trusted outcome data first. |
| Premium subscription | Weak early | Core value must stay free to grow reports. |
| Sponsored placement in rankings | Avoid | Destroys the trust that makes the product work. |

**Include now or later?** Later. Build nothing billable in v1; ship only the hooks: outbound "Open in agent" click tracking with attribution params (added to P11), the rule that money never touches ranking (P0), and a disclosure line in "How we verify". Start partner conversations once the beta shows real usage (e.g. ~1,000 tries/week and a healthy try→report rate), and upgrade Vercel to Pro before any revenue.

---

## Part 12 — Name & domain decision

| Question | Decision |
|---|---|
| Name | **Playbook Hunt** |
| Domain | **playbookhunt.com** (also register playbookhunt.ai; optional huntplaybook.com redirect). Reserve @playbookhunt handles. Run a quick trademark search before launch. |
| Tie the domain to Muse? | No. A neutral brand avoids trademark/permission risk, keeps rankings credible, fits the multi-agent roadmap (Dots, Grok-Bot, Manus, Instinct) and keeps partner leverage. The product stays Muse-first ("What do you want Muse to do?", Muse preselected, "Tested with Muse"). |
| "Playbook" vs "workflow" | "Playbook": consumer-friendly, implies a proven plan; "workflow" reads as B2B automation. Lead with the task in titles; use "playbook" in supporting copy. Never call them prompts. |
| Playbook Hunt vs Playbooksmith | Playbook Hunt: "hunt" matches the core action (find what works) and is instantly clear. Playbooksmith can later name the creator program ("Become a Playbooksmith"). |
| Logo | "Playbook" + "**Hunt**" with "Hunt" in the orange accent `#FF5A1F`. Muse blue stays reserved for Muse. |
| Hero subline | "Proven playbooks with real results". |

### Folder & repo layout (decided)
```
dynamicsai/playbookhunt/
  playbookhunt_prompt/             plan, coding-agent prompts, tracker CSV, original references
  playbookhunt_design/             draw_frames.py, frame PNGs, Muse avatar asset
  playbookhunt_content_templates/  playbook / use-case / starter-kit templates
  playbookhunt_app/                the website's code repo (git, branch main) → GitHub repo "playbookhunt"
    docs/design, docs/brand, docs/content-templates   inputs for the coding agent
```
