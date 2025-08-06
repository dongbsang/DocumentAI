import yaml
import os

MAX_CONTEXT_LEN = 1500  # LLM 토큰 초과 방지용

def load_resume_prompt(category: str, context: str) -> str:
    """
    카테고리에 맞는 YAML 프롬프트를 로드하고 context를 삽입합니다.
    """
    if category.strip() == "이력서":
        yaml_path = os.path.join("app", "prompt", "resume_info.yaml")
    else:
        raise ValueError(f"지원되지 않는 카테고리: {category}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        prompt_yaml = yaml.safe_load(f)

    template = prompt_yaml.get("template", "")
    prompt = template.replace("{{context}}", context.strip())
    
    return prompt

def get_prompt_template(
    context: str, category: str, use_handwriting: bool = False
) -> str:
    """
    문서 내용과 카테고리에 따라 적절한 프롬프트 문자열을 생성합니다.
    """
    context = context.strip()
    print(f"Context : {context}")
    handwriting_notice = "[이 문서는 손글씨일 수 있음]\n" if use_handwriting else ""

    prompt = load_resume_prompt(category, context)
    if not prompt:
        raise ValueError("프롬프트를 로드할 수 없습니다. 카테고리를 확인하세요.")
    
    return (handwriting_notice + prompt).strip()
