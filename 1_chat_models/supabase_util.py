from supabase import Client


class SupabaseChatMessageHistory:
    def __init__(self, session_id: str, table_name: str, client: Client):
        self.session_id = session_id
        self.table_name = table_name
        self.client = client
        self.messages = self.get_chat_history()  # Load chat history on initialization

    def get_chat_history(self):
        """Load chat history from the Supabase database"""
        response = self.client.from_(self.table_name).select("*").eq("session_id", self.session_id).execute()
        
        # Return the list of messages sorted by time
        return sorted(response.data, key=lambda x: x['created_at']) if response.data else []

    def add_user_message(self, message: str):
        """Add user message to the database"""
        self.add_message("user", message)

    def add_ai_message(self, message: str):
        """Add AI message to the database"""
        self.add_message("ai", message)

    def add_message(self, role: str, content: str):
        """Add a message to the database and update the local message list"""
        message_data = {
            "session_id": self.session_id,
            "role": role,
            "content": content,
            "created_at": "now()"
        }
        response = self.client.from_(self.table_name).insert(message_data).execute()
        
        self.messages.append(message_data)

