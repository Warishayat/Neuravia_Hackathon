from dotenv import load_dotenv
from langchain_groq import ChatGroq
import warnings
import os
warnings.filterwarnings('ignore')
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

print("API is set in the enviroment")
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)
print(model.invoke("Who came first egg or hen").content)
