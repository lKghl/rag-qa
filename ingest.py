import re
from pathlib import Path
from core import CHUNK_SIZE,CHUNK_OVERLAP,COLLECTION_NAME,chroma_client,model

doc_dir = Path(__file__).resolve().parent/"docs"

_HTML_TAG = re.compile(r"</?(?:div|img|br|hr|center|span|font|table|tr|td|th|thead|tbody|sup|sub)\b[^>]*>", re.IGNORECASE)
_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_NAV_LINK = re.compile(r"\[([^\]]*(?:传送门|官方文档|源代码|原文|同一节)[^\]]*)\]\([^)]*\)")
_MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_CITATION = re.compile(r"(?<![A-Za-z0-9_\]])\[\d+\]")
_BOLD = re.compile(r"\*\*(?![\s])([^*]*[\u4e00-\u9fff][^*]*?)(?<![\s])\*\*")
_FENCE = re.compile(r"(?m)^\s*```\s*[a-zA-Z0-9+]*\s*(\{[^}]*\})?\s*$")
_QUOTE = re.compile(r"(?m)^\s*>\s?")
_TRAILING_WS = re.compile(r"[ \t]+\n")
_REF_HEADING = re.compile(r"^(#+)\s*参考文献")

def _drop_reference_sections(text:str) -> str:
    lines = text.split("\n")
    out = []
    i, n = 0, len(lines)
    while i < n:
        m = _REF_HEADING.match(lines[i])
        if m:
            level = len(m.group(1))
            i += 1
            while i < n:
                m2 = re.match(r"^(#+)\s", lines[i])
                if m2 and len(m2.group(1)) <= level:
                    break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)

def clean_txt(text:str) -> str:
    text = _drop_reference_sections(text)
    text = _MD_IMAGE.sub(r"\1", text)
    text = _NAV_LINK.sub("", text)
    text = _MD_LINK.sub(r"\1", text)
    text = _CITATION.sub("", text)
    text = _HTML_TAG.sub("", text)
    text = text.replace("$", "")
    text = _BOLD.sub(r"\1", text)
    text = _FENCE.sub("", text)
    text = text.replace("[TOC]", "")
    text = _QUOTE.sub("", text)
    text = _TRAILING_WS.sub("\n", text)
    return text

def load_documents(doc_dir:Path):
    docs = {}
    for path in sorted(Path(doc_dir).glob("*.md")):
        docs[path.stem] = clean_txt(path.read_text(encoding="utf-8"))
    return docs

def split_documents(docs:dict):
    ids = 1
    for doc_name in docs.keys():
        lines = [line for line in docs[doc_name].splitlines() if line.strip()]
        sections = []
        current_heading = ""
        paragraph = ""
        for line in lines:
            if line[0] == "#":
                if paragraph != "":
                    sections.append((current_heading,paragraph))
                paragraph = ""
                current_heading = line.lstrip("#").strip()
                continue
            paragraph = paragraph + line + "\n"
        sections.append((current_heading,paragraph))

        chunks_info = []
        step = CHUNK_SIZE-CHUNK_OVERLAP
        for heading,paragraph in sections:
            for i in range(0,len(paragraph),step):
                chunk = paragraph[i:i+CHUNK_SIZE]
                min_back = None
                min_front = None
                if chunk[-1] not in "。！？" :
                    for symbol in "。！？":
                        idx = paragraph[i+CHUNK_SIZE:].find(symbol)
                        if idx != -1:
                            min_back = idx if min_back is None else min(min_back,idx)
                if i != 0 and paragraph[i-1] not in "。！？":
                    for symbol in "。！？":
                        idx = paragraph[i::-1].find(symbol)
                        if idx != -1:
                            min_front = idx if min_front is None else min(min_front,idx)
                if min_back is not None and min_front is not None and min_back <= 100 and min_front <= 100:
                    chunk = paragraph[i-min_front+1:i+CHUNK_SIZE+min_back+1]
                elif min_back is not None and min_back <= 100:
                    chunk = paragraph[i:i+CHUNK_SIZE+min_back+1]
                elif min_front is not None and min_front <= 100:
                    chunk = paragraph[i-min_front+1:i+CHUNK_SIZE]
                chunks_info.append((doc_name,f"chunk_{ids}",heading,chunk))
                ids += 1
    return chunks_info

def split_info(chunks_info):
    chunk_ids = []
    chunks = []
    metadatas = []
    for doc_name,chunk_id,heading,chunk in chunks_info:
        chunk_ids.append(chunk_id)
        chunks.append(chunk)
        metadata = {}
        metadata["source"]=doc_name
        metadata["heading"]=heading
        metadatas.append(metadata)
    return chunk_ids,chunks,metadatas

def filter_chunks(chunks_info):
    merged = []
    merge_dropped = 0
    for item in chunks_info:
        if len(item[3]) < 50 and merged:
            prev = merged[-1]
            if len(prev[3]) + len(item[3]) <= 480:
                merged[-1] = (prev[0], prev[1], prev[2], prev[3] + item[3])
                continue
            merge_dropped += 1
            continue
        merged.append(item)

    kept = []
    dropped = []
    for item in merged:
        if len(item[3]) > 20:
            cjk = sum(1 for c in item[3] if '\u4e00' <= c <= '\u9fff')
            if cjk / len(item[3]) < 0.15:
                dropped.append((item, cjk / len(item[3])))
                continue
        kept.append(item)

    print(f"[过滤] 微块合并：{len(chunks_info)} → {len(merged)} 块（{merge_dropped} 个微块因超 480 封顶被丢弃）")
    print(f"[过滤] 垃圾块丢弃：{len(merged)} → {len(kept)} 块（中文占比<15%，共 {len(dropped)} 块）")
    for item, ratio in dropped[:30]:
        print(f"  [丢弃] {item[1]} ({len(item[3])}字, 中文{ratio*100:.0f}%): {item[3][:50]!r}")
    if len(dropped) > 30:
        print(f"  ……还有 {len(dropped)-30} 块，预览从略")
    return kept

if __name__ == "__main__":
    docs = load_documents(doc_dir)
    chunks_info = split_documents(docs)
    chunks_info = filter_chunks(chunks_info)
    chunk_ids,chunks,metadatas = split_info(chunks_info)
    embeddings = model.encode(chunks,normalize_embeddings=True).tolist()

    for collection in chroma_client.list_collections():
        if COLLECTION_NAME == collection.name:
            chroma_client.delete_collection(name=COLLECTION_NAME)

    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(collection.count())
