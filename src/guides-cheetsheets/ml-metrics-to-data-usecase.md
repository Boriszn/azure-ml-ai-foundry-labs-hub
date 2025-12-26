# ml-metrics-to-data-usecase.md

Cheatsheet: **How ML metrics relate to concrete data and use cases (Azure ML v2 context)**

---

## 0. Scenario & Azure ML v2 pipeline

**Business scenario – Online bike webshop**

An online store sells bicycles (city, mountain, e-bike, kids). Goals:

1. **Predict the optimal selling price** for each bike → **Regression**  
2. **Predict which bikes will break soon (within 3 months)** → **Binary classification**

Typical Azure ML v2 flow:

> **Train → Score → Evaluate → (Maybe) Retrain**  
> - Train a model on historical bike data.  
> - Score validation / test data.  
> - Evaluate with metrics (MAE, RMSE, R², Accuracy, F1, AUC, etc.).  
> - If metrics are poor: adjust features/algorithms and retrain.

All examples below use **tiny toy datasets** so the link between **data → predictions → metrics** stays clear.

---

## 1. Base data: bike webshop example

Each row is a sold bike:

- **Features (X)**: `bike_type`, `brand`, `frame_material`, `gears`, `age_in_inventory_days`, `has_suspension`, …  
- **Regression target (y_reg)**: `sale_price_eur`  
- **Classification target (y_clf)**: `broke_within_3_months` (0 = no, 1 = yes)

Base sample (no predictions yet):

| bike_id | bike_type | brand     | frame_material | gears | age_in_inventory_days | has_suspension | sale_price_eur | broke_within_3_months |
|--------:|-----------|-----------|----------------|:-----:|----------------------:|:--------------:|----------------:|-----------------------:|
| 1       | city      | UrbanRide | aluminum       | 7     | 12                    | 0              | 450            | 0                     |
| 2       | mountain  | TrailPro  | aluminum       | 18    | 25                    | 1              | 890            | 1                     |
| 3       | e-bike    | VoltGo    | aluminum       | 10    | 40                    | 1              | 2200           | 0                     |
| 4       | kids      | FunBike   | steel          | 3     | 5                     | 0              | 190            | 0                     |
| 5       | mountain  | TrailPro  | carbon         | 22    | 30                    | 1              | 1450           | 1                     |
| 6       | city      | UrbanRide | steel          | 5     | 18                    | 0              | 380            | 0                     |

Three separate scenarios derived from this kind of data:

- **Scenario A:** GOOD regression model (price)  
- **Scenario B:** OK regression model (price)  
- **Scenario C:** BAD classification model (failure; imbalanced)

For each scenario:

1. Dataset with predictions  
2. Task type (Regression or Classification)  
3. Metrics table with:
   - Metric  
   - Simple description  
   - Interpretation for this scenario  
   - Example value  
   - Indicative “good range” for similar business cases

---

## 2. Scenario A – GOOD regression model (price prediction)

**Task type:** Regression – predict `sale_price_eur`.

### 2.1 Example dataset (GOOD predictions)

Model predictions are very close to real prices:

| bike_id | bike_type | Actual price (€) | Model prediction (€) |
|--------:|-----------|-----------------:|---------------------:|
| 1       | city      | 450              | 455                  |
| 2       | mountain  | 890              | 905                  |
| 3       | e-bike    | 2200             | 2180                 |
| 4       | kids      | 190              | 200                  |
| 5       | mountain  | 1450             | 1435                 |

Intuition: errors are tiny (a few euros) → strong pricing model.

### 2.2 Regression metrics for GOOD model

| Metric name | Simple description | Interpretation for this dataset | Example value (illustrative) | Typical “GOOD” range for this use case* |
|------------|--------------------|---------------------------------|------------------------------|-----------------------------------------|
| **MAE – Mean Absolute Error** | Average absolute difference between actual and predicted prices. Lower is better. | Average error per bike is only a few euros. | **≈ 15 €** | **\< 50 €** for bikes in ~200–2200 € range |
| **MSE – Mean Squared Error** | Average of squared errors; large errors contribute strongly. | Very low → no big outliers in pricing errors. | **≈ 250 €²** | Clearly below (price range)², e.g. **≪ 50 000 €²** |
| **RMSE – Root Mean Squared Error** | Square root of MSE; same units as price. | Typical error similar to MAE (~10–20 €), confirming tight predictions. | **≈ 16 €** | **\< 60 €** |
| **R² – Coefficient of determination** | Fraction of variance in price explained by model (1 = perfect, 0 = predict-mean). | Very high → almost all price variation captured. | **≈ 0.99** | **> 0.9** |
| **Normalized MAE** | MAE divided by typical price or price range; relative error. | Very small → average error ≈ 1–2 % of price. | **≈ 0.01–0.02** | **\< 0.05** (error \< 5 %) |
| **Normalized RMSE** | RMSE scaled by price level / range. | Also very small → robust across cheap and expensive bikes. | **≈ 0.015–0.02** | **\< 0.07** |
| **Spearman correlation** | Rank correlation between true price and predicted price. | Close to 1 → higher true price → higher predicted price almost always. | **≈ 0.99** | **> 0.9** |

