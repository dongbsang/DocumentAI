from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ✅ HuggingFace 임베딩 모델 (무료 공개 모델 사용)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ 벡터 저장소 경로
VECTOR_STORE_PATH = "./vectorstore/index.faiss"


def create_vectorstore_from_chunks(chunks: list[str]):
    """
    분할된 텍스트 조각들을 임베딩하고 FAISS 벡터 저장소에 저장하지 않고 메모리에서 사용합니다.
    """
    if not chunks:
        raise ValueError("입력된 텍스트 청크가 비어 있습니다.")

    return FAISS.from_texts(chunks, embedding=embedding_model)


def load_vectorstore():
    """
    저장된 FAISS 벡터 저장소를 로드합니다.
    """
    return FAISS.load_local(VECTOR_STORE_PATH, embeddings=embedding_model)
