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
        "DAON": 80000, "PROJEKT PRODUKT": 301300, "Ash Compact": 102000,
        #그 밖에 각 브랜드별 가격정보(브랜드별 아이템 가격 총합/브랜드별 아이템수)를 데이터베이스로부터 불러와서 평균가를 정의.
    }
    return brand_price.get(brand.lower(), 50000)  # 브랜드 가격이 없다면 기본값 50000 반환

# 피드백 조건에 따른 필터 함수 정의
def apply_filter(recommendations, feedback_type, feedback_value, reference_item):
    filtered_recommendations = recommendations

    if feedback_type == "price":
        if feedback_value == "cheaper":
            filtered_recommendations = [item for item in filtered_recommendations if item['price'] < reference_item['price']]
        elif feedback_value == "expensive":
            filtered_recommendations = [item for item in filtered_recommendations if item['price'] > reference_item['price']]

    elif feedback_type == "brand":
            # 브랜드별 가격을 기준으로 필터링
        brand_avg_price = get_brand_price(reference_item['brand'])
        if feedback_value == "budget":
            filtered_recommendations = [item for item in filtered_recommendations if get_brand_price(item['brand']) < brand_avg_price]
        elif feedback_value == "luxury":
            filtered_recommendations = [item for item in filtered_recommendations if get_brand_price(item['brand']) > brand_avg_price]
    
    # Shape 필터링 (각각의 shape군으로 필터링)
    elif feedback_type == "shape":
        shape_categories = {
            "square": ["square", "poly"],  # 각진 형태
            "big lens": ["cats", "boeing"],   # 알이 큰 형태
            "round": ["boeing", "orval", "cats", "round"], #둥근 형태
            "frameless": ["frameless"],     # 테가 없는 형태
            # 추가적인 형태 분류
        }
        valid_shapes = shape_categories.get(feedback_value, [])
        filtered_recommendations = [item for item in filtered_recommendations if item['shape'] in valid_shapes]


    elif feedback_type == "material":
        if feedback_value in ["metal", "plastic", "titan"]:
            filtered_recommendations = [item for item in filtered_recommendations if item['material'] == feedback_value]
    
    # 색상 필터링 (HSV 값으로 필터링)
    elif feedback_type == "color":
        reference_hsv = rgb_to_hsv(reference_item['color'])
        adjusted_hsv = {
            "more_red": (10, 0, 0),    # 빨간 색상 증가
            "darker": (0, 0, -20),     # 더 어두운 색상
            "more_transparent": (0, 0, 255),  # 투명도 증가
            # 기타 컬러 변화 추가
            # 원래는 피드백이 특정 색이나 밝음, 어두움, 더 따뜻한 색 등을 요구하면
            # GPT API를 써 해당 요구에 맞춘 필터링("feedback_color":(n, n, n)과 같은 형식)을 반환하도록 구현하려 했으나
            # 추후 키워드 검색 방식으로 바꿨기에, 일단 키워드로 제공할 테이블 작성 중이었음. 보완 필요.
        }
        hsv_adjustment = adjusted_hsv.get(feedback_value, (0, 0, 0))
        filtered_recommendations = filter_by_hsv(filtered_recommendations, reference_hsv, hsv_adjustment)

    elif feedback_type == "width":
        if feedback_value == "narrower":
            filtered_recommendations = [item for item in filtered_recommendations if item['width'] < reference_item['width']]
        elif feedback_value == "wider":
            filtered_recommendations = [item for item in filtered_recommendations if item['width'] > reference_item['width']]

    elif feedback_type == "length":
        if feedback_value == "shorter":
            filtered_recommendations = [item for item in filtered_recommendations if item['length'] < reference_item['length']]
        elif feedback_value == "longer":
            filtered_recommendations = [item for item in filtered_recommendations if item['length'] > reference_item['length']]

    elif feedback_type == "weight":
        if feedback_value == "lighter":
            filtered_recommendations = [item for item in filtered_recommendations if item['weight'] < reference_item['weight']]
        elif feedback_value == "heavier":
            filtered_recommendations = [item for item in filtered_recommendations if item['weight'] > reference_item['weight']]

    return filtered_recommendations
