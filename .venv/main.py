import openai
import requests
from feedback_filter import apply_filter
from dotenv import load_dotenv
import os

from openai.lib.azure import API_KEY_SENTINEL

load_dotenv()
API_KEY = os.getenv('API_KEY_SENTINEL')

def fetch_glasses_data_from_server(user_id):
    """
    Spring 서버에서 유저 ID로 안경 데이터를 가져옵니다.
    """
    try:
        # Flask에서 Spring API 호출하여 유저 ID로 안경 데이터 조회
        response = requests.get(f"http://localhost:8080/find/{user_id}")
        response.raise_for_status()
        return response.json()['data']  # Assuming the response contains a 'data' field with glasses info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching glasses data: {e}")
        return None

def analyze_feedback(feedback_type, feedback_value):
    """
    선택된 키워드와 값에 맞는 추천 필터링 조건 추출
    """
    if feedback_type == "price":
        return "price", feedback_value
    if feedback_type == "color":
        return "color", feedback_value
    if feedback_type == "width":
        return "width", feedback_value

    return None, None

def filter_recommendations(feedback_type, feedback_value, glasses_data):
    recommendations = glasses_data

    # 선택된 피드백을 기반으로 필터링 진행
    if feedback_type:
        recommendations = apply_filter(recommendations, feedback_type, feedback_value)

    return recommendations[0] if recommendations else None

def display_keywords():
    """
    사용자가 선택할 수 있는 키워드 목록을 표시
    """
    print("키워드를 선택하세요:")
    print("1. 가격 (비싸다/저렴하다)")
    print("2. 색상 (밝다/어둡다)")
    print("3. 크기 (크다/작다)")
    print("3. 모양 (각진/알이 큰/둥근/무테)") #뿔테, 굵은 테, 반무테 등 추가 필요
    print("4. 브랜드 (비싸다/저렴하다)")
    print("5. 재질 (금속/플라스틱/티타늄)")
    print("6. 무게 (무겁다/가볍다)")


def get_user_choice():
    """
    사용자로부터 선택을 받아옵니다.
    """
    display_keywords()
    try:
        choice = int(input("선택한 키워드 번호를 입력하세요: "))
        if choice == 1:
            feedback_type = "price"
            feedback_value = input("가격 조건을 입력하세요 (1비싸다/2저렴하다): ")
        elif choice == 2:
            feedback_type = "color"
            feedback_value = input("색상 조건을 입력하세요 (1밝다/2어둡다): ")
        elif choice == 3:
            feedback_type = "size"
            feedback_value = input("크기 조건을 입력하세요 (1크다/2작다): ")
        else:
            print("잘못된 선택입니다.")
            return get_user_choice()

        return feedback_type, feedback_value
    except ValueError:
        print("숫자를 입력해 주세요.")
        return get_user_choice()

if __name__ == "__main__":
    # 사용자로부터 키워드와 조건 선택
    feedback_type, feedback_value = get_user_choice()

    user_id = input("사용자 ID를 입력하세요: ")  # 사용자의 ID를 입력받고
    glasses_data = fetch_glasses_data_from_server(user_id)

    if glasses_data is None:
        print("안경 데이터를 가져오는 데 실패했습니다.")
    else:
        # 추천 결과 필터링
        best_recommendation = filter_recommendations(feedback_type, feedback_value, glasses_data)
        print("추천 상품:", best_recommendation if best_recommendation else "추천이 없습니다.")

"""
openai.api_key = API_KEY #오픈에이아이 에이피아이키

def fetch_recommendations_from_server():
    try:
        response = requests.get("http://localhost:5000/api/recommendations")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recommendations: {e}")
        return []

def analyze_feedback(feedback_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3", 
            messages=[
                {"role": "system", "content": "Analyze feedback into feedback_type and feedback_value. And if the feedback mentions a color adjustment, return the corresponding HSV adjustment (as a tuple of (hue, saturation, value))."},
                {"role": "user", "content": feedback_text}
            ]
        )
        result = eval(response.choices[0].message['content'])

        feedback_type = result.get("feedback_type")
        if feedback_type == "color":
        # reference_item의 색상 HSV 값 계산
            reference_hsv = rgb_to_hsv(reference_item['color'])
            feedback_value = (
            feedback_data.get("hue", 0),          # 색상 조정
            feedback_data.get("saturation", 0),  # 채도 조정
            feedback_data.get("value", 0)        # 명도 조정
            )
            return reference_hsv, [feedback_value]
            else: 
                feedback_value = result.get("feedback_value")
                
    except Exception as e:
        print(f"Error analyzing HSV feedback: {e}")
        return None, None

        

def filter_recommendations(feedback_list, reference_item):
    recommendations = fetch_recommendations_from_server()
    for feedback_text in feedback_list:
        feedback_type, feedback_value = analyze_feedback(feedback_text)

        if feedback_data:
            feedback_type = feedback_data.get("feedback_type")
            feedback_value = feedback_data.get("feedback_value")

        if feedback_type == "color":
            reference_hsv, adjusted_hsv = analyze_feedback_with_hsv(feedback_text, reference_item)
            if reference_hsv and adjusted_hsv:
                recommendations = filter_by_hsv(recommendations, reference_hsv, adjusted_hsv)
        else:
            recommendations = apply_filter(recommendations, feedback_type, feedback_value, reference_item)

        # 필터링 후 결과가 하나 남으면 즉시 반환
        if len(recommendations) == 1:
            return recommendations[0]

    # 모든 필터링을 적용해도 여러 항목이 남았다면, 첫 번째 항목 반환
    return recommendations[0] if recommendations else None

if __name__ == "__main__":
    # 첫 번째 피드백과 추가 피드백 입력
    feedback_list = []
    initial_feedback = input("피드백을 입력하세요: ")
    feedback_list.append(initial_feedback)

    #while input("추가 피드백을 입력하시겠습니까? (예/아니오): ").lower() == "예":
     #   additional_feedback = input("추가 피드백을 입력하세요: ")
      #  feedback_list.append(additional_feedback)

    reference_item = {
        "price": 50000, "brand": "A", "shape": "round", "material": "plastic",
        "color": "black", "width": 47, "length": 45.5, "weight": 7.5
    }
    best_recommendation = filter_recommendations(feedback_list, reference_item)

    if best_recommendation:
        print("추천 상품:")
        print(best_recommendation)
    else:
        print("적절한 추천이 없습니다.")
"""