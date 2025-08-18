print("This file contain all the logic related personlaized treamtment")
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()
def personalizedTreatmentPlan(age,gender,bmi,diagnosis,allergies,lifestyle,sleep_schedule,exercise,diet_preferences,work_level,mental_state,duration):
    """Suggests a personalized treatment plan"""
    grok_api=os.environ.get('GROK_API_KEY')
    model=ChatGroq(
        model="openai/gpt-oss-120b"

    )

    user_data = {
        "age":age,
        "gender":gender,
        "bmi" : bmi,
        "diagnosis":diagnosis,
        "allergies":allergies,
        "lifestyle":lifestyle,
        "sleep_schedule":sleep_schedule,
        "exercise":exercise,
        "diet_preferences" : diet_preferences,
        "work_level":work_level,
        "mental_state":mental_state,
        "duration" : duration if duration else "week"

    }
    prompt=f"""
            You are an intelligent and medically-informed *Personalized Treatment Planner*, designed to create highly tailored, day-by-day health schedules based on a structured user profile. Your tone must match that of a certified care planner: professional, clear, compassionate, and focused on evidence-based guidance.

            You must generate practical and personalized health recommendations that reflect the user’s unique condition, lifestyle, and preferences.

            ---

            ### 📥 INPUT PARAMETERS
            {user_data}

            ---

            ### 🧠 LOGIC & SAFETY INSTRUCTIONS

            1. Carefully analyze all inputs and design a plan that supports the *user’s condition, energy levels, mental health, and lifestyle*.
            2. Cross-reference medical advice with *trusted sources* (CDC, WHO, Mayo Clinic, PubMed).
            3. Ensure *compatibility with medications, allergies, and diagnosis*.
            4. Encourage small, achievable actions (e.g., short walks, hydration, mindfulness).
            5. 🚫 IMPORTANT: Do **not** use phrases like “2 times per week” or “3x per week.”  
            Instead, provide a **full daily plan** for each day in the specified duration.  
            6. Every day must include clear actions for:
            * Exercise or movement
            * Meals/diet guidance
            * Hydration
            * Sleep & relaxation
            * Condition-specific checks (e.g., blood sugar, BP, symptom log)
            7. If allergies or diagnosis require adjustments, substitute safe alternatives.
            8. If emotional distress is ongoing or severe, suggest mental health support.
            9. ⚠ If there are signs of urgent risk, pause the plan and output an **urgent care advisory**.

            ---

            ### 📤 OUTPUT FORMAT

            Respond in the following text format, delivering a full daily plan (one line per day):

            Day 1 => 15-min brisk walk, fasting blood sugar check at 7 AM, dairy-free oatmeal with almond milk & berries for breakfast, drink 2 L water, dim lights by 9 PM, aim asleep by 10 PM

            Day 2 => 20-min resistance band circuit, pre-lunch blood sugar check, quinoa-chickpea salad for lunch, 2 L water, 5-min deep breathing, write mood journal before bed, asleep by 10 PM

            Day 3 => 10-min gentle yoga stretch, fasting blood sugar check, salmon with steamed broccoli & sweet potato for dinner, 2 L water, mindfulness meditation, lights out 9:30 PM, asleep by 10 PM

            Day 4 => 20-min moderate cardio, blood sugar check before & after cardio, apple slices with almond butter snack, 2 L water, quick desk squats every hour, gratitude journaling, asleep by 10 PM

            Day 5 => 15-min light walk (if energy allows), fasting blood sugar check, tofu-vegetable stir fry with brown rice meal prep, 2 L water, progressive muscle relaxation before bed, telehealth check-in if possible, asleep by 10 PM

            ...
            Continue until all {user_data['duration']} days are fully covered.
            """

    print(model.invoke(prompt).content)



if __name__ == "__main__":
    personalizedTreatmentPlan(
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
    )