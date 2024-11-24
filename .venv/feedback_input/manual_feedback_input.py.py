def display_keywords():
    """
    사용자가 선택할 수 있는 키워드 목록을 표시
    """
    print("원하시는 안경테 조건과 관련된 키워드를 선택하세요:")
    print("1. 가격")
    print("2. 색")
    print("3. 크기")
    print("4. 모양")
    print("5. 브랜드")
    print("6. 재질")
    print("7. 무게")

def get_price_choice():
    """
    가격 선택 (텍스트로 입력 받음)
    """
    choice = input("가격 조건을 입력하세요 (더 비싼/더 저렴한): ").strip().lower()
    if choice == "더 비싼":
        return "expensive"
    elif choice == "더 저렴한":
        return "cheaper"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_price_choice()

def get_color_choice():
    """
    색상 선택 (텍스트로 입력 받음)
    """
    choice = input("색 조건을 입력하세요 (더 밝은 색/더 어두운 색): ").strip().lower()
    if choice == "더 밝은 색":
        return "lighter"
    elif choice == "더 어두운 색":
        return "darker"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_color_choice()

def get_size_choice():
    """
    크기 선택 (텍스트로 입력 받음)
    """
    choice = input("크기 조건을 입력하세요 (알이 더 큰/알이 더 작은): ").strip().lower()
    if choice == "알이 더 큰":
        return "bigger"
    elif choice == "알이 더 작은":
        return "smaller"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_size_choice()

def get_shape_choice():
    """
    모양 선택 (텍스트로 입력 받음)
    """
    choice = input("모양 조건을 입력하세요 (각진 테/알이 큰 테/둥근 테/무테): ").strip().lower()
    if choice == "각진 테":
        return "square"
    elif choice == "알이 큰 테":
        return "big lens"
    elif choice == "둥근 테":
        return "round"
    elif choice == "무테":
        return "frameless"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_shape_choice()

def get_brand_choice():
    """
    브랜드 선택 (텍스트로 입력 받음)
    """
    choice = input("브랜드 조건을 입력하세요 (고가 브랜드/중저가 브랜드): ").strip().lower()
    if choice == "고가 브랜드":
        return "budget"
    elif choice == "중저가 브랜드":
        return "luxury"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_brand_choice()

def get_material_choice():
    """
    재질 선택 (텍스트로 입력 받음)
    """
    choice = input("재질 조건을 입력하세요 (금속/플라스틱/티타늄): ").strip().lower()
    if choice == "금속":
        return "metal"
    elif choice == "플라스틱":
        return "plastic"
    elif choice == "티타늄":
        return "titan"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_material_choice()

def get_weight_choice():
    """
    무게 선택 (텍스트로 입력 받음)
    """
    choice = input("무게 조건을 입력하세요 (더 무겁게/더 가볍게): ").strip().lower()
    if choice == "더 무겁게":
        return "heavier"
    elif choice == "더 가볍게":
        return "lighter"
    else:
        print("잘못된 선택입니다. 다시 입력해주세요.")
        return get_weight_choice()

def get_user_choice():
    """
    사용자로부터 선택을 받아옵니다.
    """
    display_keywords()
    try:
        choice = int(input("선택한 키워드를 입력하세요: "))
        if choice == 가격:
            feedback_type = "price"
            feedback_value = get_price_choice()
        elif choice == 색:
            feedback_type = "color"
            feedback_value = get_color_choice()
        elif choice == 크기:
            feedback_type = "size"
            feedback_value = get_size_choice()
        elif choice == 모양:
            feedback_type = "shape"
            feedback_value = get_shape_choice()
        elif choice == 브랜드:
            feedback_type = "brand"
            feedback_value = get_brand_choice()
        elif choice == 재질:
            feedback_type = "material"
            feedback_value = get_material_choice()
        elif choice == 무게:
            feedback_type = "weight"
            feedback_value = get_weight_choice()
        else:
            print("잘못된 선택입니다.")
            return get_user_choice()

        return feedback_type, feedback_value

    except ValueError:
        print("잘못된 입력입니다. 해당하는 키워드를 입력하세요.")
        return get_user_choice()

# 테스트 실행
feedback_type, feedback_value = get_user_choice()
print(f"선택된 키워드: {feedback_type} = {feedback_value}")
