# ai-ml-flow-cheatsheet.md

## 1. High-Level Flow

Standard machine learning workflow:

1. **Train** – teach the model using labeled data  
2. **Score** – use the trained model to make predictions on new data  
3. **Evaluate** – measure how good the predictions are with metrics  

Short form:

> **Train → Score → Evaluate**

---

## 2. Train

### What is Training?

Training is the process where a machine learning model **learns patterns** from historical data.

- Input:  
  - Features (X) – columns used for prediction  
  - Labels/Targets (y) – correct answers
- Output:  
  - A **trained model** with internal parameters adjusted to fit the data

### Intuition

- The model sees many examples (features + correct label)
- The model adjusts internal parameters to minimize error (e.g., loss function)
- After training, the model should be able to generalize to unseen data

---

## 3. Score

### What is Scoring?

Scoring is the process of **using a trained model to make predictions** on a dataset.

- Input:  
  - Trained model  
  - New data (often **validation** or **test** set after a train/test split)
- Output:  
  - Predictions (e.g., class labels, probabilities, or numeric values)

### Typical Usage

- After splitting data into **train** and **test**:
  - Train set → used for **training**
  - Test set → used for **scoring** and **evaluation**
- The model is applied to the test set to generate predicted values

In Azure ML Designer, this is typically done with the **“Score Model”** component.

---

## 4. Evaluate

### What is Evaluation?

Evaluation is the process of **comparing predictions to the true labels** and calculating **quality metrics**.

- Input:  
  - Predictions from the scoring step  
  - True labels (ground truth) from the dataset
- Output:  
  - Metrics that describe model performance

### Examples of Metrics

**Classification**

- **Accuracy** – fraction of correct predictions  
- **Precision** – fraction of predicted positives that are actually positive  
- **Recall** – fraction of actual positives that were correctly found  
- **F1 score** – harmonic mean of precision and recall  
- **AUC (Area Under ROC Curve)** – ability to separate classes at different thresholds

**Regression**

- **MSE (Mean Squared Error)** – average of squared differences between predicted and actual values  
- **RMSE (Root Mean Squared Error)** – square root of MSE, in same units as target  
- **MAE (Mean Absolute Error)** – average of absolute differences  
- **R² (Coefficient of Determination)** – how much variance in the target is explained by the model

In Azure ML Designer, this is typically done with the **“Evaluate Model”** component.

---

## 5. Order of Operations (Conceptual + Azure ML)

### Conceptual ML Workflow

1. **Train** – fit model on training data  
2. **Score** – generate predictions on validation/test data  
3. **Evaluate** – compute metrics based on predictions vs. true labels  

### Azure ML Designer Example

Typical Azure ML Designer pipeline:

1. **Split Data**  
   - Split into train and test sets (e.g., 70% train, 30% test)

2. **Train Model**  
   - Component: **Train Model**  
   - Input: training portion of data + algorithm  
   - Output: trained model

3. **Score Model**  
   - Component: **Score Model**  
   - Input: trained model + test dataset  
   - Output: scored dataset (predictions + original labels)

4. **Evaluate Model**  
   - Component: **Evaluate Model**  
   - Input: scored dataset  
   - Output: evaluation metrics (e.g., accuracy, AUC, errors)

---

## 6. Summary Table

| Step      | Main Question                          | Input                           | Output                    | Azure ML (Designer)       |
|----------|-----------------------------------------|---------------------------------|---------------------------|---------------------------|
| Train    | How should the model learn?            | Train data (features + labels)  | Trained model             | **Train Model**           |
| Score    | What does the model predict?           | Trained model + test data       | Predictions (scores)      | **Score Model**           |
| Evaluate | How good are these predictions overall?| Predictions + true labels       | Metrics (AUC, MSE, etc.) | **Evaluate Model**        |

Core idea:

> **Train the model → Score on test data → Evaluate with metrics**
