from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter


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
