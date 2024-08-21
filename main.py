from typing import Annotated
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from langserve import add_routes
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
langchain_project = os.getenv("TestChatAgent")
service_url = os.getenv("SERVICE_URL")

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


llm = ChatGroq(temperature=0,
    model="llama3-70b-8192")


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


#Graph Building
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile()
# from IPython.display import Image, display

# try:
#     display(Image(graph.get_graph().draw_mermaid_png()))
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass
# def textToSpeech(text):
#     from gtts import gTTS
#     import subprocess
#     tts = gTTS(text, lang='en', slow=False)
#     tts.save("voice_output.mp3")
#     subprocess.call(["afplay","voice_output.mp3"])
# def speechToText():
#     import speech_recognition as sr
#     r = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         print("Say something!")
#         audio = r.listen(source)
#     try:
#         print("You said: " + r.recognize_google(audio))
#         return r.recognize_google(audio)
#     except sr.UnknownValueError:
#         print("Could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#     return ""


app=FastAPI(
    title="TestAgent Server",
    description="Simple server for test agent",
    version="1.0"
)
# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware)
add_routes(
    app, graph, path = "/graph"
) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# final = graph.invoke({"messages": ["Hello!"]})
# print(final['messages'])
# while True:
#     user_input = input("User: ")
#     # user_input = speechToText()
#     # while(user_input==""):
#     #     user_input = speechToText()
    
#     # print("User:",user_input)
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         # textToSpeech("Goodbye!")
#         break
#     for event in graph.stream({"messages": ("user", user_input)}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#             # textToSpeech(value["messages"][-1].content) 

