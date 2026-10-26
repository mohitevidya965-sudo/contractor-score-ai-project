import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Contractor-Score AI Framework",
    page_icon="🏗️",
    layout="wide"
)

# 2. Header Section
st.title("🏗️ Contractor-Score AI Framework")
st.caption("Municipal Infrastructure Public Procurement Risk Predictor")

# 3. Load Data & Calculate Risk Metrics
@st.cache_data
def load_data():
    return pd.read_csv("contractors.csv")

try:
    df = load_data()

    # Dynamic Scoring & Risk Flagging
    def calculate_vendor_score(row):
        delay_pct = max(0, row['avg_delay_pct'])
        timeline_score = max(0, 40 - (delay_pct * 0.8))
        
        overrun_pct = max(0, row['avg_overrun_pct'])
        budget_score = max(0, 48 - (overrun_pct * 0.96))
        
        active_proj = row['active_projects']
        cap_score = 12 if active_proj <= 3 else (8 if active_proj <= 5 else 4)
        
        total_score = round(timeline_score + budget_score + cap_score, 2)
        return total_score

    def classify_risk(score):
        if score >= 75:
            return "LOW_RISK"
        elif score >= 50:
            return "MEDIUM_RISK"
        else:
            return "HIGH_RISK"

    df['vendor_score'] = df.apply(calculate_vendor_score, axis=1)
    df['risk_tier'] = df['vendor_score'].apply(classify_risk)
    df['risk_score_pct'] = round(100 - df['vendor_score'], 2)

    # 4. Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview & Risk Metrics", 
        "🔍 Contractor Lookup", 
        "🎯 Tender Bidding Simulator",
        "📋 Raw Data & Export"
    ])

    # TAB 1: Overview & Risk Metrics
    with tab1:
        st.subheader("Key Portfolio Indicators")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Contractors", len(df))
        high_risk_count = len(df[df['risk_tier'] == 'HIGH_RISK'])
        col2.metric("High Risk Vendors", high_risk_count)
        col3.metric("Avg Risk Score", f"{df['risk_score_pct'].mean():.2f}%")

        st.subheader("Risk Distribution Breakdown")
        risk_counts = df['risk_tier'].value_counts()
        st.bar_chart(risk_counts, width='stretch')

    # TAB 2: Contractor Lookup
    with tab2:
        st.subheader("Search & Filter Contractors")
        search_term = st.text_input("Search contractor by name:")
        if search_term:
            filtered_df = df[df['contractor_name'].str.contains(search_term, case=False, na=False)]
        else:
            filtered_df = df
        st.dataframe(filtered_df, width='stretch')

    # TAB 3: Tender Bidding Simulator (NEW FEATURE FOR HACKATHON WIN!)
    with tab3:
        st.subheader("🎯 Live Tender Bid Risk Evaluator")
        st.write("Simulate a new municipal tender bid to get an instant AI safety assessment before awarding the contract.")
        
        sim_col1, sim_col2 = st.columns(2)
        
        with sim_col1:
            bidder_name = st.text_input("Bidder / Company Name", "Apex Infra Corp")
            estimated_budget = st.number_input("Proposed Tender Value (in ₹ Lakhs)", min_value=10.0, value=150.0, step=10.0)
            active_load = st.slider("Current Active Projects Load", min_value=1, max_value=10, value=3)
        
        with sim_col2:
            hist_delay = st.slider("Historical Avg Delay Rate (%)", min_value=0.0, max_value=100.0, value=15.0)
            hist_overrun = st.slider("Historical Avg Budget Overrun (%)", min_value=0.0, max_value=100.0, value=10.0)
        
        # Calculate Simulation Risk
        sim_timeline = max(0, 40 - (hist_delay * 0.8))
        sim_budget = max(0, 48 - (hist_overrun * 0.96))
        sim_cap = 12 if active_load <= 3 else (8 if active_load <= 5 else 4)
        sim_total_score = round(sim_timeline + sim_budget + sim_cap, 2)
        sim_risk_pct = round(100 - sim_total_score, 2)
        
        st.divider()
        st.subheader("📋 Evaluation Result & AI Tender Recommendation")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Calculated Performance Score", f"{sim_total_score} / 100")
        res_col2.metric("Predicted Failure Risk Rate", f"{sim_risk_pct}%")
        
        if sim_total_score >= 75:
            res_col3.success("🟢 RECOMMENDED FOR AWARD")
            st.success(f"**Verdict:** {bidder_name} demonstrates high historical reliability and low delivery risk. Proceed with tender processing.")
        elif sim_total_score >= 50:
            res_col3.warning("🟡 CONDITIONAL / NEEDS REVIEW")
            st.warning(f"**Verdict:** {bidder_name} poses moderate delay or overrun risk. Require additional financial guarantees before awarding.")
        else:
            res_col3.error("🔴 HIGH RISK - REJECT BID")
            st.error(f"**Verdict:** {bidder_name} exhibits severe risk indicators (over-capacity or excessive historical delays). Tender award not recommended.")

    # TAB 4: Export Options
    with tab4:
        st.subheader("Export Project Data")
        st.write("Download the updated risk scoring ledger for municipal tender evaluation.")
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Risk Assessment CSV",
            data=csv_data,
            file_name="contractor_risk_report.csv",
            mime="text/csv",
        )

except Exception as e:
    st.error(f"Error loading contractors dataset: {e}")