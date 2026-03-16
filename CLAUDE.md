# Wealth Architect - Project Context

## Project Overview
A web application that transforms a text-based investment prompt chain into an interactive portfolio builder. Helps users (friends/family) create personalized investment portfolios based on their financial situation, risk tolerance, and goals.

## Goal
Create a shareable frontend where users input their financial details and receive:
- A personalized portfolio with ticker allocations
- Visual pie chart matching the allocation table
- Detailed explanations for each holding
- Tax guidance and disclaimers

---

## Current State (as of March 14, 2026)

### App Status
- **LIVE** at https://the-portfolio-pilot.streamlit.app/
- GitHub repo: `EricDelgSLS/wealth_architect` (public)
- Auto-deploys on push to `main` branch
- API key stored in Streamlit Cloud secrets

### Files in Project
- `WA_backend.py` - Backend with Gemini API calls + **optimized Portfolio Architect prompt (v3)**
- `WA_app.py` - Streamlit frontend with sequential 7-step wizard + intro + report pages + **browser print button**
- `requirements.txt` - Dependencies (streamlit, google-generativeai, plotly, pandas, python-dotenv)
- `AGENTS.md` - Context file for Codex (points to CLAUDE.md)
- `CLAUDE.md` - This file (project context)
- `AI Investing Prompt Chain Gemini.txt` - Original monolithic prompt chain (north star for output format)
- `Prompt_References.md` - Reference prompts for building optimized Portfolio Architect prompt
- `Project_ The _Wealth Architect_ Application.txt` - PRD/guide document
- `PROMPT_ARCHITECTURE.txt` - Detailed prompt mapping guide
- `PROMPT_ARCHIVE_v1.txt` - Archive of all prompts (v1 = January 17, 2026 baseline)
- `PROMPT_ARCHIVE_v2.txt` - Archive (v2 = January 18, 2026 — Core/Satellite, DCA strategy)
- `Claude_Code_Prompt_WA_Update.md` - Post-feedback update notes from user

### What's Working ✅
- **Sequential 7-step wizard flow** (no more confusing tabs)
- **Intro page** with philosophy, goals, and disclaimer
- **Step 1: Basics** - Age slider, state input
- **Step 2: Financial Foundation** - Emergency fund Y/N, debt Y/N (advisory warning, not blocker)
- **Step 3: Current Assets** - Free-text input for investable assets (non-retirement focused)
- **Step 4: The Numbers** - Lump sum + biweekly income with $ text inputs and calculation helper
- **Step 5: Risk Profile** - Market crash scenario with A/B/C/D reactions
- **Step 6: Market Perspective** - Includes stock convictions, ESG preferences, market sentiment
- **Step 7: Review & Generate** - Summary of all inputs with corrections box
- **Final Report Page** - Portfolio output + Tax section + Disclaimer + "What's Next" guidance
- Session state management across all steps
- Back/Next navigation throughout
- Start Over functionality
- **"What's Next" expanders** with AI guidance (high-performance models, project folders, quarterly check-ins)
- **Optimized Portfolio Architect prompt** with 8 expert frameworks (Bogle, Swensen, Fama-French, Dalio, Marks, Buffett, Rogoff, Cathie Wood)
- **Browser print button** - Users can save report as PDF using browser's native print-to-PDF
- **Privacy statement** - Clear disclosure on intro page that data is session-only, not stored

### Completed Milestones
- [x] App deployed to Streamlit Cloud (March 2026)
- [x] Tested with 4 real users (Enrik, Ron, Birdy, Eric)
- [x] Portfolio Architect prompt v3 with dividend info + overlap guardrails
- [x] Print button cleaned up

### In Progress
- [ ] **UI/UX Theme** — Choose palette (Emerald Green, Sky Blue, or Green+Gold), implement config.toml
- [ ] **PROMPT_ARCHIVE_v3.txt** — Archive current prompts after v3 changes
- [ ] Commit + push v3 changes to deploy

### Post-Launch Features (Nice to Have)
- [ ] Pie chart visualization (Plotly imported but not yet rendering)
- [ ] Structured JSON output from portfolio prompt (for chart/table sync)
- [ ] Mobile responsiveness improvements
- [ ] Historical backtesting tool (separate script — needs Yahoo Finance/Alpha Vantage API)
- [ ] Automated prompt quality testing (20+ scenarios, scored by AI)

---

## Architecture: Prompt Structure

The app uses specialized prompts for different tasks:

1. **Asset Auditor** (Gemini 3 Pro) - Analyzes messy asset text
2. **Risk Translator** (Gemini 2.5 Flash) - Converts reactions to risk profile
3. **Portfolio Architect** (Gemini 3 Pro) - CORE prompt that builds the portfolio
4. **Static Content** - Tax guidance and disclaimers (built into UI)

See `PROMPT_ARCHITECTURE.txt` for full specifications and JSON schemas.

---

## Next Steps

### Phase 1: Prompt Optimization ✅ COMPLETE
**Completed:**
- ✅ Built optimized Portfolio Architect prompt with 8 expert frameworks
- ✅ Incorporated expert lenses from `Prompt_References.md` (Example 3)
- ✅ Maintained output format from north star (tables: lump sum, biweekly DCA, holdings explained)
- ✅ Enforced guardrails: 5% single stock cap, 15% sector cap, 60% core requirement
- ✅ Added self-audit checklist for AI to verify output before generating
- ✅ Keep implementation tips plain-language, emphasize AI-assisted quarterly reviews

