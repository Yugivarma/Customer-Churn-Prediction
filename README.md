# 📊 Customer Churn Prediction Project 🚀

Welcome to the Customer Churn Prediction project repository! This project is a journey through the realms of data exploration, insightful model building, and the thrill of deploying a machine learning model. Let's delve into the fascinating world of data science!

## 📌 Project Overview

The primary objective of this project is to predict customer churn, empowering businesses to identify and retain customers at risk of leaving. The journey comprises an enchanting Exploratory Data Analysis (EDA), an ingenious model-building phase, and the magic of deployment using Flask and HTML.


---

## 🏗️ Project Structure


---

## 📊 1️⃣ Exploratory Data Analysis (EDA)

**Notebook:** `Cust_Churn_Project_code.ipynb`

### Key Tasks:
- Removed redundant columns
- Handled missing values and corrected data types
- Conducted univariate and bivariate analysis
- Created visualizations using:
  - Bar charts
  - Heatmaps
  - Count plots
  - Point plots
  - Distribution analysis

**Original Dataset:**  
`WA_Fn-UseC_-Telco-Customer-Churn.csv`

---

## 🤖 2️⃣ Model Building & Evaluation


### Process:
- Feature preprocessing (scaling & encoding)
- Handled class imbalance using SMOTE / SMOTEENN
- Trained multiple classification models
- Selected **XGBoost** as the final model

---

## 🚀 3️⃣ Flask Deployment

**Deployment Script:** `app.py`

### Flask Routes:
- `/loadpage` → Loads the home page
- `/predict` → Accepts customer data and returns churn prediction

---

## ▶️ Running the Application

### 1️⃣ Install Dependencies
Ensure you have Flask installed. If not, install it using `pip install Flask`.

### 2️⃣ Run the Flask App
Run the application script using 'python app.py' in the Anaconda Prompt.

### 3️⃣ Open in Browser
(http://127.0.0.1:5000)

You can now test real-time churn predictions.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Imbalanced-Learn
- Matplotlib
- Seaborn
- Flask

---

## 🎯 Key Highlights

- Built an end-to-end ML project from raw data to deployment
- Achieved high predictive performance using XGBoost
- Applied business-focused evaluation metrics
- Deployed a production-ready ML model using Flask

---

## 📈 Business Impact

This solution helps businesses:
- Identify customers at risk of churn
- Take proactive retention measures
- Improve customer lifetime value

---

⭐ If you found this project helpful, consider giving it a star!





