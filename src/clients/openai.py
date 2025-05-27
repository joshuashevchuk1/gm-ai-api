from typing import BinaryIO
from openai import OpenAI

class OpenaiClient:
    def __init__(self):
        self.client = OpenAI()


    async def text_chat(self, text: str, meet_key: str):
        messages = []
        messages.append({
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
                })
        messages.append({
                    "role": "user",
                    "content": "Meeting Transcript: " + "hello world"
                })
        messages.append({
            "role": "user",
            "content": "User Message: " + text
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=messages
        )

        return response.choices[0].message.content