# 🌾 KrishiRakshak AI

### AI-Powered Rice Pest Identification, Growth Stage Detection & Crop Protection

KrishiRakshak AI is an artificial intelligence-powered agricultural support platform developed as part of the **Smart India Hackathon (SIH)**.

The platform helps farmers identify rice pests from uploaded images, detect their growth stages, and receive suitable control measures and recommendations to support crop protection and agricultural decision-making.

## 🚀 Key Features

- **Rice Pest Identification:** Identify rice pests using image-based machine learning.
- **Growth Stage Detection:** Detect the growth stages of identified pests.
- **Early-Stage Detection:** Dedicated early-stage detection model.
- **AI-Based Recommendations:** Provide stage-specific pest control prescriptions.
- **Agricultural Knowledge Base:** Use structured agricultural information to support recommendations.
- **Farmer-Oriented Interface:** Designed to make pest identification and crop protection guidance accessible.

## 🧠 Technology Stack

- Python
- PyTorch
- Machine Learning
- Gradio
- Gemini API
- Image Processing
- JSON-based Knowledge Base

## 📂 Project Structure

```text
KrishiRakshakAI/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── backend/
│
├── data/
│   ├── class_names.json
│   ├── knowledge_base.json
│   └── early_stage_dataset/
│
├── ml/
│   ├── model.pth
│   ├── inference.py
│   ├── stage_detector.py
│   ├── stage_prescriptions.py
│   └── train_mobilenet.py
│
├── original_data/
│
├── safety/
│
└── training/
    ├── early_stage_model.pth
    └── train_early_stage.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shreyasnigam01/KrishiRakshak-AI.git
cd KrishiRakshak-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key or `.env` file to GitHub.

### 5. Run the application

```bash
python app.py
```

## 📊 Dataset and Models

The project includes trained machine-learning models and supporting agricultural datasets.

The main dataset is excluded from this repository to keep the Git repository lightweight. Dataset access and provenance should be documented separately.

Included model files:

- `ml/model.pth`
- `training/early_stage_model.pth`

## 👥 Team & Contributors

Developed as part of the **Smart India Hackathon (SIH)**.

- **Shreyas Nigam** – Project Developer
- **Kunsh Billa** – Project Developer

GitHub profiles:

- [Shreyas Nigam](https://github.com/shreyasnigam01)
- [Kunsh Billa](https://github.com/JinxedHuracan)

## 🎯 Project Objective

To leverage artificial intelligence and machine learning for accessible agricultural intelligence, helping farmers identify rice pests, understand their growth stages, and make informed crop protection decisions.

## ⚠️ Disclaimer

KrishiRakshak AI is an agricultural decision-support project. Recommendations should be validated against local agricultural guidance and expert advice before implementation.

## 📄 License

A license will be added after the project contributors agree on the appropriate licensing terms.# 🌾 KrishiRakshak AI

### AI-Powered Rice Pest Identification, Growth Stage Detection & Crop Protection

KrishiRakshak AI is an artificial intelligence-powered agricultural support platform developed as part of the **Smart India Hackathon (SIH)**.

The platform helps farmers identify rice pests from uploaded images, detect their growth stages, and receive suitable control measures and recommendations to support crop protection and agricultural decision-making.

## 🚀 Key Features

- **Rice Pest Identification:** Identify rice pests using image-based machine learning.
- **Growth Stage Detection:** Detect the growth stages of identified pests.
- **Early-Stage Detection:** Dedicated early-stage detection model.
- **AI-Based Recommendations:** Provide stage-specific pest control prescriptions.
- **Agricultural Knowledge Base:** Use structured agricultural information to support recommendations.
- **Farmer-Oriented Interface:** Designed to make pest identification and crop protection guidance accessible.

## 🧠 Technology Stack

- Python
- PyTorch
- Machine Learning
- Gradio
- Gemini API
- Image Processing
- JSON-based Knowledge Base

## 📂 Project Structure

```text
KrishiRakshakAI/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── backend/
│
├── data/
│   ├── class_names.json
│   ├── knowledge_base.json
│   └── early_stage_dataset/
│
├── ml/
│   ├── model.pth
│   ├── inference.py
│   ├── stage_detector.py
│   ├── stage_prescriptions.py
│   └── train_mobilenet.py
│
├── original_data/
│
├── safety/
│
└── training/
    ├── early_stage_model.pth
    └── train_early_stage.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shreyasnigam01/KrishiRakshak-AI.git
cd KrishiRakshak-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key or `.env` file to GitHub.

### 5. Run the application

```bash
python app.py
```

## 📊 Dataset and Models

The project includes trained machine-learning models and supporting agricultural datasets.

The main dataset is excluded from this repository to keep the Git repository lightweight. Dataset access and provenance should be documented separately.

Included model files:

- `ml/model.pth`
- `training/early_stage_model.pth`

## 👥 Team & Contributors

Developed as part of the **Smart India Hackathon (SIH)**.

- **Shreyas Nigam** – Project Developer
- **Kunsh Billa** – Project Developer

GitHub profiles:

- [Shreyas Nigam](https://github.com/shreyasnigam01)
- [Kunsh Billa](https://github.com/JinxedHuracan)

## 🎯 Project Objective

To leverage artificial intelligence and machine learning for accessible agricultural intelligence, helping farmers identify rice pests, understand their growth stages, and make informed crop protection decisions.

## ⚠️ Disclaimer

KrishiRakshak AI is an agricultural decision-support project. Recommendations should be validated against local agricultural guidance and expert advice before implementation.

## 📄 License

A license will be added after the project contributors agree on the appropriate licensing terms.
