# feedback_input/feedback_analysis.py
from feedback_input.gpt_feedback_input import gpt_feedback_input
from feedback_input.manual_feedback_input import manual_feedback_input


def feedback_analysis():
    """
    GPT API를 사용하여 피드백을 얻고, 실패 시 수동 입력으로 전환하여 피드백을 처리
    """
    feedback_text = """
    사용자가 원하시는 안경테 조건을 선택하려고 합니다. 다음 중 무엇을 선택하시겠습니까?
    1. 가격
    2. 색상
    3. 크기
    4. 모양
    5. 브랜드
    6. 재질
    7. 무게
    """

    # GPT API를 사용하여 피드백 유형을 결정
    feedback_type, feedback_value = gpt_feedback_input(feedback_text)

    if feedback_type is None or feedback_value is None:
        print("GPT API 호출에 실패하여, 수동 입력으로 전환합니다.")
        feedback_type, feedback_value = manual_feedback_input()
    else:
        print(f"GPT가 결정한 피드백: {feedback_type} = {feedback_value}")

    return feedback_type, feedback_value


# 테스트 실행
feedback_type, feedback_value = feedback_analysis()
if feedback_type and feedback_value:
    print(f"선택된 피드백: {feedback_type} = {feedback_value}")
