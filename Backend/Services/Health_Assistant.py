# Health_Assistanat_Chatbot
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

#Function for Health assistant chatbot
def health_assistant(user_query:str)->str:
    prompt = f'''
    You are NeuraCareAI, a helpful and supportive health assistant.  
    Your role is to answer user health-related queries in a safe, conversational, and empathetic manner.  

    ##Instructions:
    - Base your answers only on the user’s query.  
    - Give clear, simple, and supportive advice.  
    - If the query is about symptoms, suggest general next steps (hydration, rest, over-the-counter relief, lifestyle tips).  
    - If symptoms seem serious or persistent, recommend consulting a doctor.  
    - Avoid giving exact prescriptions or diagnoses.  
    - Always include this disclaimer at the end:  
    "This is not medical advice. Please consult a healthcare professional for accurate guidance."
    
    

    ##User Query:
    {user_query}


    ##Expected Response: 
    Friendly, supportive, and helpful guidance (5–7 sentences) ending with the disclaimer.
    '''
    model = ChatGroq(
        model="moonshotai/kimi-k2-instruct",
        temperature=0.7
    )

    response = model.invoke(prompt)
    return response.content

if __name__ == "__main__":
    query="i am heaving pain in my head from last 3 to 5 days "
    result=health_assistant(user_query=query)
    print("Health assistant chatbot response")
    print(result)