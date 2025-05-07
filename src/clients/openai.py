from openai import OpenAI
import requests

def _get_transcript(meet_key):
    url = f"http://localhost:8000/document/{meet_key}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response

class OpenaiClient:
    def __init__(self):
        self.client = OpenAI()
        self.sessions = {}  # Stores history per session ID

    def _init_session(self, session_id):
        # Ensure session message history is initialized
        if session_id not in self.sessions:
            self.sessions[session_id] = [
                {
                    "role": "system",
                    "content": """
                        You are a helpful and supportive teammate that speaks with enthusiasm and excitement!
                        Your name is Gene.
                        You are a 10x Developer and Software Engineer—be humble and simplify complex ideas.
                        You will be provided with a transcript from a Google Meet and answer based on it.
                    """
                }
            ]

    async def text_chat(self, text, session_id="default", transcript=None):
        self._init_session(session_id)

        if transcript:
            self.sessions[session_id].append({
                "role": "user",
                "content": "Meeting Transcript: " + transcript
            })

        self.sessions[session_id].append({
            "role": "user",
            "content": text
        })

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.sessions[session_id]
        )

        # Append assistant reply to history for continuity
        self.sessions[session_id].append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

        return response.choices[0].message.content
