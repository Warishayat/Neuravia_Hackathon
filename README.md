# NeuroCare-AI 🧠🏥

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge)](https://)
[![Healthcare](https://img.shields.io/badge/Healthcare-Tech-4ECDC4?style=for-the-badge)](https://)

**An all-in-one intelligent health assistant platform** combining cutting-edge AI with practical medical tools for comprehensive healthcare solutions. Built with passion by **Team KlugPeps**.

![NeuroCare-AI Dashboard](https://media.nature.com/lw1024/magazine-assets/d42473-023-00106-8/d42473-023-00106-8_25389508.jpg)

## ✨ Features

### 🧠 Brain Tumor Detection
- **AI-powered MRI scan analysis** with confidence scoring
- **Detects glioma, meningioma, and pituitary tumors**
- **Real-time processing** with detailed session logging
- **Educational tool** with exportable results

### 📄 Medical Report Analyzer
- **PDF medical report processing** with RAG pipeline
- **Natural language Q&A** about your health reports
- **Secure local processing** with vectorization
- **Instant insights** from complex medical documents

### 💊 MediGuide AI Pharmacist
- **Medicine identification** from images
- **Comprehensive drug information**: usage, dosage, side effects
- **Supported formats**: JPG, JPEG, PNG
- **Instant medication guidance**

### 🤖 Health Assistant Chatbot
- **24/7 AI health companion**
- **General wellness guidance**
- **Conversation history** with session tracking
- **Personalized health responses**

### 🏋️ Personalized Treatment Plans
- **Custom wellness plans** based on health profile
- **Lifestyle-based recommendations**
- **Diet and exercise guidance**
- **Mental wellness support**

### 😊 Real-time Emotion Detection
- **Webcam-based mood analysis**
- **Instant wellness advice**
- **Privacy-focused local processing**
- **Mental health support**

## 🚀 Live Demo

Experience NeuroCare-AI live:  
👉 **[https://neurocare-ai0.streamlit.app/](https://neurocare-ai0.streamlit.app/)**

## 🛠️ Technology Stack

- **Frontend**: Streamlit, HTML/CSS
- **Backend**: Python 3.8+
- **AI Models**: LangChain, Groq API, Custom AI Models
- **Database**: SQLite with BCrypt encryption
- **Computer Vision**: OpenCV, PIL
- **Authentication**: Encrypted Cookie Management
- **Real-time Processing**: WebRTC, Async operations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Webcam (for emotion detection)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/neurocare-ai.git
cd neurocare-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Add your API keys to .env file
```

5. **Initialize database**
```bash
python -c "from app import init_db; init_db()"
```

6. **Run the application**
```bash
streamlit run app.py
```

## 🏗️ Project Structure

```
neurocare-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── users.db              # SQLite database (auto-generated)
├── Mediguide/            # Medicine identification module
├── Health_Assistant/     # Chatbot functionality
├── Health_Risk/          # Risk prediction module
├── Medical_Reports/      # PDF processing module
├── Personalize_treatment/# Treatment planning
├── emotion_detection/    # Mood detection
├── tumor_detection/      # MRI analysis
└── temp_mediguide/       # Temporary image storage
```

## 👥 Team KlugPeps

### Core Contributors
- **Warishayat** - Team Lead & Full-Stack AI Engineer
- **Salaar Tariq** - AI Developer & Model Architect
- **Fakiha Hashmat** - Frontend + AI Engineer
- **Mehreen** - AI Engineer & Pipeline Development
- **Khadeejah** - AI Engineer & Integration Specialist

### What does "KlugPeps" mean?
"KlugPeps" combines the German word "Klug" (meaning smart/clever) with "Peps" (people), representing our team of smart individuals creating intelligent solutions.

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
ENCRYPTION_KEY=your_encryption_key
DATABASE_URL=sqlite:///users.db
```

### Database Schema
```sql
users (
    email TEXT PRIMARY KEY,
    password TEXT
)
```

## 💡 Usage Examples

### Brain Tumor Detection
1. Upload an MRI image
2. Click "Detect Tumor"
3. View AI analysis with confidence scores
4. Download session logs

### Medical Report Analysis
1. Upload PDF medical report
2. Ask questions about your report
3. Receive AI-powered insights
4. Maintain conversation history

### Health Risk Assessment
1. Enter health parameters
2. Get personalized risk analysis
3. View structured recommendations
4. Track assessment history

## 🛡️ Privacy & Security

- **Data Protection**: All medical data processed locally when possible
- **Encryption**: BCrypt password hashing + encrypted cookies
- **No Data Storage**: Medical images and reports processed temporarily
- **Privacy-First**: Webcam data never leaves your device
- **Secure Authentication**: Email-based accounts with secure sessions

## ⚠️ Medical Disclaimer

> **Important**: NeuroCare-AI is an educational and informational tool. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions you may have regarding medical conditions.

**Never disregard professional medical advice or delay in seeking it because of something you have read or interpreted using this application.**

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Areas for Contribution
- New health modules
- UI/UX improvements
- Performance optimization
- Additional integrations
- Documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, questions, or feedback:
- 📧 Email: warishayat666@gmail.com
- 🐛 [Issue Tracker](https://github.com/yourusername/neurocare-ai/issues)
- 💬 [Discussions](https://github.com/yourusername/neurocare-ai/discussions)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Open-source AI and healthcare communities
- Medical professionals who provided guidance
- All contributors and testers
- The AI research community for groundbreaking work

---

**Made with ❤️ for better healthcare accessibility**

![Healthcare Innovation](https://img.shields.io/badge/Innovation-Healthcare-2A9D8F?style=for-the-badge)
![AI for Good](https://img.shields.io/badge/AI_for_Good-Health-264653?style=for-the-badge)

**© 2024 NeuroCare-AI. All rights reserved. Built by Team KlugPeps.**
