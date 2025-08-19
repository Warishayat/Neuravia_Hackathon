# Health_Assistanat_Chatbot
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def health_assistant(user_query: str):
    prompt = f"""
You are NeuraCareAI, a helpful and supportive health assistant.
- Base your answers only on the user’s query.
- Give clear, simple, supportive advice.
- If symptoms are serious/persistent, advise seeing a doctor.
- Avoid exact prescriptions or diagnoses.
- Always end with: "This is not medical advice. Please consult a healthcare professional for accurate guidance."

User query: {user_query}
Respond in 5–7 sentences and end with the disclaimer.
""".strip()
    model = ChatGroq(model="moonshotai/kimi-k2-instruct", temperature=0.7, streaming=True)
    for chunk in model.stream(prompt):
        yield (chunk.content or "")

if __name__ == "__main__":
    query = "i am having pain in my head for the last 3 to 5 days"
    print("Health assistant chatbot response (streaming):\n")
    response = ""
    for token in health_assistant(query):
        print(token, end="", flush=True)
        response += token
    print("\n\nFinal Response:\n", response)
