# RAG Application with FastAPI Backend and Streamlit Client

This project is a Retrieval-Augmented Generation (RAG) application that combines a FastAPI backend for document processing and vector search with a Streamlit frontend for user interaction.

## Features

- **FastAPI Backend**: Document processing, text extraction, vector embeddings, and Qdrant vector database integration
- **Streamlit Client**: User-friendly interface for uploading documents and querying the knowledge base
- **RAG Pipeline**: Document chunking, embedding generation, and semantic search
- **Vector Database**: Qdrant integration for efficient similarity search

## Prerequisites

- Python 3.12+
- pip
- Qdrant vector database server

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd project4
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

## Running the Application

### 1. Start Qdrant Vector Database

First, you need to have Qdrant running. You can either:

**Option A: Use Docker (Recommended)**
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

**Option B: Install Qdrant locally**
```bash
# Follow instructions at https://qdrant.tech/documentation/guides/installation/
```

### 2. Start FastAPI Backend

In one terminal:
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start FastAPI development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The FastAPI server will be available at `http://localhost:8000`

### 3. Start Streamlit Client

In another terminal:
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start Streamlit
streamlit run client.py --server.port 8501
```

The Streamlit interface will be available at `http://localhost:8501`

## Usage

### FastAPI Backend

The FastAPI backend provides the following endpoints:

- `POST /upload/`: Upload PDF documents for processing
- `POST /chat/`: Chat with the RAG system
- `GET /docs`: Interactive API documentation (Swagger UI)

### Streamlit Client

1. **Upload Documents**: Use the file uploader to add PDF documents to the knowledge base
2. **Process Documents**: Click "Process Documents" to extract text and generate embeddings
3. **Query Knowledge Base**: Ask questions and get relevant responses from your documents

## Project Structure

```
project4/
├── main.py                 # FastAPI application entry point
├── client.py              # Streamlit client interface
├── dependencies.py         # FastAPI dependencies and business logic
├── models.py              # Data models
├── schemas.py             # Pydantic schemas
├── rag/                   # RAG pipeline components
│   ├── extractor.py       # Text extraction from PDFs
│   ├── transformer.py     # Text processing and embedding
│   ├── repository.py      # Vector database operations
│   └── service.py         # RAG service orchestration
├── scraper.py             # Web scraping utilities
├── upload.py              # File upload handling
├── requirements.txt       # Python dependencies
└── qdrant_storage/        # Vector database storage
```

## Configuration

Key configuration options in `.env`:

- `QDRANT_HOST`: Qdrant server host (default: localhost)
- `QDRANT_PORT`: Qdrant server port (default: 6333)
- `COLLECTION_NAME`: Vector collection name (default: knowledgebase)
- `CHUNK_SIZE`: Text chunk size for processing (default: 512)
- `COLLECTION_SIZE`: Vector embedding dimensions (default: 768)

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Linting
```bash
flake8
mypy .
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Error**
   - Ensure Qdrant server is running on the correct port
   - Check firewall settings

2. **Import Errors**
   - Verify virtual environment is activated
   - Check all dependencies are installed

3. **Memory Issues**
   - Reduce `CHUNK_SIZE` for large documents
   - Monitor system memory usage

### Logs

The application uses Loguru for logging. Check console output for detailed error messages and debugging information.

## API Documentation

Once the FastAPI server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the API documentation
