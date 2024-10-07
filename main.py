import pyttsx3
import pyaudio
import vosk
import json

class VoiceAssistant:
    def __init__(self):
        # Initialize pyttsx3 for Text-to-Speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Set speed rate of speech
        self.tts_engine.setProperty('volume', 1.0)  # Set volume level 0.0 to 1.0

        # Initialize Vosk for Speech-to-Text
        self.model = vosk.Model(r"D:\vosk-model-en-us-0.22\vosk-model-en-us-0.22")  # Path to the Vosk model
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()

    def speak(self, text):
        """Converts text to speech using pyttsx3."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def recognize_speech(self):
        """Converts speech to text using Vosk."""
        stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        print("Listening...")
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                result_dict = json.loads(result)
                if result_dict.get('text'):
                    print("Recognized:", result_dict['text'])
                    return result_dict['text']
    
    def run(self):
        """Main loop to run the voice assistant."""
        self.speak("Hello! How can I assist you today?")
        
        while True:
            command = self.recognize_speech()

            if "exit" in command or "stop" in command:
                self.speak("Goodbye!")
                break

            # Here you can add more functionality based on commands
            if "hello" in command:
                self.speak("Hello there!")
            elif "your name" in command:
                self.speak("I am your voice assistant.")
            else:
                self.speak(f"You said: {command}")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
