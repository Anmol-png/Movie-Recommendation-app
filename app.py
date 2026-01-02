import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import face_recognition

st.title("Distraction Sense: AI Study Assistant")
st.write("Helps you stay focused by detecting yawns and looking away.")

class VideoProcessor(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="rgb24")
        face_locations = face_recognition.face_locations(img)
        
        alert_text = ""
        
        for (top, right, bottom, left) in face_locations:
            # Draw rectangle around face
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.rectangle(((left, top), (right, bottom)), outline="blue", width=3)
            
            # Simple dummy detection (for prototype)
            # In real, you can use landmarks to detect yawns and looking away
            alert_text = "👀 Stay focused!"  # placeholder alert
            
            # Draw alert
            font = ImageFont.load_default()
            draw.text((10,10), alert_text, fill=(255,0,0), font=font)
            
            img = np.array(img_pil)
        
        return img

webrtc_streamer(key="distraction-sense", video_transformer_factory=VideoProcessor)