**Remaining (Optional):**
- [ ] Optimize Asset Auditor prompt (currently works, but could be enhanced)
- [ ] Optimize Risk Translator prompt (currently works, but could be enhanced)
- [ ] Test prompt quality with various user inputs and iterate

### Phase 2: Save as PDF ✅ COMPLETE
- ✅ Implemented browser print button (users press Ctrl+P / Cmd+P to save as PDF)
- ✅ Uses `streamlit.components.v1.html()` for proper JavaScript execution
- ✅ Added clear instructions for Windows/Mac/Mobile users
- ✅ Removed fpdf2 dependency (was too fragile, failed after 4 fix attempts)
- ✅ Added privacy statement to intro page

### Phase 3: Testing & Optimization ✅ COMPLETE
- ✅ Tested with 4 real users
- ✅ Iterated on prompt based on feedback (v3: dividends, overlap guardrails)
- ✅ Cleaned up save/print UX

### Phase 4: Deployment ✅ COMPLETE
- ✅ Deployed to Streamlit Cloud at https://the-portfolio-pilot.streamlit.app/
- ✅ Tested shareable link
- ✅ Got feedback from friends/family (Enrik, Ron, Birdy)

### Phase 5: Polish & Theming (CURRENT)
- [ ] Choose and implement UI theme (dark mode + green/blue/gold accents)
- [ ] Create PROMPT_ARCHIVE_v3.txt
- [ ] Commit + push v3 changes
- [ ] Test live app with dividend output

### Phase 6: Future Enhancements (Nice to Have)
- [ ] Add Plotly pie chart visualization
- [ ] Consider JSON output from Portfolio Architect for easier parsing
- [ ] Historical backtesting tool (separate script)
- [ ] Automated prompt quality testing (20+ scenarios)
- [ ] Mobile responsiveness improvements

---

## Key Design Decisions

1. **Non-Retirement Focus**: This tool builds portfolios for taxable brokerage accounts, not 401(k)/IRA. Retirement guidance is educational only.

2. **Sequential Wizard Flow**: Users complete one step before moving on (no tab jumping). Feels like an interview.

3. **Prompt Versioning Rule**:
   - All prompts are archived in `PROMPT_ARCHIVE_v*.txt` files
   - When ANY prompt is modified, create a new version file (v2, v3, etc.)
   - The new file should contain ALL current prompts (not just the changed one)
   - Include a VERSION HISTORY section at the bottom noting what changed
   - This allows easy reference to previous versions and rollback if needed
   - Current version: `PROMPT_ARCHIVE_v3.txt` (March 14, 2026 — dividends + overlap guardrail)

4. **Market Perspective Section**: Expanded beyond "sector tilt" to capture:
   - Sector expertise (work-related knowledge)
   - Individual stock convictions (with reasoning)
   - ESG/ethical preferences (sin stock avoidance)
   - General market sentiment

4. **Debt as Advisory**: High-interest debt triggers a warning but doesn't block portfolio creation. User proceeds assuming debt is handled separately.

5. **Pie Chart + Table Sync**: Both will render from same data source to ensure they always match.

6. **North Star Prompt**: The original `AI Investing Prompt Chain Gemini.txt` contains proven output format. New prompts should follow this structure.

7. **Expert Lenses for Portfolio Logic**: Draw from Bogle, Swensen, Fama-French, Dalio, Buffett, and tech/AI perspectives (see `Prompt_References.md`).

---

## Reference Documents
- `PROMPT_ARCHITECTURE.txt` - Detailed prompt specs and JSON schemas
- `AI Investing Prompt Chain Gemini.txt` - Original prompt chain (north star for format)
- `Prompt_References.md` - **NEW** Rich prompt fragments for optimized Portfolio Architect
- `Project_ The _Wealth Architect_ Application.txt` - Original PRD

---

## Session Notes

**December 28, 2025**:
- Audited current project state
- Mapped out prompt architecture (4 prompts + static content)
- Identified gap: prompts return narrative, need JSON
- Created PROMPT_ARCHITECTURE.txt guide
- Created this CLAUDE.md file

**January 9, 2026**:
- Rebuilt `WA_app.py` with sequential 7-step wizard (replaced tab-based UI)
- Added intro page with philosophy, goals, disclaimer
- Added "How to calculate biweekly investment" expander
- Changed number inputs to text inputs with $ prefix for clarity
- Expanded Step 6 from "Sector Tilt" to "Market Perspective" (includes stock convictions, ESG, sentiment)
- Added example expander with 4 types of market perspectives
- Added "What's Next" section to final report (second opinion, adjustments, living document)
- Updated backend `generate_final_plan()` to accept full user_data dict
- Fixed various markdown rendering issues (dollar sign escaping)
- Added "Round to whole dollars" notes on income inputs
- **UI SKELETON COMPLETE** - Ready for prompt optimization

**January 10, 2026**:
- User tested full flow - reported smooth experience up to output
- Fixed scroll-to-top issue on final report page (added JavaScript)
- Updated "Get a Second Opinion" expander to recommend high-performance reasoning models (GPT-4o, o1, Gemini 2.0)
- Updated "Living Document" expander to recommend ChatGPT Project folders / Gemini Gems for portfolio memory
- Updated prompt implementation tips for plain-language, AI-assisted quarterly reviews
- Added `Prompt_References.md` with reference prompts from original ChatGPT portfolio-building sessions
- **Current output structure looks good** - tables clean, explanations useful
- Ready to optimize Portfolio Architect prompt using reference materials

