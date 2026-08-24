# Explainable and Generalizable AI: Inductive Learning and Explanation-Based Learning

## Project objective
Compare an inductive learning model with an explanation-based, symbolic learning model and evaluate:
- generalization to unseen Iris samples
- predictive accuracy
- precision, recall and F1
- explanation transparency
- model complexity

## Dataset
Iris classification dataset:
- 150 instances
- 4 numerical input features
- 3 classes: setosa, versicolor, virginica
- 50 samples per class

The dataset is available directly through scikit-learn's `load_iris()` function, so the project does not require downloading a separate file. A CSV copy is included as `iris_dataset.csv`.

## Models
### 1. Inductive learning
A Decision Tree (`DecisionTreeClassifier`) learns decision rules from labelled training examples.

### 2. EBL-inspired learning
The project implements a compact symbolic domain theory:
1. petal length <= 2.45 -> setosa
2. petal length > 2.45 and petal width <= 1.75 -> versicolor
3. petal length > 2.45 and petal width > 1.75 -> virginica

This is explicitly an **EBL-inspired educational implementation**, not a full classical theorem-proving EBG system. Classical EBL uses background/domain knowledge to explain an example and then operationalize the explanation into a generalized concept.

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Fixed experimental setup
- train/test split: 70/30
- stratified split
- random_state = 42
- decision-tree max_depth = 4

## Observed test results
- Inductive Decision Tree accuracy: 88.89%
- EBL-inspired Rule Model accuracy: 93.33%
- Inductive macro F1: 0.8888
- EBL-inspired macro F1: 0.9327

## Interpretation
The EBL-inspired model uses explicit domain rules, so every prediction can be traced to one of three rules. The inductive tree learns its own decision structure from data and can generalize without manually supplied rules, but its learned explanation is a tree path and is more dependent on the training sample.

## Important academic limitation
Do not claim that the three Iris rules are a canonical implementation of classical EBL. They are a transparent symbolic approximation designed to demonstrate the role of background knowledge in explanation-driven generalization.

## Project files
- `main.py` - complete implementation
- `iris_dataset.csv` - CSV copy of dataset
- `requirements.txt` - Python packages
- `results/model_comparison.csv` - numerical comparison
- `results/inductive_decision_tree.png` - learned tree
- `results/inductive_confusion_matrix.png` - confusion matrix
- `results/ebl_confusion_matrix.png` - EBL confusion matrix
- `results/accuracy_comparison.png` - accuracy graph
- `results/sample_explanations.csv` - symbolic explanations
- `results/decision_tree_rules.txt` - learned tree rules
