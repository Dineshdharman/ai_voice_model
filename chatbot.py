from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """ 
Answer the question below.

Here is the conversation history:
{context}

Question: {question}

Answer:
"""

# Load the model
model = OllamaLLM(model="llama3")
# Create the prompt template
prompt = ChatPromptTemplate.from_template(template)
# Combine the prompt template and model
chain = prompt | model

def handle_conversation():
    context = ""
    print("welcome")
    
    while True:
        user_input = input("you: ")
        if user_input.lower() == "exit":
            break
        
        # Pass dynamic user input and context
        result = chain.invoke({"context": context, "question": user_input})
        print(result)
        
        # Update context with the current conversation
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()
