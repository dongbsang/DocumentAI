import os
from langchain_community.llms import LlamaCpp
from app.services.rag_service import process_uploaded_file
from app.services.prompt_service import get_prompt_template

model_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "mistral-7b-instruct-v0.1.Q5_K_M.gguf"
)

llm = LlamaCpp(
    model_path=model_path,
    temperature=0.3,
    max_tokens=2048,
    top_p=0.95,
    n_ctx=32768,  # 모델 최대 context 크기
    verbose=True  # 디버깅용 로그 출력
)


def analyze_document(
    file_bytes: bytes,
    file_format: str,
    category: str,
    use_handwriting: bool = False
) -> str:
    """
    문서 분석
    Args:
        file_bytes (bytes): _description_
        file_format (str): _description_
        category (str): _description_
        use_handwriting (bool, optional): _description_. Defaults to False.

    Returns:
        str: _description_
    """

    try:
        result = process_uploaded_file(file_bytes, file_format)
        print(f"전체 텍스트 길이: {len(result['text'])}자")

        # 길이 제한
        # 텍스트가 없을 경우 기본 메시지 설정
        if not result["text"]:
            result["text"] = "[텍스트를 추출하지 못했습니다.]"

        prompt = get_prompt_template(
            context=result["text"],
            category=category,
            use_handwriting=use_handwriting
        )
        print(f"프롬프트 길이: {len(prompt)}")
        print("start---------------------------------------")
        llm_response = llm.invoke(prompt)
        print("end---------------------------------------")
        print(f"응답: {llm_response}")
        print(f"응답 길이: {len(llm_response)}")

        if isinstance(llm_response, dict) and "choices" in llm_response:
            answer = llm_response["choices"][0].get("text", "")
        else:
            # 혹시 문자열로 바로 오면 그대로
            answer = str(llm_response)

        return answer.strip()

    except Exception as e:
        return f"❌ 분석 중 오류 발생: {e}"