**January 17, 2026** (Session resumed after context compaction):
- ✅ **Built optimized Portfolio Architect prompt** (`PLAN_SYSTEM_PROMPT` in `WA_backend.py`)
  - Added 8 expert frameworks as internal AI guidance (Bogle, Swensen, Fama-French, Dalio, Marks, Buffett, Rogoff, Cathie Wood)
  - Risk profile → allocation mapping (A=40/60, B=60/40, C=80/20, D=90/10)
  - Safety guardrails (5% single stock, 15% sector, 60% core, 15% speculative)
  - Handling user convictions (sector expertise, stock picks, ESG, sentiment)
  - Self-audit checklist (6 verification points before output)
  - Plain language output format with required sections
- ✅ **Added PDF download functionality**
  - Added `fpdf2` to `requirements.txt`
  - Built `generate_pdf_report()` function in `WA_backend.py`
  - Custom `WealthArchitectPDF` class with branded header/footer
  - Markdown-to-PDF parser handles tables, bullets, paragraphs
  - Title page with user profile summary
  - Styled section headers with steel blue underlines
  - Tax considerations and disclaimer pages
  - Added download button to `WA_app.py` (line 599-610)
- User noticed PDF functionality was already added during compaction (by user)
- Verified optimized prompt was correctly integrated
- Discussed remaining prompts (Asset Auditor, Risk Translator) - decision to test first, optimize if needed
- **Decision: Skip pie chart for MVP** - move to post-launch enhancements
- **Updated CLAUDE.md** to reflect pre-launch vs post-launch priorities
- **User going to test app now** - will report back with results

**January 18, 2026**:
- User tested app end-to-end, then audited Portfolio Architect prompt with ChatGPT
- Created `ChatGPT Audit and Adjustment Summary.txt` and `wealth_architect_claude_guide_implementation_notes.md`
- Audit identified need for more flexibility for aggressive (C/D) users and lump sum DCA guidance
- ✅ **Updated Portfolio Architect prompt (v2)** with following changes:
  - Added **Core/Satellite split** tied to risk profile:
    - A/B (Conservative/Moderate): 80% Core / 20% Satellite of equities
    - C (Growth): 70% Core / 30% Satellite of equities
    - D (Aggressive): 65% Core / 35% Satellite of equities
  - **Restructured guardrails** into "Always enforced" vs "Risk-adjusted":
    - Single stock cap (5%) and sum=100% are non-negotiable
    - Sector cap flexes from 15% → 20% for C/D users with stated conviction
    - Core requirement: A/B need 65%, C/D need 55%
    - Satellite cap: A/B max 20%, C/D may reach 30-35%
  - Added **Lump Sum Deployment Strategy** section (new output section):
    - Only appears when lump sum >= $10,000
    - Recommends 4-8 weekly installments based on amount
    - Explains DCA benefits and tradeoffs clearly
    - Gives user permission to invest all at once if preferred
  - Added SMH to ETF universe for semiconductor exposure
  - Updated self-audit checklist (now 8 items)
- ✅ **Created PROMPT_ARCHIVE_v2.txt** with full version history
- **Decision**: Kept JSON output format proposal from audit for later - current markdown narrative works well

**January 18, 2026 (continued) - v2 Prompt Testing & PDF Audit**:
- ✅ **Tested v2 prompt with 3 scenarios** - all outputs excellent:
  - **Scenario 1 (Young Tech Worker, Reaction D)**: Core/Satellite split correct (60%/30%), DCA section appeared for $10k, SMH included for semiconductor conviction, honest tradeoff explanations
  - **Scenario 3 (ESG Millennial, Reaction C)**: ESG funds substituted correctly (ESGU, VSGX, ESML), ICLN/PHO for climate conviction, BGRN green bonds instead of BND, 24% satellite within C profile limits
  - **Scenario 8 (Inflation-Anxious Business Owner, Reaction B)**: Heavy TIPS allocation (20%), commodities/energy hedges, business-owner-specific advice (input cost hedging, tax location), 6-week DCA schedule for $50k
- ✅ **v2 prompt validated** - Core/Satellite logic, risk-adjusted guardrails, and DCA section all working as designed
- **PDF Download still failing** - shows "PDF generation encountered an issue" warning
- ✅ **Audited PDF generation code** - identified potential issues (see PDF Error Audit section below)

**January 18, 2026 (continued) - Browser Print Implementation**:
- After 4 failed attempts to fix fpdf2, decided to implement browser print instead
- ✅ **Replaced PDF download with browser print button**:
  - Users press Ctrl+P (or Cmd+P) and save as PDF using browser
  - 100% reliable, works on all platforms
  - Added clear instructions for Windows/Mac/Mobile
- ✅ **Added privacy statement to intro page**:
  - Clarifies no data storage, session-only, developer can't see inputs
  - Mentions AI processes inputs via curated prompts
  - Builds trust for users sharing financial data
- ✅ **Fixed print button** - initial `st.markdown` approach didn't execute JS; switched to `components.html()` with `window.top.print()`
- Added "Future PDF Polish Options" section to CLAUDE.md (weasyprint, reportlab, pdfkit)

