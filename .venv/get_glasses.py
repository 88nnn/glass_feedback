from flask import Flask, request, jsonify
#import chromadb_search
import requests
from process_feedback import process_feedback
#from feedback_filter import apply_filter
#glasses_routes = Blueprint('glasses_routes', __name__)
#sys.path.append(os.path.join(os.path.dirname(__file__), 'input'))

def get_demo_data():
    # 데모 데이터를 반환하는 함수
    return [
        {
            "color": "brown",
            "id": 0,
            "material": "metal",
            "model": "BLUE VB 01",
            "shape": "square"
        },
        {
            "color": "brown",
            "id": 14,
            "material": "metal",
            "model": "UD134",
            "shape": "square"
        },
        {
            "color": "brown",
            "id": 16,
            "material": "plastic",
            "model": "베이커 C4",
            "shape": "square"
        },
        {
            "color": "yellow",
            "id": 24,
            "material": "plastic",
            "model": "504 Classic JD",
            "shape": "square"
        },
        {
            "color": "brown",
            "id": 31,
            "material": "plastic",
            "model": "FRANKLIN HYD",
            "shape": "square"
        }
    ]


app = Flask(__name__)

#user_id, feedback_list = process_feedback()

#유저의 안경 데이터를 외부 API에서 조회하는 함수.
#Flask 서버에서 호출하여 유저의 안경 정보를 반환합니다.
@app.route('/glasses/find/<int:user_id>', methods=['GET'])

def get_glasses(user_id):
    # GlassesController의 getGlassesByUserId 엔드포인트 호출
    url = f"http://localhost:8080/glasses/find/{user_id}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            glasses_data = response.json()  # JSON 형태로 반환된 안경 데이터
            if glasses_data:
                print(glasses_data["data"])  # 받은 데이터 출력 (디버깅용)
                return jsonify(glasses_data["data"])  # JSON 형식으로 반환
                # return glasses_data["data"]  # JSON 형식으로 반환
            else:
                # 데이터가 없을 경우 데모 데이터를 반환
                return jsonify(get_demo_data())
                # return glasses_data["data"]
        else:
            print(f"Error fetching glasses data: {response.status_code}")
            return jsonify(get_demo_data())  # API 호출 실패 시 데모 데이터를 반환
    except Exception as e:
        print(f"Error in get_glasses_by_user_id: {e}")
        return jsonify(get_demo_data())  # 예외 발생 시 데모 데이터를 반환

if __name__ == "__main__":
    app.run(debug=True, port=5000)



"""



def __init__(self):
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection("eyewear_collection")

        def calculate_average(self, glasses_data, attribute):
            values = [getattr(glass, attribute, None) for glass in glasses_data if getattr(glass, attribute, None)]
            return sum(values) / len(values) if values else None

        # 피드백 분석
        feedback_analysis = feedback_input()
        feedback_type, feedback_value = feedback_analysis.analyze(feedback_text)

        # ChromaDB 검색
        chroma_search = ChromaDBSearch()
        filtered_items = chroma_search.search(feedback_type, feedback_value, reference_item)

        # 결과 반환
        return jsonify(filtered_items), 200
"""