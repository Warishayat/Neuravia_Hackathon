from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

def personalizedTreatmentPlan(age, gender, bmi, diagnosis, allergies, lifestyle, sleep_schedule, exercise, diet_preferences, work_level, mental_state, duration):
    grok_api = os.environ.get('GROK_API_KEY')
    model = ChatGroq(model="openai/gpt-oss-120b")

    user_data = {
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "diagnosis": diagnosis,
        "allergies": allergies,
        "lifestyle": lifestyle,
        "sleep_schedule": sleep_schedule,
        "exercise": exercise,
        "diet_preferences": diet_preferences,
        "work_level": work_level,
        "mental_state": mental_state,
        "duration": duration if duration else "week"
    }

    prompt = f"""
            You are an intelligent and medically-informed *Personalized Treatment Planner*, designed to create highly tailored, day-by-day health schedules based on a structured user profile. Your tone must match that of a certified care planner: professional, clear, compassionate, and focused on evidence-based guidance.

            You must generate practical and personalized health recommendations that reflect the user’s unique condition, lifestyle, and preferences.

            ### INPUT PARAMETERS
            {user_data}

            ### OUTPUT FORMAT

            Respond in the following text format, delivering a full daily plan (one line per day):

            Day 1 => 15-min brisk walk, fasting blood sugar check at 7 AM, dairy-free oatmeal with almond milk & berries for breakfast, drink 2 L water, dim lights by 9 PM, aim asleep by 10 PM

            Day 2 => 20-min resistance band circuit, pre-lunch blood sugar check, quinoa-chickpea salad for lunch, 2 L water, 5-min deep breathing, write mood journal before bed, asleep by 10 PM

            Continue until all {user_data['duration']} days are fully covered.
            """

    for chunk in model.stream(prompt):
        yield chunk.content or ""

if __name__ == "__main__":
    for chunk in personalizedTreatmentPlan(
        age=29,
        gender="female",
        bmi=24.1,
        diagnosis=["sugar"],
        allergies=["milk"],
        lifestyle="average",
        sleep_schedule=6,
        exercise="sometimes",
        diet_preferences="normal",
        work_level="desk job",
        mental_state="tired",
        duration="month",
    ):
        print(chunk, end="")
