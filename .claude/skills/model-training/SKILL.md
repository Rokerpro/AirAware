---
name: model-training
description: Build a reproducible baseline-first training and validation pipeline with preprocessing kept separate from training, no data leakage, and saved model and preprocessing artifacts. Use when it is time to train a model.
---

# Model training

Baseline first, then improve. Keep the code simple enough for the team to explain. Do not start expensive training (large models, long GPU runs, big hyperparameter sweeps) without stating why it is needed and getting the user's agreement. Do not install dependencies or download large models without asking.

## Workflow
1. Confirm the dataset audit and split are done (run dataset-audit first if not).
2. Fix random seeds and record library versions.
3. Split data first, using the agreed split (time-based or group-based where relevant). Keep the test set untouched until final evaluation.
4. Build the baseline (e.g. "predict yesterday's value", majority class, or a simple linear model) and record its validation score.
5. Put preprocessing in its own module or function, fitted on the training split only (e.g. a scikit-learn Pipeline or equivalent).
6. Train the chosen model on the training split and tune only against the validation split.
7. Save artifacts to a known folder: the model, the fitted preprocessing, the feature list and order, the config (seed, hyperparameters, data version) and the validation scores.
8. Reload the saved artifacts and check they reproduce the same validation predictions.
9. Report only scores that were actually produced by running the code.

## Deliverables
- Separate code for: data loading, preprocessing, training.
- Baseline score and model score on the validation split.
- Saved artifacts: model, preprocessing, feature list, config, metrics file.
- A short note on how to rerun training from scratch.

## Common failure modes
- Fitting scalers, encoders or imputers on all the data.
- Tuning on the test set.
- Features that are not available at prediction time.
- Saving the model but not the preprocessing, so inference cannot reproduce inputs.
- No seed, so results cannot be repeated.
- Jumping to a complex model before the baseline works.
