# Run with: streamlit run WA_app.py

import streamlit as st
import streamlit.components.v1 as components
import WA_backend as backend
import plotly.express as px
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="The Portfolio Pilot",
    page_icon="✈️",
    layout="centered"
)

# --- SESSION STATE INITIALIZATION ---
if 'current_step' not in st.session_state:
    st.session_state['current_step'] = 0  # Start at intro page

# User inputs stored across steps
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {
        'age': 30,
        'state': '',
        'has_emergency_fund': None,
        'has_high_interest_debt': None,
        'debt_details': '',
        'current_assets_text': '',
        'audit_result': None,
        'lump_sum': 0,
        'biweekly_income': 0,
        'risk_reaction': '',
        'risk_result': None,
        'has_sector_tilt': None,
        'sector_tilt_text': '',
        'final_corrections': '',
        'final_report': None,
        'portfolio_json': None
    }

TOTAL_STEPS = 7

# --- HELPER FUNCTIONS ---
def next_step():
    if st.session_state['current_step'] < TOTAL_STEPS + 1:  # +1 for report page
        st.session_state['current_step'] += 1

def prev_step():
    if st.session_state['current_step'] > 0:
        st.session_state['current_step'] -= 1

def go_to_report():
    st.session_state['current_step'] = TOTAL_STEPS + 1

def render_progress():
    """Show step indicator (only for steps 1-7, not intro)"""
    step = st.session_state['current_step']
    if 1 <= step <= TOTAL_STEPS:
        st.markdown(f"**Step {step} of {TOTAL_STEPS}**")
        st.progress(step / TOTAL_STEPS)
        st.markdown("---")

# --- HEADER ---
st.title("✈️ The Portfolio Pilot")
st.markdown("*Your AI co-pilot for building a smarter portfolio.*")

# --- STEP RENDERING ---
step = st.session_state['current_step']

# ==========================================
# STEP 0: WELCOME / INTRO PAGE
# ==========================================
if step == 0:
    st.markdown("---")

    st.markdown("""
    ### What This Is

    This tool helps you build a **real, long-term investment plan** that you can feel good about.
    The goal is to educate you on *why* and *what* you're investing in, not just give you a list of tickers.

    **The strategy is built on proven ideas:**
    - No hype, no guessing, no trying to "time the market"
    - Low-cost, diversified index funds as the foundation
    - Personalized based on your risk tolerance and goals
    - Designed to grow in the background without daily stress
    """)

    st.markdown("""
    ### What This Isn't

    This is your **core wealth-building engine** - not a get-rich-quick scheme.

    Want to keep some "casino money" on the side to chase meme stocks or crypto? That's fine -
    just track it separately. Think of *this* portfolio as the stable foundation that keeps
    growing while you sleep.
    """)

    st.info("""
    **The Goal:** Build a balanced portfolio that, over the long haul, should outperform
    letting your money sit in a savings account or even a basic S&P 500 fund - with
    diversification that helps you weather the storms.
    """)

    st.markdown("""
    ### How to Get the Most Out of This

    1. **Be thorough with your answers** - especially about your current assets
    2. **Be honest about risk tolerance** - the best portfolio is one you can actually stick with
    3. **Share your convictions** - if you believe in specific companies or sectors, tell us why
    4. **This is a starting point** - you can always adjust allocations later based on how it feels

    *The whole process takes about 5 minutes.*
    """)

    st.markdown("---")

    st.info("""
    **Your Privacy:**
    - Your data is **not stored** - it only exists during this session
    - Your inputs are processed by AI using curated investment prompts
    - The developer of this tool **cannot see your inputs**
    - When you close this page, your data is gone
    - No account, no tracking, no database
    """)

    st.warning("""
    **Disclaimer:** This is not investment advice. Invest at your own risk.
    Past performance doesn't guarantee future results. This tool is for educational purposes
    to help you think through your investment strategy. When in doubt, consult a licensed
    financial advisor.
    """)

    st.markdown("")
    if st.button("Let's Build Your Portfolio →", type="primary", key="start_button"):
        next_step()
        st.rerun()

