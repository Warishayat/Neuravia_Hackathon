print("This file contains all the logic related to user risk prediction (diabetes, stroke, etc.)")
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

def healthRiskPrediction(age, gender, smoking, alcohol, exercise_frequency, sleep_quality, bmi, blood_pressure, glucose_level, medical_history):
    """Predicts likelihood of chronic diseases based on user health data."""
    load_dotenv()
    groq_api = os.environ.get('GROQ_API_KEY')
    model = ChatGroq(model='openai/gpt-oss-120b')

    # Format input parameters as a clear string (not JSON)
    user_data = f"""
    USER HEALTH PROFILE:
    - Age: {age}
    - Gender: {gender}
    - Smoking: {"Yes" if smoking else "No"}
    - Alcohol: {"Yes" if alcohol else "No"}
    - Exercise: {exercise_frequency}/week
    - Sleep Quality: {sleep_quality}/5
    - BMI: {bmi}
    - Blood Pressure: {blood_pressure}
    - Glucose Level: {glucose_level if glucose_level else "Not provided"}
    - Medical History: {", ".join(medical_history) if medical_history else "None"}
    """

    prompt = f"""
Role:
You are an empathetic AI Health Risk Assessor that calculates chronic disease risks (diabetes, stroke, tumor, Alzheimer’s, dementia). 
Respond with warmth, clarity, and structured bullet points.

Rules:
1.Opening:  
"Hello! I’ve analyzed your health data. Here’s your personalized risk assessment:"

2. Disease Risk Format (per condition):  
- [Disease]: [Score]% ([Risk Tier])  
    - [Key Factor 1]  
    - [Key Factor 2]  
Example:  
- Diabetes: 12% (Low Risk)  
    - Normal glucose levels (95 mg/dL)  
    - Healthy BMI (23.5)  

3. Advice:  
- Low Risk: "Great job! Your risk is low. Keep it up—take care!"  
- Medium/High Risk: "Please consult a doctor soon. Meanwhile:"  
    - [Habit 1]  
    - [Habit 2]  

User Data:
{user_data}

Output Example:
---
Hello! I’ve analyzed your health data. Here’s your personalized risk assessment:

- Diabetes: 12% (Low Risk)  
- Normal glucose levels (95 mg/dL)  
- Healthy BMI (23.5)  

- Stroke: 8% (Low Risk)  
- Ideal blood pressure (120/80)  
- Non-smoker  

- Tumor (Cancer): 15% (Low Risk)  
- Young age (32)  
- No smoking history  

Advice:  
Great job! Your risks are low. To stay healthy:  
- Continue exercising 3+ times/week  
- Maintain your excellent sleep habits  
- Limit alcohol to occasional use  

Take care! 💙
"""

    response = model.invoke(prompt)
    print(response.content)

if __name__ == "__main__":
    healthRiskPrediction(
        age=32,
        gender="Female",
        smoking=False,
        alcohol=True,
        exercise_frequency=3,
        sleep_quality=4,
        bmi=23.5,
        blood_pressure="120/80",
        glucose_level=95,
        medical_history=["Asthma"]
    )
