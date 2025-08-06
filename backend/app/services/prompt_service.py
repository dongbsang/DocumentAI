
MAX_CONTEXT_LEN = 1500  # LLM 토큰 초과 방지용


def get_prompt_template(
    context: str, category: str, use_handwriting: bool = False
) -> str:
    """
    문서 내용과 카테고리에 따라 적절한 프롬프트 문자열을 생성합니다.

    Args:
        context (str): OCR 또는 PDF에서 추출한 텍스트
        category (str): '영수증', '자기소개서' 등 문서 유형
        use_handwriting (bool): 손글씨 여부에 따른 안내 추가

    Returns:
        str: 완성된 프롬프트 문자열
    """

    # 문맥 길이 제한
    context = context.strip()[:MAX_CONTEXT_LEN]

    # 손글씨 힌트 텍스트
    handwriting_notice = "[이 문서는 손글씨일 수 있음]\n" if use_handwriting else ""

    if category == "영수증":
        template = f"""
        {handwriting_notice}
        너는 OCR로 추출된 영수증 문서를 분석하는 전문가야.

        아래는 문서 내용이야:
        ---
        {context}
        ---
        문서로부터 다음 항목을 추출해줘:
        1. 상호명
        2. 날짜
        3. 총 금액
        4. 부가세 포함 여부
        5. 주요 품목 (이름, 수량, 단가, 총액)

        JSON 형식으로 작성해줘.
        """
    elif category == "자기소개서":
        template = f"""
        {handwriting_notice}
        아래는 OCR로 추출된 자기소개서 내용이야:
        ---
        {context}
        ---
        자기소개서를 요약하고 다음 항목을 뽑아줘:
        1. 이름
        2. 학위, 전공
        3. 경력 요약

        핵심 내용만 간결하게 bullet point 형식으로 정리해줘.
        """
    else:
        template = f"""
        {handwriting_notice}
        아래는 OCR 또는 PDF에서 추출한 문서 내용입니다:
        ---
        {context}
        ---

        문서의 주요 요점을 간단히 요약하고,
        필요한 경우 구조화된 항목으로 정리해줘.
        """

    return template.strip()
