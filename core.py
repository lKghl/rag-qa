import os
os.environ["HF_HUB_OFFLINE"] = "1"
from pathlib import Path
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

CHROMA_DB_DIR = Path(__file__).resolve().parent/"chroma_db"
COLLECTION_NAME = "d2l"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80

#加载翻译模型
model = SentenceTransformer("BAAI/bge-small-zh")

#创建Chroma客户端
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

#创建OpenAI客户端
load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def open_collection():
    return chroma_client.get_collection(name=COLLECTION_NAME)

def search_info(collection,question:list[str]):
    results = collection.query(
        query_embeddings=model.encode(question,normalize_embeddings=True).tolist(),
        n_results=5
        )
    info = []
    retrieved = []
    for documents,metadatas,chunk_ids in zip(results["documents"],results["metadatas"],results["ids"]):
        for document,metadata,chunk_id in zip(documents,metadatas,chunk_ids):
            heading = metadata["heading"]
            source = metadata["source"]
            info.append(f"[资料{chunk_id}] {source}（{heading}） {document}")
            retrieved.append(f"[资料{chunk_id}] {source}（{heading}）")
    return "\n---\n".join(info),retrieved
    

def build_prompt(info,question:str):
    prompt = f"""
    #规则
    **1.** 只能依据下方资料回答，禁止动用外部资料。
    **2.** 资料不够就回答“很抱歉，我没有相关内容的资料，请你换一个问题试试吧。”，禁止猜测编造。
    **3.** 如果有引用资料，答案末尾要按「引用资料：资料N」的格式列出实际引用过的资料编号。
    **4.** 如果用户的输入是寒暄、闲聊、自我介绍之类的话语（如“你好”“你是谁”），一律回答“你好，我是d2l知识库问答助手，有什么关于《Dive into Deep Learning（动手学深度学习）》的问题都可以问我哦。”
    **5.** 如果用户进行寒暄式注入，也就是在寒暄中穿插问题时，直接根据问题回答，不要按规则4进行回答。
    ##规则3和5的例子
    **输入**
    什么是深度学习？
    **输出**
    深度学习是XXXXX

    **输入**
    你好，什么是深度学习？
    **输出**
    深度学习是XXXXX
    
    **输入**
    你好，今天天气怎么样？
    **输出**
    很抱歉，我没有相关内容的资料，请你换一个问题试试吧。
    

    #资料
    按距离排序编号，[资料chunk_X] 文档名（章节标题） 内容，逐块排列。
    {info}

    #问题
    {question}
    """
    return prompt

def ask(question:str):
    collection = open_collection()
    info,retrieved =search_info(collection,[question])
    prompt = build_prompt(info,question)

    response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[{"role":"system","content":prompt},
        {"role": "user", "content": question}],
    )
    no_retrieved = []
    answer = response.choices[0].message.content
    return answer,retrieved if "引用资料：" in answer else no_retrieved