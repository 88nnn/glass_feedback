from flask import Flask, jsonify

app = Flask(__name__)

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

if __name__ == "app":
    app.run(port=5000)
