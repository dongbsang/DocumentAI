import os
import base64
import mimetypes
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv

from flask import Blueprint, request, jsonify, current_app

#from app.services.pdf_service import process_pdf
#from app.services.word_service import process_word
#from app.services.hwp_service import process_hwp
#from app.services.ocr_service import process_image  # 이미지 ➔ OCR

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def dectect_file_format(file_bytes: bytes, filename: str) -> str:
    """
    GPT-4o Vision 모델을 이용해 파일 형식(pdf, hwp, word, image) 중 하나를
    반드시 JSON { "format": "..." } 으로만 응답받아 반환합니다.
    """
    # 1) 확장자 기반으로 MIME 타입 추측
    mime_type, _ = mimetypes.guess_type(filename)
    if not mime_type:
        mime_type = "application/octet-stream"

    # 2) Base64 인코딩 → data URL 생성
    b64      = base64.b64encode(file_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64}"

    # 3) GPT-4o Vision에 멀티모달 요청
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 문서 포맷 분류기입니다. 첨부된 파일을 보고 "
                    "지원 가능한 형식(pdf, hwp, word, image) 중 하나를 "
                    "반드시 JSON {\"format\":\"...\"} 으로만 응답하세요."
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text",      "text": "이 파일을 확인해주세요."},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    # 4) 응답에서 JSON 문자열 그대로 꺼내서 리턴
    fmt_json = resp.choices[0].message.content.strip()
    current_app.logger.info(f"Detected format: {fmt_json}")
    return fmt_json

'''
def extract_by_format(file_bytes: bytes,
                      fmt: str,
                      user_category: str,
                      ignore_handwriting: bool) -> dict:
    """
    1) 포맷별 전처리 함수 호출
    2) OpenAI에 “양식 기반 추출” 요청
    """
    # 2-1. 전처리: PDF→이미지, Word→텍스트, HWP→텍스트, Image→이미지
    if fmt == "pdf":
        pages = process_pdf(BytesIO(file_bytes), to_images=True)
        # pages: List[BytesIO]
        # 합쳐서 GPT-Vision 호출
        content = ""
        for pg in pages:
            content += analyze_image_with_gpt(pg,
                user_category, ignore_handwriting) + "\n\n"
        return {"analysis": content}

    if fmt == "image":
        return {"analysis": analyze_image_with_gpt(
            BytesIO(file_bytes), user_category, ignore_handwriting)}

    if fmt in ("word","hwp"):
        txt = process_word(BytesIO(file_bytes)) if fmt == "word" else process_hwp(BytesIO(file_bytes))
        return {"analysis": analyze_text_with_gpt(
            txt, user_category, ignore_handwriting)}

    raise ValueError(f"지원하지 않는 포맷: {fmt}")

def analyze_image_with_gpt(img_stream: BytesIO,
                           user_category: str,
                           ignore_handwriting: bool) -> str:
    """
    GPT-4V 호출: “이 이미지는 PDF 자기소개서이며, 손글씨 무시하고
    {category} 양식 기준으로 텍스트만 뽑아줘” 등의 프롬프트
    """
    system = (
        "당신은 문서 분석가입니다. 이 이미지는 " +
        f"{user_category} 형식의 문서로, " +
        ("손글씨를 무시" if ignore_handwriting else "손글씨도 포함") +
        "하고, 양식에 맞추어 주요 필드를 JSON으로 뽑아주세요."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-vision-preview",
        messages=[
            {"role":"system", "content": system},
        ],
        files=[{"name":"file", "file": img_stream}]
    )
    return resp.choices[0].message.content

def analyze_text_with_gpt(text: str,
                          user_category: str,
                          ignore_handwriting: bool) -> str:
    """
    GPT-3.5/4 호출: “이 텍스트는 {category} 문서이며,
    손글씨 부분 무시하고 ~ 양식 기반으로 JSON으로 반환”
    """
    system = (
        "당신은 문서 분석가입니다. 이 텍스트는 " +
        f"{user_category} 형식의 문서로, " +
        ("손글씨를 무시" if ignore_handwriting else "손글씨도 포함") +
        "하고, 양식에 맞추어 주요 필드를 JSON으로 뽑아주세요."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system", "content": system},
            {"role":"user",   "content": text}
        ]
    )
    return resp.choices[0].message.content
'''