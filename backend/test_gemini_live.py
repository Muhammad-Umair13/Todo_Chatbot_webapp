import os
from dotenv import load_dotenv
from src.chatbot.services import AgentService
from sqlmodel import Session, create_engine
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_actual_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in .env")
        return

    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    
    agent = AgentService(api_key=api_key)
    
    # We need a session, but since we don't expect tool calls for this simple test, 
    # we can use a mock or a dummy sqlite session
    engine = create_engine("sqlite:///:memory:")
    with Session(engine) as session:
        try:
            print("Sending message to Gemini...")
            response, tools = agent.run(
                session=session,
                user_id="test_user",
                user_message="Hello, who are you and what can you do?",
                conversation_history=[]
            )
            print("\nGemini Response:")
            print(response)
            print("\nTool Calls:", tools)
        except Exception as e:
            print(f"\nError occurred: {e}")

if __name__ == "__main__":
    test_actual_gemini()
