import speech_recognition as sr
import logging

import os
from gtts import gTTS
import google.generativeai as genai
import streamlit as st



#this is logger for the application

LOG_DIR="logs"
LOG_FILE_NAME="application.log"


os.makedirs(LOG_DIR, exist_ok=True)


log_path=os.path.join(LOG_DIR,LOG_FILE_NAME)


logging.basicConfig(
        
    filename=log_path,
    format="[%(asctime)s ] %(name)s - %(levelname)s- %(message)s",
    level=logging.INFO
)




def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio =r.listen(source)
    try:
        print("Recognizing")
        query=r.recognize_google(audio,language="en-in")
        print(f"user said:{query}\n")
    except Exception as e:
        logging.info(e)
        print("say that again please")
        return "None"
    return query





def text_to_speech(text):
    ttx=gTTS(text=text,lang="en")
    ttx.save("speech.mp3")
    






def gemini_model(user_input):
    genai.configure(api_key="AIzaSyCyQcJoXai4L3c3_JmxnrgrD_lD6bsR9AA")
    model = genai.GenerativeModel("gemini-pro")
    response=model.generate_content(user_input)
    results=response.text
    return results



def main():
    st.title("Multilingual Ai Assistant")
    
    if st.button("Ask Me Anything"):
        with st.spinner("Listening..."):
            text=takeCommand()
            response=gemini_model(text)
            text_to_speech(response)
            
            
            audio_file=open("speech.mp3",'rb')
            audio_bytes=audio_file.read()
            
            st.text_area(label="Response:",value=response,height=350)
            st.audio(audio_bytes,format='audio/mp3')
            st.download_button(label="Download speech",
                               data=audio_bytes,
                               file_name="speech.mp3",
                               mime="audio/mp3")
                                      
main()    
    
   
  

             
    