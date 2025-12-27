# azure-ml-ai-foundry-labs-hub

Hands-on **Azure Machine Learning (DP-100)** and **Microsoft AI Foundry / Azure AI Studio (AI Engineer)** notebooks, artifacts, and cheatsheets — covering classic ML, MLOps, Responsible AI, privacy techniques, and GenAI patterns (RAG + fine-tuning).

> **Sources & attribution:** This repo is based on and extends the official MicrosoftLearning labs:
> - Azure ML (DP-100): https://github.com/MicrosoftLearning/mslearn-azure-ml/blob/main/index.md  
> - AI Studio / AI Foundry: https://github.com/MicrosoftLearning/mslearn-ai-studio/blob/main/index.md  
> Content here is **expanded** with additional explanations, examples, screenshots, troubleshooting, and reusable templates.

_NOTE_: Repository in work/progress phase some section will be updated and reworked. 

---

## Table of contents
- [What you’ll find here](#what-youll-find-here)
- [Repository layout](#repository-layout)
- [Notebooks index](#notebooks-index)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Responsible AI (RAI) dashboards](#responsible-ai-rai-dashboards)
- [Privacy & SmartNoise](#privacy--smartnoise) [in progress]
- [GenAI: RAG + fine-tuning](#genai-rag--fine-tuning) [in progress]
- [Cheatsheets](#cheatsheets)
- [Artifacts & large files](#artifacts--large-files)
- [Contributing](#contributing)
- [License & disclaimer](#license--disclaimer)
- [Acknowledgements](#acknowledgements)

---

## What you’ll find here

This repository is designed as a **single hub** for practical, exam-aligned, real-world Azure ML + AI Foundry work:

### Classic ML + MLOps (DP-100-aligned)
- Training & evaluation notebooks (regression/classification)
- Custom environments and reproducible runs
- Hyperparameter tuning
- MLflow tracking + model registry patterns
- Pipelines (training → scoring → evaluation)
- Deployment endpoints (managed online endpoints / batch patterns)
- Model artifacts & run outputs (where appropriate)

### Responsible AI + governance
- Responsible AI dashboards (model explanations, error analysis, fairness)
- Reproducible evaluation patterns and reporting
- Notes on common pitfalls & interpretation tips

### Privacy engineering
- Privacy-aware data practices and examples
- Usage examples with **SmartNoise** (or similar DP tooling where applicable)

### GenAI (AI Foundry / Azure AI Studio-aligned) [in progress]
- RAG with **Azure AI Search**
- Promptflow / orchestration patterns (where used)
- Fine-tuning patterns for LLMs (where supported/available in your tenant)
- Practical evaluation notes for LLM apps (quality + safety)

### Cheatsheets & learning notes
- ML/LLM metrics cheat sheets + small examples
- Simplified neural network definitions (MLP/CNN/RNN/GAN, etc.)
- ML algorithms explained in “plain English”
- Troubleshooting playbook for common Azure issues

---


Notebooks index
---------------

### DP-100 / Azure ML notebooks

Located under: `notebooks/dp100-azure-ml/`

-   **01-train-custom-environments-automl.ipynb**\
    Custom environments, training runs, and AutoML patterns.

-   **02-diabetes-class-mlflow-tracking.ipynb**\
    Experiment tracking with MLflow, logging metrics/artifacts.

-   **03-hyperparm.ipynb**\
    Hyperparameter tuning patterns and sweep concepts.

-   **03-ml-flow.ipynb**\
    MLflow fundamentals (tracking + model packaging patterns).

-   **04-pipelines.ipynb**\
    Pipelines: training → scoring → evaluation.

-   **05-responsible-ai.ipynb**\
    Responsible AI: explanations, error analysis, fairness workflow.

-   **06-mlflow-autolog.ipynb**\
    Autologging patterns and how to interpret runs/metrics.

-   **07-endpoints.ipynb**\
    Deployment endpoints and scoring patterns.

### AI Foundry / Azure AI Studio notebooks

Located under: `notebooks/ai-foundry/`

-   **rag-azure-ai-search/**\
    Indexing, retrieval, grounding patterns, evaluation notes.

-   **fine-tuning/**\
    Fine-tuning workflows (where supported), dataset formatting, evaluation.

-   **evaluation/**\
    LLM app evaluation patterns (quality + safety), logging, dashboards.

* * * * *

Prerequisites
-------------

You can run most notebooks **directly in Azure ML Studio / AI Foundry**.\
For local execution, you'll typically need:

-   An Azure subscription with access to:

    -   Azure ML workspace (DP-100 content)

    -   AI Foundry / Azure AI Studio (GenAI content)

    -   Azure Storage (used by both)

    -   (GenAI) Azure AI Search (for RAG)

-   Azure CLI + ML extension (optional but useful)

-   Python 3.10+ (recommended)

-   Permission to create compute / endpoints (or a pre-provisioned environment)

* * * * *

Quickstart
----------

### Option A --- Run in Azure ML Studio / AI Foundry (recommended)

1.  Create or open your **Azure ML Workspace** or **AI Foundry Project**.

2.  Upload the relevant notebook folder from `notebooks/`.

3.  Select a compute (or create one).

4.  Run cells top-to-bottom.

### Option B --- Run locally (optional)

1.  Clone the repo:

1.  `az login `

> Notes:
>
> -   Some notebooks assume Studio-managed identities and compute. Local execution may require extra auth setup.
>
>
> -   For endpoint deployments, ensure your account has permission to create managed online endpoints.

* * * * *

Responsible AI (RAI) dashboards
-------------------------------

Responsible AI dashboards typically include:

-   **Model explanations** (global/local feature importance)

-   **Error analysis** (where predictions fail)

-   **Fairness** analysis (distribution + disparity insights)

Recommended practice:

-   Keep **evaluation datasets** versioned (or reproducible).

-   Save key dashboard screenshots under:

    -   `artifacts/rai/`

    -   `artifacts/screenshots/`

If a notebook produces a dashboard, document:

-   model name/version

-   dataset used

-   compute used

-   dashboard configuration (e.g., class labels, sensitive features)

* * * * *

Privacy & SmartNoise
--------------------

Where privacy techniques are demonstrated:

-   Use **only non-sensitive / synthetic** data in this repository.

-   Avoid committing any customer data, IDs, secrets, or endpoints.

Recommended:

-   Put privacy notebooks under `notebooks/dp100-azure-ml/privacy/`

-   Put library notes and examples under `guides/` or `cheatsheets/`

* * * * *

GenAI: RAG + fine-tuning
------------------------

### RAG with Azure AI Search

Typical components you'll see in the RAG notebooks:

-   ingestion (documents → chunks)

-   embeddings

-   AI Search index creation

-   retrieval + grounding

-   evaluation (quality + safety)

Store:

-   sample docs under `artifacts/sample-data/` (only if redistributable)

-   screenshots of indexes and evaluation under `artifacts/screenshots/`

### Fine-tuning

Fine-tuning notebooks (where supported) focus on:

-   dataset formatting

-   training job configuration

-   evaluation strategy (offline + human review checkpoints)

-   deployment notes

> Important: Fine-tuning availability and exact steps can vary by tenant, region, and model.

* * * * *

Cheatsheets
-----------

Located under: `cheatsheets/`

This section is intended to be **fast to scan** and practical:

-   **ML metrics**: definitions + how to interpret + small examples

-   **LLM evaluation**: quality, groundedness, relevance, safety signals

-   **Neural networks**: MLP/CNN/RNN/GAN and "what they're good for"

-   **Algorithms**: simplified explanations for common models

* * * * *

Artifacts & large files
-----------------------

### Trained models

Prefer saving models in **MLflow format** and storing only what's needed:

-   `/models/<model-name>/...`

### Screenshots & dashboards

-   `/screenshots/`


### Git LFS (recommended)

If you store larger model artifacts, enable Git LFS:

`git lfs install
git lfs track "*.pkl"  "*.onnx"  "*.pt"  "*.joblib"  "*.zip"  `

> Tip: Avoid committing large, auto-generated outputs (logs, cache, temp files).

* * * * *

Contributing
------------

Contributions are welcome if they improve clarity and reusability:

-   Add explanations, diagrams, or troubleshooting notes

-   Improve notebook robustness (idempotency, better error handling)

-   Add "exam hints" sections (without copying protected exam content)

Suggested workflow:

1.  Create a branch

2.  Keep changes scoped (one notebook/guide per PR)

3.  Add screenshots only when they add real value

4.  Never include secrets or sensitive data

* * * * *

License & disclaimer
--------------------

-   This repository contains **original notes and extensions** built on top of publicly available MicrosoftLearning labs.

-   Follow the licenses in the referenced MicrosoftLearning repositories for any reused content.

-   **No affiliation** with Microsoft is implied.

-   Do not upload proprietary, customer, or confidential data.

> If you add a LICENSE file: MIT is common for your own content, but ensure it doesn't conflict with any upstream terms.

* * * * *

Acknowledgements
----------------

-   MicrosoftLearning Azure ML labs: <https://github.com/MicrosoftLearning/mslearn-azure-ml>

-   MicrosoftLearning AI Studio / AI Foundry labs: <https://github.com/MicrosoftLearning/mslearn-ai-studio>

If you find this useful, consider starring the upstream MicrosoftLearning repos as well.

* * * * *

Todos
--------------------------------------------------

-   Add `requirements.txt` / `environment.yml` aligned to the notebooks

-   Add a `guides/setup-azure-ml.md` with workspace + compute setup screenshots

-   Add a `guides/setup-ai-foundry.md` with project + connections setup

-   Add `cheatsheets/ml-metrics.md` and `cheatsheets/llm-metrics.md`

-   Add `.gitignore` for notebook outputs and local caches

-   `git clone https://github.com/boriszn/azure-ml-ai-foundry-labs-hub.git cd azure-ml-ai-foundry-labs-hub `

    -   Create a virtual environment:

    -   `python -m venv .venv source .venv/bin/activate # macOS/Linux  # .\.venv\Scripts\activate  # Windows PowerShell  `

    -   Install deps (adjust as needed per notebook):

    -   `pip install -r requirements.txt `

    -   Authenticate (if using Azure SDK/CLI workflows):

