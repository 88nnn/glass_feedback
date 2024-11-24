from flask import Flask, request, jsonify
from feedback_analysis import FeedbackAnalysis
from chromadb_search import ChromaDBSearch
from flask import Flask, request, jsonify
from feedback_analysis import feedback_analysis
from feedback_filter import apply_filter
from get_reference_item import get_glasses, calculate_reference_item

app = Flask(__name__)

@app.route('/feedback', methods=['POST'])
def process_feedback():
    try:
        #data = request.json
        #feedback_text = data['feedback']
        #reference_item = data['reference_item']
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
"""
@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    recommendations = [
        {"image": "www.image.1", "model": "UNIT1", "price": 50000,
         "brand": "A", "shape": "round", "material": "plastic",
         "color": "black", "width": 47, "length": 45.5, "weight": 7.5},
        {"image": "www.photo.2", "model": "UNIT A", "price": 100000,
         "brand": "B", "shape": "poly", "material": "titan",
         "color": "transperant", "width": 40, "length": 44, "weight": 20},
        {"image": "www.icon.3", "model": "set 3", "price": 30000,
         "brand": "A", "shape": "oval", "material": "metal",
         "color": "silver", "width": 37, "length": 38.5, "weight": 16.7},
        {"image": "www.picture.4", "model": "UNIT4", "price": 220000,
         "brand": "B", "shape": "square", "material": "titan",
         "color": "navy", "width": 55, "length": 51.5, "weight": 22},
        {"image": "www.image.5", "model": "sunG", "price": 14000,
         "brand": "C", "shape": "boeing", "material": "plastic",
         "color": "pink", "width": 67, "length": 65.5, "weight": 19},
        # 추가 아이템들
    ]
    return jsonify(recommendations)
"""