**February 3, 2026 - PDF Code Cleanup**:
- ✅ **Removed all fpdf2 code** from WA_backend.py (~350 lines deleted)
- ✅ **Removed fpdf2 from requirements.txt**
- Browser print works cleanly - no need for native PDF generation
- If native PDF is ever needed post-launch, consider weasyprint or reportlab (see Future PDF Polish Options below)

**February 9, 2026 - Pre-Deployment Planning**:
- ✅ **Testing complete** - app working great end-to-end
- **Ready for deployment** - moving to Streamlit Cloud
- Confirmed model usage:
  - **Gemini 3 Pro Preview** for Asset Auditor + Portfolio Architect (quality matters)
  - **Gemini 2.5 Flash** for Risk Translator (fast, cheap)
- Decision: Password-protect app for now (friends/family only)
- Decision: Monitor API costs before scaling to public
- User will familiarize with Google AI Studio quota/billing before deploying

**February 15, 2026 - Rebrand to "The Portfolio Pilot"**:
- ✅ **Renamed app from "Wealth Architect" to "The Portfolio Pilot"**
- Updated all user-facing text in WA_app.py (6 changes)
- Updated AI prompt context in WA_backend.py (2 changes)
- File names remain unchanged (WA_app.py, WA_backend.py) for simplicity
- New branding: Airplane icon (✈️) + tagline "Your AI co-pilot for building a smarter portfolio"
- Ready to commit and push to GitHub

**March 10, 2026 - Deployment to Streamlit Cloud**:
- ✅ **Deployed app to Streamlit Cloud** at https://the-portfolio-pilot.streamlit.app/
- Encountered private repo access issue — Streamlit has OAuth but not GitHub App access
- ✅ **Updated .gitignore** to exclude documentation files before making repo public:
  - CLAUDE.md, PROMPT_ARCHIVE_*.txt, PROMPT_ARCHITECTURE.txt, Prompt_References.md
  - TEST_SCENARIOS.txt, ChatGPT*.txt, wealth_architect_claude_guide*.md, Project_*.txt
- Made repo temporarily public for Streamlit Cloud access
- Added GOOGLE_API_KEY to Streamlit secrets (TOML format, quotes required)
- App successfully deployed and functional

**March 14, 2026 - Post-Feedback Updates (v3 Prompt)**:
- Collected feedback from 4 testers: Enrik, Ron, Birdy, Eric
- ✅ **Added Dividend/Yield Info column** to Holdings Explained table in Portfolio Architect prompt
  - Only populated for income-producing holdings (bond ETFs, SGOV, dividend ETFs)
  - Growth-focused holdings show "N/A — growth-focused"
  - Added beginner-friendly paragraph explaining dividends, DRIP, reinvestment
  - Updated self-audit checklist to verify dividend info included
- ✅ **Added VTI/VEA overlap guardrail** — prompt now prevents recommending both VXUS and VEA together
  - VTI (US-only) and VEA (international developed) have NO overlap — Enrik's concern was unfounded
  - But VXUS includes VEA's territory, so triple-stacking was a valid risk
