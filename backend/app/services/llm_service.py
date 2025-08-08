from langchain_ollama import OllamaLLM
from app.services.rag_service import process_uploaded_file
from app.services.prompt_service import get_prompt_template

# ✅ Ollama는 model_path 필요 없음
llm = OllamaLLM(
    model="mistral",   # 설치된 Ollama 모델 이름
    temperature=0.3,
    top_p=0.95
)


def analyze_document(
    file_bytes: bytes,
    file_format: str,
    category: str,
    use_handwriting: bool = False
) -> str:
    """
    문서 분석
    """
    try:
        result = process_uploaded_file(file_bytes, file_format)
        print(f"전체 텍스트 길이: {len(result['text'])}자")

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
            answer = str(llm_response)

        return answer.strip()

    except Exception as e:
        return f"❌ 분석 중 오류 발생: {e}"
