# Will & Rusty's Playdate RAG Chat

A Retrieval-Augmented Generation (RAG) application that lets you chat with transcripts from Will and Rusty's Playdate podcast using local AI models.

## Features

- 🎧 **YouTube Transcript Download**: Automatically download transcripts from YouTube videos
- 🤖 **Local AI Chat**: Chat with podcast content using Ollama models (no API keys needed!)
- 🔍 **Smart Search**: Find relevant information across multiple episodes
- 📚 **Source Citations**: See which episodes your answers came from
- 🧹 **Transcript Cleaning**: Clean up messy transcripts for better AI responses

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install langchain langchain-community langchain-chroma langchain-ollama
pip install sentence-transformers chromadb youtube-transcript-api
```

### 2. Install Ollama

- Download from [ollama.ai](https://ollama.ai)
- Install a model: `ollama pull qwen3:8b`

### 3. Download Transcripts

```bash
python working_transcript_downloader.py
```

### 4. Run the RAG Chat

```bash
python rag_app.py
```

## Project Structure

```
podcast_rag_project/
├── rag_app.py                          # Main RAG chat application
├── download_transcripts.py    # Download YouTube transcripts
├── transcript_cleaner.py               # Clean up transcript formatting
├── transcripts/                        # Folder for transcript files
│   ├── playdate137.txt
│   ├── playdate138.txt
│   └── ...
├── chroma_db/                          # Vector database (auto-created)
└── venv/                               # Virtual environment
```

## Usage Examples

Ask questions like:
- "Who are the hosts of this podcast?"
- "What games do they talk about in episode 137?"
- "What's Will's opinion on [topic]?"
- "Which episodes mention [specific game]?"

## Configuration

### Change AI Model
Edit `rag_app.py`:
```python
chat_model = Ollama(model="qwen3:4b", temperature=0.1)  # Faster
chat_model = Ollama(model="qwen3:8b", temperature=0.1)  # Better quality
```

### Adjust Chunk Size
For longer/shorter context:
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,    # Smaller = faster, larger = more context
    chunk_overlap=200
)
```

## Troubleshooting

### YouTube Download Issues
- Some videos might not have transcripts
- Try the manual transcript cleaner if auto-download fails
- Check if the video has captions enabled

### Slow AI Responses
- Switch to smaller model (qwen3:4b)
- Reduce chunk_size in rag_app.py
- Reduce number of retrieved chunks (k=3 instead of 6)

### Memory Issues
- Use smaller embedding model
- Process fewer documents at once
- Restart the application periodically

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your own podcast transcripts
5. Submit a pull request

## License

MIT License - mine but i dont care what happens with this

## Acknowledgments

- Will and Rusty for the entertaining podcast content
- Ollama team for making local AI accessible
- LangChain community for the RAG framework