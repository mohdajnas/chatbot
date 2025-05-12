import requests
import speech_recognition as sr
import pyttsx3
from transformers import pipeline

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Function to speak text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to convert speech to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ STT error: {e}")
        return ""

# Function to call Ollama REST API
def get_ollama_response(user_input):
    url = "http://192.168.5.46:1234/v1/chat/completions"
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        print("Error:", response.status_code, response.text)
        return "⚠️ Failed to get a response."

# Main loop
def main():
    print("🎙️ Voice chatbot with sentiment analysis (say 'exit' to quit).")
    while True:
        user_input = listen()
        if not user_input:
            continue
        print(f"You: {user_input}")

        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break

        # Analyze sentiment
        sentiment = sentiment_pipeline(user_input)[0]
        print(f"🧠 Sentiment: {sentiment['label']} (score: {sentiment['score']:.2f})")

        # Get response from Ollama
        response = get_ollama_response(user_input)
        print(f"Response: {response}")
        speak(response)

if __name__ == "__main__":
    main()
