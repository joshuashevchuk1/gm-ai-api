import requests
from openai import OpenAI

class OpenaiClient:
    def __init__(self):
        self.client = OpenAI()

    def _get_transcript(self,meet_key):
        url = f"http://localhost:8000/document/{meet_key}/transcript"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "meet_key": meet_key,
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != "200":
            return None
        return response

    def _get_convo_history(self,meet_key):
        url = f"http://localhost:8000/document/{meet_key}/convo_history"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "meet_key": meet_key,
        }

        response = requests.post(url, headers=headers, json=data)
        return response


    async def text_chat(self, text: str, meet_key: str):
        messages = []
        convo_resp = self._get_convo_history(meet_key)
        transcript_res = self._get_transcript(meet_key)

        if convo_resp is not None:
            messages.append(convo_resp.text)
        elif transcript_res is not None and convo_resp is None:
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
                "content": "Meeting Transcript: " + transcript_res.content
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