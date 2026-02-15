# Wealth Architect - Session Memory

## Purpose
This file captures important context, decisions, and logic from development sessions that may not be fully captured in CLAUDE.md. Use this to quickly onboard a new Claude Code window.

---

## Session: January 18, 2026

### Key Accomplishments
1. **Updated Portfolio Architect Prompt to v2** - Added Core/Satellite split, risk-adjusted guardrails, lump sum DCA
2. **Created PROMPT_ARCHIVE_v2.txt** - Full version history documented
3. **Tested v2 prompt with 3 scenarios** - All outputs excellent
4. **Audited PDF generation code** - Identified likely causes of failure

### What Changed in v2
The prompt was audited with ChatGPT and updated to be more flexible for different user types:

**Core/Satellite Split (NEW)**
- Divides equities into Core (index funds) and Satellite (thematic/conviction)
- A/B users: 80% Core / 20% Satellite
- C users: 70% Core / 30% Satellite
- D users: 65% Core / 35% Satellite
- This is internal logic - not exposed to user

**Risk-Adjusted Guardrails (CHANGED)**
- Sector cap: 15% default → 20% for C/D with conviction
- Core requirement: 60% fixed → A/B need 65%, C/D need 55%
- Satellite cap: 15% fixed → A/B max 20%, C/D max 30-35%

**Lump Sum DCA Section (NEW)**
- Only appears when lump sum >= $10,000
- Recommends 4-8 weekly installments based on amount
- Explains tradeoffs (timing risk vs opportunity cost)
- Gives permission to invest all at once

### v2 Prompt Testing Results
Tested 3 scenarios - all passed:
- **Scenario 1 (Aggressive tech worker)**: Core/Satellite correct, DCA section appeared, SMH included
- **Scenario 3 (ESG millennial)**: ESG funds substituted, green bonds, climate tilts
- **Scenario 8 (Inflation-anxious business owner)**: Heavy TIPS, commodities/energy hedges, 6-week DCA

### PDF Error Audit
**Status**: PDF generation failing silently

**Likely Causes (prioritized):**
1. **Unicode encoding (P0)** - fpdf2 uses Latin-1, Gemini outputs curly quotes/em-dashes
2. **Table truncation (P1)** - 25 char limit cuts off ETF names
3. **Bold sub-headers (P1)** - `**text:**` patterns not styled
4. **No error logging (P2)** - Can't see actual exception

**Fixes needed in `WA_backend.py`:**
- Add Latin-1 sanitization before all `pdf.cell()` calls
- Increase truncation limit from 25 to 35 chars
- Add better error logging

### What We Decided NOT to Do
- JSON output format (keep markdown narrative - works well)
- Server-side validation/re-run logic (trust the prompt)
- Deterministic Core/Satellite function in backend (prompt handles it)

---

## Session: January 17, 2026

### Key Accomplishments
1. **Optimized Portfolio Architect Prompt** - The main prompt that generates portfolios
2. **PDF Download Feature** - Full implementation with styled output
3. **Prompt Archive System** - Versioning rule for tracking prompt changes
4. **Test Scenarios Document** - 10 comprehensive test cases

---

## Prompt Design Philosophy

### Why 8 Expert Frameworks?
The Portfolio Architect prompt uses 8 investment expert "lenses" as **internal AI guidance** (not user-facing):
- **John Bogle**: Low-cost index funds, minimize fees
- **David Swensen**: Diversify across uncorrelated asset classes
- **Fama-French**: Small-cap and value factor tilts for aggressive investors
- **Ray Dalio**: Global diversification, don't over-concentrate in one country
- **Howard Marks**: Understand cycles, real risk = permanent capital loss
- **Warren Buffett**: Quality over speculation, time in market
- **Ken Rogoff**: Inflation and currency risk awareness
- **Cathie Wood**: Tech/innovation lens when user expresses that conviction

**Key insight from user**: "I want to give the AI as much professional guidance as possible" - sophisticated internal thinking, but simple plain-language output for users.

### Risk Profile Mapping
Critical mapping that determines equity/bond split:
- **Reaction A** (sell everything): Conservative → 40% equities / 60% bonds+cash
- **Reaction B** (sell some): Moderate → 60% equities / 40% bonds+cash
- **Reaction C** (do nothing): Growth → 80% equities / 20% bonds+cash
- **Reaction D** (buy more): Aggressive → 90% equities / 10% bonds+cash

