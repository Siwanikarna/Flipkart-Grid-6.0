# Smart Vision Technology Quality Control - Flipkart GRID 6.0

## 🎯 Overview
This repository contains our solution for Flipkart GRID 6.0 Hackathon, focusing on Smart Vision Technology for Quality Control. Our solution addresses multiple use cases using advanced computer vision and machine learning techniques to automate quality testing processes.

## 🌟 Use Cases

### 1. OCR Label Information Extraction (20% weightage)
- **Technology Stack:**
  - PaddleOCR for text extraction
  - OpenAI GPT-4 for advanced text analysis
  - Rule-based pattern matching
- **Features:**
  - Extracts brand name, product name, pack size
  - Identifies MRP, batch number
  - Detects manufacturing and expiry dates
  - Parses additional product information
- **Confidence Scoring:** Provides confidence scores for extracted information

### 2. Expiry Date Validation (10% weightage)
- **Technology Stack:**
  - PaddleOCR for date extraction
  - Custom date format parser
- **Features:**
  - Supports multiple date formats
  - Validates expiry dates
  - MRP verification
  - Handles various date representations

### 3. Brand Recognition and Count Verification (30% weightage)
- **Technology Stack:**
  - Facebook's DETR (DEtection TRansformer) for object detection
  - PaddleOCR for text recognition
  - OpenAI GPT-4 for brand analysis
- **Features:**
  - Object detection and counting
  - Brand name identification
  - Visual bounding box display
  - Category-wise object counting

### 4. Fresh Produce Shelf Life Prediction (40% weightage)
- **Technology Stack:**
  - VGG-based deep learning model
  - TensorFlow/Keras
- **Features:**
  - Predicts shelf life up to 14+ days
  - Real-time image processing
  - Support for various fruits and vegetables
  - Day-wise categorization

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/flipkart-grid-vision

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-api-key"  # Linux/Mac
# or
set OPENAI_API_KEY="your-api-key"  # Windows
```

## 📦 Dependencies
- streamlit
- paddleocr
- openai
- pillow
- numpy
- torch
- transformers
- tensorflow
- keras

## 🚀 Usage

### Running the Applications

1. **Label Information Extractor:**
```bash
streamlit run usecase1_2.py
```

2. **Brand Recognition System:**
```bash
streamlit run usecase3.py
```

3. **Shelf Life Predictor:**
```bash
streamlit run usecase4.py
```

## 📊 Model Details

### OCR and Information Extraction
- **PaddleOCR:** Used for text extraction with angle classification
- **GPT-4:** Advanced text analysis and information categorization
- **Custom Rule Engine:** Pattern matching for specific product information

### Object Detection
- **DETR-ResNet-50:** Pre-trained model for object detection and counting
- **Features:** Multi-object detection, confidence scoring, bounding box visualization

### Shelf Life Prediction
- **VGG-based Model:** Custom-trained for produce freshness assessment
- **Input:** 224x224 RGB images
- **Output:** 14 shelf life categories

## 🎥 Demo
https://www.canva.com/design/DAGUIXRkrsg/TKv1qNO5eERNz-3yfcg3iw/edit?utm_content=DAGUIXRkrsg&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## 📝 Project Structure
```
.
├── usecase1_2.py          # Label & Expiry Date Detection
├── usecase3.py            # Brand Recognition & Counting
├── usecase4.py            # Shelf Life Prediction
├── requirements.txt       # Project dependencies
└── models/
    └── shelf_life_prediction_model_vgg.keras
```

## 👥 Team Members
- Siwani Karna
- Poluru Reddy Jahanve

## 🤝 Contributing
Feel free to submit issues and enhancement requests!

## 🙏 Acknowledgments
- Flipkart GRID 6.0 for organizing this hackathon
- OpenAI for GPT-4 API
- Facebook AI Research for DETR
- PaddlePaddle team for PaddleOCR
