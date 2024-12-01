from model.agent import Agent


agent = Agent()

graph = agent.graph # model


temp = """K팝 그룹 ‘빅뱅’이 지드래곤의 신곡을 통해 2년7개월 만에 다시 뭉쳤다.

지드래곤의 소속사 갤럭시코퍼레이션에 따르면 지드래곤은 22일 오후 2시 빅뱅 멤버 태양과 대성이 피처링한 신곡 ‘홈 스위트 홈’(HOME SWEET HOME)을 발표했다.

빅뱅의 멤버인 지드래곤·태양·대성이 함께 신곡을 내는 것은 2022년 4월 빅뱅 신곡 ‘봄여름가을겨울’ 이후 처음이다. 세 멤버는 앞서 지난 9월 서울 올림픽공원 올림픽홀에서 열린 태양의 솔로 콘서트 무대에 함께 올라 빅뱅의 히트곡 ‘위 라이크 2 파티’(WE LIKE 2 PARTY)를 불렀다.

‘홈 스위트 홈’은 과거의 향수가 느껴지는 힙합 리듬 위에 지드래곤의 자유로운 랩이 펼쳐지는 곡이다. 갤럭시코퍼레이션은 “팬들과 대중의 곁을 한순간도 떠난 적이 없다는 메시지를 담았다”며 “무대 위에서 자유롭게 뛰놀며 즐기는 듯한 가사와 리듬을 통해 듣는 이들에게 즐거움을 선사한다”고 소개했다."""

url = "https://www.youtube.com/watch?v=-eLJd-OA9zY"

#print(graph.invoke({"youtube_content" : temp}))

print(graph.invoke({"youtube_link" : url}))

