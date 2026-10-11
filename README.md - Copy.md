# 🎓 EduPulse AI - Student Analytics & Success Platform

> **Early Academic Risk Detection & Intelligent Support Recommendation Engine**

EduPulse AI is an end-to-end Machine Learning powered educational analytics platform designed to help educators, academic advisors, and institutional administrators identify early signs of academic risk and deliver personalized, actionable support interventions to students.

> ⚠️ **Hackathon & Prototype Disclaimer**: The dataset (`students_1200.csv`) is synthetically generated for demonstration purposes, and the trained model is a proof-of-concept prototype. It is not validated for real-world institutional or high-stakes academic decision-making.

---


## 🌟 Key Features

* **📊 Cohort Analytics Overview**: Real-time cohort KPIs (Total Students, High Risk %, Avg GPA, Avg Attendance, Assignment Completion) accompanied by Plotly visual analytics (Risk Distribution, GPA vs. Attendance Scatter, Department & Grade Level Risk Breakdowns).
* **🎓 Student Risk Predictor & Deep-Dive**: Search and inspect individual student profiles to view Machine Learning risk predictions (`High`, `Medium`, `Low`), class probabilities, and feature indicator z-score impact badges.
* **🛠️ Personalized Recommendation Engine**: Context-aware intervention generator that maps low metrics to specific recovery actions (e.g., bi-weekly advisor coaching, peer tutoring, LMS orientation, wellness counseling, financial aid assistance).
* **🔮 Interactive What-If Simulator**: Real-time scenario planning tool allowing advisors to adjust student parameters (attendance, study hours, assignment completion, stress level) and visually compare simulated vs. baseline risk probabilities.
* **📁 Student Data Explorer**: Interactive directory featuring multi-attribute filtering (Major, Grade Level, Risk Level) and instant CSV data export.

---

## 🛠️ Technology Stack

* **Core Language**: Python 3.14
* **Web Framework**: Streamlit (v1.65.0)
* **Machine Learning**: Scikit-Learn (v1.9.1) - Random Forest Classifier
* **Data Processing & Analytics**: Pandas, NumPy
* **Data Visualization**: Plotly Express & Plotly Graph Objects
* **Model Serialization**: Joblib

---

## 🤖 Model Approach & Architecture

### Data Generation & Feature Engineering
Synthetic data generator (`generate_data.py`) generates 1,200 student academic profiles based on latent capability indices and correlated metrics:
* **Academic Metrics**: Attendance Rate (%), GPA (4.0 scale), Assignment Completion Rate (%), Midterm Score (%), Study Hours/Week.
* **Engagement & Well-being**: LMS Portal Engagement, Class Participation, Stress Level (1-10 scale), Tuition Payment Status.

### Machine Learning Classifier
* **Algorithm**: `RandomForestClassifier` (120 estimators, max depth 10, class-balanced weights).
* **Training Pipeline**: `train_model.py` performs a 80/20 stratified split (`train_test_split`) to maintain risk class proportions.
* **Performance**: Achieves **90.00% accuracy** across 3 risk tiers (`High`, `Medium`, `Low`).

---

## 📁 Repository Structure

```
EduPulse_AI/
├── app.py                  # Main Streamlit web application
├── generate_data.py        # Synthetic dataset generator script
├── train_model.py          # Machine learning model training script
├── requirements.txt        # Python dependency specifications
├── .gitignore              # Git ignore rules for virtualenvs & cache
├── README.md               # Project documentation & setup guide
├── data/
│   └── students_1200.csv   # Generated student dataset (1,200 records)
├── models/
│   └── risk_model.pkl      # Saved Random Forest model artifact
└── src/
    ├── __init__.py         # Package initializer
    ├── data_loader.py      # Data loading, filtering & KPI computation
    ├── model_utils.py       # Model loading, inference & indicator explanation
    └── recommendations.py  # Personalized academic intervention logic
```

---

## 🚀 Quickstart & Setup Instructions

### 1. Clone the Repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd EduPulse_AI
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Generate Data & Train Model (Optional / Pre-packaged)
```bash
# Generate 1,200 synthetic student records
python generate_data.py

# Train the Random Forest model
python train_model.py
```

### 4. Run the Streamlit Dashboard
```bash
python -m streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## ⚠️ Limitations & Future Roadmap

* **Synthetic Data Base**: Current model is trained on realistic synthetic student data. Future iterations will support direct LMS database integration (e.g., Canvas, Blackboard API via OAuth).
* **Demographic Bias Protection**: Intentionally excludes demographic attributes to prevent bias in academic risk prediction.
* **Longitudinal Tracking**: Future releases will incorporate time-series modeling to track student metric trends across multiple semesters.

---

## 🔐 Production Deployment & Security Requirements

Prior to deploying EduPulse AI in a live university environment with real student records:
1. **Authentication & FERPA Authorization**: Implement Single Sign-On (OAuth 2.0 / SAML 2.0 via Azure AD or Google Workspace) and strict Role-Based Access Control (RBAC) to ensure students can access only their own metrics while advisors access assigned cohorts.
2. **Model Deserialization Integrity**: SHA-256 checksum verification is enforced via `verify_model_integrity()` in `src/model_utils.py` prior to `joblib.load()`.
3. **CSV Export Sanitization**: Spreadsheet formula trigger escaping (`=`, `+`, `-`, `@`) is applied to CSV downloads to prevent spreadsheet code execution.
