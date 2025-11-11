"""
개선된 프롬프트 서비스
- YAML 기반 프롬프트 로드
- 다양한 카테고리 지원
"""
import yaml
import os

MAX_CONTEXT_LEN = 1500  # LLM 토큰 초과 방지용


class PromptService:
    """프롬프트 관리 서비스"""
    
    def __init__(self, prompt_dir=None):
        if prompt_dir is None:
            self.prompt_dir = os.path.join("app", "prompt")
        else:
            self.prompt_dir = prompt_dir
    
    def load_prompt(self, prompt_name: str, context: str = "") -> str:
        """
        YAML 파일에서 프롬프트를 로드하고 context를 삽입
        
        Args:
            prompt_name: 프롬프트 파일명 (확장자 제외)
            context: 삽입할 컨텍스트 텍스트
            
        Returns:
            str: 완성된 프롬프트
        """
        yaml_path = os.path.join(self.prompt_dir, f"{prompt_name}.yaml")
        
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"프롬프트 파일을 찾을 수 없습니다: {yaml_path}")
        
        with open(yaml_path, "r", encoding="utf-8") as f:
            prompt_yaml = yaml.safe_load(f)
        
        template = prompt_yaml.get("template", "")
        
        # context 삽입
        prompt = template.replace("{{context}}", context.strip())
        
        return prompt
    
    def list_available_prompts(self):
        """
        사용 가능한 프롬프트 목록 반환
        
        Returns:
            list: 프롬프트 파일명 목록
        """
        prompts = []
        
        if not os.path.exists(self.prompt_dir):
            return prompts
        
        for filename in os.listdir(self.prompt_dir):
            if filename.endswith('.yaml'):
                prompts.append(filename.replace('.yaml', ''))
        
        return prompts


# 기존 함수 호환성 유지 (레거시)
def load_resume_prompt(category: str, context: str) -> str:
    """
    카테고리에 맞는 YAML 프롬프트를 로드하고 context를 삽입합니다.
    """
    service = PromptService()

    if category.strip() == "resume":
        return service.load_prompt("resume_info", context)
    elif category.strip() == "receipt":
        return service.load_prompt("receipt_info", context)
    elif category.strip() == "diagnosis":
        return service.load_prompt("diagnosis_info", context)
    else:
        raise ValueError(f"지원되지 않는 카테고리: {category}")


def get_prompt_template(
    context: str, category: str, use_handwriting: bool = False
) -> str:
    """
    문서 내용과 카테고리에 따라 적절한 프롬프트 문자열을 생성합니다.
    """
    context = context.strip()
    print(f"Context : {context[:200]}...")  # 처음 200자만 출력
    handwriting_notice = "[이 문서는 손글씨일 수 있음]\n" if use_handwriting else ""

    prompt = load_resume_prompt(category, context)
    if not prompt:
        raise ValueError("프롬프트를 로드할 수 없습니다. 카테고리를 확인하세요.")

    return (handwriting_notice + prompt).strip()
