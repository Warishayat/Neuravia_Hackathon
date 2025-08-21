from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import time

def healthRiskPrediction(age, gender, smoking, alcohol, exercise_frequency, sleep_quality, bmi, blood_pressure, glucose_level, medical_history):
    load_dotenv()
    groq_api = os.environ.get('GROQ_API_KEY')
    model = ChatGroq(model='openai/gpt-oss-120b')

    user_data = f"""
USER HEALTH PROFILE:
- Age: {age}
- Gender: {gender}
- Smoking: {"Yes" if smoking else "No"}
- Alcohol: {"Yes" if alcohol else "No"}
- Exercise: {exercise_frequency} times per week
- Sleep Quality: {sleep_quality}/5
- BMI: {bmi}
- Blood Pressure: {blood_pressure}
- Glucose Level: {glucose_level if glucose_level else "Not provided"}
- Medical History: {", ".join(medical_history) if medical_history else "None"}
"""

    prompt = f"""
Role:
You are an empathetic AI Health Risk Assessor that calculates chronic disease risks including diabetes, cardiovascular diseases, stroke, and other health conditions. 

CRITICAL FORMATTING INSTRUCTIONS:
- You MUST respond using rich markdown formatting with tables, headers, and bullet points
- Use ## and ### for section headers with emojis
- Create tables with | symbols for risk overview
- Use bullet points for lists
- Structure the response with clear sections

RESPONSE FORMAT REQUIREMENTS:
## 🏥 Health Risk Assessment

### 📊 Risk Summary Table
| Condition | Risk Level | Key Factors | Recommendations |
|-----------|------------|-------------|-----------------|

### 🌟 Positive Health Factors
- 

### 📈 Areas for Improvement
- 

### 🎯 Action Plan
- 

User Data:
{user_data}

Please provide a comprehensive health risk assessment using the exact markdown format shown above with tables and proper formatting.
"""

    response = model.invoke(prompt)
    content = response.content

    # Stream the response line by line for better formatting
    lines = content.split("\n")
    for line in lines:
        if line.strip():  # Only yield non-empty lines
            yield line + "\n"
            time.sleep(0.08)

if __name__ == "__main__":
    for chunk in healthRiskPrediction(
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
    ):
        print(chunk, end='')