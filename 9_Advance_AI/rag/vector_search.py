from service import vector_service
from transform import embed
async def get_rag_content(prompt :str):
    rag_content = await vector_service.search(
        "knowledgebase" , embed(prompt),3,0.7
    )

    rag_content_str = "\n"
    for cur_c in rag_content:
        rag_content_str = rag_content_str+ cur_c.payload["original_text"]+"\n"
    
    return rag_content_str