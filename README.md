# 💳 Fraud Detection System (End-to-End ML + Rule-Based System)

## 📌 Overview

This project is an **end-to-end fraud detection system** that combines:

- Machine Learning (XGBoost)
- Rule-based detection (business logic)
- Real-time API (FastAPI)
- Interactive dashboard (Streamlit)
- PostgreSQL data pipeline

The system simulates **real-world banking fraud detection workflows**, including data ingestion, feature engineering, model training, and real-time prediction.

---

## 🎯 Business Problem

Financial institutions process millions of transactions daily. Fraudulent transactions:

- Cause direct financial loss  
- Damage customer trust  
- Require fast and accurate detection  

### Key Challenges

- Highly imbalanced data (fraud < 1%)
- Fraud patterns evolve over time
- False negatives are extremely costly

### Goal

Build a system that:

- Detects fraud in real-time  
- Minimizes missed fraud cases  
- Provides explainable decisions  

---

## 🧠 Solution Approach

A **hybrid fraud detection system** is implemented:


Input → Rule Engine → ML Model → Decision


### Why Hybrid?

| Component      | Purpose                          |
|---------------|----------------------------------|
| Rule Engine   | Catch obvious fraud instantly     |
| ML Model      | Detect complex hidden patterns    |
| Thresholding  | Control risk sensitivity          |

---

## 🏗️ System Architecture


PostgreSQL → Pipeline → Feature Engineering → ML Model (XGBoost)
↓
FastAPI API
↓
Streamlit Dashboard


---

## ⚙️ Technical Pipeline

### 1. Data Ingestion
- Source: Transaction dataset (~1M rows)
- Stored in PostgreSQL (`transactions_raw`)

### 2. Data Validation
- Null checks  
- Duplicate detection  
- Fraud distribution analysis  

### 3. Preprocessing
- Remove duplicates  
- Drop irrelevant columns (IDs)  
- Remove invalid balance records  
- Handle missing values  

### 4. Feature Engineering

#### 🔹 Balance Features
- `orig_balance_error`
- `dest_balance_error`

#### 🔹 Behavioral Features
- `is_full_drain`
- `is_high_amount`

#### 🔹 Fraud Pattern Features
- `empty_orig_with_amount`
- `suspicious_zero_pattern`
- `zero_balance_after_txn`

#### 🔹 Time Features
- `hour`
- `is_night`

#### 🔹 Encoding
- One-hot encoding of transaction type  

---

### 5. Feature Selection
- Low variance removal  
- RandomForest feature importance  

---

### 6. Handling Imbalance
- SMOTE (Synthetic Minority Oversampling)  
- Controlled fraud ratio (~10%)  

---

### 7. Model Training

**Model Used:**
- XGBoost Classifier  

**Key Parameters:**
- `n_estimators = 300`
- `max_depth = 6`
- `learning_rate = 0.1`
- `scale_pos_weight` for imbalance  

---

### 8. Evaluation

**Metrics:**
- Precision  
- Recall  
- F1-score  
- ROC-AUC  

**Results:**
- ROC-AUC: ~0.996  
- Fraud Recall: ~98%  
- Very low false negatives  

---

## 🤖 ML Logic

The model outputs:

- **Probability of Fraud (0–1)**  

Decision rule:

```python
if probability >= 0.8:
    Fraud
else:
    Normal


⚖️ Decision System (Hybrid)
Rule Engine (Priority)

Examples:

Empty account + large transaction
Full balance drain
High-value transfer



➡️ These trigger instant fraud detection

ML Model (Fallback)

Used when:

No rule is triggered
Fraud pattern is complex
Final Decision Flow
Rule → ML → Threshold → Output
🌐 Deployment
Backend (API)
Framework: FastAPI
Endpoint:
POST /predict
Frontend (Dashboard)
Framework: Streamlit

## Features:

Fraud prediction input
Analytics dashboard
Risk visualization
Database
PostgreSQL
📊 Dashboard Features
KPI metrics (fraud rate, total transactions)
Fraud distribution charts
Time-based fraud trends
Real-time fraud prediction
🧪 Example API Input
{
  "step": 1,
  "type": "CASH_OUT",
  "amount": 300000,
  "oldbalanceOrg": 0,
  "newbalanceOrig": 0,
  "oldbalanceDest": 0,
  "newbalanceDest": 300000,
  "isFlaggedFraud": 0
}
⚠️ Limitations (Critical - Industry Transparency)
1. Data Bias
Fraud concentrated in specific transaction types
Limited generalization
2. Synthetic Data (SMOTE)
May introduce unrealistic patterns
3. Static Threshold
Fixed threshold (0.8) not optimal for all scenarios
4. No Concept Drift Handling
Model not updated with evolving fraud patterns
5. Limited Explainability
No SHAP / feature-level explanations
6. No Real-Time Streaming
System is batch-based


🔐 Ethical & Compliance Considerations
No personal data used
Partial explainability of decisions
Designed for GDPR-compliant environments


🚀 Future Improvements
Add SHAP explainability
Implement real-time streaming (Kafka)
Dynamic thresholding
Automated model retraining pipeline
Fraud scoring system (0–100)
User authentication & logging


🛠️ Tech Stack
Python
Pandas / NumPy
Scikit-learn
XGBoost
FastAPI
Streamlit
PostgreSQL


🏆 Key Highlights
End-to-end ML pipeline
Hybrid fraud detection system
Real-time API + dashboard
Handles class imbalance effectively
Production-style architecture


👨‍💻 Author

Tanmay Khairnar
Master’s in Data Science & Business Analytics


## App link :
https://fraud-transaction-detection-system-1.onrender.com
