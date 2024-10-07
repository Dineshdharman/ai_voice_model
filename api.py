import vosk
import json
import pyttsx3
import pyaudio
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Ollama model initialization (replaces OpenAI GPT)
model = OllamaLLM(model="llama3")
template = """
        Answer the question below.

        Here is the conversation history :{context}

        Question:{question}

        Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Function to process command (either simple or via Llama)
def process_command(command, context=""):
    command = command.lower()

    # Rule-based simple commands
    if "time" in command:
        return "The current time is 3 PM."
    elif "your name" in command:
        return "My name is Assistant."
    elif "weather" in command:
        return "The weather is sunny."
    else:
        # For complex queries, use the Ollama Llama model
        return ask_llama(command, context)

# Ask Ollama Llama model if the command is not in rule-based responses
def ask_llama(command, context=""):
    try:
        # Send the command to the local Ollama Llama model
        result = chain.invoke({"context": context, "question": command})
        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to convert text to speech (TTS)
def speak(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

# Vosk model initialization for speech recognition
model_path = "D:/vosk-model-en-in-0.5/vosk-model-en-in-0.5"
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Audio setup
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

context = ""  # Global context variable to hold conversation history

# Function to handle voice input
def handle_voice_input():
    global context  # Declare context as global to modify it inside this function
    while True:
        data = stream.read(8192)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            recognized_text = result['text']
            print(f"Recognized: {recognized_text}")
            
            if recognized_text:
                # Process the recognized text and get the response from the assistant
                response = process_command(recognized_text, context)
                print(f"Assistant: {response}")
                speak(response)

                # Update conversation context (for use in multi-turn conversations)
                context += f"User: {recognized_text}\nAI: {response}\n"

# Function to handle text input
def handle_text_input():
    global context  # Declare context as global to modify it inside this function
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = process_command(user_input, context)
        print(f"Assistant: {response}")
        speak(response)

        # Update conversation context (for use in multi-turn conversations)
        context += f"User: {user_input}\nAI: {response}\n"

# Main function to choose input mode
def main():
    print("Choose your input mode:")
    print("1. Voice")
    print("2. Text")

    choice = input("Enter 1 for Voice, 2 for Text: ")

    if choice == '1':
        print("Voice input selected. Speak now.")
        handle_voice_input()
    elif choice == '2':
        print("Text input selected. Start typing.")
        handle_text_input()
    else:
        print("Invalid choice. Please restart and choose again.")

if __name__ == "__main__":
    main()
