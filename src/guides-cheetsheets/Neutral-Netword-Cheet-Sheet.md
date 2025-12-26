# Neural Network Cheat Sheet (Azure ML Context)

Let’s go one by one and then map each type to **typical tasks** and **how you’d use it in Azure ML (v2)**.

---

## 1. MLP – Multilayer Perceptron

### What it is  
The “classic” neural network:

- Layers of fully connected neurons (Dense layers).
- Data flows only forward (no loops, no recurrence).
- Non-linear activations (ReLU, sigmoid, etc.) between layers.

### What it’s good for

- **Tabular data** (most business data in tables):
  - Customer churn prediction
  - Credit scoring
  - Sales prediction, pricing
- **Simple classification / regression**:
  - “Will the passenger buy extra baggage?” (yes/no)
  - “Expected flight delay in minutes” (number)

MLP is often your **first deep learning baseline**.

### How to use in Azure ML

**Option A – AutoML (tabular)**  
You don’t even need to write the MLP yourself:

- Create an **AutoML job** for:
  - `classification` / `regression` / `forecasting`
- Azure AutoML may try deep models (MLPs) among others.
- You just:
  - Register your dataset (MLTable)
  - Define target column
  - Submit AutoML job
  - Pick the best model and deploy.

**Option B – Custom training (PyTorch / TensorFlow)**  

1. **Write training script** (e.g. `train.py`) with your MLP.
2. Create a **command job** in Azure ML:
   - `code: ./src`
   - `command: python train.py --data_path ${{inputs.data}} --epochs 20`
   - `environment`: curated PyTorch / TensorFlow env.
   - `inputs`: bind to your MLTable or URI folder.
   - `compute`: CPU or GPU cluster.
3. Use the SDK/CLI to:
   - Submit the job  
   - Log metrics  
   - Register the trained model  
   - Deploy to **online endpoint** for real-time predictions or **batch endpoint**.

---

## 2. CNN – Convolutional Neural Network

### What it is  
Network with **convolution layers** that:

- Look at **local patches** of the input (e.g. 3×3 region in an image).
- Share weights across the whole image.
- Often followed by pooling and fully connected layers.

### What it’s good for

- **Images**:
  - Image classification (Is this a damaged turbine blade?).
  - Object detection (Find suitcases vs people in security footage).
  - Segmentation (which pixels are “ice” vs “water”).
- **1D signals**:
  - Time series (sensor data, audio)
  - Some NLP models (1D conv over tokens).

### How to use in Azure ML

**Option A – AutoML for vision**  
Azure ML has **AutoML for images** (v2):

- Tasks: `image-classification`, `image-object-detection`, `image-instance-segmentation`.
- You:
  - Store images in Blob.
  - Create MLTable describing the images + labels.
  - Run an AutoML vision job → it trains several CNN architectures for you.
  - Deploy the best model as an endpoint.

**Option B – Custom CNN (PyTorch / TF)**  

1. Implement CNN model in PyTorch/TF.
2. Use a **GPU compute cluster** (e.g. `Standard_NC6s_v3`) in Azure ML.
3. Training via command job or pipeline job:
   - Data mounted or downloaded from Blob / DataLake.
4. Track:
   - Loss / accuracy via MLflow logging.
5. Register the model and deploy as:
   - **Real-time endpoint** for per-image predictions.
   - **Batch endpoint** for large offline scoring of image sets.

---

## 3. RNN – Recurrent Neural Network (LSTM / GRU)

### What it is  
Network designed for **sequences**:

- Processes data step-by-step (time step t, then t+1, etc.).
- Maintains a **hidden state** that carries information from previous steps.
- Practical variants: **LSTM** and **GRU** (solve simple RNN’s vanishing gradient problem).

### What it’s good for

- **Time series & sequential data**:
  - Demand forecasting.
  - Sensor readings over time.
  - Flight delays as a sequence of time-dependent factors.
- **Language / text** (though transformers dominate now):
  - Sentiment analysis.
  - Text classification.
  - Sequence labeling (e.g., NER).

Today, you’ll often use **transformers** instead of RNNs for NLP, but RNNs are still valid in simpler or resource-constrained scenarios.

### How to use in Azure ML

Azure ML doesn’t give you “RNN button,” but you can **bring your own**:

1. **Custom script** with PyTorch/TF:
   - Define LSTM/GRU model.
   - Prepare sequence datasets (padding, batching).
   - Train with GPU (recommended for larger models).
2. Use **time series** datasets from your DataLake / Blob.
3. Submit as **command job** or as part of a **pipeline**:
   - Step 1: data prep/splitting.
   - Step 2: training job for the RNN.
   - Step 3: evaluation & metrics logging.
4. Register model & deploy:
   - Real-time endpoint for “predict next step” style APIs.
   - Batch endpoint for forecasting large ranges at once.

**Alternative:** AutoML time-series (forecasting)  
- AutoML often uses **tree-based** and **DNN-based** models under the hood.  
- You don’t control exact architecture, but it’s great if you just want “best forecasting model” quickly without hand-building an RNN.

---

## 4. GAN – Generative Adversarial Network

### What it is  

Two networks trained together:

- **Generator (G)**: tries to generate realistic data (image, audio, etc.) from random noise or latent vectors.
- **Discriminator (D)**: tries to distinguish real data from generated data.
- They “fight” each other (adversarial training) until the generator produces data that the discriminator can’t easily distinguish from real.

### What it’s good for

- **Generating new samples**:
  - Synthetic images (e.g. satellite imagery, art, people, etc.).
- **Data augmentation**:
  - Create extra training images where real data is scarce.
- **Anomaly detection**:
  - Train GAN on “normal” data, then see where it fails → potential anomalies.
- **Image-to-image** tasks:
  - Super-resolution, style transfer, denoising.

GANs are powerful but **harder to train** (instability, mode collapse).

### How to use in Azure ML

Always **custom** (no AutoML for GANs):

1. Implement GAN in PyTorch/TF.
   - Define Generator & Discriminator.
   - Training loop with alternating G and D steps.
2. Use Azure ML to:
   - Run your training on **GPU clusters**.
   - Log metrics and sample images to track progress.
3. Register **generator model** (usually the part you deploy).
4. Deploy:
   - **Batch endpoint** to generate lots of synthetic data.
   - **Real-time endpoint** for “on demand” generation (careful with latency and GPU costs).

**Responsible AI** note:  
If you generate realistic faces / documents / voices, you need policies around **deepfakes, misuse, and disclosure**. For enterprise projects, this must be documented (RAI).

---

## Putting it all together – quick cheat sheet

| Type | Intuition | Best for | Typical Azure ML usage |
|------|-----------|----------|------------------------|
| **MLP** | Fully connected layers | Tabular data, simple classification/regression | AutoML (tabular) or custom PyTorch/TF command job; deploy to online/batch endpoint |
| **CNN** | Convolutions over local patches | Images, 1D signals, some time series | AutoML for vision (image tasks) or custom CNN training on GPU; deploy |
| **RNN (LSTM/GRU)** | Keeps hidden state across steps | Time series, sequences, simpler NLP tasks | Custom training on sequence data (command job/pipeline); or AutoML forecasting (black box DL) |
| **GAN** | Generator vs discriminator | Data generation, augmentation, anomaly detection, image-to-image | Custom PyTorch/TF on GPUs; focus on experiment tracking & RAI; deploy generator for batch/online generation |
