# hyperparameter-tuning-cheatsheet.md

## What hyperparameter tuning is
Process of searching hyperparameter values to maximize a chosen validation metric while avoiding overfitting. Typical goal: better generalization on unseen data.

---

## Quick workflow (order that works)
1. **Define search space** — which hyperparameters will be tuned and their ranges/choices.  
2. **Pick sampling method** — how candidates are selected from the space.  
3. **Set objective & budget** — primary metric + direction (maximize/minimize), number of trials, parallelism, time limit.  
4. **Enable early termination** — stop poorly performing runs to save time/cost.  
5. **Track results** — log metrics/params/artifacts for comparison and reproducibility.

---

## Sampling methods (how candidates are chosen)
- **Grid**: tries **every** combination from discrete lists. Deterministic; explodes with many options.
- **Random**: samples combinations uniformly at random; covers large spaces well with fixed budgets.
- **Sobol (quasi-random)**: low-discrepancy sequence; spreads points more evenly than pure random.
- **Bayesian**: model-based, learns from previous trials and proposes promising next points (sample-efficient; best with continuous, moderate-dimensional spaces).  
  *Note:* does **not** try all combinations; no guarantee of the absolute global optimum.

---

## Search space types (common distributions)
- **Choice([...])** — discrete set, e.g., `reg_rate ∈ {0.01, 0.1, 1.0}`.
- **Uniform(min, max)** — flat range.
- **LogUniform(min, max)** — uniform in log-space (great for rates over orders of magnitude).
- **Normal(μ, σ)** — bell curve around a mean.
- **QUniform(min, max, q)** — like Uniform but **quantized**; only values `min + k·q`.  
  *q = step size (quantum).*
- **QNormal(μ, σ, q)** — Normal, then snapped to step `q`.
- **RandInt(upper)** — integer range.

**Tip:** rates (learning rate, weight decay/regularization) usually benefit from **log-scale** ranges.

---

## Early termination (stop weak runs early)
- **Bandit**: stop a run if it lags the current best by more than a tolerance (`slack_factor`/`slack_amount`) after a grace period.
- **Median stopping**: stop if performance at a given step is worse than the median of completed runs.
- **Truncation**: periodically remove the worst X% of active runs.

Set an **evaluation interval** and a **warm-up** (grace) phase to avoid killing late-bloomers. Ensure metric direction (maximize/minimize) is correct.

---

## Picking metrics (classification example)
- **ROC-AUC**: probability a random positive scores higher than a random negative; threshold-free ranking quality.
- **PR-AUC**: preferred when positives are rare (class imbalance).  
AUC values guide quality (≈0.5 random; ≥0.8 good; ≥0.95 excellent—check for leakage).

---

## Preventing overfitting while tuning
- Prefer **simpler models** or stronger **regularization** when gaps appear between train and validation.
- Use **cross-validation** for robust estimates.
- Keep a final **hold-out test set** unseen during tuning.

---

## Example: regularization sweep
```python
# Discrete choices (weak → strong)
reg_rate = Choice(values=[1e-2, 1e-1, 1.0])

# Or log-scale range across orders of magnitude
reg_rate = LogUniform(min_value=1e-6, max_value=1e-1)
