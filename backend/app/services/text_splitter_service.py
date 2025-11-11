from typing import List

# langchain 최신 버전에서는 text_splitter가 별도 패키지로 분리됨
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✅ langchain_text_splitters에서 import 성공")
except ImportError:
    # 구버전 호환성
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        print("✅ langchain.text_splitter에서 import 성공 (구버전)")
    except ImportError:
        raise ImportError(
            "TextSplitter를 import할 수 없습니다.\n"
            "다음 명령어로 설치하세요: pip install langchain-text-splitters"
        )


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    주어진 텍스트를 작은 청크 단위로 분할합니다.

    Args:
        text (str): 분할할 원본 텍스트
        chunk_size (int): 청크 하나의 최대 문자 수 (기본: 1000)
        chunk_overlap (int): 청크 간 중복되는 문자 수 (기본: 200)

    Returns:
        List[str]: 분할된 텍스트 청크 목록
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )
    return splitter.split_text(text)
