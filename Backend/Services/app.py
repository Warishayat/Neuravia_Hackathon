import streamlit as st
import sqlite3
import bcrypt
import warnings
import tempfile
import sys, os
import pandas as pd
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager
import cv2
import av
sys.path.append(os.path.abspath(".."))
from PIL import Image
from Mediguide import encode_image,Pharmacist_specialist
from Health_Assistant import health_assistant
from Health_Risk import healthRiskPrediction
from Medical_Reports import rag_pipeline, query_medical_report,save_temp_file,cleanup_temp_file
from Personalize_treatment import personalizedTreatmentPlan
from emotion_detection import process_frame
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase 
from tumor_detection import save_image_url,brain_tumor_classifier


warnings.filterwarnings('ignore')
load_dotenv()
key = os.getenv("key")

@st.cache_data
def init_db():
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

@st.cache_data
def add_user(email,password):
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (email,password) VALUES (?,?)",(email,hashed.decode("utf-8")))
        conn.commit()
    except sqlite3.IntegrityError:
        st.warning("⚠️ Email already exists. Please login.")
    conn.close()

@st.cache_data
def get_user(email,password):
    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?",(email,))
    row=c.fetchone()
    conn.close()
    if row:
        stored_hashed=row[0]
        return bcrypt.checkpw(password.encode(),stored_hashed.encode("utf-8"))
    return False

init_db()
cookies=EncryptedCookieManager(prefix="neuroai_",password=key)
if not cookies.ready():
    st.stop()
page_bg="""<style>[data-testid="stAppViewContainer"]{background:linear-gradient(-45deg,#0a3d62,#2980b9,#16a085,#2c3e50);background-size:400% 400%;animation:gradientShift 20s ease infinite;color:white;font-family:'Segoe UI',sans-serif}[data-testid="stHeader"]{background-color:rgba(0,0,0,0)}div[data-baseweb="tab-list"]{position:sticky!important;top:0;width:100%;background:rgba(10,61,98,0.95);z-index:1000;display:flex;font-size:15px!important;justify-content:center;gap:20px!important;padding:12px 0;border-radius:0 0 20px 20px;flex-wrap:nowrap!important;overflow-x:auto!important;scrollbar-width:none}div[data-baseweb="tab-list"]::-webkit-scrollbar{display:none}.btn-custom{display:inline-block;margin-top:25px;padding:14px 36px;background:#ffffff;color:#2980b9;border-radius:30px;font-weight:bold;font-size:18px;text-decoration:none;transition:0.3s}.btn-custom:hover{background:black!important;color:white!important}div.stButton>button{background:linear-gradient(90deg,#007BFF,#00D4FF);color:white;border:none;padding:12px 30px;font-size:18px;font-weight:bold;border-radius:12px;cursor:pointer;box-shadow:0px 0px 15px rgba(0,212,255,0.8);transition:all 0.3s ease-in-out}div.stButton>button:hover{transform:scale(1.05);background:black!important;color:white!important}div.stButton>button:active{transform:scale(0.98);color:black;box-shadow:0px 0px 10px rgba(0,212,255,0.7)}</style>"""
st.markdown(page_bg,unsafe_allow_html=True)
if "logged_in" not in st.session_state:st.session_state.logged_in=False
if "email" not in st.session_state:st.session_state.email=""
if cookies.get("logged_in")=="true":
    st.session_state.logged_in=True
    st.session_state.email=cookies.get("email")
