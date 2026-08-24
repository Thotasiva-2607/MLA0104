"""
Smart Loan Approval using Decision Tree
---------------------------------------
Dataset: Kaggle Loan Approval Prediction Dataset
Source: https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset

Run:
    pip install -r requirements.txt
    python loan_approval_decision_tree.py

Optional:
    python loan_approval_decision_tree.py --csv loan_approval_dataset.csv
"""

import argparse
import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.inspection import permutation_importance

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
TEST_SIZE = 0.20
OUTPUT_DIR = Path("outputs")


def clean_columns(df):
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Remove accidental leading/trailing spaces from string cells.
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def load_dataset(csv_path):
    if not Path(csv_path).exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}\n"
            "Download loan_approval_dataset.csv from the Kaggle source "
            "and place it in the project folder."
        )

    df = pd.read_csv(csv_path)
    df = clean_columns(df)

    required = {
        "loan_id", "no_of_dependents", "education", "self_employed",
        "income_annum", "loan_amount", "loan_term", "cibil_score",
        "residential_assets_value", "commercial_assets_value",
        "luxury_assets_value", "bank_asset_value", "loan_status"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    return df


def prepare_target(df):
    df = df.copy()

    # Dataset uses Approved / Rejected.
    mapping = {
        "approved": 1,
        "rejected": 0,
        "1": 1,
        "0": 0
    }

    df["loan_status"] = (
        df["loan_status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )

    if df["loan_status"].isna().any():
        raise ValueError("Unexpected values found in loan_status.")

    # Loan ID is an identifier, not a predictive feature.
    df = df.drop(columns=["loan_id"])

    return df


def build_preprocessor(X):
    categorical = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical = X.select_dtypes(include=np.number).columns.tolist()

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipe, numerical),
        ("cat", categorical_pipe, categorical)
    ], remainder="drop")

    return preprocessor, numerical, categorical


def get_feature_names(preprocessor):
    try:
        return list(preprocessor.get_feature_names_out())
    except Exception:
        return [f"feature_{i}" for i in range(
            len(preprocessor.transformers_)
        )]


def calculate_root_attribute_scores(X_train, y_train):
    """
    Calculates a transparent root-node attribute ranking using
    single-feature decision stumps.

    For each feature:
      - Information Gain = parent entropy - weighted child entropy
      - Gain Ratio = Information Gain / split information
      - Gini Reduction = parent Gini - weighted child Gini

    Continuous attributes are split at their median for this educational
    comparison. The sklearn DecisionTree model below performs its own
    optimal threshold search during training.
    """
    rows = []

    y = np.asarray(y_train)
    classes, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    parent_entropy = -np.sum(p * np.log2(p + 1e-12))
    parent_gini = 1 - np.sum(p ** 2)

    Xc = X_train.copy()

    for col in Xc.columns:
        values = Xc[col]

        if pd.api.types.is_numeric_dtype(values):
            threshold = values.median()
            groups = [values <= threshold, values > threshold]
            split_description = f"<= {threshold:.3f}"
        else:
            # For categorical variables, use category == most common value
            mode = values.mode(dropna=True)
            if mode.empty:
                continue
            category = mode.iloc[0]
            groups = [values == category, values != category]
            split_description = f"== {category}"

        weighted_entropy = 0.0
        weighted_gini = 0.0
        split_info = 0.0

        for mask in groups:
            mask = np.asarray(mask)
            n = mask.sum()
            if n == 0:
                continue

            child = y[mask]
            _, child_counts = np.unique(child, return_counts=True)
            probs = child_counts / child_counts.sum()

            child_entropy = -np.sum(probs * np.log2(probs + 1e-12))
            child_gini = 1 - np.sum(probs ** 2)

            weight = n / len(y)
            weighted_entropy += weight * child_entropy
            weighted_gini += weight * child_gini

            split_info -= weight * np.log2(weight + 1e-12)

        info_gain = parent_entropy - weighted_entropy
        gini_reduction = parent_gini - weighted_gini
        gain_ratio = info_gain / split_info if split_info > 0 else 0.0

        rows.append({
            "feature": col,
            "split": split_description,
            "information_gain": info_gain,
            "gain_ratio": gain_ratio,
            "gini_reduction": gini_reduction
        })

    return pd.DataFrame(rows).sort_values(
        "information_gain", ascending=False
    )


def evaluate_model(model, X_test, y_test, name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1": f1_score(y_test, y_pred, zero_division=0),
        "ROC_AUC": roc_auc_score(y_test, y_prob)
    }

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)
    print(pd.Series(metrics).to_string())
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=["Rejected", "Approved"],
        zero_division=0
    ))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return metrics, y_pred, y_prob