# ==========================================
# STEP 1: THE BASICS
# ==========================================
elif step == 1:
    render_progress()
    st.header("Let's Start With the Basics")
    st.markdown("""
    First, we need to understand your timeline and location. Your age helps determine
    how aggressive your portfolio can be, and your state helps with tax considerations.
    """)

    st.session_state['user_data']['age'] = st.slider(
        "What is your age?",
        min_value=18,
        max_value=80,
        value=st.session_state['user_data']['age']
    )

    st.session_state['user_data']['state'] = st.text_input(
        "What state do you live in?",
        value=st.session_state['user_data']['state'],
        placeholder="e.g., California, Texas, New York"
    )

    st.markdown("")
    if st.button("Next →", type="primary", key="step1_next"):
        next_step()
        st.rerun()

# ==========================================
# STEP 2: FINANCIAL FOUNDATION
# ==========================================
elif step == 2:
    render_progress()
    st.header("Your Financial Foundation")
    st.markdown("""
    Before we build your investment portfolio, let's make sure your foundation is solid.
    These two factors are critical to understand before putting money into the market.
    """)

    st.subheader("Emergency Fund")
    st.markdown("Do you have 3-6 months of living expenses saved in an easily accessible account (like a savings account)?")

    emergency_fund = st.radio(
        "Emergency Fund Status",
        options=["Yes, I have an emergency fund", "No, I'm still building it"],
        index=0 if st.session_state['user_data']['has_emergency_fund'] == True else
              1 if st.session_state['user_data']['has_emergency_fund'] == False else 0,
        key="emergency_fund_radio",
        label_visibility="collapsed"
    )
    st.session_state['user_data']['has_emergency_fund'] = (emergency_fund == "Yes, I have an emergency fund")

    st.markdown("---")

    st.subheader("High-Interest Debt")
    st.markdown("Do you have any high-interest debt (credit cards, personal loans with 15%+ APR)?")

    has_debt = st.radio(
        "High-Interest Debt Status",
        options=["No high-interest debt", "Yes, I have some high-interest debt"],
        index=1 if st.session_state['user_data']['has_high_interest_debt'] == True else 0,
        key="debt_radio",
        label_visibility="collapsed"
    )
    st.session_state['user_data']['has_high_interest_debt'] = (has_debt == "Yes, I have some high-interest debt")

    # Show warning if they have debt (advisory, not blocker)
    if st.session_state['user_data']['has_high_interest_debt']:
        st.warning("""
        **Financial Tip:** It's highly recommended that you pay off high-interest debt first.
        Any gains made in the stock market are most likely not going to beat the 20-30% interest
        loss on credit card debt. We'll proceed assuming this is being taken care of separately.
        """)
        st.session_state['user_data']['debt_details'] = st.text_input(
            "Briefly describe your debt situation (optional):",
            value=st.session_state['user_data']['debt_details'],
            placeholder="e.g., $5k on a credit card at 24% APR"
        )

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="step2_back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="step2_next"):
            next_step()
            st.rerun()

# ==========================================
# STEP 3: CURRENT ASSETS
# ==========================================
elif step == 3:
    render_progress()
    st.header("Your Current Assets")
    st.markdown("""
    Tell us about your current investable assets. This helps us understand what you're
    working with and identify anything that might need to be consolidated or repositioned.

    **Include things like:**
    - Cash in savings/checking accounts (beyond your emergency fund)
    - Existing investments in taxable brokerage accounts (stocks, ETFs, crypto)
    - Any other liquid assets you want to put to work

    *Note: We're focused on non-retirement investing here. Your 401(k) and IRA are great
    for retirement - we'll touch on those in your report - but this portfolio is for
    wealth building outside of those tax-advantaged accounts.*
    """)

    st.session_state['user_data']['current_assets_text'] = st.text_area(
        "Describe your current assets:",
        value=st.session_state['user_data']['current_assets_text'],
        height=150,
        placeholder="Example: I have $15k in a savings account earning 4%, $3k in an old 401k from a previous job, $2k in random stocks on Robinhood (mostly AAPL and some NVIDIA), and about $500 in Bitcoin."
    )

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="step3_back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="step3_next"):
            # Run audit on assets
            if st.session_state['user_data']['current_assets_text']:
                with st.spinner("Analyzing your assets..."):
                    audit_result = backend.audit_assets(
                        st.session_state['user_data']['current_assets_text']
                    )
                    st.session_state['user_data']['audit_result'] = audit_result
            next_step()
            st.rerun()

