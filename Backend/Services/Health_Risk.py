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

User Data:
{user_data}
"""

    response = model.invoke(prompt)
    content = response.content

    # Stream line by line instead of word by word
    for line in content.split("\n"):
        yield line
        time.sleep(0.05)

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
        print(chunk)
