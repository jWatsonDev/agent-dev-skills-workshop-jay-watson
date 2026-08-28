import os

import streamlit as st
import vertexai
from vertexai import agent_engines

AGENT_RESOURCE_NAME = os.environ["AGENT_RESOURCE_NAME"]
_, PROJECT_ID, _, LOCATION, *_ = AGENT_RESOURCE_NAME.split("/")
WEATHY_AVATAR = "weathy.svg"

st.set_page_config(page_title="ReadyNow!", page_icon="🧭")

header_logo, header_text = st.columns([1, 5])
with header_logo:
    st.image(WEATHY_AVATAR, width=72)
with header_text:
    st.title("ReadyNow!")
    st.caption("Meet Weathy — your FEMA emergency preparedness assistant. Agent Dev Skills Workshop, Challenge 6.")


@st.cache_resource
def get_agent():
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    return agent_engines.get(AGENT_RESOURCE_NAME)


@st.cache_resource
def get_session():
    return get_agent().create_session(user_id="streamlit-user")


agent = get_agent()
session = get_session()

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, content in st.session_state.messages:
    avatar = WEATHY_AVATAR if role == "assistant" else None
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

prompt = st.chat_input("Ask about weather, evacuation routes, local news, or general safety…")
if prompt:
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=WEATHY_AVATAR):
        placeholder = st.empty()
        full_response = ""
        for event in agent.stream_query(
            user_id="streamlit-user",
            session_id=session["id"],
            message=prompt,
        ):
            for part in event.get("content", {}).get("parts", []):
                if "text" in part:
                    full_response += part["text"]
                    placeholder.markdown(full_response)
        st.session_state.messages.append(("assistant", full_response))
