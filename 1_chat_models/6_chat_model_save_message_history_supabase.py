# Example Source: https://python.langchain.com/v0.2/docs/integrations/memory/google_firestore/

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from supabase_util import SupabaseChatMessageHistory
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = "http://127.0.0.1:54321"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SESSION_ID = "my_session"  # This could be a username or a unique ID
TABLE_NAME = "chat_history"



# Initialize Supabase Chat Message History
print("Initializing Supabase Chat Message History...")
chat_history = SupabaseChatMessageHistory(
    session_id=SESSION_ID,
    table_name=TABLE_NAME,
    client=supabase,
)
print("Chat History Initialized.")
print("Current Chat History:", chat_history.messages)

# Initialize Chat Model
model = ChatOpenAI()

print("Start chatting with the AI. Type 'exit' to quit.")

while True:
    human_input = input("User: ")
    if human_input.lower() == "exit":
        break

    chat_history.add_user_message(human_input)

    ai_response = model.invoke(chat_history.messages)
    chat_history.add_ai_message(ai_response.content) # type: ignore

    print(f"AI: {ai_response.content}")
