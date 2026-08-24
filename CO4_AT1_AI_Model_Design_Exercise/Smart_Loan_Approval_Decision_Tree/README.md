# Smart Loan Approval using Decision Tree

## Problem
Predict whether a loan application is approved or rejected using applicant and financial attributes.

## Dataset
Kaggle: Loan Approval Prediction Dataset by architsharma01
URL: https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset

The dataset contains 4,269 records and 13 columns (including the target).
The model drops `loan_id` and uses the remaining 11 predictors.

## Main predictors
- no_of_dependents
- education
- self_employed
- income_annum
- loan_amount
- loan_term
- cibil_score
- residential_assets_value
- commercial_assets_value
- luxury_assets_value
- bank_asset_value

Target:
- loan_status: Approved / Rejected

## AI technique
Decision Tree Classifier.

The implementation also calculates root-level Information Gain, Gain Ratio and Gini Reduction scores for educational attribute-selection comparison. The actual sklearn tree uses Gini impurity for the final model and compares it with entropy and log-loss.

## Run
1. Put `loan_approval_dataset.csv` in this folder.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run:
   `python loan_approval_decision_tree.py`

The program creates:
- confusion matrix
- ROC curve
- feature importance
- information gain graph
- decision tree visualization
- criterion comparison CSV
- final metrics CSV
- saved `.joblib` model

## Important
This is an academic demonstration model, not a production banking credit-decision system.
