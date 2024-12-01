import streamlit as st
import requests

def login(api_base_url):
    st.title("로그인")
    
    username = st.text_input("사용자 이름")
    user_data = {"name": username}
    
    if st.button("로그인"):
        response = requests.get(f"{api_base_url}/login/{username}")
        if response.status_code == 200:
            st.success("로그인 성공!")
            st.session_state.logged_in = True
            st.session_state.user_info = user_data
            st.rerun()
        else:
            st.error("로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")
        
    if st.button("회원가입"):
        response = requests.post(f"{api_base_url}/login/", json=user_data)
        if response.status_code == 200:
            st.success("회원가입 성공!")
            st.session_state.logged_in = True
            st.session_state.user_info = user_data
            st.rerun()
        else:
            message = response.json.get("detail")
            st.error(f"회원가입 실패 {message}")
