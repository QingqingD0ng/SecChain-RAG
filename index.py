# index.py
import json, os
from llama_index.core import Document, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from dotenv import load_dotenv
from traceloop_config import initialize_traceloop
from traceloop.sdk.decorators import workflow, task
from document_processing import partition_documents, categorize_elements
from logging_config import get_logger

# Initialize logger
logger = get_logger()

# Initialize Traceloop
initialize_traceloop()

# Load .env file contents into env
load_dotenv('env.txt')

# ElasticsearchStore is a VectorStore that takes care of ES Index and Data management.
es_vector_store = ElasticsearchStore(index_name="sec_chain", vector_field='document_vector', text_field='document', es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"), es_api_key=os.getenv("ELASTIC_API_KEY"))

@workflow(name="document_ingestion_workflow")
def main():
    logger.info("Starting document ingestion workflow")
    
    # Embedding Model to do local embedding using Ollama.
    ollama_embedding = OllamaEmbedding("mistral")

    # LlamaIndex Pipeline configured to take care of chunking, embedding and storing the embeddings in the vector store.
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=1024, chunk_overlap=20),
            ollama_embedding,
        ],
        vector_store=es_vector_store
    )

    # Partition and categorize documents
    logger.info("Partitioning documents")
    raw_elements = partition_documents("Data/Guidelines")
    categorized_elements = categorize_elements(raw_elements)

    # Convert to LlamaIndex Documents
    logger.info("Converting to LlamaIndex documents")
    documents = [Document(text=element.text, metadata={"type": element.type, "source": element.source}) for element in categorized_elements]
    
    logger.info("Running ingestion pipeline")
    pipeline.run(documents=documents)
    
    logger.info("Document ingestion workflow completed")

if __name__ == "__main__":
    main()
