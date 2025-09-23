# app/services/retriever_service.py
from typing import Optional, List
from app.vectorstore.faiss_store import get_faiss_store

class RetrieverConfig:
    def __init__(
        self,
        k: int = 3,
        score_threshold: Optional[float] = None,
        filter_metadata: Optional[dict] = None
    ):
        """
        :param k: 召回的文档数量
        :param score_threshold: 相似度阈值（0-1），None 表示不过滤
        :param filter_metadata: 元数据过滤条件，例如 {"department": "legal"}
        """
        self.k = k
        self.score_threshold = score_threshold
        self.filter_metadata = filter_metadata

def retrieve_docs(query: str, config: RetrieverConfig) -> List[str]:
    """
    根据 RetrieverConfig 检索文档
    """
    store = get_faiss_store()
    if not store:
        return []

    # 获取检索器
    retriever = store.as_retriever(search_kwargs={"k": config.k})

    # 如果支持过滤条件，可以加上
    if config.filter_metadata:
        retriever.search_kwargs["filter"] = config.filter_metadata

    docs = retriever.get_relevant_documents(query)

    # 如果设置了相似度阈值，过滤掉低于阈值的结果
    if config.score_threshold is not None:
        docs = [
            doc for doc in docs
            if hasattr(doc, "score") and doc.score >= config.score_threshold
        ]

    return [doc.page_content for doc in docs]

# 在 LangChain（或任何 RAG 系统）里，Retriever 是 负责“召回”与用户问题相关文档 的模块。
# 它的本质：用户 query  →  向量化  →  检索（Retriever） →  返回候选文档
# Retriever 的行为主要取决于 配置参数，这些参数决定了：
#
# 召回数量 (k)
# 取多少个最相似的文档。
# k 大 → 更全面，但可能引入噪音。
# k 小 → 更精确，但可能遗漏信息。
#
# 相似度度量方式（Cosine / L2 / Inner Product）
# 影响相似度计算方式，进而影响排序结果。
# 常见选择：余弦相似度（cosine similarity）：常用，量纲无关，范围 [-1, 1]; 内积（dot product）：适合经过归一化的向量，速度快; 欧氏距离（L2 distance）：传统距离度量。
#
# 相似度阈值（score_threshold）:
# 过滤掉低于某个相似度分数的结果。
# 可以防止无关文档混入。
#
# 过滤条件（metadata filter）
# 比如只检索特定标签、日期范围、业务线的文档。
#
# 企业场景常用（权限控制、知识库分区）, 在企业里，不同业务部门可能需要不同的 Retriever 配置，比如：
# 客服部门 → 召回数大（k=5），确保找全答案
# 法务部门 → 阈值高（score_threshold=0.8），确保只返回高置信度内容
# 技术文档搜索 → 可能限制只搜某类标签（metadata filter）


