import openai
import requests
from feedback_filter import apply_filter
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from get_reference_item import get_glasses
import logging
# 로그 설정
logging.basicConfig(level=logging.INFO)
from openai.lib.azure import API_KEY_SENTINEL

load_dotenv()
API_KEY = os.getenv('API_KEY_SENTINEL')

@app.route('/feedback', methods=['POST'])
def receive_feedback():
    data = request.get_json()

    user_id = data.get('userId')
    feedback = data.get('feedback')

    if not user_id or not feedback:
        return jsonify({"status": "error", "message": "userId와 feedback가 필요합니다."}), 400

    # Step 1: Get feedback from GPT or manual input
    feedback_type, feedback_value = feedback_analysis()

    # 현재는 로그로 피드백을 남기고 있습니다.
    logging.info(f"Received feedback for user {user_id}: {feedback}")

    # 유저 데이터를 기반으로 안경 정보 가져오기
    glasses_data = get_glasses(user_id)
    if not glasses_data:
        return jsonify({"status": "error", "message": "유저 데이터 또는 안경 정보를 찾을 수 없습니다."}), 404

    # Step 3: Calculate reference item based on feedback
    reference_item = calculate_reference_item(feedback_type, feedback_value, glasses_data)
    if not reference_item:
        return jsonify({"error": "Could not calculate reference item"}), 400


    # Step 4: Filter glasses data based on feedback
    filtered_glasses = apply_filter(glasses_data, feedback_type, feedback_value, reference_item)

    # Step 5: Return filtered recommendations
    return jsonify({"recommended_glasses": filtered_glasses})
    # 여기서 피드백을 처리하는 로직을 추가합니다. 예를 들어, 피드백 저장 등

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


"""
def fetch_glasses_data_from_server(user_id):
    #Spring 서버에서 유저 ID로 안경 데이터를 가져옵니다.
    try:
        # Flask에서 Spring API 호출하여 유저 ID로 안경 데이터 조회
        response = requests.get(f"http://localhost:8080/find/{user_id}")
        response.raise_for_status()
        return response.json()['data']  # Assuming the response contains a 'data' field with glasses info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching glasses data: {e}")
        return None

"""
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