import cv2
from langchain_groq import ChatGroq
from typing import Dict

llm = ChatGroq(model="moonshotai/kimi-k2-instruct", temperature=0.7)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
emotion_cache: Dict[str, str] = {"last_emotion": None, "last_advice": ""}

def detect_emotion(frame) -> str:
    """Detects emotion from a frame: happy, sad, neutral"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)

    if len(faces) == 0:
        return "neutral"

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=22, minSize=(25, 25))
        if len(smiles) > 0:
            return "happy"
        else:
            return "sad" if roi_gray.mean() < 110 else "neutral"
    return "neutral"


def get_mood_advice(emotion: str) -> str:
    """Returns advice based on emotion, using cache to avoid repeated API calls"""
    if emotion == "happy":
        return "Smile is the Sunnah of Prophet Muhammad (SAW). Keep spreading positivity!"

    # Use cached advice if same emotion
    if emotion_cache["last_emotion"] == emotion:
        return emotion_cache["last_advice"]

    # Prompt for LLM
    if emotion == "sad":
        prompt = """
        The user seems sad.
        Provide a short, empathetic self-care suggestion to uplift their mood
        and encourage them until they feel happy."
        """
    else:  # neutral
        prompt = """
        The user seems neutral.
        Provide a short positive message or motivation to lighten their mood."
        """

    response = llm.invoke(prompt).content.strip()

    # Update cache
    emotion_cache["last_emotion"] = emotion
    emotion_cache["last_advice"] = response

    return response


def process_frame(frame):
    """Process a frame and overlay emotion + advice"""
    emotion = detect_emotion(frame)
    advice = get_mood_advice(emotion)

    # Draw rectangle
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 6)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"Emotion: {emotion}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #Advice bottom
    h, w, _ = frame.shape
    y0, dy = h - 100, 30
    for i, line in enumerate(advice.split("\n")):
        yy = y0 + i*dy
        cv2.putText(frame, line, (20, yy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return frame