- ✅ **Cleaned up print/save button** — removed clunky platform instructions, simplified to button + one-line caption
- **UI/UX Theme Design** — researched Streamlit theming capabilities:
  - `.streamlit/config.toml` supports: primaryColor, backgroundColor, secondaryBackgroundColor, textColor, borderColor, linkColor, font, baseRadius
  - CSS injection via `st.markdown(unsafe_allow_html=True)` for advanced styling (fragile across versions)
  - Three palette options proposed: Emerald Money (green), Sky Blue Aviation (blue), Green+Gold Hybrid
  - All share dark background (#0F172A) — user testing on Canva before choosing
- **Codex integration planned** — Claude Code as lead developer, Codex as junior for execution
  - Created AGENTS.md for Codex project context
- **Deferred items**: AI double-read (skip), wild portfolio (skip), mobile (defer), backtesting (future), automated testing (future)
- **Development workflow confirmed**: Local testing via `streamlit run WA_app.py` runs independently from live cloud app. Push to GitHub auto-deploys.

**Next Session**: Choose theme palette, implement config.toml, create PROMPT_ARCHIVE_v3.txt, commit + push + test live.

---

## Deployment Guide (Streamlit Cloud)

### Pre-Deployment Checklist

**⚠️ CRITICAL - Complete BEFORE deploying:**

1. **✅ Check Gemini API Status**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Navigate to **API Keys** section
   - Verify your quota and rate limits:
     - Free tier: 15 RPM, 1M TPM, 1,500 RPD
     - If exceeded, you may need to add billing
   - **Add billing method** (even if staying on free tier - prevents surprise shutdowns)
   - **Set billing alert:**
     - Go to [Google Cloud Console → Billing → Budgets & Alerts](https://console.cloud.google.com/billing)
     - Create budget: $20/month (conservative for friends/family usage)
     - Set alerts at 50%, 90%, 100%

2. **✅ Test App Locally One More Time**
   - Run `streamlit run WA_app.py`
   - Complete full flow (all 7 steps + report generation)
   - Test browser print functionality (Ctrl+P / Cmd+P)
   - Verify all prompts working (Asset Auditor, Risk Translator, Portfolio Architect)

3. **✅ Create GitHub Account** (if you don't have one)
   - Go to [github.com](https://github.com/)
   - Sign up (free tier is fine)
   - Verify email

4. **✅ Prepare Code for Git**
   - Create `.gitignore` file (to exclude secrets)
   - Remove any test files or sensitive data

---

### Step-by-Step Deployment

#### Phase 1: Push to GitHub (30 minutes)

**Step 1.1: Install Git** (if not already installed)
- Windows: Download from [git-scm.com](https://git-scm.com/)
- Mac: Already installed (or use `brew install git`)
- Verify: Run `git --version` in terminal

**Step 1.2: Create .gitignore File**
```bash
# In wealth_architect folder, create .gitignore with this content:
.env
__pycache__/
*.pyc
.DS_Store
*.pdf
test_*.py
```

**Step 1.3: Initialize Git Repository**
```bash
# In terminal, navigate to wealth_architect folder:
cd c:\Users\ericd\OneDrive\Desktop\wealth_architect

# Initialize git
git init

# Add all files (except those in .gitignore)
git add .

# Create first commit
git commit -m "Initial commit - Wealth Architect MVP ready for deployment"
```

**Step 1.4: Create GitHub Repository**
- Go to [github.com/new](https://github.com/new)
- Repository name: `wealth-architect`
- Description: "AI-powered portfolio builder for friends and family"
- **Privacy:** Private (recommended - keeps code hidden)
- **DO NOT** initialize with README, .gitignore, or license (you already have files)
- Click **Create Repository**

**Step 1.5: Push Code to GitHub**
```bash
# Copy the commands GitHub shows you (will look like this):
git remote add origin https://github.com/YOUR-USERNAME/wealth-architect.git
git branch -M main
git push -u origin main

# Enter GitHub credentials when prompted
```

**✅ Checkpoint:** Your code should now be visible on GitHub at `github.com/YOUR-USERNAME/wealth-architect`

---

#### Phase 2: Deploy to Streamlit Cloud (20 minutes)

**Step 2.1: Sign Up for Streamlit Cloud**
- Go to [streamlit.io/cloud](https://streamlit.io/cloud)
- Click **Sign up** or **Get started**
- **Sign in with GitHub** (easiest - auto-connects your repos)
- Authorize Streamlit to access your GitHub account

**Step 2.2: Create New App**
- Click **New app** button
- **Repository:** Select `YOUR-USERNAME/wealth-architect`
- **Branch:** `main`
- **Main file path:** `WA_app.py`
- **App URL:** Choose a custom URL (e.g., `wealth-architect-yourname`)
  - This will be: `https://wealth-architect-yourname.streamlit.app`
- Click **Advanced settings** (IMPORTANT - need to add secrets)

**Step 2.3: Add Secrets (Environment Variables)**
In the **Secrets** section, paste this (replace with your actual API key):

```toml
GOOGLE_API_KEY = "your-actual-gemini-api-key-here"
```

**⚠️ CRITICAL:**
- Get your key from [Google AI Studio → API Keys](https://aistudio.google.com/app/apikey)
- Copy the ENTIRE key (starts with `AIza...`)
- Paste it in quotes exactly as shown above
- DO NOT commit this to GitHub - only add it in Streamlit secrets

**Step 2.4: Deploy!**
- Click **Deploy**
- Streamlit will:
  1. Install dependencies from `requirements.txt`
  2. Run `WA_app.py`
  3. Show build logs in real-time
- **Wait 2-5 minutes** for first deployment

**✅ Checkpoint:** App should be live at your custom URL!

---

#### Phase 3: Add Password Protection (10 minutes)

Since you want to keep this private for now, add a simple password gate.

**Step 3.1: Update WA_app.py**
Add this at the very top of `show_intro()` function (around line 50):

```python
def show_intro():
    # Password gate (optional - remove to make public)
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 Wealth Architect - Access Required")
        password = st.text_input("Enter passphrase:", type="password")
        if st.button("Enter"):
            if password == st.secrets.get("APP_PASSWORD", ""):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect passphrase. Contact the developer for access.")
        st.stop()

    # Original intro content below...
    st.title("💼 The Wealth Architect")
```

**Step 3.2: Add Password to Streamlit Secrets**
- Go to Streamlit Cloud dashboard → Your App → Settings → Secrets
- Update secrets to include password:

```toml
GOOGLE_API_KEY = "your-actual-gemini-api-key-here"
APP_PASSWORD = "choose-a-secure-password"
```

**Step 3.3: Push Update to GitHub**
```bash
# In terminal:
git add WA_app.py
git commit -m "Add password protection for private launch"
git push
```

Streamlit will auto-detect the push and redeploy (~2 minutes).

**✅ Checkpoint:** App now requires password before showing intro page.

---

### Phase 4: Testing & Monitoring (24 hours)

**Step 4.1: Test Live App**
- Visit your app URL: `https://wealth-architect-yourname.streamlit.app`
- Enter password
- Complete full portfolio flow (all 7 steps)
- Test browser print (Ctrl+P)
- Test on mobile (if possible)

**Step 4.2: Monitor API Usage (First 48 Hours)**
- Go to [Google AI Studio → Usage](https://aistudio.google.com/)
- Check requests per day
- Expected usage per portfolio:
  - **Asset Auditor** (Gemini 3 Pro): ~2,500 input + 1,000 output tokens
  - **Risk Translator** (Gemini 2.5 Flash): ~500 input + 200 output tokens
  - **Portfolio Architect** (Gemini 3 Pro): ~3,000 input + 2,000 output tokens
  - **Total per user:** ~6,000-8,000 tokens

**Projected Costs (Gemini API Pricing - Feb 2026):**
- **Gemini 2.5 Flash:** $0.075/1M input, $0.30/1M output
- **Gemini 3 Pro Preview:** Pricing TBD (likely similar to 1.5 Pro: ~$1.25/1M input, $5/1M output)

**Conservative Estimate:**
- 10 portfolios/day × 30 days = 300 portfolios/month
- Cost: ~$5-10/month (depending on Gemini 3 Pro pricing)

**Step 4.3: Share with 2-3 Close Friends**
- Send them the link + password
- Ask for feedback on:
  - Clarity of questions
  - Quality of portfolio output
  - Any bugs or confusion
  - Mobile experience

---

### Phase 5: Go Fully Public (Optional - Post-Feedback)

**If you decide to remove password later:**

1. Remove password gate code from `WA_app.py`
2. Push to GitHub: `git push`
3. Share link publicly

**If you want to keep password but expand access:**
- Share password with trusted users only
- Consider adding usage tracking (see "Optional: Rate Limiting" below)

---

### Optional: Rate Limiting (Prevent Runaway Costs)

If you're worried about costs, add daily usage tracking:

**Add to WA_app.py** (in `generate_report()` function):

```python
# Track portfolios generated today
import datetime

def increment_usage_counter():
    today = datetime.date.today().isoformat()
    if 'usage_date' not in st.session_state or st.session_state.usage_date != today:
        st.session_state.usage_date = today
        st.session_state.portfolios_today = 0

    st.session_state.portfolios_today += 1

    # Daily limit check
    if st.session_state.portfolios_today > 50:
        st.error("Daily portfolio limit reached. Please try again tomorrow.")
        st.stop()

# Call this before generating portfolio:
increment_usage_counter()
```

This caps usage at 50 portfolios/day (~$1-2/day max cost).

---

### Troubleshooting

**Problem: App won't start - "ModuleNotFoundError"**
- **Fix:** Check `requirements.txt` includes all dependencies
- Run locally: `pip freeze > requirements.txt` to capture everything
- Push update to GitHub

**Problem: "Invalid API key" error**
- **Fix:** Check Streamlit secrets formatting (must be valid TOML)
- Verify key copied correctly from Google AI Studio
- Try regenerating API key

**Problem: App is slow to load**
- **Expected:** First load takes 30-60 seconds (Streamlit cold start)
- **After that:** Should be fast (<5 seconds)

**Problem: Session state resets unexpectedly**
- **Cause:** Streamlit Cloud restarts apps after 5 minutes of inactivity
- **Fix:** Normal behavior - users will need to start over if they leave tab idle

**Problem: Hitting rate limits**
- **Cause:** Too many requests to Gemini API
- **Fix:** Add rate limiting (see "Optional: Rate Limiting" above)
- Or upgrade to paid Gemini tier

---

### Cost Monitoring Checklist

**Daily (First Week):**
- [ ] Check Google Cloud billing dashboard
- [ ] Review Gemini API usage in AI Studio
- [ ] Note how many portfolios generated (Streamlit Analytics)

**Weekly (First Month):**
- [ ] Review total API costs
- [ ] Adjust billing alerts if needed
- [ ] Consider rate limiting if costs higher than expected

**Monthly (Ongoing):**
- [ ] Review total spend
- [ ] Decide if usage justifies keeping app public
- [ ] Consider downgrading models if costs too high (e.g., switch Asset Auditor to Flash)

---

### Next Steps After Deployment

1. **Collect Feedback** (1-2 weeks)
   - Get 10-20 real portfolios generated
   - Note common complaints or confusion
   - Track which steps users struggle with

2. **Iterate Based on Feedback** (optional)
   - Polish UX based on real usage
   - Optimize prompts if output quality varies
   - Add features users request most

3. **Scale or Keep Private** (your choice)
   - If costs manageable + feedback positive → go public
   - If costs too high → keep password-protected
   - If not enough usage → consider shutting down to save costs

---

## Quick Reference: Output Structure

The final report should include these sections (from north star + current prompt v3):

1. **PORTFOLIO STRATEGY SUMMARY** - 2-3 paragraphs explaining overall strategy
2. **INITIAL LUMP SUM DEPLOYMENT** - Table: Ticker | Name | Asset Class | Allocation % | $ Amount
3. **LUMP SUM DEPLOYMENT STRATEGY** - *(Only if lump sum >= $10k)* Weekly schedule + DCA explanation + tradeoffs
4. **BIWEEKLY DCA PLAN** - Table: Ticker | Name | Allocation % | $ Per Paycheck
5. **YOUR HOLDINGS EXPLAINED** - Table: Ticker | What It Owns | Why It's In Your Portfolio | Dividend/Yield Info
   - Dividend column only populated for income-producing holdings; "N/A — growth-focused" for others
   - Followed by beginner-friendly paragraph explaining dividends and DRIP
6. **WHY THIS PORTFOLIO WORKS FOR YOU** - 4-6 personalized bullet points
7. **IMPLEMENTATION TIPS** - Plain-language automation, quarterly check-ins, keep it simple

**Guardrails (v3 - Risk-Adjusted):**
- No single stock > 5% of total portfolio (non-negotiable)
- Sector cap: 15% default, flexes to 20% for C/D users with conviction
- Core requirement: A/B need 65%, C/D need 55% in broad-market ETFs
- Satellite cap: A/B max 20%, C/D may reach 30-35%
- Allocation percentages must sum to exactly 100%
- VXUS and VEA must not both appear in the same portfolio (overlap)

**Core/Satellite Split (within equities):**
- A/B users: 80% Core / 20% Satellite
- C users: 70% Core / 30% Satellite
- D users: 65% Core / 35% Satellite

---

## PDF Error Audit (January 18, 2026)

### Current Behavior
- PDF generation fails with generic "PDF generation encountered an issue" warning
- Report still displays correctly in browser (failsafe working)
- Error is caught silently in try/except block (no detailed logging)

### Likely Root Causes (in order of probability)

1. **Unicode Encoding (P0 - Most Likely)**
   - `fpdf2` uses Latin-1 encoding by default
   - Gemini output may contain: curly quotes (`'` `"`), em-dashes (`—`), or special characters
   - These crash PDF generation silently
   - **Fix**: Sanitize text with `.encode('latin-1', 'replace').decode('latin-1')` before rendering

2. **Table Cell Truncation (P1)**
   - Current code truncates cells to 25 characters: `cell[:25] + '...'`
   - "Vanguard Total Stock Market" (26 chars) gets cut off
   - "Holdings Explained" table has long descriptions that get lost
   - **Fix**: Increase truncation limit or use dynamic column widths

3. **Bold Sub-headers Not Handled (P1)**
   - New DCA section has `**Your Recommended Schedule:**` style sub-headers
   - Current `_clean_markdown_formatting()` strips bold but doesn't render them styled
   - **Fix**: Detect `**text:**` pattern and render as bold paragraph

4. **No Error Logging (P2)**
   - Current except block: `st.warning(f"PDF generation encountered an issue.")`
   - Doesn't print actual exception
   - **Fix**: Add `print(f"PDF Error: {e}")` or `st.warning(f"PDF Error: {e}")`

### Files to Edit
- `WA_backend.py`: Lines 409-680 (PDF generation functions)
- `WA_app.py`: Lines 606-621 (PDF error handling)

### Proposed Fixes (Prioritized)

| Priority | Issue | Fix Location | Change |
|----------|-------|--------------|--------|
| P0 | Unicode crash | `_render_table()`, `_render_section()` | Add Latin-1 sanitization to all text before `pdf.cell()` / `pdf.multi_cell()` |
| P1 | Table truncation | `_render_table()` line 664 | Increase from 25 to 35 chars, or use `multi_cell` for long content |
| P1 | Bold sub-headers | `_render_section()` | Detect `**text:**` and render with bold font before stripping |
| P2 | Error logging | `WA_app.py` line 621 | Change to `st.warning(f"PDF Error: {e}")` |

### Testing Plan
1. Add error logging first to confirm root cause
2. Fix Unicode sanitization
3. Test with Scenario 1 output (has curly quotes in "you're comfortable")
4. If still failing, address table truncation

### PDF Fix Attempts Log

**Attempt 1 (Failed):**
- Added `_sanitize_for_pdf()` function for Unicode → Latin-1 conversion
- Increased truncation from 25→35 chars
- **Error**: "Not enough horizontal space to render a single character"
- **Root Cause**: Tables with 5 columns (180px / 5 = 36px per col) combined with 35-char truncation overflows at 9pt font
- **Lesson**: Truncation limit must scale inversely with column count

**Attempt 2 (Failed):**
- Added dynamic font size and truncation based on column count:
  - 5+ columns: 7pt font, 18 char max
  - 4 columns: 8pt font, 22 char max
  - 3 or fewer: 9pt font, 30 char max
- **Error**: Same "Not enough horizontal space" error
- **Root Cause**: fpdf2 `c_margin` (cell margin) defaults to 1mm per side, eating into available width

**Attempt 3 (Failed):**
- Reduced `c_margin` from 1.0 to 0.5mm
- Further reduced font sizes and char limits:
  - 5+ columns: 6pt font, 14 char max, 10 char header
  - 4 columns: 7pt font, 18 char max, 12 char header
  - 3 or fewer: 9pt font, 28 char max, 18 char header
- Added minimum column width check (15mm) - raises exception if too narrow
- Added try/except around `_render_table()` call - if table fails, renders as plain text fallback
- **Error**: Same "Not enough horizontal space" error persists
- **Root Cause**: Error is happening OUTSIDE of table rendering (try/except didn't catch it), possibly in title page, section headers, or somewhere else

**Attempt 4 (Failed):**
- **Key insight**: Error was happening OUTSIDE table rendering - in header and title page
- Fixed header line boundary: `line(10, 18, 200, 18)` → `line(15, 18, 195, 18)` (was extending past right margin)
- Wrapped title page summary box in try/except with fallback
- Added `ln=True` to title page cells to ensure proper cursor reset
- Truncated formatted numbers to 15 chars max to prevent overflow
- **Error**: Same "Not enough horizontal space" error still occurs
- **Conclusion**: fpdf2 is too fragile for our use case. The error could be coming from anywhere in the rendering pipeline and is extremely difficult to diagnose.

### What NOT to Do (Lessons Learned)
- Don't increase truncation limit without considering column count
- Don't use fixed font sizes for all table types
- Don't ignore `c_margin` - it eats 2mm total per cell by default
- Don't extend lines past page margins (header line was going to x=200, margin was 195)
- Always add `ln=True` to last cell in a row
- fpdf2 will crash if text width > cell width, even by 1 pixel

### Sources
- [fpdf2 GitHub Issue #1250](https://github.com/py-pdf/fpdf2/issues/1250) - CJK font space issue
- [fpdf2 Tables Documentation](https://py-pdf.github.io/fpdf2/Tables.html) - Table rendering options

---

## PDF Generation - Next Steps (January 18, 2026)

After 4 failed attempts to fix fpdf2, it's clear the library is too fragile for our use case. The "not enough horizontal space" error is extremely difficult to diagnose and could be coming from anywhere in the rendering pipeline.

### Option 1: Browser Print (RECOMMENDED - Fastest)
**Effort**: 5 minutes
**Reliability**: 100% (uses browser's native print-to-PDF)

Replace the "Download PDF" button with a "Print Report" button that opens the browser print dialog. Users can save as PDF using their browser.

**Pros:**
- Zero code changes to PDF generation (remove it entirely)
- Works on all browsers
- Better formatting control (can use CSS print media queries)
- No dependencies

**Cons:**
- Slightly less convenient (extra click to save as PDF)
- User needs to know how to print to PDF

**Implementation:**
```python
# In WA_app.py, replace PDF button with:
st.markdown("""
    <script>
    function printReport() {
        window.print();
    }
    </script>
    <button onclick="printReport()">🖨️ Print Report (Save as PDF)</button>
""", unsafe_allow_html=True)
```

### Option 2: Switch to weasyprint
**Effort**: 2-3 hours (complete rewrite of PDF generation)
**Reliability**: High (uses HTML/CSS, easier to debug)

Replace fpdf2 with weasyprint, which converts HTML/CSS to PDF.

**Pros:**
- HTML/CSS is much easier to work with than fpdf2's API
- Better rendering quality
- Supports modern web features

**Cons:**
- Requires external dependencies (Cairo, Pango, GDK-Pixbuf on Windows)
- Larger install size
- Needs HTML template creation

### Option 3: Switch to reportlab
**Effort**: 3-4 hours (similar API to fpdf2 but more complex)
**Reliability**: High (industry standard, mature library)

**Pros:**
- Very mature, battle-tested
- Extensive documentation
- Fine-grained control

**Cons:**
- Steep learning curve
- More verbose API than fpdf2
- Still low-level (similar issues possible)

### Option 4: Keep Trying fpdf2
**Effort**: Unknown (could be hours of debugging)
**Reliability**: Low (4 attempts already failed)

Continue debugging fpdf2 to find the exact source of the error.

**Cons:**
- Time sink with uncertain outcome
- Even if we fix this error, another could appear
- Library seems fundamentally incompatible with our use case

---

**RECOMMENDATION:** Go with **Option 1 (Browser Print)** for MVP launch. It's the fastest, most reliable solution. Can always revisit weasyprint post-launch if users demand native PDF download.

---

## Browser Print Implementation (January 18, 2026)

✅ **Implemented Option 1 (Browser Print)**

**Changes Made:**
- Replaced PDF download button with browser print button in [WA_app.py:604-625](WA_app.py#L604-L625)
- Added instructions for Windows/Mac/Mobile users on how to save as PDF
- Button triggers `window.print()` which opens native browser print dialog
- Users select "Save as PDF" as destination in their browser

**Privacy Statement Added:**
- Added privacy info box on intro page before disclaimer
- Clarifies: no storage, session-only, developer can't see inputs, AI processes via curated prompts
- Builds user trust for sharing financial data

**Print Button Fix (January 18, 2026):**
- Initial implementation using `st.markdown` with `unsafe_allow_html=True` didn't work - Streamlit sanitizes scripts
- Fixed by using `streamlit.components.v1.html()` which creates an iframe that properly executes JavaScript
- Button calls `window.top.print()` to print the parent page (not the iframe)

**Next Step:**
- Test browser print functionality
- If testing confirms it works cleanly, **remove PDF generation code** from [WA_backend.py:350-700](WA_backend.py#L350-L700) to lighten the codebase
- This includes: `WealthArchitectPDF` class, `generate_pdf_report()`, and all helper functions (`_parse_markdown_sections`, `_render_section`, `_render_table`, etc.)

---

## Future PDF Polish Options (Post-Launch)

If native PDF download is desired in the future, consider these alternatives to fpdf2:

### Option A: weasyprint (RECOMMENDED)
- **What it does**: Converts HTML/CSS to PDF
- **Pros**: Easy styling with CSS, high-quality output, modern features
- **Cons**: Requires system dependencies (Cairo, Pango, GDK-Pixbuf on Windows)
- **Install**: `pip install weasyprint` + system deps
- **Effort**: 2-3 hours to rewrite PDF generation
- **Best for**: Clean, styled PDFs without fighting low-level APIs

### Option B: reportlab
- **What it does**: Low-level PDF generation (industry standard)
- **Pros**: Very mature, battle-tested, fine-grained control
- **Cons**: Steep learning curve, verbose API, similar issues to fpdf2 possible
- **Install**: `pip install reportlab`
- **Effort**: 3-4 hours to rewrite PDF generation
- **Best for**: Complex layouts requiring precise control

### Option C: pdfkit + wkhtmltopdf
- **What it does**: Wraps wkhtmltopdf binary to convert HTML to PDF
- **Pros**: Simple API, just pass HTML string
- **Cons**: Requires wkhtmltopdf binary installed on server (deployment complexity)
- **Install**: `pip install pdfkit` + wkhtmltopdf binary
- **Effort**: 1-2 hours
- **Best for**: Quick solution if binary can be installed on deployment target

**Recommendation**: weasyprint is the best balance of quality and ease of use. Browser print is fine for MVP launch.