\* “Good ranges” are rule-of-thumb values for this specific bike pricing context, not universal thresholds.

---

## 3. Scenario B – OK regression model (price prediction)

**Task type:** Regression – still predicting `sale_price_eur`.

### 3.1 Example dataset (OK predictions)

Predictions are in the right ballpark but often clearly off:

| bike_id | bike_type | Actual price (€) | Model prediction (€) |
|--------:|-----------|-----------------:|---------------------:|
| 1       | city      | 450              | 520                  |
| 2       | mountain  | 890              | 780                  |
| 3       | e-bike    | 2200             | 1950                 |
| 4       | kids      | 190              | 260                  |
| 5       | mountain  | 1450             | 1650                 |

Some bikes are overpriced, some underpriced, and high-priced bikes can be off by hundreds of euros.

### 3.2 Regression metrics for OK model

| Metric name | Simple description | Interpretation for this dataset | Example value (illustrative) | Typical “GOOD” range for this use case* |
|------------|--------------------|---------------------------------|------------------------------|-----------------------------------------|
| **MAE** | Average absolute price error. | Errors (~140 €) are noticeable; margins and competitiveness may suffer. | **≈ 140 €** | GOOD: **\< 50 €** → this is “OK but not great” |
| **MSE** | Average of squared errors. | Quite high → several large misses exist. | **≈ 30 000 €²** | GOOD: clearly **< 50 000 €²** here |
| **RMSE** | Typical error size in € (big errors penalised). | Often wrong by ~150–200 € → usable but risky for expensive bikes. | **≈ 175 €** | GOOD: **\< 60 €**; this is **medium / OK** |
| **R²** | How much of price variation is explained. | Captures part of the structure, but leaves a lot unexplained. | **≈ 0.6–0.7** | GOOD: **> 0.9**; “OK zone”: **0.5–0.8** |
| **Normalized MAE** | Error relative to typical price. | Errors ≈ 10–15 % of price → far from ideal. | **≈ 0.14** | GOOD: **\< 0.05**; OK: **0.05–0.2** |
| **Normalized RMSE** | Normalized RMSE. | Clearly worse than GOOD model; indicates noisy estimates. | **≈ 0.18** | GOOD: **\< 0.07** |
| **Spearman correlation** | Rank correlation between true & predicted prices. | Still positive – often ranks bikes correctly, but with misorderings. | **≈ 0.7–0.8** | GOOD: **> 0.9**; OK: **0.6–0.8** |

\* Again, ranges are rough guidelines for this scenario.

Retraining hint:  
MAE ≈ 140 € and R² ≈ 0.6 suggest a baseline that can be improved via feature engineering, hyper-parameter tuning, better algorithms (e.g. boosted trees), or more data.

---

## 4. Scenario C – BAD classification model (failure prediction, imbalanced)

**Task type:** Binary classification – predict `broke_within_3_months`.

Target:

- `0` = bike did **not** break within 3 months  
- `1` = bike **did** break within 3 months

### 4.1 Example dataset (BAD predictions)

Assume failures are **rare** (class imbalance).  
Model always predicts **“no failure”**:

| bike_id | bike_type | Actual broke? | Model probability “break soon” | Model predicted label |
|--------:|-----------|--------------:|-------------------------------:|----------------------:|
| 1       | city      | 0             | 0.10                           | 0                    |
| 2       | mountain  | 1             | 0.25                           | 0                    |
| 3       | e-bike    | 0             | 0.05                           | 0                    |
| 4       | kids      | 0             | 0.15                           | 0                    |
| 5       | mountain  | 1             | 0.30                           | 0                    |
| 6       | city      | 0             | 0.20                           | 0                    |

Confusion:

- True negatives (TN) = 4  
- False negatives (FN) = 2  
- True positives (TP) = 0  
- False positives (FP) = 0  

Accuracy = 4/6 ≈ 0.67, but the model **never detects failures**.

### 4.2 Classification metrics for BAD model (with imbalance)

