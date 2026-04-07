import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("=== Data Ingestion ===")

df = pd.read_csv("churn.csv")

df.drop(["RowNumber", "CustomerId", "Surname"], axis=1, inplace=True)

print(f"Loaded {len(df):,} records ({df.shape[1]} features)")

missing = df.isnull().mean() * 100
missing = missing[missing > 0]

if len(missing) > 0:
    print("Missing values filled:",
          ", ".join([f"{col} ({val:.1f}%)" for col, val in missing.items()]))
else:
    print("Missing values filled: None")

df["AgeGroup"] = pd.cut(df["Age"],
                        bins=[18, 30, 50, 100],
                        labels=["Young", "Middle", "Senior"])

df["BalanceSalaryRatio"] = df["Balance"] / (df["EstimatedSalary"] + 1)

df["TenureGroup"] = pd.cut(df["Tenure"],
                           bins=[0, 3, 7, 10],
                           labels=["New", "Mid", "Loyal"])

df["ActivityScore"] = df["IsActiveMember"] * df["NumOfProducts"]

print("Engineered 4 new features (AgeGroup, BalanceSalaryRatio, TenureGroup, ActivityScore)\n")


X = df.drop("Exited", axis=1)
y = df["Exited"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


num_cols = [
    "CreditScore", "Age", "Tenure", "Balance",
    "NumOfProducts", "EstimatedSalary", "BalanceSalaryRatio"
]

cat_cols = ["Geography", "Gender", "AgeGroup", "TenureGroup"]

bin_cols = ["HasCrCard", "IsActiveMember", "ActivityScore"]

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, num_cols),
    ("cat", categorical_pipeline, cat_cols),
    ("bin", "passthrough", bin_cols)
])

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(class_weight="balanced"),
    "SVM": SVC(probability=True, class_weight="balanced"),
    "XGBoost": XGBClassifier(eval_metric="logloss", scale_pos_weight=4)
}


param_grid = {
    "Logistic Regression": {
        "model__C": [0.1, 1, 10]
    },
    "Random Forest": {
        "model__n_estimators": [100, 200],
        "model__max_depth": [5, 10]
    },
    "SVM": {
        "model__C": [0.1, 1],
        "model__kernel": ["rbf"]
    },
    "XGBoost": {
        "model__n_estimators": [200, 300],
        "model__learning_rate": [0.05, 0.1],
        "model__max_depth": [4, 6]
    }
}


print("=== Model Comparison (5-Fold Cross-Validation) ===")

print("+-------------------------+-----------+-----------+----------+--------+")
print("| Model                   | Accuracy  | Precision | Recall   | F1     |")
print("+-------------------------+-----------+-----------+----------+--------+")

best_score = 0
best_model = None
best_model_name = ""
best_params = {}

for name, model in models.items():

    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    grid = GridSearchCV(
        pipe,
        param_grid[name],
        cv=5,
        scoring="f1",
        n_jobs=-1
    )

    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"| {name:<23} | {acc:.3f}     | {prec:.3f}     | {rec:.3f}    | {f1:.3f}  |")

    if f1 > best_score:
        best_score = f1
        best_model = grid.best_estimator_
        best_model_name = name
        best_params = grid.best_params_

print("+-------------------------+-----------+-----------+----------+--------+")

print(f"\n=== Best Model: {best_model_name} ===")

clean_params = {k.replace("model__", ""): v for k, v in best_params.items()}
print("Hyperparameters:", clean_params)

print("\nTop 5 Feature Importances:")

model_step = best_model.named_steps["model"]

if hasattr(model_step, "feature_importances_"):
    importances = model_step.feature_importances_

    feature_names = best_model.named_steps["preprocessor"].get_feature_names_out()

    feat_imp = sorted(zip(feature_names, importances),
                      key=lambda x: x[1],
                      reverse=True)[:5]

    for i, (feat, val) in enumerate(feat_imp, 1):
        print(f"{i}. {feat} — {val:.3f}")
else:
    print("Model does not support feature importance")

os.makedirs("models", exist_ok=True)

model_path = f"models/churn_{best_model_name.lower().replace(' ', '_')}.pkl"
joblib.dump(best_model, model_path)

print(f"\nModel saved to {model_path}")