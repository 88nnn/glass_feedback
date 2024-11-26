import openai
from chromadb_search import ChromaDBSearch

# GPT API 설정
openai.api_key = "your-openai-api-key"

def analyze_feedback_with_gpt(feedback_text):
    """
    GPT API를 통해 피드백 텍스트를 분석하는 함수.
    Args:
        feedback_text (str): 사용자가 입력한 피드백 텍스트.
    Returns:
        dict: 분석된 피드백의 유형 및 값.
    """
    try:
        # GPT API 요청 생성
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing user feedback about glasses."},
                {"role": "user", "content": feedback_text}
            ]
        )
        # GPT의 응답 텍스트 분석
        gpt_output = response['choices'][0]['message']['content']
        feedback_analysis = parse_gpt_output(gpt_output)
        return feedback_analysis
    except Exception as e:
        print(f"Error in analyze_feedback_with_gpt: {e}")
        return None

def parse_gpt_output(output):
    """
    GPT의 응답 텍스트를 구조화된 데이터로 파싱.
    Args:
        output (str): GPT API 응답 텍스트.
    Returns:
        dict: 파싱된 데이터 (피드백 유형과 값).
    """
    # 간단한 파싱 예시 (필요 시 정교화 가능)
    try:
        lines = output.split('\n')
        feedback_type = next(line.split(':')[-1].strip() for line in lines if "Type" in line)
        feedback_value = next(line.split(':')[-1].strip() for line in lines if "Value" in line)
        return {"type": feedback_type, "value": feedback_value}
    except Exception as e:
        print(f"Error in parse_gpt_output: {e}")
        return None

def search_chromadb(feedback_type, feedback_value, glasses_data):
    """
    ChromaDB를 사용하여 검색 수행.
    Args:
        feedback_type (str): 피드백 유형 (예: color, brand, shape 등).
        feedback_value (str): 피드백 값 (예: red, Daon 등).
        glasses_data (list): 검색에 사용할 기본 데이터.
    Returns:
        list: 필터링된 추천 결과.
    """
    try:
        chroma_search = ChromaDBSearch()
        filtered_items = chroma_search.search(feedback_type, feedback_value, glasses_data)
        return filtered_items
    except Exception as e:
        print(f"Error in search_chromadb: {e}")
        return []

# 전체 프로세스 통합
def process_feedback_with_gpt_and_chromadb(feedback_text, glasses_data):
    """
    GPT와 ChromaDB를 활용해 피드백 텍스트 분석 및 추천 수행.
    Args:
        feedback_text (str): 사용자가 입력한 피드백 텍스트.
        glasses_data (list): 검색에 사용할 데이터.
    Returns:
        list: 최종 추천 결과.
    """
    # GPT로 피드백 분석
    feedback_analysis = analyze_feedback_with_gpt(feedback_text)
    if not feedback_analysis:
        return {"error": "Failed to analyze feedback"}

    feedback_type = feedback_analysis.get("type")
    feedback_value = feedback_analysis.get("value")

    # ChromaDB로 검색 수행
    filtered_results = search_chromadb(feedback_type, feedback_value, glasses_data)
    return filtered_results

# 실행 예시
if __name__ == "__main__":
    feedback_text = "I prefer lightweight metal frames in a neutral color."
    sample_glasses_data = [
        {"color": "black", "brand": "Rayban", "material": "metal"},
        {"color": "silver", "brand": "Montblanc", "material": "metal"},
        {"color": "red", "brand": "Daon", "material": "plastic"}
    ]

    results = process_feedback_with_gpt_and_chromadb(feedback_text, sample_glasses_data)
    print("Recommended items:", results)
