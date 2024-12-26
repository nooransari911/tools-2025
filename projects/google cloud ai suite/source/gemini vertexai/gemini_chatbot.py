# uses static-manifest project ONLY

#import vertexai
#from vertexai.generative_models import GenerativeModel, ChatSession
import google.generativeai as genai
#from vertexai.generative_models import Part
import os, json


# TODO(developer): Update and un-comment below line
# project_id = "static-manifest"
# vertexai.init(project=project_id, location="us-west1")

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-001")

chat = model.start_chat()


def get_chat_response(chat: genai.ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

"""prompt = "Hello."
print(get_chat_response(chat, prompt))
prompt = "What are all the colors in a rainbow?"
print(get_chat_response(chat, prompt))
prompt = "Why does it appear when it rains?"
print(get_chat_response(chat, prompt))"""


while True:
    prompt = input(">> ")
    if prompt=="EXIT":
        print("Exiting....")
        exit(0)
    else:
        print(get_chat_response(chat, prompt))

