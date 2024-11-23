import streamlit as st
import time
from dotenv import load_dotenv
from langserve import RemoteRunnable
load_dotenv()

# FastAPI 서버의 URL
API_BASE_URL = "http://127.0.0.1:8000/api/user"  # 로컬 FastAPI 서버 URL

# Streamlit UI
st.title("FastAPI와 Streamlit 연동하기")

# 사용자 추가
st.header("Create a User")
with st.form("create_user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    user_data = {"name": name, "email": email}

    col1, col2, col3 = st.columns(3)
    with col1:
        create_button = st.form_submit_button("Create User")
    with col2:
        delete_button = st.form_submit_button("Delete User")
    with col3:
        update_button = st.form_submit_button("Update User")

    if create_button:
        response = requests.post(f"{API_BASE_URL}/", json=user_data)
        if response.status_code == 200:
            st.success("User created successfully!")
        else:
            st.error(f"Failed to create user: {response.json().get('detail')}")
    
    if delete_button:
        response = requests.delete(f"{API_BASE_URL}/{name}")
        if response.status_code == 200:
            st.success("User deleted successfully!")
        else:
            st.error(f"Failed to delete user: {response.json().get('detail')}")
    
    if update_button:
        response = requests.put(f"{API_BASE_URL}/{name}", json=user_data)
        if response.status_code == 200:
            st.success("User updated successfully!")
        else:
            st.error(f"Failed to delete user: {response.json().get('detail')}")

# 사용자 목록 조회
st.header("List of Users")
if st.button("Refresh User List"):
    response = requests.get(f"{API_BASE_URL}/")
    if response.status_code == 200:
        users = response.json()
        st.table(users)
    else:
        st.error("Failed to fetch user list")

# def response_generator(response):
#     for word in response.split("\n"):
#         print(word)
#         yield word + "\n"
#         time.sleep(0.05)

# async def main():
#     # llm 사용 방법
#     # llm = RemoteRunnable("http://localhost:8000/llm/")
#     st.title("fake new detection")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # 새로 고침 시 이전에 있던 채팅 기록 가져오기
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])


#     # 유저 입력 = 변수 prompt
#     if prompt := st.chat_input("What is up?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # 유저 메시지를 보여주기
#         with st.chat_message("user"): # user가 보낸 응답이라는 의미
#             st.write(prompt)

#         # session_id = "user_unique_session_id"

#         # answer = llm.invoke({"input" : prompt}, config={"configurable": {"session_id": session_id}})["output"]

#         # 메시지 기록에 담을 답변 내용을 생성
#         assistant_response = ""
#         with st.chat_message("assistant"):
#             for word in response_generator(answer):
#                 st.write(word)
#                 assistant_response += word  # 각 단어를 차례대로 모아 답변 생성

#         # 메시지 기록에 담기
#         st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main()) 