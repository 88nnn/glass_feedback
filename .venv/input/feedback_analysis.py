import sys
import os

# input 폴더 경로를 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'input'))

from gpt_feedback_input import gpt_feedback_input
from manual_feedback_input import manual_feedback_input
from statsmodels.graphics.tukeyplot import results


def feedback_analysis(feedback_text):
    """
    GPT API를 사용하여 피드백을 얻고, 실패 시 수동 입력으로 전환하여 피드백을 처리
    """
    """
    사용자가 원하시는 안경테 조건을 선택하려고 합니다. 다음 중 무엇을 선택하시겠습니까?
    1. 가격
    2. 색상
    3. 크기
    4. 모양
    5. 브랜드
    6. 재질
    7. 무게
    """
    #user_text = feedback_text

    gpt_results = gpt_feedback_input(feedback_text)
    # GPT 결과 출력
    print(f"GPT 결과: {gpt_results}")

    if not gpt_results:
        print("GPT API 호출에 실패하여, 유사도 검증 기반 키워드 입력으로 전환합니다.")
        manual_results = manual_feedback_input(feedback_text)
        print(f"수동 입력 결과: {manual_results}")
        return manual_results
    else:
        print(f"GPT가 결정한 피드백: {gpt_results}")
        return gpt_results

# 테스트 실행
if __name__ == "__main__":
    feedback_text = "명품 다각형 밝은 색 무게감 있는 느낌"  # 피드백 텍스트 예시
    feedback_results = feedback_analysis(feedback_text)
    if feedback_results:
        print(f"선택된 피드백: {feedback_results}")
