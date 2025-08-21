import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
import tempfile
import shutil
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


# save temp file before processing
def save_temp_file(file_data, file_type: str = 'pdf') -> str:
    print("Save the temp file")
    temp_dir = Path("temp_files")
    temp_dir.mkdir(exist_ok=True)
    
    if file_type != 'pdf':
        raise ValueError("Only PDF files are supported.")
    
    extension = '.pdf'
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension, dir=temp_dir)
    temp_path = temp_file.name

    try:
        if isinstance(file_data, (str, Path)):
            with open(file_data, 'rb') as src, open(temp_path, 'wb') as dst:
                shutil.copyfileobj(src, dst)
        else:  # file-like object
            with open(temp_path, 'wb') as dst:
                shutil.copyfileobj(file_data, dst)
    except Exception as e:
        cleanup_temp_file(temp_path)
        print("CLean the file")
        raise Exception(f"Error saving file: {str(e)}")

    return temp_path



# to clear the temporary file
def cleanup_temp_file(temp_path: str):
    try:
        os.remove(temp_path)
    except Exception as e:
        print(f"Error cleaning up temporary file: {e}")


# rag pipeline
def rag_pipeline(file_data, file_type: str = 'pdf'):
    print("Rag Pipeline is working")
    if file_type != 'pdf':
        raise ValueError("Only PDF files are supported.")
    try:
        temp_file_path = save_temp_file(file_data, file_type)
        
        # Load and split PDF
        loader = PyMuPDFLoader(temp_file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        vector_store = FAISS.from_documents(chunks, embeddings)
        model = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.6
        )
        
        cleanup_temp_file(temp_file_path)
        return vector_store, model

    except Exception as e:
        if 'temp_file_path' in locals():
            cleanup_temp_file(temp_file_path)
        raise e

# query medical report 
def query_medical_report(vector_store, model, query: str):
    print("Quering the medical report")
    docs = vector_store.similarity_search(query)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""You are a medical assistant AI. Analyze the following context and provide a precise response to the question.
    STRICT GUIDELINES:
    1. ONLY respond if the context contains legitimate medical/healthcare content
    2. If the context is not medical-related (healthcare, patient care, medical reports, clinical data, hospital documents), respond: "I can only assist with legitimate medical documents and reports."
    3. If the question cannot be answered from the context, respond: "The requested information is not available in this medical document."
    4. Base your response strictly on the provided context - do not extrapolate or add external knowledge
    CONTEXT:
    {context}
    QUESTION:
    {query}
    MEDICAL VALIDATION: First confirm this is a legitimate medical document before responding.
    RESPONSE:"""
    response = model.invoke(prompt)
    return response.content

if __name__ == "__main__":
    filepath = r"C:\Users\HP\Desktop\Neuravia_hackathon\Neuravia_Hackathon\Backend\Pdfs\Neuravia_hackathon.pdf"
    vector_store, model = rag_pipeline(filepath, 'pdf')
    print("Vector Store is created....")
    query = "what are the features mentioned in the pdf?"
    response = query_medical_report(vector_store=vector_store, model=model, query=query)
    print("Medical Report Analysis:")
    print(response)