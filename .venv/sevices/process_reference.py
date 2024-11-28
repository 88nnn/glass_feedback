import requests
import statistics
#from markdown_it.rules_block import reference
import colorsys

from debugpy.launcher.debuggee import process

# RGB를 HSV로 변환하는 함수
def rgb_to_hsv(color):
    color_map = {
    "black": (0, 0, 0),
    "dark_blue": (240, 100, 30),
    "navy": (240, 100, 30),
    "gray": (0, 0, 80),
    "silver": (0, 0, 192),
    "white": (0, 0, 255),
    "pink": (300, 100, 200),
    "transparent": (0, 0, 255),  # 투명도는 HSV로 직접 표현 불가
    "yellow": (60, 255, 190),
    "red": (0, 255, 255),
    "green": (120, 255, 255),
    "blue": (240, 255, 255),
    "orange": (30, 255, 255),
    "purple": (270, 255, 255),
    "brown": (15, 80, 100),
    "gold": (45, 255, 215)
    }
    rgb = color_map.get(color.lower(), (128, 128, 128))  # 기본값: 중간 밝기 설정
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)

# HSV 거리 기준 필터링
def filter_by_hsv(glasses_data, reference_hsv, feedback_hsv):
    """
    HSV 거리 기준으로 필터링.
    reference_hsv: 기존 추천 상품의 HSV 값
    feedback_hsv: 사용자가 요구한 색상의 HSV 조정값 (튜플: (h_tolerance, s_tolerance, v_tolerance))
    """
    h_tolerance, s_tolerance, v_tolerance = feedback_hsv

    def build_hsv_expr(reference_hsv, adjustment):
        #HSV 조건을 expr로 변환
        h, s, v = reference_hsv
        dh, ds, dv = adjustment
        new_h = h + dh
        new_s = s + ds
        new_v = v + dv
        return f"(hue == {new_h} and saturation == {new_s} and value == {new_v})"

    """
    filtered = []
    for item in recommendations:
        item_hsv = rgb_to_hsv(item['color'])
        h_dist, s_dist, v_dist = hsv_distance(reference_hsv, item_hsv)

        if h_dist <= h_tolerance and s_dist <= s_tolerance and v_dist <= v_tolerance:
            filtered.append(item)
    """

    return [
        item for item in glasses_data
        if all(d <= t for d, t in zip(hsv_distance(reference_hsv, rgb_to_hsv(item["color"])), (h_tol, s_tol, v_tol)))
    ]


# 브랜드 가격 데이터
def get_brand_price(brand):
    brand_price = {
        "daon": 105000.0,
        "projekt produkt": 268500.0,
        "montblanc": 615000.0,
        "bibiem": 127500.0,
        "laurence paul": 240000.0,
        "lash": 232500.0,
        "금자안경": 552000.0,
        "ash compact": 106500.0,
        "yuihi toyama": 550000.0,
        "blue elephant": 138000.0,
        "eyevan": 520000.0,
        "mahrcato": 240000.0,
        "accrue": 240000.0,
        "tvr": 640000.0,
        "lunor": 770000.0,
        "kame mannen": 617000.0,
        "buddy optical": 540000.0,
        "gentle monster": 289000.0,
        "native sons": 561000.0,
        "heister": 175000.0,
        "rayban": 230000.0,
        "versace": 350000.0,
        "maska": 265000.0,
        "rawrow": 169000.0,
        "weareannu": 450000.0,
        "museum by beacon": 218000.0,
        "drain your pocket money": 450000.0,
        "fake me": 190000.0,
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

def process_reference(feedback_list, glasses_data, feedback_hsv=None):

    #피드백 리스트를 처리하여 각 유형별 옵션과 기준 값을 계산합니다.

    results = []
    for feedback in feedback_list:
        feedback_type = feedback['feedback_type']
        feedback_value = feedback.get('feedback_value', None)
        # 피드백에 맞는 데이터만 추출
        relevant_values = [glasses[feedback_type] for glasses in glasses_data if feedback_type in glasses]
        if not relevant_values:
            results.append({"feedback_type": feedback_type, "expr": None})
            continue

       expr = None

        # 데이터 필터링
        if feedback_type in ["price", "weight", "size"]:
            #가격, 무게, 크기 피드백은 중 두 번째로 큰 것과 두 번째로 작은 값을 기준으로 검색
            sorted_values = sorted(relevant_values)
            option_item = {"second_smallest": sorted_values[1], "second_largest": sorted_values[-2]} \
                if len(sorted_values) >= 2 else relevant_values #추천된 안경이 1개일 땐 해당 안경의 값을 반횐
        elif feedback_type == "color" and feedback_hsv:
            reference_hsv = rgb_to_hsv(relevant_values[0])
            option_item = filter_by_hsv(glasses_data, reference_hsv, feedback_hsv)
        elif feedback_type == "brand":
            option_item = None
        elif feedback_type == "brand_price":
            cheapest_brand, most_expensive_brand = calculate_brand_price(glasses_data)
            option_item = {"cheapest_brand": cheapest_brand, "most_expensive_brand": most_expensive_brand}
        elif feedback_type in ["shape", "material"]:
            option_item = statistics.mode(relevant_values)
        else:
            option_item = None

        results.append({"feedback_type": feedback_type, "option_item": option_item})
    return results


# 테스트 실행
if __name__ == "__main__":
    user_id = 1  # 임의의 유저 ID
    feedback_list = [
        {"feedback_type": "price"},
        {"feedback_type": "color"},
    ]
    glasses_data = get_glasses(user_id)

    if glasses_data:
        results = process_reference(feedback_list, glasses_data, feedback_hsv=(30, 0.2, 0.2))
        print("Feedback Processing Results:")
        for result in results:
            print(result)
    else:
        print("유저의 안경 데이터를 가져올 수 없습니다.")