import requests
import statistics
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from get_glasses import get_glasses

def filter_colors(feedback_value, relevant_values):
    # 색상 필터링: 문자열 색상 값을 그대로 반환.
    # 문자열로만 처리
    if feedback_value in relevant_values:
        return [feedback_value]
    else:
        raise ValueError(f"Color '{feedback_value}' not found in relevant colors.")


# 브랜드 가격 데이터: 평균가
def get_brand_price(brand):
    brand_price = {
        "daon": 105000,
        "projekt produkt": 268500,
        "montblanc": 615000,
        "bibiem": 127500,
        "laurence paul": 240000,
        "lash": 232500,
        "금자안경": 552000,
        "ash compact": 106500,
        "yuihi toyama": 550000,
        "blue elephant": 138000,
        "eyevan": 520000,
        "mahrcato": 240000,
        "accrue": 240000,
        "tvr": 640000,
        "lunor": 770000,
        "kame mannen": 617000,
        "buddy optical": 540000,
        "gentle monster": 289000,
        "native sons": 561000,
        "heister": 175000,
        "rayban": 230000,
        "versace": 350000,
        "maska": 265000,
        "rawrow": 169000,
        "weareannu": 450000,
        "museum by beacon": 218000,
        "drain your pocket money": 450000,
        "fake me": 190000,
    }
    return brand_price.get(brand.lower(), 300000)  # 브랜드가 없으면 기본값

# 기존 아이템 브랜드 최고/저점 가격 계산
def calculate_brand_price(recommendations):
    prices = [(item['brand'], get_brand_price(item['brand'])) for item in recommendations if item.get('brand')]
    if prices:
        # 가격 순으로 정렬
        sorted_prices = sorted(prices, key=lambda x: x[1])
        cheapest_brand = sorted_prices[0]  # 가장 싼 브랜드
        most_expensive_brand = sorted_prices[-1]  # 가장 비싼 브랜드
        return cheapest_brand, most_expensive_brand
    else:
        return None, None

def process_reference(feedback_list, glasses_data):
    # feedback_list를 types와 values로 분리 후 처리하여 각 유형별 옵션과 기준 값을 계산합니다.
    results = []
    option_item = None
    for feedback_type, feedback_value in zip(feedback_list['types'], feedback_list['values']):
        print(f"피드백 종류: {feedback_type}, 값: {feedback_value}")
        # glasses_data 내에서 피드백에 해당되는 요소만 추출
        relevant_values = [glasses.get(feedback_type) for glasses in glasses_data if feedback_type in glasses]
        # 브랜드가치는 브랜드명을 기반으로 산출하므로 브랜드명 사용
        if feedback_type == 'brand_price':
            relevant_values = [glasses["brand"] for glasses in glasses_data if "brand" in glasses]
        if not relevant_values:
            # 기존 추천 데이터가 없다면 없음(처리 불가) 메시지 출력
            results.append({"feedback_type": feedback_type, "option_item": None})
            continue
        # 재질 관련 피드백이면 사용자의 기존 추천 안경들의 material 요소 내 문자열들만 relevant_values로 받아옴.
        # relevant_values를 출력하여 검증
        print(f"피드백 종류: {feedback_type}, 거부된 전체 안경 조건relevant_values: {relevant_values}")

        # 데이터 필터링
        if feedback_type in ["price", "weight", "size"]:
            #가격, 무게, 크기 피드백은 중 두 번째로 큰 것과 두 번째로 작은 값을 기준으로 검색
            sorted_values = sorted(relevant_values)
            option_item = {"second_smallest": sorted_values[1], "second_largest": sorted_values[-2]} \
                if len(sorted_values) >= 2 else relevant_values #추천된 안경이 1개일 땐 해당 안경의 값을 반횐
            print(f"Filtered items: {option_item}")
        elif feedback_type in ["brand", "color"]:
            option_item = None  # 사용자가 지목한 브랜드나 색상만을 피드백 값으로 사용하므로, 기존 아이템을 사용할 여지 없음
        elif feedback_type == "brand_price":
            cheapest_brand, most_expensive_brand = calculate_brand_price(glasses_data)
            option_item = {"cheapest_brand": cheapest_brand, "most_expensive_brand": most_expensive_brand}
            # 평균가가 가장 싼/비싼 브랜드명를 반환
            print(f"Filtered items: {option_item}")
        elif feedback_type in ["shape", "material"]:
            option_item = statistics.mode(relevant_values)
            # 가장 많이 나온 소재를 반환
            print(f"Filtered items: {option_item}")
        else:
            option_item = None
        results.append({"feedback_type": feedback_type, "option_item": option_item})
    return results


# 테스트 실행
if __name__ == "__main__":
    user_id = 1  # 임의의 유저 ID
    print("유저 아이디: ")
    print(user_id)
    feedback_list = {
        'types': ['price', 'color', 'brand_price', 'brand', 'weight', 'shape', 'material', 'size'],
        'values': [['expensive'], ['rosegold', 'blue'], ['luxury'], ['daon', 'fake me'], ['lighter'], ['squares'],
                   ['titan'], ['bigger']]
    }

    print("\n피드백 종류/값: ")
    print(feedback_list)
    #glasses_data = []
    glasses_data =  [
                {"color": "brown", "id": 0, "material": "metal", "model": "BLUE VB 01",
                 "shape": "square", "brand": "daon", "price": "100000", "weight": "47", "size": "99"},
                {"color": "brown", "id": 14, "material": "metal", "model": "UD134",
                 "shape": "square", "brand": "금자안경", "price": "150000", "weight": "55", "size": "88"},
                {"color": "brown", "id": 16, "material": "plastic", "model": "베이커 C4",
                 "shape": "square", "brand": "lash", "price": "500000", "weight": "45", "size": "85"},
                {"color": "yellow", "id": 24, "material": "plastic", "model": "504 Classic JD",
                 "shape": "square", "brand": "daon", "price": "600000", "weight": "88", "size": "101"},
                {"color": "brown", "id": 31, "material": "plastic", "model": "FRANKLIN HYD",
                 "shape": "square", "brand": "금자안경", "price": "200000", "weight": "66", "size": "95"}
        ]
    print(glasses_data)
    results = process_reference(feedback_list, glasses_data)
    print("Feedback Processing Results:")
    for result in results:
        print(result)

    # 데이터가 없다면 처리 불가 메시지 출력
    if glasses_data:
        print(glasses_data)
        results = process_reference(feedback_list, glasses_data)
        print("\n\n\n피드백 처리 결과:")
        for result in results:
            print(result)
    else:
        print("유저의 안경 데이터를 가져올 수 없습니다.")
