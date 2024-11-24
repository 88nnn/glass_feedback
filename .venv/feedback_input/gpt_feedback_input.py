# feedback_input/gpt_feedback_input.py
import openai

# OpenAI API 키 설정 (본인의 API 키를 여기에 넣으세요)
openai.api_key = 'YOUR_API_KEY'

def rgb_to_hsv(color):
    """
    RGB 색상을 HSV로 변환하는 함수
    """
    # 색상 변환 예시 (자신의 변환 로직에 맞게 수정)
    r, g, b = color
    # RGB -> HSV 변환 (임시 예시)
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    hue = (max_val - min_val)  # 단순화된 예시
    saturation = 0  # 채도 (임시 값)
    value = max_val  # 명도 (임시 값)
    return (hue, saturation, value)


def feedback_type_request(feedback_text):
    """
    GPT API를 사용하여 피드백을 요청하고 응답을 반환
    피드백이 가격, 색상, 크기, 모양, 브랜드, 재질, 무게 중 어떤 것에 해당하는지 물어봄
    """

    try:
        # GPT API로 피드백 분석 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Please classify the following feedback into one of the following categories: price, color, size, shape, brand, material, weight."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답을 받아서 분석 결과를 반환
        feedback_type = response.choices[0].message['content'].strip().lower()

        # 반환된 피드백 타입을 확인하고 출력
        print(f"피드백의 유형은 '{feedback_type}' 입니다.")
        return feedback_type

    except Exception as e:
        print(f"Error during API request: {e}")
        return None


