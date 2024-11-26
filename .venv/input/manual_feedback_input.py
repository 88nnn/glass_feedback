import re
from difflib import get_close_matches

def preprocess_text(text):
    """
    텍스트 전처리: 소문자로 변환하고 특수문자 제거.
    """
    text = text.lower()  # 소문자로 변환
    text = re.sub(r'[^\w\s]', '', text)  # 특수문자 제거
    text = text.replace(" ", "")  # 띄어쓰기 제거
    words = text.split()
    text = " ".join([word for word in words])
    return text

def build_trie(keyword_map):
    """
    키워드 맵을 Trie 구조로 변환하여 검색 최적화.
    """
    trie = {}
    for feedback_type, options in keyword_map.items():
        for feedback_value, keywords in options.items():
            for keyword in keywords:
                node = trie
                for char in keyword:
                    node = node.setdefault(char, {})
                node["value"] = (feedback_type, feedback_value)
    return trie

def search_trie(trie, text):
    """
    Trie 구조에서 키워드 검색.
    """
    results = []
    words = text.split()
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                break
            node = node[char]
        if "value" in node:
            results.append(node["value"])
    return results

def fuzzy_match(text, keyword_map):
    """
    텍스트와 키워드 간 유사도 기반 매칭.
    """
    all_keywords = []
    for options in keyword_map.values():
        for keywords in options.values():
            all_keywords.extend(keywords)
    matches = get_close_matches(text, all_keywords, n=1, cutoff=0.7)
    return matches if matches else None


