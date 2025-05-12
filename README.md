
# 🎙️ Voice Chatbot with Ollama & LLaMA3.2

This Python project enables real-time voice interaction with a local LLM (LLaMA3.2) using [Ollama](https://ollama.com/). It captures your voice, converts it to text, sends it to a local language model, and reads the response aloud.

---

## 🛠️ Features

- 🎤 Voice input via microphone (using SpeechRecognition)
- 🧠 Text generation via LLaMA3.2 with Ollama
- 🔊 Spoken replies using pyttsx3 (offline TTS)
- 🗨️ Local, private, and open-source
- ❌ Say "exit" to quit the session

---

## 📦 Requirements

### Python Packages

Install dependencies with pip:

```bash
pip install speechrecognition pyttsx3
````

### Ollama Setup

Make sure you have [Ollama](https://ollama.com) installed and running. Then pull the model:

```bash
ollama pull llama3.2
```

> ✅ Ollama runs the language model **locally** — no API keys required!

---

## ▶️ Usage

1. Connect your microphone
2. Run the script:

```bash
python voice_chatbot.py
```

3. Speak when prompted.
4. Say **"exit"** to stop.

---

## 💻 Source Code

```python
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
```

---

## 📁 File Structure

```
voice_chatbot.py       # Main chatbot script
README.md              # This file
```

---

## 📝 Notes

* A working microphone is required.
* Google STT (used by `SpeechRecognition`) needs internet access.
* pyttsx3 works offline using your OS's default TTS engine.
* Ollama runs models locally — ideal for privacy-focused applications.

---

## 📜 License

MIT License

```

Let me know if you'd like a version that uses Whisper for offline transcription or adds GUI support.
```
