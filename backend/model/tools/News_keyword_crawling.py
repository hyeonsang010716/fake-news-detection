import time
import random
import requests
from bs4 import BeautifulSoup

def fetch_news_content(keyword):
    # 키워드로 검색 URL 생성 (띄어쓰기를 +로 변환)
    query = keyword.replace(" ", "+")
    search_url = f"https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={query}"
    
    # HTTP 요청 헤더
    headers = {
        "User-Agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36"
    }
    
    # 검색 페이지 요청
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return f"검색 페이지 요청 실패: {response.status_code}"
    # 검색 결과 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    link_tags = soup.select("a.info")[:3]  # 첫 10개의 뉴스 링크 가져오기
    links = list(set(tag["href"] for tag in link_tags)) # 중복 제거
    # 중복 제거 후 최대 3개의 링크 선택
    selected_links = links[:1]
    news_contents = []
    
 
    for news_url in selected_links:
        
        # 뉴스 페이지 요청
        news_response = requests.get(news_url, headers=headers)
        if news_response.status_code != 200:
            news_contents.append(f"뉴스 요청 실패: {news_response.status_code}")
            continue
         
        time.sleep(random.uniform(0.5, 1.5))
        # 뉴스 페이지 파싱
        news_soup = BeautifulSoup(news_response.text, "html.parser")
        article_tag = news_soup.find("article", {"id": "dic_area"})
        
        if article_tag:
            content = article_tag.get_text(strip=True, separator=" ")
            news_contents.append(f"{content}")
        else:
            news_contents.append("기사 본문을 찾을 수 없습니다.")

    
    news_contents.append("관련 기사가 없습니다.")



    
    return news_contents[0]

# 함수 실행 예시
if __name__ == "__main__":
    #keyword = '전세대출'
    keywords = ['전세대출', '가계부채', '주택담보대출', '보증기관', '전세 사기']
    #news_results = fetch_news_content(keyword)
    #for result in news_results:
    #print(news_results)
    tasks = []
    for keyword in keywords:
        tasks.append(fetch_news_content(keyword))
     
    print(tasks)

    #['전세대출', '가계부채', '주택담보대출', '보증기관', '전세 사기']