def manual_feedback_input(feedback_text):
    """
    사용자의 피드백 텍스트에서 키워드를 매칭하여 피드백 타입과 값을 반환합니다.
    """
    # 키워드 설정: 피드백 타입과 매칭될 단어들 정의
    keyword_map = {
        "price": {
        "expensive": ["더 비싼", "고가", "비싼", "값비싼", "프리미엄", "럭셔리", "명품"],
        "cheaper": ["더 저렴한", "저가", "싼", "가격 낮은", "저렴한"]
    },
    "color": {
        "lighter": ["더 밝은", "밝은 색", "밝은 색상", "밝은 톤", "명도 높은", "밝은"],
        "darker": ["더 어두운", "어두운 색", "어두운 색상", "어두운 톤", "명도 낮은", "어두운"],
        "red": ["빨간", "레드", "적색", "빨강"],
        "blue": ["파란", "블루", "청색"],
        "green": ["초록", "그린", "녹색"],
        "yellow": ["노란", "옐로우", "황색"],
        "white": ["흰", "화이트", "흰색"],
        "black": ["검은", "블랙", "검정", "검정색"],
        "pink": ["분홍", "핑크", "핑크색"],
        "purple": ["보라", "퍼플", "자주", "보라색"],
        "gray": ["회색", "그레이", "그라위", "회색톤", "그레이색"],
        "brown": ["갈색", "브라운", "갈색톤", "황갈색", "커피색"],
        "transparent": ["투명", "투명도", "투명한"],
        "silver": ["은색", "실버", "실버톤", "은색"],
        "gold": ["금색", "골드", "황금", "금빛"],
        "navy": ["네이비", "남색"],
        "charcoal": ["차콜", "차콜그레이"],
        "warm": ["따뜻한", "온화한", "따사로운", "황금빛", "오렌지", "붉은", "카키", "코랄"],
        "feminine": ["여성스러운", "부드러운 색", "파스텔", "화려한", "꽃무늬", "리본", "장식적인"],
        "cool": ["차가운", "시원한", "블루", "민트", "하늘", "보라", "아이보리"],
        "neutral": ["중립적인", "그레이", "흰색", "검정", "회색", "차콜", "베이지"],
        "vibrant": ["밝은", "강렬한", "선명한", "선명한 빨강", "형광", "네온", "파스텔", "민트"],
        "earthy": ["자연적인", "토양색", "갈색", "녹색", "모래", "흙빛", "올리브", "오렌지"],
        "metallic": ["금속적인", "은색", "금색", "로즈골드", "실버", "골드"],
        "pastel": ["파스텔", "라벤더", "연분홍", "연청", "연노랑", "연두", "피치", "민트"],
        "vintage": ["빈티지", "고풍스러운", "클래식", "브라운", "딥그린"],
            "brighter": ["더 밝은", "밝은", "선명한", "더 화사한", "더 밝게"],
            "more_red": ["더 붉은", "레드", "더 빨간", "강한 빨강"],
            "more_blue": ["더 파란", "블루", "더 푸른", "강한 파랑"],
            "more_green": ["더 초록", "그린", "강한 녹색", "더 푸르른"],
            "more_saturated": ["더 선명한", "더 강렬한", "더 진한 색"],
            "less_saturated": ["더 흐릿한", "더 연한", "더 탁한"],
            "more_transparent": ["더 투명한", "투명", "투명도 증가"],
            "metallic_finish": ["금속질", "금속", "광택", "실버", "골드"],
    },
    "shape": {
        "square": ["각진", "사각형", "네모", "각도있는", "모서리 있는"],
        "poly": ["다각형", "사각형", "오각형", "다면형", "다각형 모양", "사각형 형태"],
        "round": ["둥근", "원형", "라운드", "원"],
        "big lens": ["큰 렌즈", "큰 알", "넓은 렌즈", "큰 사이즈"],
        "frameless": ["무테", "테 없는", "프레임 없음"],
        "cats": ["캣아이", "캣츠", "고양이", "삼각형"],
        "boeing": ["보잉", "보잉 스타일"],
        "orval": ["오르발", "오발"],
    },
    "material": {
        "metal": ["금속", "메탈", "스틸", "알루미늄"],
        "plastic": ["플라스틱", "아세테이트", "아크릴", "폴리카보네이트"],
        "titan": ["티타늄", "타이타늄", "티타늄 합금"],
    },
    "brand": {
        "luxury": ["명품", "고급 브랜드", "럭셔리", "프리미엄", "고급", "고급스러운", "명품 브랜드", "유명 브랜드"],
        "budget": ["저렴한", "중저가", "합리적인 가격", "경제적인", "가성비 좋은", "저가", "가성비"],
    },
    "size": {
        "bigger": ["더 큰", "알이 더 큰", "큰 사이즈", "더 넓은", "더 크게", "사이즈 업"],
        "smaller": ["더 작은", "알이 더 작은", "작은 사이즈", "더 좁은", "더 작게", "사이즈 다운"],
    },
    "weight": {
        "heavier": ["더 무겁게", "무거운", "무게가 더 많이", "중량", "강한", "묵직한"],
        "lighter": ["더 가볍게", "가벼운", "무게가 적은", "경량", "얇은"],
    },
    }
    # 전처리
    feedback_text = preprocess_text(feedback_text)

    # Trie 빌드 및 검색
    trie = build_trie(keyword_map)
    results = search_trie(trie, feedback_text)

    # 유사도 기반 매칭 보완
    matches = fuzzy_match(feedback_text, keyword_map)
    if matches:
        results = []
        for match in matches:
            for feedback_type, options in keyword_map.items():
                for feedback_value, keywords in options.items():
                    if match in keywords:
                        results.append((feedback_type, feedback_value))

    if results:
        return results  # 다중 키워드 반환 가능
    else:
        print("일치하는 키워드를 찾을 수 없습니다. 다시 입력하세요.")
        return None

"""
    if not results:
        match = fuzzy_match(feedback_text, keyword_map)
        if match:
            for feedback_type, options in keyword_map.items():
                for feedback_value, keywords in options.items():
                    if match in keywords:
                        results.append((feedback_type, feedback_value))
    if results:
        #print(f"추출된 키워드 피드백: {feedback_results}")
        return results  # 다중 키워드 반환 가능
"""