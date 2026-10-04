I’m building a new website for discovering and sharing **AI agent playbooks/workflows** that have been tested in real-world use.

### Product concept

The core idea is:

> **Users come to the site with a task they want an AI agent to accomplish, discover a proven playbook for that task, try it themselves, and report the outcome.**

For example:

* “Lower my Comcast/internet bill”
* “Find a cheaper car insurance plan”
* “Plan a 7-day Japan trip”
* “Find the cheapest flight to Europe”
* “Research my competitors”
* “Create a marketing plan for my small business”
* “Analyze my monthly spending”
* “Compare products before I buy”
* “Navigate a medical appointment / prepare questions for my doctor”

A playbook may contain:

* The task/goal
* The AI agent it was tested with (initially Muse, but eventually agent-agnostic)
* The prompt/instructions or workflow
* Required inputs/context
* Step-by-step instructions when necessary
* The creator
* When it was last tested
* Number of people who tried it
* User-reported outcomes
* Success rate / ratings
* Quantifiable outcomes when available (e.g. $200 saved, 3 hours saved)
* Evidence or screenshots when appropriate

### Initial positioning

This should NOT feel like a generic “prompt library.”

The longer-term vision is closer to:

**“Find AI workflows that actually work for the task you want to accomplish.”**

The important differentiation is **real-world outcome data**, rather than simply collecting prompts.

The core loop is:

**Task → Discover Playbook → Try It → Report Outcome → Aggregate Results → Better Ranking/Discovery**

For example, instead of:

> “10,000 popular AI prompts”

we want something closer to:

> **Lower Your Internet Bill**
>
> 1,247 people tried this playbook
> 68% reported a successful outcome
> Median reported savings: $18/month
> Last verified: 3 days ago
> Tested with: Muse

### Initial categories

We are considering categories such as:

* 💰 Personal Finance / Saving Money
* ✈️ Travel – Booking Transport
* 🗺️ Travel – Trip Planning
* 🛍️ Shopping
* 🏢 Small Business
* ⚡ Personal Productivity
* 🏥 Health/Fitness / Navigating Medical Care
* 🎨 Creativity

The initial launch may contain roughly **40–50 curated playbooks** across these categories rather than thousands of low-quality prompts.

### Discovery / homepage

The website should be **search-first rather than leaderboard-first**.

The primary question should be:

> **“What do you want an AI agent to do?”**

Potential examples in the search box:

* “Save $500 this year”
* “Plan my Japan trip”
* “Find a cheaper flight”
* “Research my competitors”
* “Reduce my monthly bills”

Below that could be:

* Popular categories
* Trending playbooks
* Recently verified playbooks
* Playbooks with strong real-world outcomes
* Popular/new workflows

### Playbook detail page

A playbook page should clearly communicate:

1. **What problem does this solve?**
2. **What agent/model was used?**
3. **How do I use it?**
4. **What happened when other people tried it?**
5. **How recently was it verified?**
6. **Can I report my own result?**

The main CTA should probably be something like:

**Try this playbook**

followed by:

**Did it work for you? → Report your result**

### Community / ranking

Users should eventually be able to:

* Upvote/useful playbooks
* Report whether a playbook worked
* Submit their own playbooks
* Share outcomes
* Potentially provide evidence

However, **raw votes should not be the primary measure of effectiveness**.

We want to distinguish:

* Popularity
* Usage
* Verified success
* Quantifiable outcomes
* Recency

For example, a playbook with 500 votes isn't necessarily better than one with 100 votes if the latter has much stronger verified outcomes.

### Creator / referral component

Creators may optionally attach an AI-agent referral code/link to their playbook.

However, referral incentives should be **separate from the effectiveness ranking** so that creators cannot simply buy/earn ranking through referrals.

Potentially:

> Creator: Jane
> 1,200 people tried this
> Jane's referral link

But referral mechanics are secondary to the core product.

### Distribution

The initial content/discovery strategy may involve finding interesting AI-agent use cases from:

* X / Twitter
* Reddit
* Threads
* 小红书
* AI communities

Social media should primarily be a **discovery/distribution channel**, while our website becomes the destination where the workflow is structured, tested, and measured.

### Long-term vision

The initial wedge may be Muse, but the architecture should eventually support:

* Muse
* Claude
* ChatGPT
* Gemini
* other AI agents

The long-term product could become an **AI-agent recommendation/performance layer**:

> “Tell me what you want to accomplish, and show me the AI workflows that have the strongest evidence of actually accomplishing it.”

---

## What I want you to research

Please search the web for **existing websites/products that could serve as design and UX references for this product.**

I am NOT necessarily looking for sites with exactly the same business model.

Instead, identify websites that have excellent implementations of individual pieces of the experience, such as:

1. **Discovery**

   * Product Hunt
   * App/software directories
   * marketplaces
   * recommendation platforms

2. **Search + filtering**

   * Large directories
   * skill/plugin marketplaces
   * SaaS marketplaces
   * template libraries

3. **Community ranking**

   * Upvotes
   * Reviews
   * Ratings
   * Trending algorithms
   * “Most useful” / “most popular” systems

4. **Verified outcomes / reviews**

   * Platforms where users report actual results
   * Product review sites
   * Consumer recommendation sites
   * Case-study-driven marketplaces

5. **Workflow / template discovery**

   * AI prompt libraries
   * Claude skills marketplaces
   * MCP/plugin directories
   * Automation/template marketplaces
   * Notion/template marketplaces
   * Zapier-style workflow directories

6. **Playbook/detail pages**

   * Sites that clearly explain what something does
   * Show usage/results
   * Have a strong “Try/Get Started” CTA
   * Display social proof and trust signals

7. **Creator/community contribution**

   * Platforms where users submit content/workflows/templates
   * Creator profiles
   * Attribution
   * Reputation systems

8. **Homepage design**

   * Search-first discovery
   * Category navigation
   * Trending/recommended content
   * Personalization

### For each reference website, please provide:

* Website name + URL
* What part of our product it is a good reference for
* Specific UX/UI patterns worth borrowing
* What we should NOT copy
* Why it is relevant to our product
* Screenshots or specific pages/components if available

Then propose:

### A. Top 5 reference websites

The five websites you think are most useful for designing this product.

### B. Recommended design combination

For example:

> Use Website X for homepage/discovery
> Website Y for search/filtering
> Website Z for community/ranking
> Website A for playbook detail pages
> Website B for creator profiles

### C. Suggested overall UX

Please describe the ideal:

**Homepage → Search → Results → Playbook Detail → Try → Report Outcome → Ranking**

flow, including the most important UI components.

Please prioritize **existing, high-quality products with strong UX** over generic lists of AI prompt websites. I want references that can help me actually design and build the product.
