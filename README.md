### 🌐 Live Demo
Try the live application here: [Contractor-Score AI Framework Live App](https://contractor-score-ai-project-h39plwdefyqdonwifqqi8j.streamlit.app)

---
# 🏗️ Contractor-Score AI Framework

> **Smart Public Procurement & Risk Predictor** — Eliminating municipal infrastructure blind spots by evaluating historical reliability, delay metrics, and budget cost overruns.

## 🚀 Overview
The **Contractor-Score AI Framework** is an intelligent public procurement risk assessment tool designed to help municipal authorities evaluate, rank, and mitigate risks when awarding infrastructure tenders. By combining historical delay patterns and budget overrun data, the application calculates automated risk scores to flag high-risk vendors before contracts are awarded.

---

## ✨ Key Features & Dashboard Upgrades

* **📊 Multi-Tab Interactive UI:** Built using Streamlit, featuring structured sections for portfolio metrics, vendor lookup, and data export.
* **🤖 Automated Risk-Scoring Engine:** Dynamically calculates risk percentages based on average project delays (`avg_delay_pct`) and cost overruns (`avg_overrun_pct`).
* **🚦 Intelligent Risk Categorization:** Automatically classifies contractors into `HIGH_RISK`, `MEDIUM_RISK`, and `LOW_RISK` tiers.
* **📈 Visual Risk Analytics:** Integrated bar charts displaying portfolio-wide risk distributions at a glance.
* **📋 Exportable Reports:** Allows municipal officers to download filtered risk assessment data directly as a CSV report for tender evaluation boards.

---

## 🛠️ Project Structure
* `app.py` — Main Streamlit application frontend and risk-scoring logic.
* `contractors.csv` — Dataset containing contractor names, active projects, and historical performance metrics.
* `requirement.txt` — Project dependencies (Streamlit, Pandas, etc.).

---

## ⚙️ Local Installation & Running

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mohitevidya965-sudo/contractor-score-ai-project.git](https://github.com/mohitevidya965-sudo/contractor-score-ai-project.git)
   cd contractor-score-ai-project
