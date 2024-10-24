import streamlit as st
from PIL import Image
import numpy as np
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import ImageDraw
from paddleocr import PaddleOCR
import openai

# Initialize all models and processors
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
detr_processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
detr_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Configure OpenAI
openai.api_key = "your-openai-key"

def extract_text_from_image(image):
    """Extract text from image using PaddleOCR"""
    result = ocr.ocr(np.array(image), cls=True)
    text = ' '.join([line[1][0] for line in result[0]]) if result[0] else ''
    return text

def analyze_brands_with_openai(text):
    """Use OpenAI to identify brand names from the extracted text"""
    prompt = f"""
    Analyze the following text extracted from a product label and identify only the brand names.
    Only return the brand names, nothing else. If multiple brand names are found, list them one per line.
    If no brand names are found, return "No brands detected".

    Text from label: {text}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a specialized AI that identifies brand names from product labels."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error in OpenAI analysis: {str(e)}"

def count_objects(image, threshold=0.3):
    """Count and detect objects in the image using DETR"""
    inputs = detr_processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = detr_model(**inputs)
    
    target_sizes = torch.tensor([image.size[::-1]])
    results = detr_processor.post_process_object_detection(
        outputs, 
        target_sizes=target_sizes, 
        threshold=threshold
    )[0]
    
    return len(results["scores"]), results

def draw_bounding_boxes(image, results):
    """Draw bounding boxes around detected objects"""
    draw = ImageDraw.Draw(image)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [int(i) for i in box.tolist()]
        draw.rectangle(box, outline="red", width=3)
        label_text = f"{detr_model.config.id2label[label.item()]}: {score.item():.2f}"
        draw.text((box[0], box[1]), label_text, fill="red")
    return image

def main():
    st.title("Smart Product Analysis System")
    st.write("Upload an image to detect objects and extract brand information")

    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("Analyze Image"):
                with st.spinner("Processing..."):
                    # Object Detection
                    num_objects, results = count_objects(image)
                    
                    # Brand Extraction
                    extracted_text = extract_text_from_image(image)
                    brands = analyze_brands_with_openai(extracted_text)
                    
                    # Display Results
                    st.subheader("Results:")
                    
                    # Object Detection Results
                    st.write(f"Number of objects detected: {num_objects}")
                    image_with_boxes = draw_bounding_boxes(image.copy(), results)
                    st.image(image_with_boxes, caption="Detected Objects", use_column_width=True)
                    
                    # Display detected object counts by category
                    object_counts = {}
                    for label in results["labels"]:
                        category = detr_model.config.id2label[label.item()]
                        object_counts[category] = object_counts.get(category, 0) + 1
                    
        
                    
                    # Brand Detection Results
                    st.subheader("Detected Brands:")
                    st.write(brands)
                    
                    # Show extracted text in expander (for debugging)
                    with st.expander("Show extracted text"):
                        st.text(extracted_text)

if __name__ == "__main__":
    main()