| Metric name | Simple description | Interpretation for this dataset | Example value (illustrative) | Typical “GOOD” range for this use case* |
|------------|--------------------|---------------------------------|------------------------------|-----------------------------------------|
| **Accuracy** | (TP + TN) / all. Fraction of all bikes correctly classified. | ≈0.67 looks reasonable at first glance, but hides the fact that all failures are missed. | **≈ 0.67** | GOOD: **> 0.9**, and must be read together with recall/F1 for failures |
| **Precision (class 1)** | Of all bikes predicted “break soon”, how many really break? | Model never predicts class 1 → precision = 0 (or undefined → treated as 0). | **0** | GOOD: **> 0.7–0.8** |
| **Recall (class 1)** | Of all bikes that really break, how many are caught? TP / (TP + FN). | **0**: 0 % of failing bikes detected → unacceptable for quality control. | **0** | GOOD: **> 0.8** in risk/failure scenarios |
| **F1-score (class 1)** | Harmonic mean of precision and recall. | Also 0 → no skill on the “failure” class. | **0** | GOOD: **> 0.75** |
| **AUC-ROC** | Area under ROC curve: separation of positives vs negatives across thresholds (0.5 = random, 1 = perfect). | Probabilities barely separate failing vs healthy bikes → near random. | **≈ 0.5** | GOOD: **> 0.8**, very good: **> 0.9** |
| **Average Precision / PR AUC (class 1)** | Area under Precision–Recall curve for the positive (failure) class. | Very low → even top-scored bikes are rarely true failures. | **≈ 0.1–0.2** | With rare failures: **> 0.5** is strong |
| **Balanced accuracy** | Mean of recall for class 0 and class 1. Gives equal weight to both classes. | Recall₀ = 1, recall₁ = 0 → (1 + 0)/2 = 0.5. Highlights that the minority class is ignored. | **0.5** | GOOD: **> 0.8** |

\* For failure prediction / risk models, **recall, F1, PR AUC, balanced accuracy** typically matter more than raw accuracy.

Retraining hint:  
Any model with recall ≈ 0 for a critical class is effectively unusable for that business problem, regardless of accuracy. Class weighting, resampling methods (e.g. SMOTE), or different algorithms should be considered.

---

## 5. AUC, AUC_weighted & class imbalance

### 5.1 Plain AUC (ROC AUC)

- Measures the area under the ROC curve (TPR vs FPR).  
- Binary case → single number between 0 and 1:  
  - 0.5 ≈ random  
  - 1.0 = perfect separation.

### 5.2 Multi-class AUC & AUC_weighted

For **multi-class** problems (3+ classes):

- Compute **one-vs-rest AUC per class**: AUC₁, AUC₂, …  
- Combine via averaging:
  - **Macro AUC** – simple mean: each class has **equal weight**.  
  - **Weighted AUC / AUC_weighted** – weighted by class frequency.

So:

> **AUC_weighted** = average AUC across classes, weighted by how often each class appears.

### 5.3 Binary case: AUC vs AUC_weighted

- With only 2 classes, implementations often report a single ROC AUC.  
- Weighted ROC AUC and plain ROC AUC are typically identical or extremely close in practice.

### 5.4 How AUC_weighted relates to class imbalance

- AUC_weighted is useful for summarising performance on imbalanced multi-class data in a way that mirrors the real class distribution.  
- It **does not fix class imbalance** and can still hide poor performance on very small classes, because majority classes dominate the average.

Rule of thumb for this cheatsheet:

- Use **AUC_weighted** to summarise performance when a single number reflecting the actual class mix is needed.  
- Also check:
  - Per-class AUC  
  - Macro-averaged metrics  
  - For imbalanced setups: **F1, PR AUC, recall for minority classes**

---

## 6. Metric → Azure ML v2 naming quick map

When experiments run in **Azure Machine Learning (especially AutoML / Evaluate Model components)**, metrics appear under specific names.

### 6.1 Regression (Azure ML v2 / AutoML)

Typical regression metrics:

- `mean_absolute_error` (MAE)  
- `mean_squared_error` (MSE)  
- `root_mean_squared_error` (RMSE)  
- `normalized_mean_absolute_error` (Normalized MAE)  
- `normalized_root_mean_squared_error` (NRMSE)  
- `r2_score` (R²)  
- `spearman_correlation`

These map directly to the regression metric tables for **Scenario A** and **Scenario B**.

### 6.2 Classification (Azure ML v2 / AutoML)

Typical classification metrics:

- `accuracy`  
- `precision_score_*` (macro / micro / weighted variants)  
- `recall_score_*`  
- `f1_score_*`  
- `auc_weighted` / `roc_auc_score_*`  
- `average_precision_score_*` (PR AUC variants)  
- `balanced_accuracy`

These correspond to the metrics used in **Scenario C**.

---

## 7. Applying this cheatsheet in practice

1. **Identify the task type.**  
   - Price prediction → compare with **Scenario A/B (Regression)**.  
   - Failure / quality / risk prediction → compare with **Scenario C (Classification, imbalanced)**.

2. **Match the metrics.**  
   - Regression → MAE, RMSE, R², Normalized errors, Spearman.  
   - Classification → Accuracy, F1, Recall, AUC, PR AUC, Balanced accuracy.

3. **Compare to scenarios.**  
   - Do metric values look more like **GOOD**, **OK**, or **BAD** examples?  
   - Does model performance align with business risk (e.g., missing failures vs overpricing)?

4. **Decide next step.**  
   - **GOOD-like metrics** → ready for deployment and monitoring.  
   - **OK-like metrics** → candidate for further tuning or feature work.  
   - **BAD-like metrics**, especially for critical minority classes → do not deploy; revisit data, features, and algorithm choice.

