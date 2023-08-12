import os
from dotenv import load_dotenv
import gpt4all
import streamlit as st

load_dotenv()

model_dir = os.getenv("DEFAULT_MODEL_DIR")
model_name = os.getenv("MODEL_NAME")
app_title = os.getenv("TITLE")

st.title(app_title)

@st.cache_resource # one time load
def load_model():
    # set default dir of model to current project
    gpt4all.gpt4all.DEFAULT_MODEL_DIRECTORY = model_dir    
    #load model
    return gpt4all.GPT4All(model_name=model_name)

if "chatting_messages" not in st.session_state:
    st.session_state["chatting_messages"] = [
            {
                "role":"assistant", 
                "content":"Ask me a question. Data will not cross internet", 
                "question":''
            }]

for ms in st.session_state.chatting_messages:
    if ms["question"] != '': # handle Initial load 
        st.chat_message("user").write(ms["question"])    
    st.chat_message(ms["role"]).write(ms["content"])

if chat := st.chat_input("Ask questions, Data is not shared over internet", key="user_input"):
    question = [{"role":"user", "content":chat}]
    st.chat_message("user").write(chat)
    gptj = load_model() #load model.

    # show busy cursor, chat completion will take some time to process the request.
    with st.spinner('GPT model processing your request..'):
        response = gptj.chat_completion(question)
        extractAnswer = response["choices"][0]["message"]["content"]
    
    # response from model can be empty for prompt like "thank you"
    if extractAnswer != '':
        answer = {"role":"assistant", "content":extractAnswer, "question": chat}    
        st.chat_message("assistant").write(extractAnswer)
        st.session_state.chatting_messages.append(answer)
