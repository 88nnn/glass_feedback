# feedback_input/gpt_feedback_input.py
import openai, os, json
from openai import OpenAI
from sphinx.cmd.quickstart import nonempty
#from config import OPENAI_API_KEY
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


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
        #response = json.loads(response.model_dump_json())
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classifier. Based on the user's feedback, return all applicable types "
                        "from this list: ['price', 'color', 'size', 'shape', 'brand', 'brand_price', 'material', 'weight']. "
                        "Only return results in JSON format like this: {'types': ['price', 'color']}"
                    ),
                },
                {"role": "user", "content": feedback_text},
            ],
        )
        # 응답을 JSON으로 안전하게 파싱
        content = response.choices[0].message.content
        print(f"Raw Response: {content}")  # 디버깅용 출력

        # JSON 응답 파싱
        parsed_response = json.loads(content)
        types = parsed_response['types']
        return types
        """
        #categories = eval(response['choices'][0]['message']['content'])['categories']
        categories = json.loads(response.choices[0].message.content)['categories']
        return categories
        """
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def value_request(feedback_type, feedback_text):
    """
    특정 카테고리 내의 value 값만 반환, color 타입에 대해 HSV 조정 추가
    """
    options = {
        "price": ["cheaper", "expensive"],
        "color": [],  # 색상은 별도로 처리 #"color": ["redder", "darker", "brighter", "more transparent"],
        "size": ["bigger", "smaller"],
        "material": ["metal", "plastic", "titan"],
        "shape": ["square", "round", "frameless", "poly", "boeing", "cats", "orval"],
        "brand": ["Daon","Projekt produkt", "Montblanc", "Bibiem", "Laurence paul",
                  "Lash", "금자안경", "Ash compact", "Yuihi toyama", "Blue elephant", "Eyevan", "Mahrcato",
                  "Accrue", "Tvr", "Lunor", "Kame mannen", "Buddy optical", "Gentle monster", "Native sons",
                  "Heister", "Rayban", "Versace", "Maska", "Rawrow", "Weareannu", "Museum by beacon",
                  "Drain your pocket money", "Fake me"],
        "brand_price": ["budget", "luxury"],
        "weight": ["lighter", "heavier"],
    }

    if feedback_type not in options:
        print(f"Unsupported feedback type: {feedback_type}")
        return None

    try:
        #response = json.loads(response.model_dump_json())
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a classifier for '{feedback_type}'. Based on the user's feedback, "
                        f"return some value from this list: {options[feedback_type]}. " #(as a tuple of (hue, saturation, value))
                        f"If feedback mentions a color adjustment, return HSV adjustment as {{'h': +-0, 's': +-0, 'v': +-0}}. "
                        f"Else, return in JSON format like this: {{'value': 'cheaper'}}"
                    ),
                },
                {"role": "user", "content": feedback_text},
            ],
        )

        # 파싱 후 밸류 값 반환
        content = response.choices[0].message.content
        print(f"Raw Response: {content}")
            #(json.loads(response.choices[0].message.content))
        #value = (eval(response['choices'][0]['message']['content']))['value']
        # 색상 조정 HSV 지원
        if feedback_type == "color" and "h" in response_data:
            return response_data  # HSV 조정값 반환
        parsed_response = json.loads(content)
        value = parsed_response['value']
        return value

    except json.JSONDecodeError:
        print("Failed to parse JSON. Check API response format.")
        return None
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def gpt_feedback_input(feedback_text):
    """
    피드백 분석 후 (type, value) 쌍으로 반환
    """
    results = []
    try:
        # 피드백 분류
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
    print("피드백 유형 (price/color/size/material/shape/brand/weight):")
    feedback_text = "무른 소재, 금자안경, 더 차가운 색" #input("피드백 입력: ")
    print("피드백 입력: " + feedback_text)
    gpt_feedback_input(feedback_text)