# ==========================================
# STEP 4: THE NUMBERS
# ==========================================
elif step == 4:
    render_progress()
    st.header("The Numbers")
    st.markdown("""
    Now let's get specific about what you're investing. This is for **non-retirement
    investing** - money outside of your 401(k) and IRA that you want to put to work
    in a taxable brokerage account.
    """)

    st.subheader("Initial Investment")
    st.markdown("How much do you have available to invest as a lump sum right now? *(Round to whole dollars)*")

    col_dollar1, col_input1 = st.columns([0.1, 0.9])
    with col_dollar1:
        st.markdown("### $")
    with col_input1:
        lump_sum_str = st.text_input(
            "Lump Sum Amount",
            value=str(st.session_state['user_data']['lump_sum']) if st.session_state['user_data']['lump_sum'] > 0 else "",
            placeholder="10000",
            key="lump_sum_input",
            label_visibility="collapsed"
        )
        # Parse the input
        if lump_sum_str:
            cleaned = lump_sum_str.replace(",", "").replace("$", "").strip()
            if "." in cleaned:
                st.error("Please enter a whole number (no decimals). Round to the nearest dollar.")
                st.session_state['user_data']['lump_sum'] = 0
            else:
                try:
                    st.session_state['user_data']['lump_sum'] = int(cleaned)
                except ValueError:
                    st.session_state['user_data']['lump_sum'] = 0
        else:
            st.session_state['user_data']['lump_sum'] = 0

    st.markdown("---")

    st.subheader("Recurring Investment")
    st.markdown("""
    How much can you invest every two weeks (per paycheck)? *(Round to whole dollars)*

    This is your dollar-cost averaging engine that builds wealth over time.
    """)

    with st.expander("How do I calculate this?"):
        st.markdown("""
        **Simple formula:**
        1. Take your monthly take-home pay
        2. Subtract your fixed bills (rent, utilities, subscriptions, etc.)
        3. Subtract your "play money" (dining, entertainment, shopping)
        4. What's left is your investable surplus
        5. Divide by 2 for your biweekly amount

        *Example: $5,000 paycheck - $2,500 bills - $1,000 fun money = $1,500 surplus → $750 biweekly*
        """)

    col_dollar2, col_input2 = st.columns([0.1, 0.9])
    with col_dollar2:
        st.markdown("### $")
    with col_input2:
        biweekly_str = st.text_input(
            "Biweekly Amount",
            value=str(st.session_state['user_data']['biweekly_income']) if st.session_state['user_data']['biweekly_income'] > 0 else "",
            placeholder="500",
            key="biweekly_input",
            label_visibility="collapsed"
        )
        # Parse the input
        if biweekly_str:
            cleaned = biweekly_str.replace(",", "").replace("$", "").strip()
            if "." in cleaned:
                st.error("Please enter a whole number (no decimals). Round to the nearest dollar.")
                st.session_state['user_data']['biweekly_income'] = 0
            else:
                try:
                    st.session_state['user_data']['biweekly_income'] = int(cleaned)
                except ValueError:
                    st.session_state['user_data']['biweekly_income'] = 0
        else:
            st.session_state['user_data']['biweekly_income'] = 0

    if st.session_state['user_data']['biweekly_income'] > 0:
        monthly = st.session_state['user_data']['biweekly_income'] * 2
        yearly = monthly * 12
        st.success(f"That's **\\${monthly:,}/month** or **\\${yearly:,}/year** going toward your future.")

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="step4_back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="step4_next"):
            next_step()
            st.rerun()

