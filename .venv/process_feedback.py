from flask import Flask, request, jsonify
import requests
import sys
import os
from grpc import services
sys.path.append(os.path.join(os.path.dirname(__file__), 'input'))
from input.feedback_analysis import feedback_analysis
from feedback_filter import apply_filter
#from services.process_reference import calculate_option_and_reference

app = Flask(__name__)

# 피드백 처리 함수
@app.route('/feedback/save', methods=['POST'])
def process_feedback():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        feedback_text = data.get('feedback')
        user_id = data.get('user_id')

        if not feedback_text or not user_id:
            return jsonify({"error": "Missing feedback or user_id"}), 400

        # 피드백 분석
        feedback_results = feedback_analysis(feedback_text)

        # 결과가 없으면 오류 처리
        if not feedback_results:
            return jsonify({"error": "Failed to analyze feedback"}), 500

        # 피드백 결과를 여러 줄로 반환 (리스트 형식)
        feedback_list = []
        for feedback in feedback_results:
            feedback_type, feedback_value = feedback  # 각 결과에서 타입과 값을 분리
            feedback_list.append({"feedback_type": feedback_type, "feedback_value": feedback_value})
        print("완료")
        jsonify(feedback_list), 200
        # 여러 개의 피드백 결과를 반환
        return feedback_list, user_id
    except Exception as e:
        print(f"Error in process_feedback: {e}")
        return jsonify({'error': str(e)}), 500

"""
# 유저의 안경 데이터를 조회하는 라우트
@app.route('/glasses/find/<user_id>', methods=['POST'])
def get_glasses(user_id):
    # Flask에서 받은 user_id로 외부 API에서 안경 데이터를 조회
    url = f"http://localhost:8080/glasses/find/{user_id}"

    try:
        response = requests.get(url)

        # API 응답 상태 코드 확인
        print(f"API Response Code: {response.status_code}")
        if response.status_code == 200:
            glasses_data = response.json()  # JSON 형태로 반환된 안경 데이터
            if glasses_data:
                print(f"User ID: {user_id}")
                print(f"Glasses Data: {glasses_data['data']}")  # 터미널에 안경 데이터를 출력
                return jsonify(glasses_data["data"])  # 클라이언트에 안경 데이터 전송
            else:
                print(f"No glasses data found for user_id: {user_id}")
                return jsonify({"error": "No glasses data found"}), 404
        else:
            print(f"Error fetching glasses data: {response.status_code}")
            return jsonify({"error": f"Error fetching glasses data: {response.status_code}"}), 500
    except Exception as e:
        print(f"Error in get_glasses_by_user_id: {e}")
        return jsonify({'error': str(e)}), 500

    # 4. DB에서 데이터 검색 및 필터링
    @app.route('/glasses/find/<user_id>', methods=['POST'])
    def recommend_glasses():
        data = request.json
        user_id = data.get("user_id")

        # 사용자의 안경 데이터 가져오기
        glasses_response = get_glasses(user_id)
        if glasses_response[1] != 200:
            return glasses_response

        glasses_data = glasses_response[0].json

        # 비교 기준 생성
        option_item = process_reference(glasses_data)

        # ChromaDB 검색 및 필터링
        remaining_glasses = db_search(option_item, glasses_data)

        return jsonify(remaining_glasses), 200

    # DB 검색 및 필터링 함수
    def db_search(option_item, exclude_glasses):
        # 데이터베이스에서 모든 안경 데이터 조회
        all_glasses = get_all_glasses_from_db()

        # 제외해야 할 안경 ID 목록 생성
        exclude_ids = {glasses["id"] for glasses in exclude_glasses}

        # 옵션에 기반한 필터링
        filtered_glasses = []
        for glasses in all_glasses:
            if glasses["id"] in exclude_ids:
                continue

            # 필터 조건 확인
            for option in option_item:
                if glasses["shape"] != option["shape"]:
                    continue
                if glasses["color"] not in option["color"]:
                    continue
                if not (option["price_range"][0] <= glasses["price"] <= option["price_range"][1]):
                    continue

            filtered_glasses.append(glasses)

        return filtered_glasses

    def get_all_glasses_from_db():
        # ChromaDB 또는 데이터베이스에서 모든 데이터를 가져오는 함수
        return [
            {"id": 1, "shape": "round", "color": "black", "price": 150, "material": "plastic"},
            {"id": 2, "shape": "square", "color": "blue", "price": 200, "material": "metal"},
            # 추가 데이터...
        ]
"""
if __name__ == "__main__":
    app.run(debug=True, port=5000)
