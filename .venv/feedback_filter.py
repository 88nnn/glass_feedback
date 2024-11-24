import chromadb
import colorsys


# RGB를 HSV로 변환하는 함수
def rgb_to_hsv(color):
    color_map = {
        "black": (0, 0, 0),
        "dark_blue": (0, 0, 50),
        "navy": (240, 100, 30),
        "gray": (0, 0, 80),
        "silver": (0, 0, 192),
        "white": (0, 0, 255),
        "pink": (300, 100, 200),
        "transparent": (0, 0, 255),
        "yellow": (60, 255, 190),
    }
    rgb = color_map.get(color.lower(), (0, 0, 128))  # 기본값으로 중간 밝기 설정
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)

# HSV를 기반으로 색상 필터링
def filter_by_hsv(recommendations, reference_hsv, feedback_hsv):
    """
    HSV 거리 기준 필터링
    reference_hsv: 기존 추천 상품의 HSV 값
    feedback_hsv: 사용자가 요구한 색상의 HSV 조정값 (튜플: (h, s, v))
    """
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


def get_brand_price(brand):
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
    return brand_price.get(brand.lower(), 300000)  # 브랜드 가격이 없다면 기본값 50000 반환

# 피드백 조건에 따른 필터 함수 정의
def apply_filter(self, glasses_data, feedback_type, feedback_value, reference_item):
    filtered_feedback = glasses_data

    if feedback_type == "price":
        if feedback_value == "cheaper":
            filtered_feedback = [item for item in filtered_feedback if item.price < reference_item['price']]
        elif feedback_value == "expensive":
            filtered_feedback = [item for item in filtered_feedback if item.price > reference_item['price']]

    elif feedback_type == "brand":
            # 브랜드별 가격을 기준으로 필터링
        brand_avg_price = get_brand_price(reference_item['brand'])
        if feedback_value == "budget":
            filtered_feedback = [item for item in filtered_feedback if get_brand_price(item.brand) < brand_avg_price]
        elif feedback_value == "luxury":
            filtered_feedback = [item for item in filtered_feedback if get_brand_price(item.brand) > brand_avg_price]
    
    # Shape 필터링 (각각의 shape군으로 필터링)
    elif feedback_type == "shape":
        shape_categories = {
            "square": ["square", "poly"],  # 각진 형태
            "big lens": ["cats", "boeing"],   # 알이 큰 형태
            "round": ["boeing", "orval", "cats", "round"], #둥근 형태
            "frameless": ["frameless"],     # 테가 없는 형태
            # 뿔테, 굵은 테, 반무테 등 추가 필요
            # 형태 분류 추가 가능
        }
        valid_shapes = shape_categories.get(feedback_value, [])
        filtered_feedback = [item for item in filtered_feedback if item.shape in valid_shapes]


    elif feedback_type == "material":
        if feedback_value in ["metal", "plastic", "titan"]:
            filtered_feedback = [item for item in filtered_feedback if item.material == feedback_value]
    
    # 색상 필터링 (HSV 값으로 필터링)
    elif feedback_type == "color":
        reference_hsv = rgb_to_hsv(reference_item.color)
        adjusted_hsv = {
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
        }
        hsv_adjustment = adjusted_hsv.get(feedback_value, (0, 0, 0))
        filtered_feedback = filter_by_hsv(filtered_feedback, reference_hsv, hsv_adjustment)

    elif feedback_type == "size":
        if feedback_value == "bigger":
            filtered_feedback = [item for item in filtered_feedback if item.size > reference_item['size']]
        elif feedback_value == "smaller":
            filtered_feedback = [item for item in filtered_feedback if item.size < reference_item['size']]

    elif feedback_type == "weight":
        if feedback_value == "lighter":
            filtered_feedback = [item for item in filtered_feedback if item.weight < reference_item['weight']]
        elif feedback_value == "heavier":
            filtered_feedback = [item for item in filtered_feedback if item.weight > reference_item['weight']]

    return filtered_feedback