# ==========================================
# STEP 5: RISK PROFILE
# ==========================================
elif step == 5:
    render_progress()
    st.header("Your Risk Profile")
    st.markdown("""
    This helps us understand your psychological comfort with market volatility.
    There's no right or wrong answer - we just need to build a portfolio you can stick with.
    """)

    st.markdown("---")
    st.markdown("### The Scenario")
    st.markdown(
        "**Imagine this:** You invest **\\$10,000**. One year later, the market has a rough patch "
        "and your portfolio is now worth only **\\$7,000** (a 30% drop)."
    )
    st.markdown("")
    st.markdown("**What is your gut reaction?**")

    reactions = [
        "A) Sell everything immediately. I can't stomach losing more.",
        "B) Sell some to reduce risk, but keep the rest invested.",
        "C) Do nothing. I understand markets recover and I'm in this for the long haul.",
        "D) Buy more while prices are low. This is a discount!"
    ]

    # Find current index
    current_reaction = st.session_state['user_data']['risk_reaction']
    current_index = 0
    if current_reaction in reactions:
        current_index = reactions.index(current_reaction)

    st.session_state['user_data']['risk_reaction'] = st.radio(
        "Select your honest reaction:",
        options=reactions,
        index=current_index,
        key="risk_radio",
        label_visibility="collapsed"
    )

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="step5_back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="step5_next"):
            # Get risk analysis
            with st.spinner("Analyzing your risk profile..."):
                risk_result = backend.get_risk_analysis(
                    st.session_state['user_data']['age'],
                    st.session_state['user_data']['risk_reaction']
                )
                st.session_state['user_data']['risk_result'] = risk_result
            next_step()
            st.rerun()

# ==========================================
# STEP 6: MARKET PERSPECTIVE & CONVICTIONS
# ==========================================
elif step == 6:
    render_progress()
    st.header("Your Market Perspective")
    st.markdown("""
    Most of your portfolio will be diversified index funds - that's the foundation.
    But this is your chance to share any **strong beliefs** about specific companies,
    sectors, or market conditions. We'll factor these into your portfolio where appropriate.
    """)

    st.markdown("""
    **Things to consider sharing:**
    - Sectors you're bullish on based on your work or expertise
    - Specific companies you have high conviction in (and why)
    - Areas you want to *avoid* (ethical reasons, risk concerns, gut feeling)
    - General thoughts on where the market is heading
    """)

    has_convictions = st.radio(
        "Do you have any market convictions or preferences to share?",
        options=[
            "No, just build me a standard diversified portfolio",
            "Yes, I have some thoughts I'd like to share"
        ],
        index=1 if st.session_state['user_data']['has_sector_tilt'] == True else 0,
        key="convictions_radio"
    )
    st.session_state['user_data']['has_sector_tilt'] = (has_convictions == "Yes, I have some thoughts I'd like to share")

    if st.session_state['user_data']['has_sector_tilt']:
        with st.expander("See examples of what to write"):
            st.markdown("""
            **Sector expertise:**
            > *"I work heavily with AI in a corporate environment. I see how fast companies
            > are adopting these tools and I'm very bullish on the AI/semiconductor space
            > for the next decade."*

            **Individual stock conviction:**
            > *"I really believe in Google. I know from academia that they have an absurd
            > concentration of software PhDs and do a great job attracting top talent. I think
            > their AI is winning and they don't even NEED AI to be profitable. I'd like some
            > GOOGL exposure if possible."*

            **Ethical/ESG preferences:**
            > *"I don't want to invest in 'sin stocks' - no tobacco, weapons manufacturers,
            > or private prisons. I'd prefer ESG-friendly options where possible."*

            **Market sentiment:**
            > *"I think tech is overvalued right now and would prefer a more defensive
            > allocation. Also interested in international exposure since I think the US
            > has had too long of a run."*
            """)

        st.session_state['user_data']['sector_tilt_text'] = st.text_area(
            "Share your market perspective:",
            value=st.session_state['user_data']['sector_tilt_text'],
            height=150,
            placeholder="What are your convictions? Any sectors, companies, or trends you believe in? Anything you want to avoid?"
        )

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="step6_back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="step6_next"):
            next_step()
            st.rerun()

