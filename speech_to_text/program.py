import speech_recognition as sr
from transformers import pipeline

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing speech...")
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']
    
# Combine speech recognition and summarization
recognized_text = recognize_speech()
if recognized_text:
    summary = summarize_text(recognized_text)
    f = open("file.txt", "w+")
    f.write(summary)
    f.close()
        
    print("Recognized Text:", recognized_text)
    print("Summary:", summary)
