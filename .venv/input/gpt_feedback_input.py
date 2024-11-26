# feedback_input/gpt_feedback_input.py
import openai
from openai import OpenAI
from sphinx.cmd.quickstart import nonempty
client = OpenAI()
# OpenAI API 키 설정 (본인의 API 키를 여기에 넣으세요)
#OpenAI.api_key = os.getenv('OPENAI_API_KEY')
OpenAI.api_key = 

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
    7종의 type만 반환: price, color, size, shape, brand, material, weight.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classifier. Based on the user's feedback, return all applicable categories "
                        "from this list: ['price', 'color', 'size', 'shape', 'brand', 'material', 'weight']. "
                        "Only return results in JSON format like this: {'categories': ['price', 'color']}"
                    ),
                },
                {"role": "user", "content": feedback_text},
            ],
        )

        # Parse and return the categories
        categories = eval(response['choices'][0]['message']['content'])['categories']
        return categories

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def value_request(feedback_type, feedback_text):
    """
    특정 카테고리 내의 value 값만 반환
    """
    options = {
        "price": ["cheaper", "expensive"],
        "color": ["more red", "darker", "transparent"],
        "size": ["bigger", "smaller"],
        "material": ["metal", "plastic", "titan"],
        "shape": ["square", "round", "frameless", "big lens"],
        "brand": ["budget", "luxury"],
        "weight": ["lighter", "heavier"],
    }

    if feedback_type not in options:
        print(f"Unsupported feedback type: {feedback_type}")
        return None

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a classifier for '{feedback_type}'. Based on the user's feedback, "
                        f"return a single value from this list: {options[feedback_type]}. "
                        f"Only return results in JSON format like this: {{'value': 'cheaper'}}"
                    ),
                },
                {"role": "user", "content": feedback_text},
            ],
        )

        # Parse and return the value
        value = eval(response['choices'][0]['message']['content'])['value']
        return value

    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def gpt_feedback_input(feedback_text):
    """
    Analyze feedback and return a list of (type, value) pairs.
    """
    results = []
    try:
        # Classify feedback into applicable categories
        feedback_types = feedback_type_request(feedback_text)

        if not feedback_types:
            print("Could not determine feedback categories.")
            return None

        print(f"Identified feedback categories: {feedback_types}")

        for feedback_type in feedback_types:
            feedback_value = value_request(feedback_type, feedback_text)
            if feedback_value:
                results.append((feedback_type, feedback_value))

        if not results:
            print("No valid feedback values found.")
            return None

    except Exception as e:
        print(f"Error during feedback analysis: {e}")
        return None

    return results

if __name__ == "__main__":
    feedback_text = input("피드백 입력: ")
    print("피드백 유형 (price/color/size/material/shape/brand/weight):")
    gpt_feedback_input(feedback_text)
