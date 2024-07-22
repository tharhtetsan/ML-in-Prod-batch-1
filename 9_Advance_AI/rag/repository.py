from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import ScoredPoint

class VectorRepository:
    def __init__(self, host: str = "localhost", port : int = 6333) -> None:
        self.db_client = AsyncQdrantClient(host= host, port=port)




    async def create_collections(self, collection_name : str, size : int ) -> bool:
        
        """
        Any vectors in this collection should be compared via the cosine similarity calculation
        that calculates distances between vectors.
        """
        vectors_config =  models.VectorParams(
            size=size, distance=models.Distance.COSINE
        )
        response = await self.db_client.get_collections()

        collection_exists = []
        for collection in response.collections:
            if collection_name == collection.name:
                collection_exists.append(collection)


        if collection_exists:
            logger.debug(
                f"Collection {collection_name} already exists - recreating it"
            )
            await self.db_client.delete_collection(collection_name=collection_name)
            return await self.db_client.create_collection(
                collection_name=collection_name,
                vectors_config=vectors_config
            )





        logger.debug(f"Creating new collection {collection_name}")
        return await self.db_client.create_collection(collection_name=collection_name,
                                    vectors_config=models.VectorParams(
                                    size=size, distance= models.Distance.COSINE
                                    )
        ) 



    async def delete_collection(self, name : str ) -> bool:
        logger.debug(f"Deleting collection {name}")
        return await self.db_client.delete_collection(name)


    async def create(self, collection_name : str, embedding_vector : list[float],
                    original_text : str, source : str) -> None:
        response = await self.db_client.count(collection_name= collection_name)
        logger.debug( 
            f"Creating a new vector with ID {response.count} inside the {collection_name}"
                     )
        
        await self.db_client.upsert(
            collection_name= collection_name,
            points=[
                models.PointStruct(
                    id = response.count,
                    vector= embedding_vector,
                    payload={
                        "source" : source,
                        "original_text" : original_text
                    }
                )
            ]
        )

    
    async def search(self, collection_name : str, 
                     query_vector : list[float],
                     retrievel_limit : int,
                     score_threshold : float) -> list[ScoredPoint]:
        logger.debug(
            f"Searching for relevant items in the {collection_name} - collection"
            )
        vectors = await self.db_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit = retrievel_limit,
            score_threshold=score_threshold,
        )

        return vectors
    
    