import streamlit as st
import pandas as pd

st.title("🏛️ Contractor-Score AI Framework")
st.markdown("**Smart Public Procurement & Tender Risk Predictor** — Eliminating L1 blind spots by evaluating historical reliability, budget variance, and active workload capacity.")

st.title("🏛️ Contractor-Score AI Framework")
st.markdown("**Smart Public Procurement & Tender Risk Predictor** — Eliminating L1 blind spots by evaluating historical reliability, budget variance, and active workload capacity[cite: 1].")

# 1. Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("contractors.csv")

df = load_data()

# 2. Scoring Algorithm & Risk Flagging Logic (from spec)
def calculate_vendor_score(row):
    # Timeline Adherence Score (Max 40 pts)
    delay_pct = max(0, row['avg_delay_pct'])
    timeline_score = max(0, 40 - (delay_pct * 0.8))
    
    # Budget Variance Score (Max 40 pts)
    overrun_pct = max(0, row['avg_overrun_pct'])
    budget_score = max(0, 40 - (overrun_pct * 1.0))
    
    # Execution History & Quality Base (Max 20 pts)
    completion_rate = min(100, row['past_completed_projects'] * 2)
    quality_score = min(20, completion_rate * 0.2)
    
    total_score = round(timeline_score + budget_score + quality_score, 1)
    
    # Capacity Risk Flag Rule
    if row['active_projects'] > 4 or total_score < 70:
        risk_flag = "HIGH_RISK_OVER_CAPACITY"
    elif total_score < 80:
        risk_flag = "MEDIUM_RISK"
    else:
        risk_flag = "LOW_RISK"
        
    return pd.Series({

        "calculated_rating": total_score,
        "risk_status": risk_flag
    })

# Apply scoring engine across the dataset
scores_df = df.apply(calculate_vendor_score, axis=1)
master_df = pd.concat([df, scores_df], axis=1)

# 4. Tender Bidder Comparison UI (Feature 3)
st.subheader("🏛️ Municipal Tender Bidder Comparison Dashboard")
st.markdown("Side-by-side comparative view of bidding vendors for active public infrastructure tenders.")

# --- PASTE STEP 1 HERE ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Bidders Evaluated", len(master_df))
with col2:
    high_risk_count = len(master_df[master_df['risk_status'] == 'HIGH_RISK_OVER_CAPACITY'])
    st.metric("High-Risk Flags Detected", high_risk_count, delta="Review Needed", delta_color="inverse")
with col3:
    low_risk_count = len(master_df[master_df['risk_status'] == 'LOW_RISK'])
    st.metric("Optimal Low-Risk Vendors", low_risk_count, delta="Recommended")

st.divider()
# -------------------------

# Display styled dataframe
def color_risk(val):
    color = 'red' if 'HIGH_RISK' in val else ('orange' if 'MEDIUM_RISK' in val else 'green')
    return f'color: {color}; font-weight: bold;'

st.dataframe(master_df.style.map(color_risk, subset=['risk_status']), width="stretch")
# 5. Interactive Deep-Dive Inspector
st.subheader("🔍 Vendor Deep-Dive & Tender Decision Support")
selected_vendor = st.selectbox("Select Bidding Contractor for Review", master_df['contractor_name'])

vendor_data = master_df[master_df['contractor_name'] == selected_vendor].iloc[0]

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"### **Vendor:** {vendor_data['contractor_name']}")
    st.write(f"**Active Concurrent Projects:** {vendor_data['active_projects']}")
    st.write(f"**Average Timeline Delay:** +{vendor_data['avg_delay_pct']}%")
    st.write(f"**Average Budget Overrun:** +{vendor_data['avg_overrun_pct']}%")
with c2:
    st.metric("Vendor Performance Rating (0-100)", f"{vendor_data['calculated_rating']} / 100")
    st.error(f"Risk Status: {vendor_data['risk_status']}") if "HIGH" in vendor_data['risk_status'] else st.success(f"Risk Status: {vendor_data['risk_status']}")

# Real-time warning alert if rules trigger
if vendor_data['active_projects'] > 4 or vendor_data['avg_delay_pct'] > 25:
    st.warning("⚠️ **Capacity Overload Alert:** This contractor exceeds active project limits or historical delay thresholds (>25%). Awarding this tender risks project stalling[cite: 2].")