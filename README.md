# RAG Knowledge Assistant

A document-grounded question-answering application built with Python and Streamlit, containerized with Docker, and deployed to Microsoft Azure Container Apps.

## Overview

The RAG Knowledge Assistant lets users upload a PDF or text document and ask questions about its contents. Instead of relying solely on a language model's general knowledge, the application retrieves relevant document passages and provides them as context for answer generation.

**Tech stack:** Python · Streamlit · PDF/text processing · Sentence Transformers · Retrieval-Augmented Generation (RAG) · NVIDIA API · Docker · Azure Container Registry · Azure Container Apps

## How it works

1. **Upload:** The user uploads a PDF or TXT file in the Streamlit interface.
2. **Process:** The application extracts text and splits it into passages.
3. **Embed:** A sentence-transformer model represents text as numerical vectors.
4. **Retrieve:** Similarity-based retrieval selects relevant passages for the question.
5. **Generate:** A language model receives the question and retrieved context, then generates an answer.

```text
PDF / TXT upload
       |
       v
Text extraction and chunking
       |
       v
Embeddings and similarity search
       |
       v
Retrieved document context
       |
       v
NVIDIA-hosted LLM
       |
       v
Answer in Streamlit
```

## Language model

The current deployed version uses **NVIDIA Nemotron 3.5 Lightning 30B A3B** through NVIDIA's OpenAI-compatible API:

- Model ID: `nvidia/nemotron-3.5-lightning-30b-a3b`
- API base URL: `https://integrate.api.nvidia.com/v1`
- Secret environment variable: `NVIDIA_API_KEY`

Model availability may change. The model can be replaced in `answer_machine.py`.

## Run locally

Prerequisites: Python, the dependencies listed in `requirements.txt`, and a valid NVIDIA API key.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Provide the API key as an environment variable (do not commit it):

```bash
export NVIDIA_API_KEY="<your-api-key>"
```

Start the app:

```bash
streamlit run frontend.py
```

Open the local URL printed by Streamlit, typically `http://localhost:8501`.

## Docker

Build the image:

```bash
docker build --platform linux/amd64 -t rag-knowledge-assistant:local .
```

Run it locally:

```bash
docker run --rm -p 8501:8501 \
  -e NVIDIA_API_KEY="$NVIDIA_API_KEY" \
  rag-knowledge-assistant:local
```

The app is available at `http://localhost:8501`.

## Azure deployment

The application was deployed using the following components:

- **Azure Container Registry (ACR):** Stores the Docker image.
- **Azure Container Apps:** Runs the containerized Streamlit application.
- **Azure Container Apps Secrets:** Stores the NVIDIA API key outside the image.
- **Environment variables:** Exposes the secret to the application as `NVIDIA_API_KEY`.

The deployment image is built for `linux/amd64` to match the target runtime. Deployment access may be disabled outside of demonstrations to limit public exposure and API usage.

## Security and limitations

- Never commit `.env` files, API keys, or credentials to Git.
- Keep the NVIDIA API key in environment variables or a secret manager.
- Do not upload confidential documents to a publicly accessible demo.
- This is a portfolio/learning project, not a production-hardened document-processing service.
- Retrieval quality depends on text extraction, chunking, embeddings, and the document content.
- A language model can still produce incorrect answers; retrieved passages should be checked.

## What I learned

This project provided hands-on experience with building an end-to-end RAG pipeline, integrating an external LLM API, packaging a Python application in Docker, deploying to Azure, configuring secrets, and debugging container, authentication, and model-availability issues.

## Possible next steps

- Evaluate retrieval quality on a representative question set.
- Add automated tests and CI/CD.
- Improve access controls and monitoring for production use.
- Compare alternative retrieval and reranking strategies.

## License

See the repository's license file, if provided.
