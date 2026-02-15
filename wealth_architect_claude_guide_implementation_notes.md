Wealth Architect — Claude Guide & Implementation Notes

Purpose
-------
This document is a developer-focused guide for implementing the agreed risk/allocation, DCA, and prompt changes in the Wealth Architect (Claude) codebase. It is intended to be pasted into the Claude prompt files / backend code and used as a handoff for implementation and QA.

OVERVIEW — agreed principles
----------------------------
• Safety-first defaults remain for passive users. Defaults should be conservative for non-active investors.
• Use the existing crash-reaction multiple choice (A/B/C/D) as the single authoritative risk input. Do not replace this UI.
• Relax guardrails automatically for users who select C (do nothing) or D (buy more) — no extra "conviction override" checkbox required.
• Keep the current convictions free-text box (same page) for the AI to analyze for sector/thematic hints; do not require users to manually configure sector overrides.
• Always include a DCA plan in the model output when a lump sum exceeds the configured threshold (default $10,000). Provide a short explanatory blurb with the plan.

RISK MAPPING (A–D remains source-of-truth)
-----------------------------------------
User-facing crash-reaction mapping (keep exactly as-is):
• A (sell everything) → Conservative → 40% equities / 60% bonds+cash
• B (sell some) → Moderate → 60% equities / 40% bonds+cash
• C (do nothing) → Growth → 80% equities / 20% bonds+cash
• D (buy more) → Aggressive → 90% equities / 10% bonds+cash

CORE / SATELLITE LAYER (internal; no UI change)
-----------------------------------------------
Translate the equity% above into a Core / Satellite split automatically so allocations become more personalized and allow slightly larger satellite weights for C/D.

Suggested deterministic mapping for Core / Satellite split:
• A (Conservative): equity 40% → Core = 75% of equities; Satellite = 25% of equities
  - Example totals: Core = 30% of portfolio, Satellite = 10% of portfolio, Bonds = 60%

• B (Moderate): equity 60% → Core = 70% of equities; Satellite = 30% of equities
  - Example totals: Core = 42%, Satellite = 18%, Bonds = 40%

• C (Growth): equity 80% → Core = 65% of equities; Satellite = 35% of equities
  - Example totals: Core = 52%, Satellite = 28%, Bonds = 20%

• D (Aggressive): equity 90% → Core = 60% of equities; Satellite = 40% of equities
  - Example totals: Core = 54%, Satellite = 36%, Bonds = 10%

Rationale: Keep the UI simple with A–D while producing portfolios that reflect conviction for Growth / Aggressive users.

NON-NEGOTIABLE GUARDRAILS
-------------------------
• Single-stock cap: 5% of total portfolio (default).
• Sector cap (hard): 15% of portfolio for any one sector ETF unless user is C/D and satellite allows more (follow satellite pct of equity but still respect single-stock cap).
• Core minimum: implemented through Core pct of equity mapping above (prevents extreme concentration for most users).

DCA (Dollar-Cost Averaging) RULES
--------------------------------
• Threshold: default lump_sum threshold = $10,000 (configurable).
• If lump_sum > threshold, model must include a `dca_plan` object in the JSON output.
• Default recommended schedules:
  - $10k–$50k → 4 weekly buys (≈30 days) — 4 equal installments.
  - $50k–$200k → 8–12 weekly buys (60–90 days) — equal installments.
  - > $200k → multi-month schedule and suggest advisor consult (include rationale).
• Always show a short DCA explanation text describing tradeoffs (sequencing & timing risk vs opportunity cost of delayed deployment).
• The UI should display the DCA plan and a one-click confirmation that the user prefers to deploy all immediately. Do not precheck the "deploy all" option.

PROMPT / BACKEND CHANGES (high level)
-------------------------------------
1) PROMPT 2 — Risk Translator (deterministic mapping)
• Input: `crash_reaction` (A/B/C/D), age (optional), lump_sum (optional).
• Output (JSON snippet) should include these fields:
  {
    "risk_label": "Growth",
    "equity_pct": 80,
    "bond_pct": 20,
    "core_pct_of_equity": 65,
    "satellite_pct_of_equity": 35
  }
• Place this deterministic logic in Prompt 2 and/or backend translator function. This keeps A–D as the single source while returning the extra fields the Portfolio Architect expects.

2) PROMPT 3 — Portfolio Architect (core construction + DCA)
• Required JSON top-level fields in the model output now must include:
  - portfolio[] (array of holdings: ticker, name, allocation_pct, initial_buy, category, why_included, risk_note)
  - dca_plan (object)
  - dca_explanation (short string)
  - guardrails (array or object describing which guardrails triggered)
  - self_audit (object that asserts: sum==100, guardrail_violations:false)
  - explainers (short plain-language rationale block)
• The prompt must instruct the model to respect `core_pct_of_equity` and `satellite_pct_of_equity` when building the portfolio. For satellite allocations, prioritize ETFs (QQQ/sector ETFs) over single stocks, but include single stocks as small slices only when user convictions appear in the free-text box (max 5% each).

3) Add `dca_plan` generation logic in backend prompt context when lump_sum > threshold. Provide recommended schedule amounts and installment numbers to the model as variables so it returns exact installment amounts and schedule.

4) Enforce JSON-only reply (strict schema) for machine consumption; include a short human-friendly paragraph but require JSON as the single source of truth.

CODE / PSEUDO (backend placement suggestions)
--------------------------------------------
Insert a translator function (example Python) in WA_backend.py before building the final prompt:

