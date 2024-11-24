import requests

def get_glasses(user_id):
    """
    유저의 안경 데이터를 외부 API에서 조회하는 함수.
    Flask 서버에서 호출하여 유저의 안경 정보를 반환합니다.
    """
    # GlassesController의 getGlassesByUserId 엔드포인트 호출
    url = f"http://localhost:8080/glasses/find/{user_id}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            glasses_data = response.json()  # JSON 형태로 반환된 안경 데이터
            if glasses_data:
                return glasses_data["data"]  # 데이터 형식에 맞게 수정
            else:
                return None
        else:
            print(f"Error fetching glasses data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error in get_glasses_by_user_id: {e}")
        return None

def calculate_reference_item(feedback_type, feedback_value, glasses_data):
    """
    피드백 유형(feedback_type)과 값을 기반으로 평균값을 계산하여 reference_item을 정의.
    """
    if feedback_type == "price":
        # 가격에 해당하는 모든 안경의 평균 가격을 계산
        prices = [glasses['price'] for glasses in glasses_data if glasses['price'] is not None]
        if prices:
            reference_item = statistics.mean(prices)
        else:
            reference_item = None
    elif feedback_type == "size":
        # 크기에 해당하는 모든 안경의 크기를 기반으로 평균 크기 계산 (가정: size가 특정 기준으로 저장됨)
        sizes = [glasses['size'] for glasses in glasses_data if glasses['size'] is not None]
        if sizes:
            # 크기 값에 대한 로직 (단순 예시, 실제 크기 분석은 추가로 해야 함)
            reference_item = sizes  # 이 예시에서는 크기를 리스트로 반환
        else:
            reference_item = None
    elif feedback_type == "weight":
        # 무게에 해당하는 모든 안경의 무게 평균을 계산
        weights = [glasses['weight'] for glasses in glasses_data if glasses['weight'] is not None]
        if weights:
            reference_item = statistics.mean(weights)
        else:
            reference_item = None
    else:
        reference_item = None

    return reference_item