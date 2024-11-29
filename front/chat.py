import streamlit as st
import time
import requests
from typing import Dict, Union, List, Tuple

def response_generator(response):
    for word in response.split("\n"):
        print(word)
        yield word + "\n"
        time.sleep(0.05)

def chat_llm(api_base_url):
    st.title("fake new detection")

    # 채팅 기록 처리
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 화면 처리
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"): # user가 보낸 응답이라는 의미
            st.write(prompt)

        if prompt[0] == "/":
            cmd = prompt[1:]
            if cmd == "clear":
                st.session_state.messages = []
                st.rerun()
            elif cmd == "questions":
                is_connected, _questions, answers = request_server(api_base_url, "get")
                if not is_connected:
                    st.error(answer)
                    st.stop()
                st.markdown("### Questions")
                for question, answer in list(answers):
                    st.markdown(f"- {question}: {answer}")
                
            else:
                st.error("Wrong command")
        else:
            # 메시지 기록에 담을 답변 내용을 생성
            user_data = {"content": prompt}
            is_connected, answer = request_server(api_base_url, "post", user_data)
            if not is_connected:
                st.error(answer)
                st.stop()

            assistant_response = ""
            with st.chat_message("assistant"):
                for word in response_generator(answer):
                    st.write(word)
                    assistant_response += word  # 각 단어를 차례대로 모아 답변 생성

            # 메시지 기록에 담기
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})


def request_server(api_base_url: str, type: str, json_data: Dict=None) -> Union[Tuple[bool, str], Tuple[bool, List, List]]:
    if type == "post":
        response = requests.post(f"{api_base_url}/chat/", json=json_data)
        if response.status_code ==200:
            answer = response.json().get("answers")
            return [True, answer[0]["content"]]
        else:
            return [False, f"Failed connect server: {response.json().get('detail')}"]
    elif type == "get":
        response = requests.get(f"{api_base_url}/chat/")
        if response.status_code ==200:
            data = response.json()
            return [True, data.keys(), data.items()]
        else:
            return [False, f"Failed connect server: {response.json().get('detail')}"]
        
