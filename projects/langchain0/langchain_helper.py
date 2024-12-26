#from langchain_openai import OpenAI
#from langchain_google_vertexai import VertexAI
#import vertexai


import os
from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv



load_dotenv()
api_key = os.environ ["GOOGLE_API_KEY"]


def generate_response (rocket_name, query_type):
    """
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
    print(
        llm.invoke(
            "What are some of the pros and cons of Python as a programming language?"
        )
    )
    :return:
    """


    llm = GoogleGenerativeAI(model="gemini-1.5-flash-001", google_api_key=api_key)

    rocket_prompt_template = PromptTemplate.from_template (
        template="{query_type} {rocket_name} in table form. Format nicely"
    )


    response_chain = rocket_prompt_template | llm
    response = response_chain.invoke ({
        "rocket_name": rocket_name,
        "query_type": query_type
    })


    return response


def generate_response_video ():
    llm = GoogleGenerativeAI(model="gemini-1.5-flash-001", google_api_key=api_key)

    video_message = {
        "type": "image_url",
        "image_url": {
            "url": "https://fastly.picsum.photos/id/543/536/354.jpg?hmac=O-U6guSk3J8UDMCjnqQHaL8EAOR9yHXZtgA90Bf5UTc",
        },
    }

    text_message = {
        "type": "text",
        "text": "What is shown in this image?",
    }

    # Prepare input for model consumption
    message = HumanMessage(content=[text_message, video_message])

    # invoke a model response
    response = llm.invoke([message])
    return response


def chatbot (query):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    prompt = PromptTemplate(
        input_variables=["query"],
        template="""
            {query}
            """
    )

    chain = prompt | llm

    response = chain.invoke({"query": query})
    return response.content


def chatbot_base_im (query):
    pass






if __name__ == "__main__":
    pass
    #ai_response = generate_response("SpaceX Starship")
    #ai_response = generate_response_video()
    #print(ai_response)
    #print (GoogleGenerativeAI)




