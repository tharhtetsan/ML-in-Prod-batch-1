## Retrieval Augmented Generation (RAG)
convert PDF into text files
```bash
pipenv install --dev pypdf
```


Use aiofiles library to open an asynchronous connections to a file on the file system.
```bash
pipenv install --dev aiofiles
```


#### Download and Run Local Database
You can use other vector database providers such as Weaviate, Elastic, Milvus, Pinecone, Chroma or others in replacement of Qdrant. Each has a set of features and limitations to consider for your own use case.


```bash
docker pull qdrant/qdrant 
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```