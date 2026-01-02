import streamlit as st
import cv2
import numpy as np
import threading
import time
from datetime import datetime
import pyttsx3

# ---------------------- TTS Engine ----------------------
def speak_alert(message):
    """Voice alert using pyttsx3"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(message)
        engine.runAndWait()
    except:
        pass

# ------------------ Streamlit Page Setup ------------------
st.set_page_config(
    page_title="Study Focus Monitor",
    page_icon="📚",
    layout="wide"
)

# ------------------ Session State ------------------
if 'session_active' not in st.session_state:
    st.session_state.session_active = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'duration_minutes' not in st.session_state:
    st.session_state.duration_minutes = 25
if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 0
if 'motion_alerts' not in st.session_state:
    st.session_state.motion_alerts = 0
if 'previous_frame' not in st.session_state:
    st.session_state.previous_frame = None
if 'no_face_count' not in st.session_state:
    st.session_state.no_face_count = 0

# ------------------ Utility Functions ------------------
def detect_face(frame, face_cascade):
    """Detect faces in the frame"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    return frame, len(faces) > 0

def detect_motion(frame1, frame2):
    """Detect motion between frames"""
    if frame1 is None or frame2 is None:
        return False, 0
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21,21),0)
    gray2 = cv2.GaussianBlur(gray2, (21,21),0)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    motion_pixels = np.sum(thresh == 255)
    total_pixels = thresh.shape[0]*thresh.shape[1]
    motion_percentage = (motion_pixels/total_pixels)*100
    return motion_percentage > 8, motion_percentage

def get_time_remaining():
    if not st.session_state.session_active or st.session_state.start_time is None:
        return 0
    elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
    total_seconds = st.session_state.duration_minutes*60
    return max(0, total_seconds - elapsed)

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def start_session():
    st.session_state.session_active = True
    st.session_state.start_time = datetime.now()
    st.session_state.alert_count = 0
    st.session_state.motion_alerts = 0
    st.session_state.no_face_count = 0
    st.session_state.previous_frame = None
    threading.Thread(target=speak_alert, args=(f"Study session started for {st.session_state.duration_minutes} minutes. Stay focused!",), daemon=True).start()

def end_session():
    st.session_state.session_active = False
    threading.Thread(target=speak_alert, args=(f"Session completed! Total alerts: {st.session_state.alert_count}",), daemon=True).start()

# ------------------ Load Haar Cascade ------------------
@st.cache_resource
def load_face_cascade():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_cascade = load_face_cascade()

# ------------------ UI ------------------
st.title("📚 Study Focus Monitor")
st.markdown("Detects your presence and motion to keep you focused during study sessions.")

if not st.session_state.session_active:
    duration = st.slider("Study Duration (minutes)", min_value=5, max_value=180, value=25, step=5)
    st.session_state.duration_minutes = duration
    if st.button("▶️ Start Study Session"):
        start_session()
        st.experimental_rerun()
else:
    time_remaining = get_time_remaining()
    if time_remaining <= 0:
        end_session()
        st.experimental_rerun()

    st.subheader(f"Time Remaining: {format_time(time_remaining)}")
    st.subheader(f"Total Alerts: {st.session_state.alert_count}")

    # Camera feed
    camera_placeholder = st.empty()

    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640,480))
            frame, face_detected = detect_face(frame, face_cascade)

            # Face not detected
            if not face_detected:
                st.session_state.no_face_count += 1
                st.session_state.alert_count += 1
                threading.Thread(target=speak_alert, args=("Face not detected! Stay in front of the camera.",), daemon=True).start()
                cv2.putText(frame, "NO FACE DETECTED!", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
            else:
                st.session_state.no_face_count = 0

            # Motion detection
            if st.session_state.previous_frame is not None:
                motion, motion_pct = detect_motion(st.session_state.previous_frame, frame)
                if motion:
                    st.session_state.motion_alerts += 1
                    st.session_state.alert_count += 1
                    threading.Thread(target=speak_alert, args=("Excessive movement detected!",), daemon=True).start()
                cv2.putText(frame, f"Motion: {motion_pct:.1f}%", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            st.session_state.previous_frame = frame.copy()
            camera_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)
    cap.release()

    st.info("Session locked. Timer will end automatically.")

    time.sleep(0.5)
    st.rerun()

