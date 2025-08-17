from groq import Groq
import os 
from dotenv import load_dotenv
import base64


load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


#encode the image
def encode_image(image_path:str):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at this path {image_path}")
        else:
            with open(image_path,"rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"you have some issue {e}")



def Pharmacist_specialist(encode_img,query):
    """
    Pharmacist Specialist Tool
    Analyzes medicine images and answers questions about usage, dosage, and side effects. if user is passinf somthing other
    than medican dont assist with that its strictly prohibted.

    Parameters:
        img_path (str): Path/URL of the medicine image.
        prompt (str): User question (e.g., "What is this medicine used for?").

    Returns:
        str: Detailed response about the medicine.
    """
    try:
        if encode_image and query:
            messages = [
                {
                    "role" : "system",
                    "content" : """
                    You are a licensed pharmacist assistant. Strictly follow these rules:
                    1. ONLY respond to medicine-related images (pills/syrups/packaging) and questions.
                    2. Reject non-medical content with: "I can only assist with medicine-related queries."
                    3. For valid queries, provide:
                    - Medicine Name (if identifiable)
                    - Usage
                    - Dosage
                    - Side Effects
                    - Warnings                            
                    """
                },
                {
                    "role" : "user",
                    "content" : [
                        {
                            "type" : "text",
                            "text" : query
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encode_img}"
                            }
                        }

                    ]
                }
            ]

            #setup the mdel
            client = Groq(api_key=GROQ_API_KEY)
        
            completion = client.chat.completions.create(
                model = "meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                temperature=0.7,
            )

            return completion.choices[0].message.content

        else:
            return ("Upload image and pass the query both")
    except Exception as e:
        print(f"You have some issue at {e}")

if __name__ == "__main__":
    try:
        query = "what is the usage of this medicane?"
        image_path = r"C:\Users\HP\Desktop\Neuravia_hackathon\Neuravia_Hackathon\Backend\MediImage\panadol.png"
        img_encode = encode_image(image_path=image_path) if os.path.exists else FileNotFoundError("File not found at this location")
        response=Pharmacist_specialist(
            encode_img=img_encode,
            query=query,
        )
        print("Pharmacisit Specialist response:")
        print(response)
    except Exception as e:
        print(f"you have problem {e}")