```python
def translate_crash_reaction_to_allocation(crash_reaction, age=None):
    mapping = {
      'A': {'equity_pct':40, 'bond_pct':60},
      'B': {'equity_pct':60, 'bond_pct':40},
      'C': {'equity_pct':80, 'bond_pct':20},
      'D': {'equity_pct':90, 'bond_pct':10},
    }
    base = mapping[crash_reaction.upper()].copy()
    if crash_reaction == 'C':
        base.update({'core_pct_of_equity':65, 'satellite_pct_of_equity':35})
    elif crash_reaction == 'D':
        base.update({'core_pct_of_equity':60, 'satellite_pct_of_equity':40})
    elif crash_reaction == 'B':
        base.update({'core_pct_of_equity':70, 'satellite_pct_of_equity':30})
    else:
        base.update({'core_pct_of_equity':75, 'satellite_pct_of_equity':25})
    # Optional age tweak for younger users
    if age and isinstance(age, int) and age < 35:
        base['equity_pct'] = min(95, base['equity_pct'] + 5)
    return base
```

• Call this translator, then inject its result into the Prompt 3 context so that the Portfolio Architect knows exact core/satellite and equity/bond targets.

EXAMPLE JSON SCHEMA (strict) — paste into prompt file
----------------------------------------------------
Required top-level JSON object returned by model. Model must output only this JSON block (and an optional short 2–3 sentence human summary). Use the JSON for machine parsing.

```json
{
  "summary": "Short 1-2 sentence human summary",
  "portfolio": [
    {
      "ticker": "VTI",
      "name": "Vanguard Total Stock Market ETF",
      "allocation_pct": 50,
      "initial_buy": 27500,
      "category": "US Core Equity",
      "why_included": "Core US market exposure",
      "what_it_owns": "Large + mid + small cap US stocks",
      "risk_note": "Exposed to market drawdowns"
    }
  ],
  "dca_plan": {
    "lump_sum": 55000,
    "threshold_recommended": 10000,
    "recommended_schedule": "4 weekly buys",
    "instalments": 4,
    "amounts": [13750,13750,13750,13750],
    "rationale": "Mitigates sequencing risk; keeps you invested while reducing timing risk"
  },
  "dca_explanation": "Short plain-language tradeoffs between DCA and lump deployment.",
  "guardrails": {
    "single_stock_cap_pct": 5,
    "sector_cap_pct": 15,
    "violations": false
  },
  "self_audit": {
    "sum_pct": 100,
    "guardrail_violations": false
  },
  "explainers": "1-3 short lines explaining portfolio rationale"
}
```

FILES TO EDIT (exact places)
----------------------------
• PROMPT_ARCHITECTURE.txt — add fields core_pct_of_equity & satellite_pct_of_equity to Prompt 2 outputs and document the deterministic translator.
• portfolio_building_prompt.txt — add the dca_plan requirement to Prompt 3 and require strict JSON output schema.
• WA_backend.py — implement `translate_crash_reaction_to_allocation()`, compute DCA recommendation pre-prompt, inject variables into the final prompt, and parse the model’s JSON output.
• WA_app.py — render `dca_plan` block under Lump Sum output (Dual Outputs area) and render a one-sentence rationale and “deploy all now” confirmation.

TESTS / QA (minimal set)
------------------------
Add automated tests in TEST_SCENARIOS and test harness:
1) Reaction D, age 30, conviction text mentions "AI" → assert satellite >= 30% and QQQ or SMH appears in portfolio.
2) Reaction A, age 55 → assert bond_pct >= 50 and satellite <= 15%.
3) Lump_sum = $55,000 → assert `dca_plan` exists and instalments match the schedule rules (e.g., 4 or 8 installments depending on threshold).
4) Model self_audit returns sum_pct == 100 and guardrail_violations == false for all successful runs.

UX COPY SUGGESTIONS
-------------------
• Lump sum modal copy (short): "We recommend DCA for lump sums over $10,000 to reduce timing risk. Recommended: 4 weekly buys for $10–50k. You can choose to deploy all now; just be aware of sequencing risk."
• Blurb when relaxing guardrails for C/D (short): "Because you selected 'do nothing' or 'buy more' in a market drop, your portfolio includes a slightly larger thematic/satellite allocation to reflect higher risk tolerance. Core exposure remains to preserve diversification."

IMPLEMENTATION NOTES / DEV HINTS
--------------------------------
• Keep the free-text convictions field in the same wizard page; parse it for keywords (AI, Tech, Crypto, ESG, Real Estate) and pass it into Prompt 3 as `user_convictions_text`. The model should use these keywords only as hints when building satellite allocations (do not require explicit user "override").
• Enforce the 5% single-stock cap server-side if the model ever returns higher — reject output and re-run with an additional prompt instruction to fix the violation. Add server-side validation for the JSON.
• Add a server-side fallback: if the model returns malformed JSON, run a cleanup prompt that asks the model to re-output valid JSON only.
• Keep the human summary separate from the JSON and place it in the UI above the parsed portfolio.

NEXT STEPS / Handoff
--------------------
• Implement changes in the files listed above.
• Add the three QA unit tests into the test harness and run the scenarios in TEST_SCENARIOS.txt.
• Iterate on the specific core/satellite percentages if you want a different level of relaxation for C vs D. The current mapping is intentionally conservative but biased toward letting Growth/Aggressive users have a bigger satellite.

END

