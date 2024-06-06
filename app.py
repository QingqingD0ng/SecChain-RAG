# app.py
import streamlit as st
import asyncio
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

# Initialize the local LLM and settings
local_llm = Ollama(model="mistral")
Settings.embed_model = OllamaEmbedding("mistral")

# Initialize the index and query engine
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
async def query_llm(query):
    logger.info(f"Query received: {query}")
    """Asynchronous function to query the LLM and return the result."""
    bundle = QueryBundle(query, embedding=Settings.embed_model.get_query_embedding(query))
    result = query_engine.query(bundle)
    logger.info("Query processed successfully")
    return result

@workflow(name="chatbot_query_workflow")
async def handle_query(query):
    response = await query_llm(query)
    logger.info(f"Query result: {response.response}\nSources: {set([node.metadata['source'] for node in response.source_nodes])}")
    return response

# Streamlit app interface
st.title("IT Security Chain Questionnaire Assistant")

# Input text box for user query
user_query = st.text_input("Enter your question here:")

# Button to submit the query
if st.button("Submit"):
    if user_query:
        logger.info("User submitted a query")
        # Get the response from the LLM asynchronously
        response = asyncio.run(handle_query(user_query))
        # Display the response in Streamlit
        st.write("**Response:**")
        st.write(f"**Text:** {response.response}\n**Source:** {set([node.metadata['source'] for node in response.source_nodes])}\n")
    else:
        st.write("Please enter a question.")
        logger.warning("User attempted to submit an empty query")
