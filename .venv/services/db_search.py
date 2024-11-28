from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
@app.route("/search", methods=["POST"])
def db_search(glasses_data, option_item, feedback_list):
    collection_name = 'eyewear_collection'
    search_param = {"metric_type": "L2", "params": {"nprobe": 10}}
    top_k = 10
    collection = client.get_or_create_collection("eyewear_collection")

    # Milvus에서 검색
    expr_list = []
    expr_list = [build_expr(ft, fv, option_item) for ft, fv in feedback_list if build_expr(ft, fv, option_item)]
    combined_expr = " and ".join(expr_list)
    print(combined_expr)
    for feedback_type, feedback_value in feedback_list:
        expr = build_expr(feedback_type, feedback_value, option_item)
        if expr:
            expr_list.append(expr)

    # 모든 조건을 AND로 연결
    combined_expr = " and ".join(expr_list)

    search_param = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }

    # Milvus 검색 수행
    results = client.search(
        collection_name="glasses_data",
        data=[vector],
        anns_field="embedding",
        param=search_param,
        limit=10,
        expr=combined_expr  # 필터 조건 추가
    )

    return results
    # 필터링된 데이터를 ChromaDB에 삽입 및 검색
    for item in filtered_feedback:
        embedding = model.encode(f"{item['brand']} {item['shape']} {item['color']}").tolist()
        collection.add(documents=[item], embeddings=[embedding])

        # option_item을 기준으로 검색 수행
        query_embedding = model.encode(f"{option_item['brand']} {option_item['shape']} {option_item['color']}").tolist()
        search_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10,
            include=["documents"]
        )

        return search_results['documents']
    return results  # 최종적으로 검색된 안경 모델 리스트 반환

"""
    def __init__(self):
        self.client = chromadb.Client()  # ChromaDB 클라이언트 초기화
        self.collection = self.client.get_or_create_collection("eyewear_collection")

    def search(feedback_type, feedback_value, eyewear_collection):
        filtered_items = []
"""