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
def load_and_process_data():
    df = pd.read_csv("contractors.csv")
    
    # AI Risk Calculation Logic: Combine delay and cost overrun into a risk score
    df['risk_score'] = (df['avg_delay_pct'] + df['avg_overrun_pct']) / 2
    
    # Categorize into risk levels
    def assign_risk(score):
        if score > 20:
            return "HIGH_RISK"
        elif score > 10:
            return "MEDIUM_RISK"
        else:
            return "LOW_RISK"
            
    df['risk_level'] = df['risk_score'].apply(assign_risk)
    return df

try:
    df = load_and_process_data()
    
    # Define tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview & Risk Metrics", "🔍 Contractor Lookup", "📋 Raw Data & Export"])

    # TAB 1: Overview & Metrics
    with tab1:
        st.subheader("Key Portfolio Indicators")
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Total Contractors", len(df))
        high_risk_count = len(df[df['risk_level'] == 'HIGH_RISK'])
        col2.metric("High Risk Vendors", high_risk_count)
        avg_score = round(df['risk_score'].mean(), 2)
        col3.metric("Avg Risk Score", f"{avg_score}%")

        st.markdown("---")
        st.write("### Risk Distribution Breakdown")
        st.bar_chart(df['risk_level'].value_counts())

    # TAB 2: Contractor Search
    with tab2:
        st.subheader("Search & Filter Contractors")
        search_term = st.text_input("Search contractor by name:")
        if search_term:
            filtered_df = df[df['contractor_name'].str.contains(search_term, case=False, na=False)]
            st.dataframe(filtered_df,width=True)
        else:
            st.dataframe(df,width=True)

    # TAB 3: Export Options
    with tab3:
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