import os
import json
import openai
from dotenv import load_dotenv
import tempfile

# .env 파일에서 API 키 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_info_with_vision(image_path):
    """
    GPT-4o Vision 모델을 호출해 이미지에서 '공급자'와 '공급받는자' 정보를 JSON 형식으로 추출합니다.
    """
    with open(image_path, "rb") as f:
        response = openai.ChatCompletion.create(
            model="gpt-4o-vision-preview",
            messages=[
                {"role": "system", "content": "이미지에서 문서를 분석하여 JSON으로 필요한 정보를 추출합니다."},
                {"role": "user", "content": "이 이미지에서 '공급자'와 '공급받는자' 값을 JSON 형식으로 반환해주세요."}
            ],
            files=[{"file": f, "name": "document.png"}],
            temperature=0
        )

    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 원본 문자열 반환
        return content


def process_vision_stream(file_stream):
    """
    파일 스트림을 받아 임시 파일로 저장한 뒤, Vision 추출 함수를 호출합니다.
    """
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(file_stream.read())
        tmp.flush()
        tmp_path = tmp.name

    return extract_info_with_vision(tmp_path)