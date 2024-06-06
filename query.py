# query.py
from llama_index.core import VectorStoreIndex, QueryBundle, Response, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from index import es_vector_store
from traceloop_config import initialize_traceloop
from traceloop.sdk.decorators import workflow, task
from langchain.prompts.prompt import PromptTemplate
from logging_config import get_logger

# Initialize logger
logger = get_logger()

# Initialize Traceloop
initialize_traceloop()

# Local LLM to send user query to
local_llm = Ollama(model="mistral")
Settings.embed_model = OllamaEmbedding("mistral")

index = VectorStoreIndex.from_vector_store(es_vector_store)
query_engine = index.as_query_engine(local_llm, similarity_top_k=5)

# Optimized Prompt Template
prompt_template = """
You are an advanced AI assistant specializing in answering IT security chain-related questionnaires according to internal guidelines and example answers. Given the following context extracted from these documents and a user question, provide a detailed and accurate answer.

Context:
=========
{context}
=========

Question: {question}

Guidelines:
- Ensure your answer adheres to the internal guidelines and examples provided.
- The answer should be truthful and accurate.
- Include references to the document source where possible.
- Maintain a professional and informative tone in English.
"""

optimized_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

@task(name="query_llm_task")
def query_llm(query):
    logger.info(f"Query received: {query}")
    bundle = QueryBundle(query, embedding=Settings.embed_model.get_query_embedding(query))
    result = query_engine.query(bundle)
    logger.info("Query processed successfully")
    return result

@workflow(name="sample_query_workflow")
def main():
    query = "Explain the security measures for protecting sensitive data"
    result = query_llm(query)
    logger.info(f"Query result: {result.response}\nSources: {set([node.metadata['source'] for node in result.source_nodes])}")
    print(f"Text: {result.response}\nSource: {set([node.metadata['source'] for node in result.source_nodes])}\n")

if __name__ == "__main__":
    main()