if not st.session_state.logged_in:
    st.title("🔐 Welcome to NeuroCare-AI")
    choice=st.radio("Login / Signup",["Login","Signup"])
    if choice=="Login":
        email=st.text_input("Email")
        password=st.text_input("Password",type="password")
        if st.button("Login"):
            if get_user(email,password):
                st.session_state.logged_in=True
                st.session_state.email=email
                cookies["logged_in"]="true"
                cookies["email"]=email
                cookies.save()
                st.success(f"✅ Welcome back, {email}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    elif choice=="Signup":
        email=st.text_input("Enter Email")
        password=st.text_input("Choose Password",type="password")
        if st.button("Signup"):
            if email and password:
                add_user(email,password)
                st.success("🎉 Signup successful! Please login now.")
            else:
                st.warning("Please enter both email and password.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.email}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in=False
        st.session_state.email=""
        cookies["logged_in"]="false"
        cookies.save()
        st.rerun()
    # Reordered tabs as requested: Tumor Detection first, then Medical Report, then MediGuide, then Health Assistant
    tab1, tab8, tab4, tab5, tab2, tab6, tab3, tab7 = st.tabs(["Home", "Tumor Detection", "Medical Report", "MediGuide", "Health Assistant", "Treatment Plan", "Risk Prediction", "Emotion Detector"])


    with tab1:
        st.markdown(
            """
            <style>
            .hero-container {
                background-color: #f9fafb;  /* Light background */
                color: #1f1f1f;             /* Dark text */
                padding: 50px;
                border-radius: 20px;
                text-align: center;
                max-width: 1000px;
                margin: auto;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            .hero-image {
                border-radius: 20px;
                width: 100%;
                max-width: 700px;
                margin-top: 20px;
                margin-bottom: 30px;
            }
            .description {
                font-size: 18px;
                line-height: 1.6;
                margin-top: 20px;
                margin-bottom: 20px;
                text-align: left;
            }
            .description ul {
                margin-left: 20px;
            }
            .footer {
                color: #555555;
                font-size: 14px;
                text-align: center;
                margin-top: 40px;
                padding: 10px 0;
                border-top: 1px solid #ddd;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='hero-container'>
                <h1>🏥 Welcome to NeuroCare-AI</h1>
                <img src='https://media.nature.com/lw1024/magazine-assets/d42473-023-00106-8/d42473-023-00106-8_25389508.jpg' 
                    class='hero-image'>
                <div class='description'>
                    <p>NeuroCare-AI is your all-in-one intelligent health assistant, combining cutting-edge AI with practical medical tools. Our platform offers:</p>
                    <ul>
                        <li>🧠 <strong>Brain-MRI-Scan:</strong>AI-powered analysis of brain MRI scans to identify potential tumors including glioma, meningioma, and pituitary types with high-confidence results. Provides instant screening and detailed session logging for educational purposes..</li>
                        <li>💊 <strong>MediGuide:</strong> AI-powered pharmacist assistant to identify medicines, provide usage instructions, dosage guidance, side effects, and warnings.</li>
                        <li>📄 <strong>MedicalReport:</strong> Personalized treatment plans and comprehensive health reports based on medical history and lifestyle factors.</li>
                        <li>😊 <strong>Real-time Mood Detection:</strong> Monitor your emotions with webcam-based detection and Sunnah-inspired mental wellness advice.</li>
                        <li>🏋️ <strong>Personalized Fitness & Lifestyle Recommendations:</strong> Exercise, diet, sleep, and work-life guidance tailored to your needs.</li>
                        <li>⚕️ <strong>Holistic Health Insights:</strong> Combines AI-driven analysis and lifestyle tracking for proactive health management.</li>
                        <li>🛡️ <strong>Safe & Trusted Guidance:</strong> All advice is personalized, evidence-based, and privacy-conscious.</li>
                    </ul>
                    <p>Explore the tabs to access each feature and take control of your health with precision and care.</p>
                </div>
                <div class='footer'>
                    © 2025 NeuroCare-AI. All rights reserved. Built with custom AI models and advanced health technology.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tumor Detection tab (now tab8 is second after Home)
    with tab8:
        st.header("Brain Tumor Detection")
        #Instruction
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use Brain Tumor Detection:**
            
            1. **Upload Image**: Select a brain MRI image file (PNG, JPG, JPEG)
            2. **Click Detect**: Press the 'Detect Tumor' button to analyze the image
            3. **View Results**: See the classification results above
            4. **Check Logs**: All analyses are logged in the session table below
            
            **Expected Results:**
            - **glioma**: Brain tissue tumor detection
            - **meningioma**: Meninges tumor detection  
            - **pituitary**: Pituitary gland tumor detection
            - **notumor**: No tumors detected (normal MRI)
            - **invalid**: Non-MRI image uploaded
            
            **Note**: This is an AI-assisted tool for educational purposes. 
            Always consult medical professionals for actual diagnosis.
            """)
        if 'tumor_logs' not in st.session_state:
            st.session_state.tumor_logs = []
        uploaded_image = st.file_uploader(
            "Upload Brain MRI Image",
            type=['png', 'jpg', 'jpeg'],
            help="Please upload only brain MRI images for accurate tumor detection"
        )
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded MRI Image", use_container_width=True)
            
            detect_button = st.button("Detect Tumor", type="primary", disabled=False)
            
            if detect_button:
                with st.spinner("Analyzing MRI image for tumors..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_image.name)[1]) as tmp_file:
                            tmp_file.write(uploaded_image.getvalue())
                            temp_image_path = tmp_file.name
                        
                        try:
                            with open(temp_image_path, "rb") as image_file:
                                encoded_img = encode_image(image_path=temp_image_path)
                            image_url = save_image_url(temp_image_path, encoded_img)
                            result = brain_tumor_classifier(encoded_img)
                            classification_response = result['response']
                            if ':' in classification_response and '%' in classification_response:
                                class_name, confidence_str = classification_response.split(':', 1)
                                confidence = int(confidence_str.replace('%', ''))
                            else:
                                class_name = "error"
                                confidence = 0
                            class_descriptions = {
                                "glioma": "Glioma Tumor detected in brain tissue",
                                "meningioma": "Meningioma Tumor detected in meninges", 
                                "pituitary": "Pituitary Tumor detected in pituitary gland",
                                "notumor": "No tumor detected - normal brain MRI",
                                "invalid": "Invalid image - not a brain MRI",
                                "error": "Processing error - failed to analyze image"
                            }
                            description = class_descriptions.get(class_name.lower(), "Unknown classification")

                            log_entry = {
                                'timestamp': datetime.now().isoformat(),
                                'image_name': uploaded_image.name,
                                'image_url': image_url,
                                'classification': class_name.upper(),
                                'confidence': f"{confidence}%",
                                'description': description,
                                'is_valid_mri': result['is_valid_mri'],
                                'status': 'Valid' if result['is_valid_mri'] else 'Invalid'
                            }
                            st.session_state.tumor_logs.append(log_entry)

                            st.success("Analysis completed!")

                            st.subheader("Detection Results")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Classification", class_name.upper())
                            with col2:
                                st.metric("Confidence", f"{confidence}%")
                            with col3:
                                status_color = "✅" if result['is_valid_mri'] else "❌"
                                st.metric("Status", f"{status_color} {'Valid' if result['is_valid_mri'] else 'Invalid'}")
                            
                            # Show description
                            if class_name != 'invalid' and class_name != 'error':
                                if class_name == 'notumor':
                                    st.success(f"**Result:** {description}")
                                else:
                                    st.warning(f"**Result:** {description}")
                            else:
                                st.error(f"**Result:** {description}")
                            st.info(f"**Message:** {result['message']}")
                        finally:
                            os.unlink(temp_image_path)
                            
                    except Exception as e:
                        st.error(f"Error processing image: {str(e)}")

        if st.session_state.tumor_logs:
            st.subheader("Session Logs")
            log_df = pd.DataFrame(st.session_state.tumor_logs)
            display_df = log_df[['timestamp', 'image_name', 'classification', 'confidence', 'description', 'status', 'image_url']].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Display the table
            st.dataframe(
                display_df,
                column_config={
                    "timestamp": "Timestamp",
                    "image_name": "Image Name",
                    "classification": "Classification",
                    "confidence": "Confidence",
                    "description": "Description",
                    "status": "Status",
                    "image_url": st.column_config.LinkColumn("Image URL")
                },
                use_container_width=True,
                hide_index=True
            )
            
            #Logs Download
            if st.button("Download Session Logs"):
                log_json = json.dumps(st.session_state.tumor_logs, indent=2)
                st.download_button(
                    label="Download JSON Logs",
                    data=log_json,
                    file_name=f"tumor_detection_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            #Clear logs
            if st.button("Clear Logs"):
                st.session_state.tumor_logs = []
                st.rerun()
        else:
            st.info("No analysis logs yet. Upload an MRI image and click 'Detect Tumor' to get started.")
        

    #Medical Report (now tab4)
    with tab4:
        st.header("Welcome to Medical Report")
        
        # Instructions expander
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use Medical Report Analyzer:**
            
            1. **Upload PDF**: Upload your medical report in PDF format
            2. **Wait for Processing**: The system will process and vectorize your document
            3. **Ask Questions**: Type any question about your medical report
            4. **Get Answers**: Receive AI-powered insights from your report
            
            **Note**: Your data remains private and is processed locally.
            All medical information should be verified with healthcare professionals.
            """)
        
        uploaded_file = st.file_uploader("Upload your medical report (PDF)", type=["pdf"])

        if "vector_store" not in st.session_state:
            st.session_state.vector_store = None
            st.session_state.model = None
            st.session_state.pdf_uploaded = False
        if "medical_logs" not in st.session_state:
            st.session_state.medical_logs = []

        if uploaded_file:
            if not st.session_state.pdf_uploaded:
                with st.spinner("Processing PDF and creating vectors..."):
                    temp_path = save_temp_file(uploaded_file)
                    vector_store, model = rag_pipeline(temp_path)
                    cleanup_temp_file(temp_path)
                    st.session_state.vector_store = vector_store
                    st.session_state.model = model
                    st.session_state.pdf_uploaded = True
                    
                    # Log the upload
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'action': 'PDF Uploaded',
                        'file_name': uploaded_file.name,
                        'file_size': f"{uploaded_file.size / 1024:.1f} KB",
                        'status': 'Processed Successfully'
                    }
                    st.session_state.medical_logs.append(log_entry)
                    
                st.success("PDF processed! You can now ask questions about it.")

        if st.session_state.pdf_uploaded:
            query = st.text_input("Ask a question about the PDF")
            if st.button("Submit Question") and query.strip() != "":
                with st.spinner("Searching for answers..."):
                    response = query_medical_report(st.session_state.vector_store, st.session_state.model, query)
                
                # Log the query
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'action': 'Query Asked',
                    'question': query,
                    'response_length': len(response),
                    'status': 'Answered'
                }
                st.session_state.medical_logs.append(log_entry)
                
                st.markdown(f"**You:** {query}")
                st.markdown(f"**Bot:** {response}")

            # Session Logs
            if st.session_state.medical_logs:
                st.markdown("---")
                st.subheader("Session Logs")
                log_df = pd.DataFrame(st.session_state.medical_logs)
                
                # Handle missing columns gracefully
                available_columns = log_df.columns.tolist()
                display_columns = ['timestamp', 'action', 'file_name']
                
                # Only include columns that exist in the DataFrame
                if 'question' in available_columns:
                    display_columns.append('question')
                if 'response_length' in available_columns:
                    display_columns.append('response_length')
                if 'status' in available_columns:
                    display_columns.append('status')
                
                display_df = log_df[display_columns].copy()
                display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Create column configuration dynamically
                column_config = {
                    "timestamp": "Timestamp",
                    "action": "Action",
                    "file_name": "File Name"
                }
                
                if 'question' in display_columns:
                    column_config["question"] = "Question"
                if 'response_length' in display_columns:
                    column_config["response_length"] = "Response Length"
                if 'status' in display_columns:
                    column_config["status"] = "Status"
                
                st.dataframe(
                    display_df,
                    column_config=column_config,
                    use_container_width=True,
                    hide_index=True
                )
                
                if st.button("Clear Medical Logs", key="clear_medical_logs"):
                    st.session_state.medical_logs = []
                    st.rerun()
                    
        else:
            st.info("Please upload a PDF first to ask questions.")
            
    # MediGuide (now tab5)
    with tab5:
        st.header("Welcome to MediGuide")
        
        # Instructions expander
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use MediGuide:**
            
            1. **Upload Image**: Upload a medical image or report
            2. **Enter Question**: Type your question about the medication
            3. **Get Analysis**: Receive detailed information about the medicine
            
            **Supported formats**: JPG, JPEG, PNG
            **Note**: Always verify medication information with a pharmacist.
            """)
        
        if "mediguide_logs" not in st.session_state:
            st.session_state.mediguide_logs = []
        
        uploaded_file = st.file_uploader("Upload a medical image or report", type=["jpg","jpeg","png"])
        prompt = st.text_area("Enter your question or instruction")
        
        if st.button("Submit"):
            if uploaded_file and prompt:
                # Log the action
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'action': 'Image Analysis',
                    'file_name': uploaded_file.name,
                    'question': prompt[:50] + "..." if len(prompt) > 50 else prompt,
                    'status': 'Processing'
                }
                st.session_state.mediguide_logs.append(log_entry)
                
                suffix = os.path.splitext(uploaded_file.name)[1]
                os.makedirs("temp_mediguide", exist_ok=True)
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir="temp_mediguide") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_file_path = tmp_file.name
                
                with st.spinner("Analyzing medical image..."):
                    encoded = encode_image(image_path=tmp_file_path)
                    response = Pharmacist_specialist(encode_img=encoded, query=prompt)
                
                # Update log
                st.session_state.mediguide_logs[-1]['status'] = 'Completed'
                st.session_state.mediguide_logs[-1]['response_length'] = len(response)
                
                st.subheader("MediGuide Response")
                st.write(response)
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            else:
                st.warning("⚠️ Please upload a file and enter a prompt.")
        
        # Session Logs
        if st.session_state.mediguide_logs:
            st.markdown("---")
            st.subheader("Session Logs")
            log_df = pd.DataFrame(st.session_state.mediguide_logs)
            display_df = log_df[['timestamp', 'action', 'file_name', 'question', 'response_length', 'status']].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(
                display_df,
                column_config={
                    "timestamp": "Timestamp",
                    "action": "Action",
                    "file_name": "File Name",
                    "question": "Question",
                    "response_length": "Response Length",
                    "status": "Status"
                },
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("Clear MediGuide Logs", key="clear_mediguide_logs"):
                st.session_state.mediguide_logs = []
                st.rerun()

    # Health Assistant Chatbot logic (now tab2)
    with tab2:
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        if "assistant_logs" not in st.session_state:
            st.session_state.assistant_logs = []
        
        # Instructions expander
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use Health Assistant:**
            
            1. **Ask Questions**: Type any health-related question
            2. **Get Responses**: Receive AI-powered health guidance
            3. **View History**: All conversations are saved in session
            
            **Note**: This is for informational purposes only.
            Always consult healthcare professionals for medical advice.
            """)

        st.subheader("Ask the Health Assistant")

        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Enter your query:")
            submit = st.form_submit_button("Send")

            if submit and user_input:
                # Log the query
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'action': 'Chat Query',
                    'question': user_input[:50] + "..." if len(user_input) > 50 else user_input,
                    'status': 'Processing'
                }
                st.session_state.assistant_logs.append(log_entry)
                
                st.session_state.chat_history.append({"role": "user", "message": user_input})

                response_container = st.empty()
                response_text = ""

                for chunk in health_assistant(user_input):
                    response_text += chunk
                    response_container.markdown(f"**Assistant:** {response_text}")

                st.session_state.chat_history.append({"role": "assistant", "message": response_text})
                
                # Update log
                st.session_state.assistant_logs[-1]['status'] = 'Completed'
                st.session_state.assistant_logs[-1]['response_length'] = len(response_text)
        
        # Session Logs
        if st.session_state.assistant_logs:
            st.markdown("---")
            st.subheader("Session Logs")
            log_df = pd.DataFrame(st.session_state.assistant_logs)
            display_df = log_df[['timestamp', 'action', 'question', 'response_length', 'status']].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(
                display_df,
                column_config={
                    "timestamp": "Timestamp",
                    "action": "Action",
                    "question": "Question",
                    "response_length": "Response Length",
                    "status": "Status"
                },
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("Clear Assistant Logs", key="clear_assistant_logs"):
                st.session_state.assistant_logs = []
                st.rerun()
    
    # Personalized treatment plan (now tab6)
    with tab6:
        st.header("Welcome to Treatment Plan")

        if "treatment_plan" not in st.session_state:
            st.session_state.treatment_plan = ""
        if "treatment_logs" not in st.session_state:
            st.session_state.treatment_logs = []
        
        # Instructions expander
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use Treatment Plan Generator:**
            
            1. **Enter Details**: Provide your health information
            2. **Generate Plan**: Create personalized treatment plan
            3. **Follow Guidance**: Review and implement recommendations
            
            **Note**: This is a guidance tool, not medical prescription.
            Always follow your doctor's recommended treatment plans.
            """)

        # Create two columns for input parameters
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30, key="treatment_age")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="treatment_gender")
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=23.0, key="treatment_bmi")
            diagnosis = st.text_area("Diagnosis (comma separated)", key="treatment_diagnosis")
            allergies = st.text_area("Allergies (comma separated)", key="treatment_allergies")
        
        with col2:
            lifestyle = st.selectbox("Lifestyle", ["Sedentary", "Average", "Active"], key="treatment_lifestyle")
            sleep_schedule = st.number_input("Sleep hours per day", min_value=0, max_value=24, value=7, key="treatment_sleep")
            exercise = st.text_input("Exercise habits", key="treatment_exercise")
            diet_preferences = st.text_input("Diet Preferences", key="treatment_diet")
            work_level = st.selectbox("Work Level", ["Desk job", "Moderate activity", "High activity"], key="treatment_work")
            mental_state = st.selectbox("Mental State", ["Tired", "Normal", "Energetic", "Stressed"], key="treatment_mental")
            duration = st.selectbox("Duration of plan", ["week", "2 weeks", "month"], key="treatment_duration")

        # Full width button
        if st.button("Generate Treatment Plan", key="treatment_generate", use_container_width=True):
            # Process comma-separated inputs
            diagnosis_list = [d.strip() for d in diagnosis.split(",") if d.strip()]
            allergies_list = [a.strip() for a in allergies.split(",") if a.strip()]
            
            # Log the generation
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'Treatment Plan',
                'age': age,
                'gender': gender,
                'diagnosis_count': len(diagnosis_list),
                'status': 'Processing'
            }
            st.session_state.treatment_logs.append(log_entry)
            
            st.session_state.treatment_plan = ""
            st.markdown("---")  # Separator line
            response_container = st.empty()
            buffer = ""

            for chunk in personalizedTreatmentPlan(
                age=age,
                gender=gender,
                bmi=bmi,
                diagnosis=diagnosis_list,
                allergies=allergies_list,
                lifestyle=lifestyle,
                sleep_schedule=sleep_schedule,
                exercise=exercise,
                diet_preferences=diet_preferences,
                work_level=work_level,
                mental_state=mental_state,
                duration=duration
            ):
                buffer += chunk
                st.session_state.treatment_plan = buffer
                response_container.markdown(buffer, unsafe_allow_html=True)
            
            # Update log
            st.session_state.treatment_logs[-1]['status'] = 'Completed'
            st.session_state.treatment_logs[-1]['plan_length'] = len(buffer)
        
        # Session Logs (full width)
        if st.session_state.treatment_logs:
            st.markdown("---")
            st.subheader("Session Logs")
            log_df = pd.DataFrame(st.session_state.treatment_logs)
            display_df = log_df[['timestamp', 'action', 'age', 'gender', 'diagnosis_count', 'plan_length', 'status']].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            st.dataframe(
                display_df,
                column_config={
                    "timestamp": "Timestamp",
                    "action": "Action",
                    "age": "Age",
                    "gender": "Gender",
                    "diagnosis_count": "Diagnoses",
                    "plan_length": "Plan Length",
                    "status": "Status"
                },
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("Clear Treatment Logs", key="clear_treatment_logs", use_container_width=True):
                st.session_state.treatment_logs = []
                st.rerun()
                
    #Risk Prediction Logic (now tab3)
    with tab3:
        if "risk_result" not in st.session_state:
            st.session_state["risk_result"] = ""
        if "risk_logs" not in st.session_state:
            st.session_state.risk_logs = []
        
        st.header("Welcome to Health Risk Prediction")
        
        # Instructions expander
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use Health Risk Prediction:**
            
            1. **Enter Information**: Fill in your health details
            2. **Get Assessment**: Receive personalized risk analysis
            3. **Review Results**: Understand your health risks
            
            **Note**: This is a predictive tool, not a medical diagnosis.
            Always consult healthcare professionals for accurate assessment.
            """)
        
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30, help="Enter your age in years")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], help="Select your gender")
            smoking = st.checkbox("Smoking", help="Do you currently smoke?")
            alcohol = st.checkbox("Alcohol consumption", help="Do you consume alcohol regularly?")
            exercise_frequency = st.number_input("Exercise frequency (times/week)", min_value=0, max_value=14, value=3, help="How many times do you exercise per week?")
        
        with col2:
            sleep_quality = st.slider("Sleep Quality (1-5)", min_value=1, max_value=5, value=4, help="1 = Poor, 5 = Excellent")
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=23.0, help="Body Mass Index (weight in kg / height in m²)")
            blood_pressure = st.text_input("Blood Pressure", value="120/80", help="Format: systolic/diastolic (e.g., 120/80)")
            glucose_level = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=500, value=95, help="Fasting blood glucose level")
        
        medical_history_input = st.text_area("Medical History (comma separated)", 
                                    placeholder="e.g., Diabetes, Hypertension, Asthma",
                                    help="List any existing medical conditions separated by commas")
        
        # Convert medical history input to list
        medical_history = [m.strip() for m in medical_history_input.split(",")] if medical_history_input else []
        
        # Center the button - REMOVED COLUMNS LAYOUT
        if st.button("Get Health Risk Assessment", type="primary", use_container_width=True):
            # Log the assessment
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'Risk Assessment',
                'age': age,
                'gender': gender,
                'status': 'Processing'
            }
            st.session_state.risk_logs.append(log_entry)
            
            # Create a container for the streaming response - FULL WIDTH
            st.markdown("---")  # Separator line
            response_container = st.empty()
            with response_container:
                st.markdown("**Generating your personalized health assessment...** ⏳")
            
            buffer = ""
            full_response = ""
            
            # Stream the response
            for chunk in healthRiskPrediction(
                age,
                gender,
                smoking,
                alcohol,
                exercise_frequency,
                sleep_quality,
                bmi,
                blood_pressure,
                glucose_level,
                medical_history
            ):
                buffer += chunk
                full_response += chunk
                response_container.markdown(buffer, unsafe_allow_html=True)
            
            st.session_state.risk_result = full_response
            
            # Update log
            st.session_state.risk_logs[-1]['status'] = 'Completed'
            st.session_state.risk_logs[-1]['result_length'] = len(full_response)
            st.session_state.risk_logs[-1]['bmi'] = bmi
            st.session_state.risk_logs[-1]['blood_pressure'] = blood_pressure
        
        # Display previous result if exists - FULL WIDTH
        if st.session_state.risk_result:
            st.markdown("---")
            st.subheader("Your Health Assessment")
            st.markdown(st.session_state.risk_result, unsafe_allow_html=True)  # ← Full width display
            
            # Download button for the report
            report_text = f"""
    # NeuroCare-AI Health Risk Assessment Report
    ## Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    ### User Profile:
    - Age: {age}
    - Gender: {gender}
    - BMI: {bmi}
    - Blood Pressure: {blood_pressure}
    - Glucose Level: {glucose_level} mg/dL

    ### Assessment Results:
    {st.session_state.risk_result}

    ---
    *This report is generated by NeuroCare-AI for informational purposes only.
    Always consult with healthcare professionals for medical advice.*
    """
            
            st.download_button(
                label="📄 Download Report",
                data=report_text,
                file_name=f"health_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Session Logs - FULL WIDTH
        if st.session_state.risk_logs:
            st.markdown("---")
            st.subheader("Assessment History")
            
            # Enhanced logs display
            log_df = pd.DataFrame(st.session_state.risk_logs)
            
            # Handle missing columns gracefully
            available_columns = log_df.columns.tolist()
            display_columns = ['timestamp', 'action', 'age', 'gender', 'status']
            
            if 'bmi' in available_columns:
                display_columns.append('bmi')
            if 'blood_pressure' in available_columns:
                display_columns.append('blood_pressure')
            if 'result_length' in available_columns:
                display_columns.append('result_length')
            
            display_df = log_df[display_columns].copy()
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Create column configuration
            column_config = {
                "timestamp": "Timestamp",
                "action": "Action", 
                "age": "Age",
                "gender": "Gender",
                "status": "Status"
            }
            
            if 'bmi' in display_columns:
                column_config["bmi"] = st.column_config.NumberColumn("BMI", format="%.1f")
            if 'blood_pressure' in display_columns:
                column_config["blood_pressure"] = "BP"
            if 'result_length' in display_columns:
                column_config["result_length"] = st.column_config.NumberColumn("Length")
            
            st.dataframe(
                display_df,
                column_config=column_config,
                use_container_width=True,
                hide_index=True
            )
            
            if st.button("Clear Assessment History", key="clear_risk_logs", use_container_width=True):
                st.session_state.risk_logs = []
                st.session_state.risk_result = ""
                st.rerun()
    # Emotion Detector (now tab7)
    with tab7:
        st.header("Real-time Mood + Sunnah Reminder")
    
        # Instructions section
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            **How to use Emotion Detector (Coming Soon):**
            
            1. **Enable Camera**: Allow camera access when prompted.
            2. **Show Face**: Position your face in the camera view.
            
            **Note**: This feature is currently under maintenance. We appreciate your patience.
            """)
    
        # Show warning message instead of actual processing
        st.warning("⚠️ We have some issues in this tab. We are working on fixing them and apologize for the inconvenience. This feature will be available soon.")
    
        # Just display the camera without doing any processing
        try:
            ctx = webrtc_streamer(
                key="mood-reminder",
                media_stream_constraints={"video": True, "audio": False},
            )
    
            if ctx.state.playing:
                st.info("Camera is active, but emotion detection is temporarily unavailable.")
            elif ctx.state.ended:
                st.info("Camera disconnected.")
        except Exception as e:
            st.error(f"❌ Failed to start camera stream: {e}")
