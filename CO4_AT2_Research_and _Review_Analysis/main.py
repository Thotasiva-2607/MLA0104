import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)

# ============================================================
# 1. DATASET
# ============================================================
iris = load_iris(as_frame=True)
df = iris.frame.copy()
df.columns = [
    "sepal_length_cm", "sepal_width_cm",
    "petal_length_cm", "petal_width_cm", "target"
]
df["species"] = df["target"].map(dict(enumerate(iris.target_names)))

X = df[[
    "sepal_length_cm", "sepal_width_cm",
    "petal_length_cm", "petal_width_cm"
]]
y = df["target"]

print("\nDataset shape:", df.shape)
print(df.head())
print("\nClass distribution:")
print(df["species"].value_counts())

# ============================================================
# 2. TRAIN / TEST SPLIT
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# ============================================================
# 3. INDUCTIVE LEARNING
#    Decision Tree learns rules from labelled examples.
# ============================================================
inductive_model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)
inductive_model.fit(X_train, y_train)

ind_pred = inductive_model.predict(X_test)

print("\n--- INDUCTIVE LEARNING ---")
print("Accuracy:", accuracy_score(y_test, ind_pred))
print(classification_report(
    y_test, ind_pred, target_names=iris.target_names
))
print("Learned tree:")
print(export_text(
    inductive_model,
    feature_names=list(X.columns)
))

# ============================================================
# 4. EXPLANATION-BASED LEARNING (EBL-INSPIRED)
#
# Classical EBL needs a domain theory/background knowledge.
# Here the domain theory is represented by three symbolic rules.
# The rules are applied to unseen examples, demonstrating
# explanation-driven generalization.
# ============================================================
def ebl_predict(row):
    petal_length = row["petal_length_cm"]
    petal_width = row["petal_width_cm"]

    if petal_length <= 2.45:
        return 0       # setosa
    elif petal_width <= 1.75:
        return 1       # versicolor
    else:
        return 2       # virginica

def ebl_explanation(row):
    if row["petal_length_cm"] <= 2.45:
        return "petal length <= 2.45 -> setosa"
    elif row["petal_width_cm"] <= 1.75:
        return "petal length > 2.45 and petal width <= 1.75 -> versicolor"
    else:
        return "petal length > 2.45 and petal width > 1.75 -> virginica"

ebl_pred = X_test.apply(ebl_predict, axis=1)

print("\n--- EBL-INSPIRED SYMBOLIC MODEL ---")
print("Accuracy:", accuracy_score(y_test, ebl_pred))
print(classification_report(
    y_test, ebl_pred, target_names=iris.target_names
))

# Show explanations for first five test examples
print("\nSample explanations:")
for idx, row in X_test.head(5).iterrows():
    print(
        f"Index {idx}: prediction = "
        f"{iris.target_names[ebl_predict(row)]}; "
        f"reason = {ebl_explanation(row)}"
    )

# ============================================================
# 5. COMPARATIVE EVALUATION
# ============================================================
def macro_metrics(y_true, pred):
    p, r, f1, _ = precision_recall_fscore_support(
        y_true, pred, average="macro", zero_division=0
    )
    return accuracy_score(y_true, pred), p, r, f1

ind_acc, ind_p, ind_r, ind_f1 = macro_metrics(y_test, ind_pred)
ebl_acc, ebl_p, ebl_r, ebl_f1 = macro_metrics(y_test, ebl_pred)

comparison = pd.DataFrame({
    "Model": ["Inductive Decision Tree", "EBL-inspired Rules"],
    "Accuracy": [ind_acc, ebl_acc],
    "Macro Precision": [ind_p, ebl_p],
    "Macro Recall": [ind_r, ebl_r],
    "Macro F1": [ind_f1, ebl_f1],
    "Complexity": [
        f"{inductive_model.tree_.node_count} tree nodes",
        "3 rules"
    ]
})

print("\n--- COMPARISON ---")
print(comparison.to_string(index=False))

# ============================================================
# 6. CONFUSION MATRICES
# ============================================================
for title, pred, filename in [
    ("Inductive Decision Tree", ind_pred, "inductive_cm.png"),
    ("EBL-inspired Rules", ebl_pred, "ebl_cm.png")
]:
    cm = confusion_matrix(y_test, pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(cm)
    ax.set_title(title)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks(range(3), iris.target_names)
    ax.set_yticks(range(3), iris.target_names)

    for i in range(3):
        for j in range(3):
            ax.text(j, i, cm[i, j], ha="center", va="center")

    plt.tight_layout()
    plt.savefig(filename, dpi=160)
    plt.show()

# ============================================================
# 7. DECISION TREE VISUALIZATION
# ============================================================
fig, ax = plt.subplots(figsize=(15, 8))
plot_tree(
    inductive_model,
    feature_names=X.columns,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    fontsize=8,
    ax=ax
)
plt.tight_layout()
plt.savefig("inductive_decision_tree.png", dpi=180)
plt.show()

# ============================================================
# 8. ACCURACY COMPARISON
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4.5))
names = ["Inductive\nDecision Tree", "EBL-inspired\nRules"]
values = [ind_acc * 100, ebl_acc * 100]

bars = ax.bar(names, values)
ax.set_ylim(0, 100)
ax.set_ylabel("Test Accuracy (%)")
ax.set_title("Inductive vs EBL-inspired Learning")

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width()/2,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()
plt.savefig("accuracy_comparison.png", dpi=160)
plt.show()
