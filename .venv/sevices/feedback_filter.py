import chromadb
import colorsys

from markdown_it.rules_block import reference
# feedback_list를 기반으로 expr 조건 생성 후 search 함수에 반환

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
    rgb = color_map.get(color.lower(), (128, 128, 128))  # 기본값으로 중간 밝기 설정
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)
"""
 HSV를 기반으로 색상 필터링
def filter_by_hsv(recommendations, reference_hsv, feedback_hsv):
    
    #HSV 거리 기준 필터링
    #reference_hsv: 기존 추천 상품의 HSV 값
    #feedback_hsv: 사용자가 요구한 색상의 HSV 조정값 (튜플: (h, s, v))
    
    h_tolerance, s_tolerance, v_tolerance = feedback_hsv

    def hsv_distance(hsv1, hsv2):
        # 두 색상 간 HSV 거리 계산
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
"""

def build_hsv_expr(reference_hsv, adjustment):
    """
    HSV 조건을 expr로 변환
    """
    h, s, v = reference_hsv
    dh, ds, dv = adjustment
    new_h = h + dh
    new_s = s + ds
    new_v = v + dv
    return f"(hue == {new_h} and saturation == {new_s} and value == {new_v})"


def get_brand_price(option_item, feedback_value):
    #피드백 값에 따라 브랜드 목록 반환 (budget: 저가 브랜드, luxury: 고가 브랜드)
    brand_price = {
    "Daon": 105000.0,
    "Projekt produkt": 268500.0,
    "Montblanc": 615000.0,
    "Bibiem": 127500.0,
    "Laurence paul": 240000.0,
    "Lash": 232500.0,
    "금자안경": 552000.0,
    "Ash compact": 106500.0,
    "Yuihi toyama": 550000.0,
    "Blue elephant": 138000.0,
    "Eyevan": 520000.0,
    "Mahrcato": 240000.0,
    "Accrue": 240000.0,
    "Tvr": 640000.0,
    "Lunor": 770000.0,
    "Kame mannen": 617000.0,
    "Buddy optical": 540000.0,
    "Gentle monster": 289000.0,
    "Native sons": 561000.0,
    "Heister": 175000.0,
    "Rayban": 230000.0,
    "Versace": 350000.0,
    "Maska": 265000.0,
    "Rawrow": 169000.0,
    "Weareannu": 450000.0,
    "Museum by beacon": 218000.0,
    "Drain your pocket money": 450000.0,
    "Fake me": 190000.0
    }
    # 선택한 브랜드의 기준 가격 가져오기
    option_brand = option_item["brand"]
    option_price = brand_prices.get(option_brand, 300000)  # 기본값 300,000

    # 피드백 값에 따른 브랜드 필터링
    if feedback_value == "budget":
        # 사용자에게 기존에 추천됐던 상품 브랜드 중에서 가장 평균가가 싼 브랜드와 평균가가 비슷하거나 그보다 평균가가 싼 브랜드명만 list에 넣어 반환
        return [brand for brand, price in brand_prices.items() if price <= option_price]
    elif feedback_value == "luxury":
        # 사용자에게 기존에 추천됐던 상품 브랜드 중에서 가장 평균가가 비싼 브랜드와 평균가가 비슷하거나 그보다 평균가가 비싼 브랜드명만 list에 넣어 반환
        return [brand for brand, price in brand_prices.items() if option_price <= price]
    return []

# 피드백 조건에 따른 필터 함수 정의
def build_expr(feedback_list, option_item):
    filtered_feedback = []
    for feedback in feedback_list:
        feedback_type = feedback['feedback_type']
        feedback_value = feedback['feedback_type']

    reference_item = option_item
    comparable_fields = ["price", "size", "weight"]  # 통합 가능한 필드 목록
    if feedback_type in comparable_fields:
        if feedback_value in ["cheaper", "smaller", "lighter"]:
            # 최소값 처리 (price 리스트 고려)
            value = min(option_item[feedback_type]) if isinstance(option_item[feedback_type], list) else option_item[
                feedback_type]
            return f"{feedback_type} < {value}"
        elif feedback_value == "expensive":
            # 최대값 처리 (price 리스트 고려)
            value = max(option_item[feedback_type]) if isinstance(option_item[feedback_type], list) else option_item[
                feedback_type]
            return f"{feedback_type} > {value}"

    elif feedback_type == "brand_price":
        # 조건에 맞는 브랜드 리스트 가져오기
        filtered_brands = get_brand_price(option_item, feedback_value)
        if filtered_brands:
            # 브랜드 조건을 expr로 생성
            brand_expr = " or ".join([f"brand == '{brand}'" for brand in filtered_brands])
            return f"({brand_expr})"

    elif feedback_type == "brand":
        # 사용자가 지목한 브랜드 검색
        return f"brand == '{feedback_value}'"

    # Shape 필터링 (각각의 shape군으로 필터링)
    elif feedback_type == "shape":
        valid_shapes = {
            "squares": ["square", "poly"],  # 각진 형태
            "big lens": ["cats", "boeing"],   # 알이 큰 형태
            "rounds": ["boeing", "orval", "cats", "round"], #둥근 형태
            "frameless": ["frameless"],     # 테가 없는 형태
            "thick frames": ["poly", "cats"] # 굵은 테
            # 굵은 테, 반무테 등 추가 필요
            # 형태 분류 추가 가능
        }
        specific_shape = valid_shapes.get(feedback_value, [feedback_value])
        return f"shape in {specific_shape}"


    elif feedback_type == "material":
        if feedback_value in ["metal", "plastic", "titan"]:
            return f"material == '{feedback_value}'"
    
    # 색상 필터링 (HSV 값으로 필터링)
    elif feedback_type == "color":
        reference_hsv = rgb_to_hsv(option_item['color'])
        feedback_hsv = {
            "more_red": (10, 0, 0),    # 빨간 색상 증가
            "darker": (0, 0, -20),     # 더 어두운 색상
            "more_transparent": (0, 0, 255),  # 투명도 증가
            "black": (0, 0, 0),  # Black has minimal saturation and value.
            "brown": (15, 80, 100),  # Brown has low saturation and medium brightness.
            "transparent": None,  # Transparent doesn't have an HSV value.
            "silver": (0, 0, 192),  # Silver is a light gray with little saturation.
            "gold": (45, 255, 215),  # Gold has a hue around yellow-orange.
            "navy": (210, 255, 50),  # Navy has a low brightness and strong blue hue.
            "purple": (270, 255, 100),  # Purple has a high saturation and value.
            "rosegold": (15, 50, 225),  # Rose gold is a mix of pink and gold.
            "yellow": (60, 255, 255),  # Yellow is bright with full saturation.
            "charcoal": (0, 0, 70)  # Charcoal is a very dark gray.
            # 기타 컬러 변화 추가
        }.get(feedback_value, (0, 0, 0))
        return build_hsv_expr(reference_hsv, feedback_hsv)

    return None

