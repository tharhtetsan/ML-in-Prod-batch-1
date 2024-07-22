import re
from typing import Any, AsyncGenerator

import aiofiless
from transormers import AutoModel

embedder = AutoModel.from_pretrained(
    "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True 1
)


async def load(filepath : str , chunk_size  : int = 20000) -> AsyncGenerator[str,Any]:
    async with aiofiless.open(filepath,"r") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                break

            yield chunk

def clean(text: str) -> str:
    t = text.replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\. ,", "", t)
    t = t.replace("..", ".")
    t = t.replace(". .", ".")
    cleaned_text = t.replace("\n", " ").strip()
    return cleaned_text 

def embed(text: str) -> list[float]:
    return embedder.encode(text).tolist()

