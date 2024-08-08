import os
from loguru import logger
from repository import VectorRepository
from transform import clean,embed,load

class VectorService(VectorRepository):
    def __init__(self):
        super().__init__()
        

    async def store_file_content_in_db(self,file_path : str,
                                       chunk_size : int = 512,
                                       collection_name : str = "knowledgebase",
                                        collection_size : int = 768,) -> None:
        await self.create_collections(collection_name=collection_name, size=collection_size)
        logger.debug(f"Inserting {file_path} content into database")
        async for chunk in load(filepath=file_path, chunk_size=chunk_size):
            logger.debug(f"Inserting {chunk[0:20]} ... into database")
            embedding_vector = embed(clean(chunk))
            filename = os.path.basename(file_path)
            await self.create(
                collection_name=collection_name,
                embedding_vector=embedding_vector,
                original_text=chunk,
                source=filename
            )       
       
vector_service =  VectorService()

