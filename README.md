# fake-news-detection - the latest fake news detection project that uses OpenAI technology to detect the authenticity of YouTube videos
## 프로젝트 개요 
오늘날 정보는 우리의 삶을 윤택하게 만드는 중요한 도구로 자리 잡았습니다. 사람들은 유용한 정보를 통해 더 나은 선택을 하고 삶의 질을 향상시키고 있습니다. 그러나 정보의 확산과 더불어 가짜 정보, 허위 광고 등으로 인해 피해를 입는 사례도 점차 증가하고 있습니다. 특히, 최근에는 유명인을 도용한 허위 광고와 거짓된 정보를 이용해 사람들을 선동하는 행위가 빈번히 발생하고 있습니다. 이러한 문제는 신뢰할 수 있는 정보 제공의 중요성을 더욱 부각시키고 있습니다.
저희 팀은 이러한 문제를 해결하기 위해 최신 데이터 분석 기술과 대규모 언어 모델 기술을 활용하여, 정보를 진위 여부에 따라 판별해주는 시스템을 개발하게 되었습니다. 

이 프로젝트는 국민대학교 알파 프로젝트의 일환으로써 시작되었고 Stremlit을 기반으로 UI를 설계하였습니다.

또한 OpenAI의 Chatgpt-4o 모델을 기준으로 RAG 시스템을 구축하였습니다.

## 프로젝트의 주요 성과 및 기대 효과
 네이버, 구글, 유튜브 등에서 수집한 공신력 있는 데이터를 바탕으로  DB를 구축하고, 누구나 쉽게 접근할 수 있는 웹 UI을 설계하였습니다. 이 프로젝트를 통해 가짜 정보의 확산을 차단하며, 공신력 있는 정보를 더 쉽게 판별하고자 하였습니다. 사용자들은 직관적이고 간편한 채팅형 서비스를 통해 필요한 정보를 빠르게 검증할 수 있습니다. 앞으로도 프로젝트를 개선하며 허위 정보로 인한 사회적 갈등과 혼란을 줄이고 정보 투명성을 확보함으로써 안정된 사회 환경 조성에 기여하고자 합니다.

## 주요 기능
1. 대화 히스토리 기능
2. 로그인을 활용한 맞춤형 서비스

## 프로젝트에서 사용된 기술
- Langchain
    - Langgraph
- RAG
- FastAPI
- Streamlit
- Youtube API v3
- Tavily Search

## 설치 및 실행 방법
### 요구 사항
- Python==3.11
- Langchain 및 관련 라이브러리
- SQL Alchemy + FastAPI
- Streamlit
- OpenAI API 키
- TAVILY API 키
### 실행 방법
1. Git Clone or ZIP으로 다운로드 받기
    ```
    git clone https://github.com/hyeonsang010716/fake-news-detection.git
2. 가상환경 생성 및 사용
    ```
    py -3.11 -m venv 
3. requirements.txt 설치
    ```
    pip install -r requirements.txt
4. .env 파일 생성 및 환경변수 입력
    ```
    TAVILY_API_KEY=your_tavily_api_key
    OPENAI_API_KEY=your_openai_api_key
5. 백엔드 실행
    ```
    cd fake-news-detection/backend/
    python main.py
6. Streamlit 실행
    ```
    cd fake-news-detection/front/
    streamlit run app.py

## file Structure
```
|- backend             # 백엔드 파일 디렉토리 
|   |- api             # FastAPI 디렉토리
|   |   |- router      # Router 기능
|   |   |   |- answer     
|   |   |   |- question
|   |   |- schema      # 스키마 구조
|   |   |   |- answer     
|   |   |   |- question
|   |   |   |- user
|   |- database        # Database 관련 코드 모음
|   |   |- database.db
|   |   |- models.py   # 모델 관련 정의
|   |   |- database.py # 데이터베이스 설정
|   |- main.py         # 메인 파일
|   |- model_test.py   # 모델 테스트
|   |
|   |- model           # LLM 디렉토리
|   |   |- tools       # RAG 도구 디렉토리
|   |   |   |- __init__.py
|   |   |   |- News_keyword_crawling.py
|   |   |   |- tavily_search.py
|   |   |   |- youtube_download.py
|   |   |- __init__.py
|   |   |- agent.py
|   |   |- prompt.py
|   |   |- state.py
|
|- front
|   |- app.py          # UI  파일
|   |- chat.py         # Chating 기능
|   |- login.py        # login 기능
## 세부 진행 과정
[PDF 파일 보기](https://github.com/hyeonsang010716/fake-news-detection/docs/alpha_project.pdf)
## 프로젝트 라이선스
이 프로젝트는 MIT License를 따름니다.