# ==========================================
# STEP 7: REVIEW & GENERATE
# ==========================================
elif step == 7:
    render_progress()
    st.header("Review & Generate Your Plan")
    st.markdown("Here's a summary of everything you've told us. Review it and make any corrections below.")

    st.markdown("---")

    # Summary
    ud = st.session_state['user_data']

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Basics**")
        st.markdown(f"- Age: {ud['age']}")
        st.markdown(f"- State: {ud['state'] or 'Not specified'}")

        st.markdown("**Foundation**")
        ef_status = "Yes" if ud['has_emergency_fund'] else "No"
        debt_status = "Yes" if ud['has_high_interest_debt'] else "No"
        st.markdown(f"- Emergency Fund: {ef_status}")
        st.markdown(f"- High-Interest Debt: {debt_status}")

    with col2:
        st.markdown("**The Numbers**")
        st.markdown(f"- Lump Sum: ${ud['lump_sum']:,}")
        st.markdown(f"- Biweekly: ${ud['biweekly_income']:,}")

        st.markdown("**Risk Profile**")
        reaction_short = ud['risk_reaction'][:1] if ud['risk_reaction'] else "Not set"
        st.markdown(f"- Reaction: {reaction_short}")

        st.markdown("**Sector Tilt**")
        tilt_status = "Yes" if ud['has_sector_tilt'] else "No"
        st.markdown(f"- Has Tilt: {tilt_status}")

    if ud['current_assets_text']:
        st.markdown("**Current Assets**")
        st.markdown(f"> {ud['current_assets_text'][:200]}{'...' if len(ud['current_assets_text']) > 200 else ''}")

    if ud['has_sector_tilt'] and ud['sector_tilt_text']:
        st.markdown("**Sector Conviction**")
        st.markdown(f"> {ud['sector_tilt_text'][:200]}{'...' if len(ud['sector_tilt_text']) > 200 else ''}")

    st.markdown("---")

    st.subheader("Any Corrections?")
    st.markdown("If anything above is wrong or you want to add context, note it here:")
    st.session_state['user_data']['final_corrections'] = st.text_area(
        "Corrections or additional context (optional):",
        value=st.session_state['user_data']['final_corrections'],
        height=80,
        placeholder="e.g., Actually my lump sum is $12k not $10k, or I forgot to mention I also have a Roth IRA...",
        label_visibility="collapsed"
    )

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="step7_back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Generate My Portfolio 🚀", type="primary", key="step7_generate"):
            with st.spinner("Building your personalized portfolio... This may take a moment."):
                # Compile all user data and generate final report
                final_report = backend.generate_final_plan(
                    st.session_state['user_data']
                )
                st.session_state['user_data']['final_report'] = final_report
                # For now, portfolio_json would come from backend
                # st.session_state['user_data']['portfolio_json'] = ...
            go_to_report()
            st.rerun()

