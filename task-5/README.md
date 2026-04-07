# 🚀 Machine Learning Pipeline with Feature Engineering

## 📌 Overview

This project implements an end-to-end Machine Learning pipeline for predicting customer churn using structured banking data. The pipeline handles data ingestion, preprocessing, feature engineering, model training, hyperparameter tuning, evaluation, and model persistence.

---

## 🎯 Objective

Predict whether a customer will churn (`Exited = 1`) based on demographic and account-related features.

---

## 📂 Dataset Features

### 🔹 Input Features

- CreditScore
- Geography
- Gender
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard
- IsActiveMember
- EstimatedSalary

### 🔹 Target Variable

- `Exited` → 1 (Churn), 0 (No Churn)

---

## ⚙️ Pipeline Architecture

```

Raw Data → Cleaning → Feature Engineering → Preprocessing →
Model Training → Hyperparameter Tuning → Evaluation → Model Saving

```

---

## 🧹 Data Preprocessing

- Dropped unnecessary columns:
  - RowNumber
  - CustomerId
  - Surname

- Handled missing values:
  - Numerical → Median Imputation
  - Categorical → Most Frequent

- Scaling:
  - StandardScaler applied to numerical features

- Encoding:
  - OneHotEncoder for categorical variables

---

## 🧠 Feature Engineering

Created new features to improve model performance:

- **AgeGroup** → Binned age into categories
- **BalanceSalaryRatio** → Financial stability indicator
- **TenureGroup** → Customer loyalty segmentation
- **ActivityScore** → Product usage × activity status

---

## 🤖 Models Used

- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- XGBoost

---

## 🔧 Hyperparameter Tuning

Used **GridSearchCV** with:
- 5-Fold Cross Validation
- Scoring Metric: **F1 Score**

---

## ⚖️ Handling Class Imbalance

- Applied:
  - `class_weight="balanced"` (Logistic, RF, SVM)
  - `scale_pos_weight=4` (XGBoost)

This improved recall and overall F1-score.

---

## 📊 Model Performance

| Model                 | Accuracy | Precision | Recall | F1 Score |
|----------------------|----------|----------|--------|----------|
| Logistic Regression  | 0.712    | 0.386    | 0.710  | 0.500    |
| Random Forest        | 0.839    | 0.597    | 0.644  | **0.619** |
| SVM                  | 0.795    | 0.498    | 0.752  | 0.599    |
| XGBoost              | 0.814    | 0.532    | 0.698  | 0.604    |

---

## 🏆 Best Model

**Random Forest Classifier**

### 🔹 Hyperparameters
```
max_depth: 10
n_estimators: 200
```

---

## 📈 Feature Importance (Top 5)

1. Age  
2. NumOfProducts  
3. Balance  
4. ActivityScore  
5. BalanceSalaryRatio  

---

## 💾 Model Persistence

The trained model is saved using `joblib`:

```
models/churn_random_forest.pkl
````

---

## 🛠️ Technologies Used

- Python
- pandas
- numpy
- scikit-learn
- XGBoost
- joblib

---

## 🚀 How to Run

```bash
python train.py
````

---

## 📌 Key Learnings

* Importance of feature engineering in improving model performance
* Handling class imbalance using class weights
* Using pipelines for clean and reusable ML workflows
* Model comparison using cross-validation and F1-score
* Extracting feature importance for interpretability
