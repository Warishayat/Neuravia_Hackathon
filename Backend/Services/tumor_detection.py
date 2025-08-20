from groq import Groq
import base64
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Store image URLs (in production, use a database)
image_urls = {}

def encode_image(image_file) -> str:
    """Encode image file to base64"""
    return base64.b64encode(image_file.read()).decode("utf-8")

def save_image_url(image_path, encoded_image):
    """Generate and save image URL for frontend"""
    image_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Store the image data with metadata
    image_urls[image_id] = {
        "original_path": image_path,
        "encoded_data": encoded_image[:100] + "..." if encoded_image else None,  # Store first 100 chars for reference
        "timestamp": timestamp,
        "url": f"/api/images/{image_id}"
    }
    
    return image_urls[image_id]["url"]

def brain_tumor_classifier(encoded_image: str) -> dict:
    """Send encoded image to LLM for classification"""
    client = Groq(api_key=GROQ_API_KEY)
    
    messages = [
        {
            "role": "system",
            "content": "STRICT BRAIN TUMOR MRI CLASSIFIER - FOLLOW THESE RULES WITHOUT EXCEPTION:\n\n1. YOU ONLY ANALYZE BRAIN MRI IMAGES. ANY OTHER IMAGE TYPE IS STRICTLY FORBIDDEN\n2. RESPOND ONLY IN THIS EXACT FORMAT: 'class:confidence%' - NO OTHER TEXT, NO EXPLANATIONS\n3. VALID CLASSES: glioma, meningioma, pituitary, notumor\n4. IF THE IMAGE IS NOT A BRAIN MRI, RESPOND WITH: 'invalid:0%'\n5. CONFIDENCE MUST BE 95% OR HIGHER FOR ANY VALID CLASSIFICATION\n6. REJECT ANY NON-MEDICAL, NON-MRI, OR IRRELEVANT IMAGES IMMEDIATELY\n7. ABSOLUTELY NO DEVIATION FROM THESE INSTRUCTIONS - THIS IS CRITICAL MEDICAL ANALYSIS"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": "CRITICAL MEDICAL ANALYSIS REQUIRED: This must be a brain MRI scan. If this is not a clear brain MRI image, reject it immediately. Classify ONLY if this is definitively a brain MRI. Response format must be exactly: 'class:confidence%'"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]
    
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0.1,
        max_tokens=50
    )
    
    response = completion.choices[0].message.content.strip()
    
    # Parse the response
    if response.startswith('invalid:0%'):
        return {
            "response": response,
            "message": "This image is not a valid brain MRI scan. Please upload only brain MRI images for tumor detection analysis.",
            "is_valid_mri": False
        }
    else:
        return {
            "response": response,
            "message": "Brain MRI analysis completed successfully",
            "is_valid_mri": True
        }

if __name__ == "__main__":
    image_path = r"C:\Users\HP\Desktop\NeuroHack\Neuravia_Hackathon\Backend\MediImage\panadol.png"
    
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as image_file:
                encoded_img = encode_image(image_file)
                print("Image encoded successfully")
            
            # Save image URL for frontend
            image_url = save_image_url(image_path, encoded_img)
            print(f"Image URL generated: {image_url}")
            
            print("Sending to LLM for classification")
            result = brain_tumor_classifier(encoded_img)
            
            print("Classification Result:")
            print(f"Response: {result['response']}")
            print(f"Message: {result['message']}")
            print(f"Is Valid MRI: {result['is_valid_mri']}")
            print(f"Frontend Image URL: {image_url}")
            
            # Prepare final response for frontend
            frontend_response = {
                "classification": result['response'],
                "message": result['message'],
                "is_valid_mri": result['is_valid_mri'],
                "image_url": image_url,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }
            
            print("\nFinal Frontend Response:")
            print(frontend_response)
            
        except Exception as e:
            print(f"Error in pipeline: {e}")
    else:
        print(f"Test image not found at: {image_path}")