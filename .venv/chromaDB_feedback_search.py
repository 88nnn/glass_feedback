import chromadb


def search_glasses_by_feedback(feedback_type, feedback_value, eyewear_collection):

    def __init__(self):
        self.client = chromadb.Client()  # ChromaDB 클라이언트 초기화
        self.collection = self.client.get_or_create_collection("eyewear_collection")

    def search(feedback_type, feedback_value, eyewear_collection):
        filtered_items = []

        # 매핑 테이블을 참고하여 사용자 피드백에 맞는 필터 항목 찾기
        for entry in mapping_table:
            # 예시로 사용자가 원하는 조건에 맞는 추천 항목 찾기 (피드백에서 직접 받음)
            if 'color' in feedback_type:
                feedback_colors = entry.get('feedback_colors', [])
                if feedback_type['color'] not in feedback_colors:
                    continue
            if 'price' in feedback_type:
                feedback_prices = entry.get('feedback_prices', [])
                if feedback_type['price'] not in feedback_prices:
                    continue
            if 'brand' in feedback_type:
                feedback_brands = entry.get('feedback_brands', [])
                if feedback_type['brand'] not in feedback_brands:
                    continue
            if 'shape' in feedback_type:
                feedback_shapes = entry.get('feedback_shapes', [])
                if feedback_type['shape'] not in feedback_shapes:
                    continue
            if 'material' in feedback_type:
                feedback_materials = entry.get('feedback_materials', [])
                if feedback_type['material'] not in feedback_materials:
                    continue
            if 'size' in feedback_type:
                feedback_sizes = entry.get('feedback_sizes', [])
                if feedback_type['size'] not in feedback_sizes:
                    continue
            if 'weight' in feedback_type:
                feedback_weights = entry.get('feedback_weights', [])
                if feedback_type['weight'] not in feedback_weights:
                    continue

            # 사용자가 원하는 피드백에 맞는 항목만 필터링해서 추천 리스트에 추가
            filtered_recommendations.append(entry)

        # 매핑 테이블에서 필터된 추천 항목을 기준으로 임베딩 생성
        embeddings = []

        for recommendation in filtered_recommendations:
            # 각 항목에 대해 임베딩 생성
            for key in ['feedback_colors', 'feedback_shapes', 'feedback_prices', 'feedback_brands', 'feedback_materials', 'feedback_sizes', 'feedback_weights']:
                recommendation_info = f"{key}: {', '.join(map(str, recommendation.get(key, [])))}"
                embedding = model.encode(recommendation_info).tolist()
                embeddings.append(embedding)

        # ChromaDB에서 검색 (각 항목을 위한 임베딩으로 쿼리)
        results = []
        for embedding in embeddings:
            result = eyewear_collection.query(
                query_embeddings=[embedding],
                n_results=5,
                include=["documents", "distances"]
            )
            results.extend(result['documents'])  # 검색된 안경 모델 리스트를 결과에 추가

        return results  # 최종적으로 검색된 안경 모델 리스트 반환

