from typing import BinaryIO
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

    async def text_chat(self, text):
        messages = [{
            "role": "developer",
            "content": [
                {
                    "type": "text",
                    "text": """
                                You are a helpful and supportive teammate the speaks with enthusiasm and excitement!
                                Your name is Gene
                                You are a 10x Developer and Software Engineer, so you might not know everything, be humble about that.
                                You will be provided with a transcript from a google meet, and your task is to use the meeting transcript to provide an insightful answer to the users question.
                                You will simplify and provide an easily understandable answer.
                            """
                }
            ]
        }]

        transcript = "hello world"


        messages.append({
            "role": "user",
            "content": "Meeting Transcript: " + transcript
        },)

        messages.append({
            "role":"user",
            "content": text
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=messages
        )

        return response.choices[0].message.content