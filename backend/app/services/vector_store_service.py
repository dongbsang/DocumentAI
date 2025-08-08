from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# ✅ HuggingFace 임베딩 모델
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ✅ 벡터 저장소 경로
VECTOR_STORE_PATH = "./vectorstore"
VECTOR_INDEX_FILE = "index.faiss"


def create_vectorstore_from_chunks(chunks: list[str]) -> FAISS:
    """
    분할된 텍스트 조각들을 임베딩하고 메모리 내 FAISS 벡터 저장소를 생성합니다.
    """
    if not chunks:
        raise ValueError("입력된 텍스트 청크가 비어 있습니다.")

    return FAISS.from_texts(chunks, embedding=embedding_model)


def save_vectorstore(vectorstore: FAISS):
    """
    FAISS 벡터 저장소를 로컬 디스크에 저장합니다.
    """
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    vectorstore.save_local(VECTOR_STORE_PATH)


def load_vectorstore() -> FAISS:
    """
    저장된 FAISS 벡터 저장소를 로드합니다.
    """
    return FAISS.load_local(VECTOR_STORE_PATH, embeddings=embedding_model)
