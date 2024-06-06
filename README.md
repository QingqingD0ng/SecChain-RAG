# SecureChain Project

This project demonstrates the use of a Language Learning Model (LLM) integrated with Elasticsearch for document retrieval and response generation. The application leverages several components for data processing, data ingestion, data retrieval and response generation.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Setup](#environment-setup)
- [Elastic Search Setup](#elastic-search-setup)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
![SecureChain Workflow](https://i.ibb.co/WcyrHdk/securechain-workflow.png)

The SecureChain project integrates a Retrieval-Augmented Generation (RAG) model with Elasticsearch to enhance document retrieval and response generation capabilities. This methodology leverages advanced natural language processing (NLP) techniques to deliver accurate and contextually relevant answers to queries related to IT security. The framework comprises several components, including data ingestion, document processing, vector storage, and query handling, which together form a cohesive system for efficient information retrieval.

### Data Ingestion and Preprocessing

1. **Document Partitioning**: The initial phase involves partitioning various document types (e.g., PDF, DOCX, DOC, XLSX, and images) utilizing the `unstructured.partition` library. This step extracts textual elements and metadata, facilitating subsequent processing stages.
   - PDF documents are processed using high-resolution strategies and table inference models.
   - DOCX and DOC files are decomposed into textual elements.
   - XLSX files are parsed to extract their content.
   - Image files undergo optical character recognition (OCR) to extract embedded text.

2. **Element Categorization**: The extracted elements are categorized based on their content type (e.g., text, tables). This categorization is crucial for structured indexing and retrieval, ensuring that each element can be accurately identified and processed.

### Embedding and Vector Storage

3. **Embedding Model Initialization**: The local Language Learning Model (LLM), `Ollama`, is initialized with the pre-trained `mistral` model. This model generates high-dimensional embeddings for both queries and document elements, facilitating semantic search capabilities.
   - **OllamaEmbedding**: This component generates embeddings for document elements and queries, converting textual data into vector representations.

4. **Vector Store Configuration**: An Elasticsearch-based vector store (`ElasticsearchStore`) is configured to manage and store these embeddings. This setup ensures efficient and scalable retrieval operations by indexing the document embeddings and enabling semantic searches.

### Query Processing and Response Generation

5. **Query Engine Initialization**: The `VectorStoreIndex` is constructed from the Elasticsearch vector store, enabling the query engine to perform similarity searches and retrieve relevant document sections.
   - The query engine leverages the local LLM to interpret and respond to user queries.

6. **Prompt Optimization**: A customized prompt template is developed to guide the response generation process. This template ensures that answers adhere to internal guidelines, provide accurate references to source documents, and maintain a professional tone.

### Logging and Observability
7. **Logging Configuration**: A comprehensive logging setup is established using the `logging` library to monitor and debug the various stages of document processing and query handling. This includes logging for document partitioning, element categorization, embedding, and query responses.

## Demo

![SecureChain Interface](https://i.ibb.co/9sXgc30/Screenshot-2024-06-03-at-23-48-03.png)

## Features

- Document retrieval using RAG
- Semantic search using Elasticsearch
- Response generation using a local Language Learning Model
- Observability with Traceloop

## Installation

### Prerequisites

- Python 3.7 or higher
- Elasticsearch
- Ollama
- pip (Python package installer)
- Tracecloop
  
### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/QingqingD0ng/SecChain.git
   cd llm-demo-project
1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
1. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
For more information, refer to the Unstructured Full Installation Guide.
1. **Install unstructured with all document types:**
   ```bash
   pip install "unstructured[all-docs]"
1. **Run Mistral locally:**
Download and install Ollama. After installing Ollama, run this command to download and run mistral:
   ```bash
   ollama run mistral
   
## Usage
### Environment Setup
1.  **Configure ElasticSearch:**
Replace the placeholder values with your own API_KEY in `env.txt`
2.  **Configure  Tracelop**
Replace the placeholder values with your own configurations in `loop_config.py`

### Running the Streamlit Interface
To run the Streamlit interface for a more interactive experience:
```bash
streamlit run app.py
```
