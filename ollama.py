import subprocess
import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"❌ STT request error: {e}")
        return ""

def query_ollama(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "llama3.2"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=prompt)

    if stderr.strip():
        print("[stderr]:", stderr.strip())
    if stdout.strip():
        return stdout.strip()
    return "⚠️ No response received."

def interact_with_ollama():
    print("🎙️ Voice mode activated (say 'exit' to quit).")
    while True:
        user_input = listen()
        if not user_input:
            continue
        print(f"You: {user_input}")

        if user_input.lower() == "exit":
            print("👋 Exiting...")
            break

        response = query_ollama(user_input)
        print(f"Ollama: {response}")
        speak(response)

if __name__ == "__main__":
    interact_with_ollama()