### Safety Guardrails (Non-Negotiable)
These are enforced in the prompt and should be verified in testing:
1. No single stock > 5% of total portfolio
2. No single sector > 15% of total portfolio
3. At least 60% must be diversified broad-market ETFs
4. Speculative positions should not exceed 15%
5. Allocations MUST sum to exactly 100%

### Handling User Convictions
The prompt treats user convictions seriously - this is what makes portfolios personal:
- **Sector expertise**: Add up to 15% sector exposure
- **Individual stock**: Include at up to 5% with risk explanation
- **ESG preferences**: Respect exclusions, suggest alternatives (ESGV, ESGU, VSGX)
- **Market sentiment**: Adjust allocation, explain tradeoff
- **No convictions**: Standard Bogle/Swensen diversified portfolio

---

## Technical Decisions

### PDF Generation
- Uses `fpdf2` library (added to requirements.txt)
- Custom `WealthArchitectPDF` class with header/footer branding
- Parses markdown sections by `####` headers
- Renders tables, bullets, paragraphs with proper formatting
- Title page shows user profile summary
- Tax and disclaimer pages at the end
- **Error handling**: If PDF fails, report still displays (try/except wrapper)

### Dollar Sign Escaping
Streamlit interprets `$` as LaTeX. The backend escapes dollar signs:
```python
return response.text.replace("$", "\\$")
```
The PDF generator reverses this:
```python
clean_report = report_markdown.replace('\\$', '$').replace('\$', '$')
```

### Prompt Versioning Rule
When ANY prompt is modified:
1. Create new `PROMPT_ARCHIVE_v{N}.txt` file
2. Include ALL current prompts (not just changed one)
3. Add VERSION HISTORY section noting what changed
4. Current version: `PROMPT_ARCHIVE_v2.txt`

---

## What's NOT Done Yet

### Pre-Launch
- [x] Test updated v2 prompt with various user profiles ✅
- [x] Verify lump sum DCA section appears correctly for >= $10k ✅
- [ ] **Fix PDF download** (see PDF Error Audit above)
- [ ] UI/UX cosmetic polish
- [ ] Deploy to Streamlit Cloud

### Post-Launch (Nice to Have)
- [ ] Pie chart visualization (Plotly imported but not rendering)
- [ ] Structured JSON output from portfolio prompt
- [ ] Custom theming
- [ ] Mobile improvements

---

## Files Quick Reference

| File | Purpose |
|------|---------|
| `WA_backend.py` | All prompts + Gemini API + PDF generation |
| `WA_app.py` | Streamlit UI (7-step wizard + report page) |
| `CLAUDE.md` | Main project context (read this first) |
| `PROMPT_ARCHIVE_v2.txt` | **CURRENT** - All prompts frozen at v2 |
| `PROMPT_ARCHIVE_v1.txt` | Previous version (baseline) |
| `TEST_SCENARIOS.txt` | 10 test cases for validation |
| `Prompt_References.md` | Original ChatGPT prompts for reference |
| `PROMPT_ARCHITECTURE.txt` | Flow diagrams and JSON schemas |
| `ChatGPT Audit and Adjustment Summary.txt` | Audit findings that led to v2 |
| `wealth_architect_claude_guide_implementation_notes.md` | Detailed implementation guide from audit |

---

## How to Start a New Session

1. Read `CLAUDE.md` first - it has current state and next steps
2. Check `TEST_SCENARIOS.txt` if testing
3. Check `PROMPT_ARCHIVE_v1.txt` for current prompt text
4. If modifying prompts, create `PROMPT_ARCHIVE_v2.txt`

---

## User Preferences (Learned This Session)

- Prefers **PLAN mode** before making code changes
- Wants **sophisticated AI guidance** internally but **plain language** for users
- Values **prompt versioning** for rollback capability
- Wants **report to always display** even if PDF fails
- Prefers **test scenarios** to validate prompt quality
- Uses Claude Code for extended development sessions

---

## Models Used
- **Smart Model**: `gemini-3-pro-preview` (audit, portfolio generation)
- **Fast Model**: `gemini-2.5-flash` (risk analysis, simple tasks)
