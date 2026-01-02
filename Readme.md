🚨 Operational Cost Leakage Detection System

📌 Overview
This project is an end-to-end machine learning–based operational cost leakage detection system designed to identify abnormal cost patterns, explain their root causes, and recommend optimization strategies.
It helps organizations reduce hidden operational losses using data-driven insights.

The system combines:

Machine Learning (Isolation Forest) for anomaly detection

Business rule–based root cause analysis

An interactive Streamlit dashboard for real-world usability

🎯 Problem Statement

Operational processes often suffer from hidden cost leakages due to factors such as:

Excessive waiting or idle time

Traffic congestion and route detours

Poor asset utilization

Excess inventory holding

These issues are difficult to detect manually.
This project aims to automatically detect such leakages and suggest corrective actions.

🚀 Key Features

📊 Operational Cost Calculation from raw operational data

🤖 ML-based Anomaly Detection using Isolation Forest

🧠 Explainable Root Cause Analysis

🛠 Optimization Recommendations for each detected issue

📈 Interactive Dashboard built with Streamlit

📁 CSV Upload Mode for batch analysis

🎛 Manual Simulation Mode for real-time what-if analysis

⬇️ Downloadable Leakage Report

🧩 Tech Stack

Programming Language: Python

Machine Learning: Scikit-learn (Isolation Forest)

Data Handling: Pandas

Visualization: Matplotlib, Streamlit charts

Frontend / UI: Streamlit

Development: Google Colab (ML logic), VS Code (application & UI)

🧠 System Architecture
Raw Operational Data
        ↓
Operational Cost Calculation
        ↓
ML-based Anomaly Detection
        ↓
Root Cause Analysis
        ↓
Optimization Suggestions
        ↓
Interactive Streamlit Dashboard

📂 Project Structure
operational-cost-leakage-system/
│── app.py
│── requirements.txt
│── README.md

▶️ How to Run the Project
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run the Application
streamlit run app.py

3️⃣ Open in Browser
http://localhost:8501

🧪 Input Options
🔹 CSV Upload Mode

Upload operational data in CSV format

System detects cost leakages, explains reasons, and estimates savings

🔹 Manual Simulation Mode

Adjust operational parameters using sliders

Perform real-time what-if analysis for a single scenario