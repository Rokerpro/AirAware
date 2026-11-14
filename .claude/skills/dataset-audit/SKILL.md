---
name: dataset-audit
description: Audit a dataset before training: schema, quality, missing values, duplicates, imbalance, leakage risks, bias, and the right split and preprocessing. Use when a new dataset is loaded or before building a training pipeline.
---

# Dataset audit

Every number in the report must come from code that was actually run on the data, or be marked unverified. Never fabricate statistics. Do not modify the original data files; write any cleaned data to a new file.

## Workflow
1. Record the source, licence, download date and citation of each dataset.
2. Load the data and print shape, column names, types and a few sample rows.
3. Check quality: missing values per column, duplicate rows, impossible or out-of-range values, units, inconsistent labels or categories.
4. Check the target: distribution, class balance (or spread for regression), and any rows without a target.
5. Check coverage across groups that matter (time periods, locations, demographics, sources). Note under-represented groups and possible biases.
6. Look for leakage: features derived from the target, information from the future, IDs that encode the label, duplicates that would land in both train and test.
7. Recommend a split that matches real use: time-based for forecasting, group-based when predicting for unseen entities, stratified for imbalanced classes. Never a random split on time-ordered data.
8. Recommend preprocessing, fitted on the training split only.
9. Use the dataset-auditor subagent for a second read-only review if useful.

## Deliverables
- **Data card**: source, licence, citation, size, columns, target.
- **Quality table**: column | type | % missing | notes. Numbers from executed code only.
- **Target and group coverage**, with the code that produced them.
- **Leakage and bias risks**, each with severity.
- **Recommended split and preprocessing.**
- **Observed vs assumed**: clearly separated.

## Common failure modes
- Reporting statistics that were estimated rather than computed.
- Scaling, imputing or encoding on the full dataset before splitting.
- Random splits on time series or grouped data.
- Ignoring that some data is model output rather than measurement.
- Dropping missing rows in a way that removes a whole group or season.
