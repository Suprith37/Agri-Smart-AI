# 🌱 Agri Smart AI

> **AI-powered precision agriculture system for plant disease detection, crop recommendation, fertilizer recommendation, and weather-based farming insights.**

## 📌 Overview

**Agri Smart AI** is an AI-powered agricultural advisory system designed to help farmers make better, data-driven farming decisions. The system combines **Machine Learning, Deep Learning, soil data, historical agricultural data, and weather information** into a single web-based platform.

It provides three major agricultural recommendations:

* 🌿 **Plant Disease Detection** using CNN
* 🌾 **Crop Recommendation** using Random Forest
* 🧪 **Fertilizer Recommendation** based on soil nutrient conditions
* 🌦️ **Weather Forecasting** for improved agricultural planning

The goal is to **improve crop productivity, reduce resource wastage, and promote sustainable agriculture**.

---

## 🚀 Key Features

### 🌿 Plant Disease Detection

A **Convolutional Neural Network (CNN)** is trained using **38,000+ leaf images** from the PlantVillage dataset.

* Detects **38 different plant diseases**
* Achieves **99.55% accuracy**
* Supports early disease identification
* Helps reduce potential crop damage

### 🌾 Crop Recommendation

A **Random Forest classifier** analyzes agricultural conditions to recommend suitable crops.

The recommendation considers:

* Soil conditions
* NPK values
* Climate conditions
* Historical crop yield data

**Accuracy: 95.12%**

### 🧪 Fertilizer Recommendation

The system provides fertilizer suggestions based on:

* Soil nutrient levels
* Crop requirements
* NPK conditions
* Crop growth stage

This helps reduce unnecessary fertilizer usage and nutrient wastage.

### 🌦️ Weather Integration

Weather information is incorporated to support better agricultural decision-making and improve the relevance of crop and fertilizer recommendations.

### 💻 Web-Based Platform

All the modules are integrated into a single, user-friendly web interface, allowing farmers to access AI-based agricultural insights from one platform.

---

## 🧠 System Workflow

```text
             ┌─────────────────────┐
             │      User Input      │
             │                     │
             │ Leaf Image / Soil   │
             │ Data / Crop Details │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │   Data Processing   │
             │                     │
             │ Image Preprocessing │
             │ Data Normalization  │
             └──────────┬──────────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
    ┌─────────────────┐   ┌──────────────────┐
    │   CNN Model     │   │ Random Forest    │
    │                 │   │                  │
    │ Disease         │   │ Crop             │
    │ Detection       │   │ Recommendation   │
    └────────┬────────┘   └─────────┬────────┘
             │                      │
             ▼                      ▼
    ┌─────────────────┐   ┌──────────────────┐
    │ Disease Result  │   │ Crop Suggestion  │
    └─────────────────┘   └─────────┬────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │ Fertilizer Advice  │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Weather Information│
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │  Final Agricultural│
                         │    Recommendations │
                         └────────────────────┘
```

---

## 📊 Dataset

### PlantVillage Dataset

Used for plant disease detection.

* **38,000+ images**
* **15 plant species**
* **38 disease classes**
* Used to train the CNN disease classification model

### Indian Agricultural Production Dataset

Used for agricultural analysis and crop recommendation.

* **46 years of agricultural data**
* Covers **1970–2015**
* Includes crop production
* Includes cultivated area
* Includes yield-related information
* Provides historical agricultural trends

---

## 🤖 Machine Learning Models

| Task                    | Model         |   Accuracy |
| ----------------------- | ------------- | ---------: |
| Plant Disease Detection | CNN           | **99.55%** |
| Crop Recommendation     | Random Forest | **95.12%** |

The CNN model demonstrated strong performance in plant disease classification, while Random Forest achieved the best performance among the evaluated models for crop recommendation.

---

## 🛠️ Technology Stack

### Machine Learning & AI

* Python
* TensorFlow / PyTorch
* Scikit-learn
* OpenCV

### Data Processing

* NumPy
* Pandas
* Matplotlib

### Backend

* Flask

### Datasets

* PlantVillage Dataset
* Indian Agricultural Production Dataset
* Kaggle

---

## 📁 Project Structure

```text
Agri-Smart-AI/
│
├── dataset/
│   ├── plant_disease/
│   └── agricultural_data/
│
├── models/
│   ├── disease_detection/
│   └── crop_recommendation/
│
├── preprocessing/
│
├── static/
│
├── templates/
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

> The exact project structure may vary depending on the implementation.

---

## ⚙️ Methodology

### 1. Data Collection

Agricultural datasets containing plant images, soil information, crop data, and weather information are collected.

### 2. Data Preprocessing

Images are resized, normalized, enhanced, and augmented. Structured data is cleaned, normalized, and scaled.

### 3. Disease Detection

The CNN extracts visual features from leaf images and classifies them into different disease categories.

### 4. Crop Recommendation

Random Forest analyzes soil, climate, and historical agricultural information to recommend suitable crops.

### 5. Fertilizer Recommendation

The system analyzes soil nutrient conditions and crop requirements to provide suitable fertilizer suggestions.

### 6. System Integration

All modules are integrated into a web-based platform to provide farmers with a unified agricultural advisory system.

---

## 📈 Results

The proposed system achieved:

* **99.55% accuracy** in plant disease detection
* **95.12% accuracy** in crop recommendation
* Effective fertilizer recommendations based on soil conditions
* Integration of weather information for improved decision-making
* A unified platform for multiple agricultural requirements

---

## 🎯 Problem Addressed

Traditional agricultural practices face several challenges:

* Manual disease identification can be slow and requires expert knowledge.
* Improper fertilizer usage can cause nutrient wastage and soil degradation.
* Crop selection may not adequately consider soil and climate compatibility.
* Existing agricultural solutions often address individual problems rather than providing an integrated solution.

**Agri Smart AI** aims to address these challenges through a single AI-powered platform.

---

## 🔮 Future Scope

Future improvements include:

* 📚 Expanding crop and disease datasets
* 📡 Integrating real-time agricultural sensors
* 🌍 Improving adaptability across different farming environments
* 🗣️ Adding multilingual support
* 📱 Improving accessibility through mobile applications
* 📴 Supporting offline operation in areas with limited internet connectivity

---

## 👥 Team

**Agri Smart AI** was developed by students from the
**Department of Computer Science and Engineering,
The National Institute of Engineering, Mysore.**

---

## 📄 Research Paper

This project is based on the research paper:

**"Agri Smart AI: Crop and Fertilizer Advisor with Leaf Disease Detection Using Machine and Deep Learning"**

Published in the **2025 International Conference on Intelligent Computing and Knowledge Extraction (ICICKE)**.

---

## ⭐ Project Highlights

```text
🌿 38+ Plant Disease Classes
🖼️ 38,000+ Training Images
🧠 CNN-Based Disease Detection
🌾 Random Forest Crop Recommendation
🧪 Fertilizer Recommendation
🌦️ Weather Integration
📊 Data-Driven Agricultural Insights
💻 Web-Based Platform
🎯 99.55% Disease Detection Accuracy
🎯 95.12% Crop Recommendation Accuracy
```

---

## 📜 License

This project is intended for **academic and research purposes**.