def price_value_request(feedback_text):
    """
    피드백이 가격에 관한 것일 경우, 사용자가 원하는 가격 조건을 묻고 반환합니다.
    예: 더 비싼, 더 저렴한 등.
    """
    try:
        # GPT API로 가격 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Please classify the following feedback as related to 'price'. Then, ask the user if they want a more expensive or cheaper item."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 가격 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if "expensive" in feedback:
            print("더 비싼 조건을 찾고 있습니다.")
            return "expensive"
        elif "cheaper" in feedback:
            print("더 저렴한 조건을 찾고 있습니다.")
            return "cheap"
        else:
            print("가격 조건을 명확히 알 수 없습니다.")
            return None

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def color_value_request(feedback_text):
    try:
        # GPT API로 색 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "If the feedback mentions a color adjustment, return the corresponding HSV adjustment (as a tuple of (hue, saturation, value))."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 색 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if feedback is not none:
            feedback_value = (
            feedback_data.get("hue", 0),          # 색상 조정
            feedback_data.get("saturation", 0),  # 채도 조정
            feedback_data.get("value", 0)        # 명도 조정
            )
            return [feedback_value]
        else:
            print("정의되지 않은 색상 조건입니다. 피드백 불가")
            return None
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def size_value_request(feedback_text):
    try:
        # GPT API로 크기 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Based on the feedback, answer whether the user wants a biggerr frame or a smaller frame."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 가격 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if "bigger" in feedback:
            print("더 큰 조건을 찾고 있습니다.")
            return "bigger"
        elif "smaller" in feedback:
            print("더 작은 조건을 찾고 있습니다.")
            return "smaller"
        else:
            print("크기 조건을 명확히 알 수 없습니다.")
            return None

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def material_value_request(feedback_text):
    try:
        # GPT API로 재질 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Based on the feedback, answer whether the user wants a metal frame or a plastic frame or a titan frame."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 가격 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if "metal" in feedback:
            print("금속 재질을 찾고 있습니다.")
            return "metal"
        elif "plastic" in feedback:
            print("플라스틱 재질을 찾고 있습니다.")
            return "plastic"
        elif "titan" in feedback:
            print("티타늄 재질을 찾고 있습니다.")
            return "titan"
        else:
            print("재질 조건을 명확히 알 수 없습니다.")
            return None

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def shape_value_request(feedback_text):
    try:
        # GPT API로 모양 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Based on the feedback, answer whether the user wants a squre frame or a round frame or a frameless or a big lens frame."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 가격 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if "square" in feedback:
            print("더 각진 조건을 찾고 있습니다.")
            return "square"
        elif "big lens" in feedback:
            print("더 알이 큰 조건을 찾고 있습니다.")
            return "big lens"
        elif "round" in feedback:
            print("더 둥근 조건을 찾고 있습니다.")
            return "round"
        elif "frameless" in feedback:
            print("무테를 찾고 있습니다.")
            return "frameless"
        else:
            print(" 조건을 명확히 알 수 없습니다.")
            return None

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def brand_value_request(feedback_text):
    try:
        # GPT API로 브랜드 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Based on the feedback, answer whether the user wants a budget brand or a luxury brand."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 가격 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if "budget" in feedback:
            print("더 중저가인 조건을 찾고 있습니다.")
            return "budget"
        elif "luxury" in feedback:
            print("더 고가인 조건을 찾고 있습니다.")
            return "luxury"
        else:
            print(" 조건을 명확히 알 수 없습니다.")
            return None

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def weight_value_request(feedback_text):
    try:
        # GPT API로 무게 관련 조건을 요청
        response = openai.ChatCompletion.create(
            model="gpt-3",  # GPT 모델 선택
            messages=[
                {
                    "role": "system",
                    "content": "Based on the feedback, answer whether the user wants a heavier frame or a lighter frame."
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ]
        )

        # GPT 응답에서 가격 조건에 대한 피드백을 반환
        feedback = response.choices[0].message['content'].strip().lower()

        if "lighter" in feedback:
            print("더 가벼운 조건을 찾고 있습니다.")
            return "lighter"
        elif "heavier" in feedback:
            print("무거운 조건을 찾고 있습니다.")
            return "heavier"
        else:
            print("무게 조건을 명확히 알 수 없습니다.")
            return None

    except Exception as e:
        print(f"Error during API request: {e}")
        return None


def gpt_feedback_input(feedback_text):
    """
    사용자가 입력한 텍스트를 GPT API로 분석하여 피드백 유형(type)과 값(value)을 반환
    """
    #feedback_type = gpt_feedback_request(feedback_text)

    try:
        # GPT API로 피드백 유형을 요청
        feedback_type = feedback_type_request(feedback_text)

        if feedback_type is None:
            print("피드백 유형을 판별할 수 없습니다.")
            return None, None

        print(f"피드백 유형: {feedback_type}")

        # 만약 피드백 유형이 'price'라면 가격 조건을 물어보는 추가 작업 수행
        if feedback_type == "price":
            feedback_value = price_value_request(feedback_text)
            return feedback_type, feedback_value

        # 다른 유형에 대해서는 그에 맞는 값을 물어봄 (예: color, size 등)
        elif feedback_type == "color":
            feedback_value = color_value_request(feedback_text)  # 색상에 대한 조건을 처리하는 함수 (예시)
            return feedback_type, feedback_value

        elif feedback_type == "size":
            feedback_value = size_value_request(feedback_text)  # 크기 관련 조건을 처리하는 함수 (예시)
            return feedback_type, feedback_value

        elif feedback_type == "material":
            feedback_value = material_value_request(feedback_text)  # 재질에 대한 조건을 처리하는 함수 (예시)
            return feedback_type, feedback_value

        elif feedback_type == "shape":
            feedback_value = shape_value_request(feedback_text)  # 모양 관련 조건을 처리하는 함수 (예시)
            return feedback_type, feedback_value

        elif feedback_type == "brand":
            feedback_value = brand_value_request(feedback_text)  # 브랜드에 대한 조건을 처리하는 함수 (예시)
            return feedback_type, feedback_value

        elif feedback_type == "weight":
            feedback_value = weight_value_request(feedback_text)  # 무게 관련 조건을 처리하는 함수 (예시)
            return feedback_type, feedback_value

        # 다른 타입에 대해서 추가적인 요청이 필요한 경우 여기에 추가...
        else:
            print(f"{feedback_type}에 대한 조건을 물어보는 기능이 구현되지 않았습니다.")
            return feedback_type, None

    except Exception as e:
        print(f"Error during feedback analysis: {e}")
        return None, None
