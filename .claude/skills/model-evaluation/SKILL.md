---
name: model-evaluation
description: Evaluate a trained model honestly: task-appropriate metrics, comparison with the baseline, error analysis, overfitting and generalization checks, and performance across groups. Use after training and before presenting results.
---

# Model evaluation

Report the real numbers, including failures. Never present a result that was not produced by running code on the held-out data.

## Workflow
1. Pick metrics that fit the task and the users, and say why:
   - classification: precision, recall, F1, confusion matrix, ROC/PR-AUC for imbalanced data;
   - regression or forecasting: MAE, RMSE, and error in real units;
   - other tasks: the metric named in the brief, plus one a user would understand.
2. Evaluate the baseline and the model on the same held-out test split.
3. Compare train, validation and test scores to check for overfitting.
4. Break results down by relevant groups (time periods, seasons, locations, classes, demographics). Note where the model is worse than the baseline.
5. Inspect errors: false positives and false negatives, or the largest errors, and look for patterns.
6. If possible, test on data from a different period or source to check generalization.
7. Write limitations plainly.

## Deliverables
- **Metrics table**: metric | baseline | model, on the test split.
- **Train vs validation vs test** scores.
- **Per-group table**, with weak groups highlighted.
- **Error analysis**: examples and patterns.
- **Limitations and failure cases.**
- The code or notebook cell that produced each number.

## Common failure modes
- Accuracy on imbalanced data.
- Evaluating on data that was used for training or tuning.
- Comparing model and baseline on different data.
- Hiding groups or periods where the model fails.
- Overstating a small improvement that is within noise.