# ==========================================
# FINAL REPORT PAGE
# ==========================================
elif step == TOTAL_STEPS + 1:
    # Force scroll to top of page
    st.markdown('<div id="top"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        /* Scroll to top on page load */
        </style>
        <script>
        window.scrollTo(0, 0);
        </script>
        """,
        unsafe_allow_html=True
    )

    st.header("Your Portfolio Pilot Report")

    ud = st.session_state['user_data']

    # Display the final report FIRST (always show this)
    if ud['final_report']:
        st.markdown(ud['final_report'])
    else:
        st.error("No report generated. Please go back and complete all steps.")

    st.markdown("---")

    # Save/Print Instructions
    if ud['final_report']:
        st.markdown("""
        **Save Your Report:**
        To save this report as a PDF, use your browser's print function:
        - **Windows/Chrome:** Press `Ctrl+P` → Select "Save as PDF" as the destination
        - **Mac/Safari:** Press `Cmd+P` → Click "PDF" dropdown → "Save as PDF"
        - **Mobile:** Use your browser's share menu → "Print" → "Save as PDF"
        """)

        # Print button using components.html (executes JS properly)
        components.html("""
            <button onclick="window.top.print()" style="
                background-color: #FF4B4B;
                color: white;
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.5rem;
                font-size: 1rem;
                cursor: pointer;
                font-weight: 500;
            ">🖨️ Print / Save as PDF</button>
        """, height=50)

    # TODO: Once backend returns JSON, render pie chart and tables here
    # Example pie chart placeholder (will be driven by portfolio_json):
    # if ud['portfolio_json']:
    #     df = pd.DataFrame(ud['portfolio_json']['portfolio'])
    #     fig = px.pie(df, values='allocation_pct', names='ticker', title='Portfolio Allocation')
    #     st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Tax & Disclaimer Section
    st.subheader("Tax Considerations")
    st.markdown("""
    - **Long-term vs Short-term Gains:** Investments held over 1 year qualify for lower long-term capital gains tax rates (0%, 15%, or 20% depending on income). Investments sold within 1 year are taxed as ordinary income.
    - **Tax-Advantaged Accounts:** Consider maxing out 401(k) and IRA contributions before investing in taxable brokerage accounts.
    - **Bond Fund Taxation:** Interest from bond funds (like SGOV, SCHP) is typically taxed as ordinary income.
    - **Consult a Professional:** For personalized tax advice, consult a CPA or tax advisor.
    """)

    st.subheader("Important Disclaimer")
    st.warning("""
    **This is educational content, not investment advice.** Past performance does not guarantee
    future results. All investments carry risk, including potential loss of principal.
    This tool is designed to help you think through your investment strategy, but you should
    consult with a licensed financial advisor before making investment decisions.
    Invest at your own risk.
    """)

    st.markdown("---")

    st.subheader("What's Next?")
    st.markdown("""
    **This portfolio is a starting point, not a set-it-and-forget-it answer.**

    Here are some ways to keep building on this foundation:
    """)

    with st.expander("Get a Second Opinion"):
        st.markdown("""
        Consider auditing this portfolio with another AI for a different perspective.

        **Pro tip:** Use the latest high-performance reasoning models for more thoughtful, nuanced analysis:
        - **OpenAI GPT-5.2** (Thinking mode for complex reasoning)
        - **Google Gemini 3 Pro** (state-of-the-art reasoning and multimodal understanding)
        - **Anthropic Claude Opus 4.6** (excellent for detailed financial analysis)

        These models excel at catching edge cases and providing detailed explanations.

        Just describe your situation, share the portfolio, and ask if they see any blind spots
        or have alternative suggestions.
        """)

    with st.expander("Adjust as Needed"):
        st.markdown("""
        If this portfolio feels too conservative or too aggressive after reviewing it, that's
        useful information. You can:
        - Shift weight from broad ETFs (VOO/VTI) into specific sectors
        - Add or remove positions based on your comfort level
        - Ask follow-up questions about specific tickers or alternatives
        """)

    with st.expander("Treat This as a Living Document"):
        st.markdown("""
        Your portfolio should evolve with you.

        **Make it easy to revisit:** Save this portfolio in a ChatGPT Project folder or Gemini
        Gem. That way, the AI remembers your goals, risk profile, and holdings - so future
        conversations build on this foundation instead of starting from scratch.

        **Check in quarterly:** Take a quick look at your allocations. If something's drifted
        significantly or you want to add exposure to a new sector, use AI to research it first.
        A few minutes of AI-assisted research can make your moves more methodical and informed.

        **Adjust for life changes:** New job, marriage, house purchase - these all affect your
        risk tolerance and timeline. Update your AI project folder when big things change.
        """)

    st.markdown("---")

    # Option to start over
    if st.button("Start Over", key="start_over"):
        st.session_state['current_step'] = 0
        st.session_state['user_data'] = {
            'age': 30,
            'state': '',
            'has_emergency_fund': None,
            'has_high_interest_debt': None,
            'debt_details': '',
            'current_assets_text': '',
            'audit_result': None,
            'lump_sum': 0,
            'biweekly_income': 0,
            'risk_reaction': '',
            'risk_result': None,
            'has_sector_tilt': None,
            'sector_tilt_text': '',
            'final_corrections': '',
            'final_report': None,
            'portfolio_json': None
        }
        st.rerun()
