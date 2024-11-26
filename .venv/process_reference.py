import requests
import statistics
#from markdown_it.rules_block import reference
import colorsys

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
    "gold": (45, 255, 215),
    "charcoal": (0, 0, 70),
    "light_gray": (0, 0, 190),
    "beige": (40, 50, 200),
    "teal": (160, 255, 128),
    "peach": (30, 150, 250),
    "mint": (150, 255, 200),
    }
    rgb = color_map.get(color.lower(), (128, 128, 128))  # 기본값: 중간 밝기 설정
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)

# HSV 거리 기준 필터링
def filter_by_hsv(recommendations, reference_hsv, feedback_hsv):
    """
    HSV 거리 기준으로 필터링.
    reference_hsv: 기존 추천 상품의 HSV 값
    feedback_hsv: 사용자가 요구한 색상의 HSV 조정값 (튜플: (h_tolerance, s_tolerance, v_tolerance))
    """
    h_tolerance, s_tolerance, v_tolerance = feedback_hsv

    def hsv_distance(hsv1, hsv2):
        h1, s1, v1 = hsv1
        h2, s2, v2 = hsv2
        h_dist = min(abs(h1 - h2), 360 - abs(h1 - h2))  # Hue는 360도 원형
        s_dist = abs(s1 - s2)
        v_dist = abs(v1 - v2)
        return h_dist, s_dist, v_dist

    filtered = []
    for item in recommendations:
        item_hsv = rgb_to_hsv(item['color'])
        h_dist, s_dist, v_dist = hsv_distance(reference_hsv, item_hsv)

        if h_dist <= h_tolerance and s_dist <= s_tolerance and v_dist <= v_tolerance:
            filtered.append(item)

    return filtered

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

# 브랜드 평균 가격 계산
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

def calculate_option_and_reference(feedback_list, glasses_data, feedback_hsv=None):

    #피드백 리스트를 처리하여 각 유형별 옵션과 기준 값을 계산합니다.

    results = []
    for feedback in feedback_list:
        feedback_type = feedback['feedback_type']
        relevant_values = []  # 피드백에 맞는 데이터만 추출
        option_item = None

        # 데이터 필터링
        for glasses in glasses_data:
            if feedback_type == "price" and glasses.get("price") is not None:
                relevant_values.append(glasses["price"])
            elif feedback_type == "color" and glasses.get("color") is not None:
                relevant_values.append(glasses["color"])
            elif feedback_type == "brand" and glasses.get("brand") is not None:
                relevant_values.append(glasses["brand"])
            elif feedback_type == "shape" and glasses.get("shape") is not None:
                relevant_values.append(glasses["shape"])
            elif feedback_type == "material" and glasses.get("material") is not None:
                relevant_values.append(glasses["material"])
            elif feedback_type == "weight" and glasses.get("weight") is not None:
                relevant_values.append(glasses["weight"])
            elif feedback_type == "size" and glasses.get("width") is not None and glasses.get("length") is not None:
                # 가로, 세로 크기의 평균값을 사용
                relevant_values.append((glasses["width"] + glasses["length"]) / 2)



    # 평균값 계산
    if feedback_type in ["price", "weight", "size"] and relevant_values:
        sorted_values = sorted(relevant_values)
        if len(sorted_values) >= 2:
            option_item = {"second_smallest": sorted_values[1], "second_largest": sorted_values[-2]}
    elif feedback_type in ["shape", "material"] and relevant_values:
        option_item = statistics.mode(relevant_values)  # 문자열 데이터에서 가장 빈도가 높은 값
    elif feedback_type == "color" and feedback_hsv:
        reference_hsv = rgb_to_hsv(relevant_values[0]) if relevant_values else None
        option_item = filter_by_hsv(glasses_data, reference_hsv, feedback_hsv) if reference_hsv else None
    elif feedback_type == "brand":
        cheapest_brand, most_expensive_brand = calculate_brand_price_range(relevant_values)
        option_item = {
            "cheapest_brand": cheapest_brand,
            "most_expensive_brand": most_expensive_brand
        }
    else:
        option_item = None

    results.append({"feedback_type": feedback_type, "option_item": option_item})
    return results

    #return option_item, reference_item


# 테스트 실행
if __name__ == "__main__":
    user_id = 1  # 임의의 유저 ID
    feedback_list = [
        {"feedback_type": "price"},
        {"feedback_type": "color"},
    ]
    glasses_data = get_glasses(user_id)

    if glasses_data:
        results = calculate_option_and_reference(feedback_list, glasses_data, feedback_hsv=(30, 0.2, 0.2))
        print("Feedback Processing Results:")
        for result in results:
            print(result)
    else:
        print("유저의 안경 데이터를 가져올 수 없습니다.")