def save_plots(model, X_test, y_test, feature_names, attribute_scores):
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. Class distribution
    plt.figure(figsize=(7, 5))
    sns.countplot(x=y_test.map({0: "Rejected", 1: "Approved"}))
    plt.title("Loan Approval Class Distribution - Test Set")
    plt.xlabel("Loan Status")
    plt.ylabel("Number of Applications")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "class_distribution.png", dpi=200)
    plt.close()

    # 2. Confusion matrix
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=["Rejected", "Approved"],
        yticklabels=["Rejected", "Approved"]
    )
    plt.title("Decision Tree Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=200)
    plt.close()

    # 3. ROC curve
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f"Decision Tree (AUC = {auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "roc_curve.png", dpi=200)
    plt.close()

    # 4. Feature importance
    importances = pd.Series(
        model.named_steps["model"].feature_importances_,
        index=feature_names
    ).sort_values(ascending=False).head(12)

    plt.figure(figsize=(9, 6))
    importances.sort_values().plot(kind="barh")
    plt.title("Decision Tree Feature Importance")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "feature_importance.png", dpi=200)
    plt.close()

    # 5. Root attribute selection comparison
    top = attribute_scores.head(10).sort_values("information_gain")
    plt.figure(figsize=(9, 6))
    plt.barh(top["feature"], top["information_gain"])
    plt.title("Top Attributes by Information Gain")
    plt.xlabel("Information Gain")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "information_gain.png", dpi=200)
    plt.close()

    # 6. Tree visualization
    plt.figure(figsize=(24, 12))
    plot_tree(
        model.named_steps["model"],
        feature_names=feature_names,
        class_names=["Rejected", "Approved"],
        filled=True,
        rounded=True,
        max_depth=3,
        fontsize=8
    )
    plt.title("Decision Tree (First 3 Levels)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "decision_tree.png", dpi=200)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        default="loan_approval_dataset.csv",
        help="Path to loan_approval_dataset.csv"
    )
    args = parser.parse_args()

    print("SMART LOAN APPROVAL - DECISION TREE")
    print("-" * 70)

    raw = load_dataset(args.csv)
    print(f"Dataset shape: {raw.shape}")
    print("\nMissing values:")
    print(raw.isnull().sum())

    df = prepare_target(raw)

    X = df.drop(columns=["loan_status"])
    y = df["loan_status"].astype(int)

    # Hold-out split with stratification.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    print(f"\nTraining records: {len(X_train)}")
    print(f"Testing records : {len(X_test)}")

    # Attribute-selection comparison before one-hot encoding.
    attribute_scores = calculate_root_attribute_scores(X_train, y_train)
    print("\nTop attributes by Information Gain:")
    print(attribute_scores.head(10).to_string(index=False))
    attribute_scores.to_csv(
        OUTPUT_DIR / "attribute_selection_scores.csv",
        index=False
    )

    preprocessor, numerical, categorical = build_preprocessor(X_train)

    # Decision Tree using Gini impurity.
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", DecisionTreeClassifier(
            criterion="gini",
            max_depth=8,
            min_samples_split=10,
            min_samples_leaf=4,
            class_weight=None,
            random_state=RANDOM_STATE
        ))
    ])

    model.fit(X_train, y_train)

    feature_names = list(
        model.named_steps["preprocessor"].get_feature_names_out()
    )

    metrics, y_pred, y_prob = evaluate_model(
        model, X_test, y_test, "Decision Tree (Gini)"
    )

    # Compare Gini, Entropy and log-loss splitting.
    comparison = []
    for criterion in ["gini", "entropy", "log_loss"]:
        candidate = Pipeline([
            ("preprocessor", build_preprocessor(X_train)[0]),
            ("model", DecisionTreeClassifier(
                criterion=criterion,
                max_depth=8,
                min_samples_split=10,
                min_samples_leaf=4,
                random_state=RANDOM_STATE
            ))
        ])
        candidate.fit(X_train, y_train)
        m, _, _ = evaluate_model(
            candidate, X_test, y_test,
            f"Decision Tree ({criterion})"
        )
        comparison.append(m)

    comparison_df = pd.DataFrame(comparison)
    OUTPUT_DIR.mkdir(exist_ok=True)
    comparison_df.to_csv(
        OUTPUT_DIR / "criterion_comparison.csv", index=False
    )

    print("\nCriterion comparison:")
    print(comparison_df.to_string(index=False))

    # Save the final model.
    import joblib
    joblib.dump(model, OUTPUT_DIR / "loan_approval_decision_tree.joblib")

    save_plots(
        model, X_test, y_test,
        feature_names, attribute_scores
    )

    # Example prediction for a new applicant.
    sample = pd.DataFrame([{
        "no_of_dependents": 2,
        "education": "Graduate",
        "self_employed": "No",
        "income_annum": 6000000,
        "loan_amount": 15000000,
        "loan_term": 10,
        "cibil_score": 750,
        "residential_assets_value": 10000000,
        "commercial_assets_value": 5000000,
        "luxury_assets_value": 12000000,
        "bank_asset_value": 6000000
    }])

    pred = model.predict(sample)[0]
    prob = model.predict_proba(sample)[0, 1]

    print("\n" + "=" * 70)
    print("SAMPLE LOAN APPLICATION")
    print("=" * 70)
    print("Prediction:", "APPROVED" if pred == 1 else "REJECTED")
    print(f"Approval probability: {prob:.2%}")

    # Save a compact results file.
    result_df = pd.DataFrame([metrics])
    result_df.to_csv(OUTPUT_DIR / "final_results.csv", index=False)

    print("\nFiles generated inside ./outputs/")
    for p in sorted(OUTPUT_DIR.iterdir()):
        print(" -", p.name)


if __name__ == "__main__":
    main()
