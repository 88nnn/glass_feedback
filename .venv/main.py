import openai
import requests
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))
from flask import Flask, request, jsonify
import logging

from get_glasses import get_glasses
from process_feedback import process_feedback
from services.process_reference import process_reference
from services.feedback_filter import build_expr
from services.db_search import db_search

# 로그 설정
logging.basicConfig(level=logging.INFO)
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
@app.route('/feedback/save', methods=['POST'])
@app.route('/glasses/find/<user_id>', methods=['POST'])
def main():
    try:
        feedback_list, user_id = process_feedback()  # 1. 피드백 처리
        #피드백 리스트 형식: {'types': ['price', 'color', 'brand_price', 'brand', 'weight', 'shape', 'material', 'size'],
        # 'values': [['expensive'], ['rosegold', 'blue'], ['luxury'], ['daon', 'fake me'], ['lighter'], ['squares'], ['titan'], ['bigger']]}
        if not feedback_list:
            raise ValueError("No feedback_list found.")
        elif not user_id:
            raise ValueError("No user ID found")
        print(feedback_list, user_id)
        glasses_data = get_glasses(user_id)  # 2. 안경 데이터 조회
        #안경 데이터 형식:
        if not glasses_data:
            glasses_data = [
                {"color": "brown", "id": 0, "material": "metal", "model": "BLUE VB 01",
                 "shape": "square", "brand": "daon", "price": "100000", "weight": "47", "size": "99"},
                {"color": "brown", "id": 14, "material": "metal", "model": "UD134",
                 "shape": "square", "brand": "금자안경", "price": "150000", "weight": "55", "size": "88"},
                {"color": "brown", "id": 16, "material": "plastic", "model": "베이커 C4",
                 "shape": "square", "brand": "lash", "price": "500000", "weight": "45", "size": "85"},
                {"color": "yellow", "id": 24, "material": "plastic", "model": "504 Classic JD",
                 "shape": "square", "brand": "daon", "price": "600000", "weight": "88", "size": "101"},
                {"color": "brown", "id": 31, "material": "plastic", "model": "FRANKLIN HYD",
                 "shape": "square", "brand": "금자안경", "price": "200000", "weight": "66", "size": "95"}
            ]
            raise ValueError("No glasses data found.")
        print(glasses_data)
        option_list = process_reference(feedback_list, glasses_data) # 3. 기준 데이터 생성
        if not option_list:
            raise ValueError("No option list found.")
        print(option_list)
        feedback_item = db_search(glasses_data, option_list, feedback_list)  # 4. DB 검색 및 필터링
        return feedback_item
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)