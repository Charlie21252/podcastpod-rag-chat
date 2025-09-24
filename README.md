Will & Rusty's Playdate RAG Chat

AI-powered chat application that lets you have conversations with podcast transcripts using Retrieval-Augmented Generation (RAG)


What it does:

This RAG application allows you to chat with podcast episodes as if you're having a conversation with the content itself. Ask questions about specific episodes, hosts' opinions, topics discussed, or find information across multiple episodes instantly.

Full demo Demo- 

<!-- Sample Conversation -->

🎧 Will & Rusty's Playdate RAG Chat 🎧

Ask questions about the podcast episodes!
Type 'exit' or 'quit' to end the conversation


Your question: Who are the hosts of this podcast?

Answer: <think>
Let me analyze the provided podcast transcripts to see any mention of the hosts

from the transcript it is ovious that 
The hosts of this podcast are Will and Rusty, as mentioned in the 
Will and Rusty's Playdate podcast episodes.

Sources (3 relevant chunks found):
   • Episode 137 (playdate137.txt)
   • Episode 139 (playdate139.txt)
   • Episode 140 (playdate140.txt)


Your question: what is wills opinion on baseball?

Searching through episodes...

Answer: <think>
Let me analyze the provided podcast transcript to understand Will's opinion on baseball.

From the transcript, I can see several mentions of baseball:

1. "The worst part about baseball games is if unless you're like really knowing unless you really know a lot about baseball without the commentary sometimes it's kind of hard to know what the [__] going on or or like what uh is the best play here."

2. "There's no home runs." (This seems to be a comment about baseball games)

3. "Uh, you can't just grab a cheap ticket for the last few innings to drink a beer and a dog. Enjoy." (This is about baseball games)

4. "Uh, in comes lesser innings, a play on extra innings. Available only after the bottom of the fifth inning." (This is about baseball rules)

5. "Like we'll go to a Mets game and he posts like a picture of like we like every time I go with Willie, he has picked the seats that are going to be the closest to Wanoto even if we're sacrificing like visibility of the rest of the game."

6. "I think I meant in the context of the Mets like being bad. No matter what Pete Alonzo does in his

Sources (4 relevant chunks found):
   • Episode 120 (playdate120.txt)
   • Episode 132 (playdate132.txt)
   • Episode 135 (playdate135.txt)
   • Episode 136 (playdate136.txt)


<!-- Key Features -->

- *Smart Search*: Find relevant information across multiple podcast episodes
- *Natural Conversation*: Ask questions in plain English
- *Source Citations*: See exactly which episodes your answers came from
- *Local AI*: Runs entirely on your machine using Ollama (no API keys)
- *Fast Responses*: Optimized for quick Q&A sessions
- *Clean Transcripts*: Automatically downloads and cleans YouTube transcripts


<!-- Tech Stack Used -->

- *Python 3.8+* - Core application
- *LangChain** - RAG framework and document processing
- *Ollama* - Local AI model execution (Qwen 3.2 4B)
- *ChromaDB* - Vector database for semantic search
- *Sentence Transformers* - Text embeddings
- *YouTube Transcript API* - Automatic transcript downloading



<!-- How to set it up yourself -->


1. Clone and Setup
git clone https://github.com/yourusername/podcast-rag-chat.git
cd podcast-rag-chat

python -m venv venv
source venv/bin/activate   
for Windows: venv\Scripts\activate

pip install -r requirements.txt


2. Install Ollama
Download from https://ollama.ai
Then pull a model:
ollama pull qwen3:4b


3. Download Transcripts
python download_transcripts.py

4. Run the Chat
python rag_app.py

<!-- How It Works -->

1. *Transcript Ingestion*: YouTube transcripts are downloaded and cleaned
2. *Document Chunking*: Large transcripts split into manageable pieces
3. *Vector Embeddings*: Text converted to numerical representations
4. *Semantic Search*: User questions matched with relevant transcript chunks
5. *AI Generation*: Local AI model generates answers using retrieved context
6. *Citation*: Sources automatically tracked and displayed

Example Questions to Try:

- "Who are the podcast hosts?"
- "What storys do they tell in episode 137?"
- "What's their funniest moment?"
- "Do Will and Rusty ever disagree?"
- "Which episode talks about [specific thing]?"
- "What's their opinion on [specific topic]?"

<!-- Configuration -->

If you want to change the AI Model
In rag_app.py, modify:
chat_model = Ollama(model="qwen3:8b")  # For better quality (slower)
chat_model = Ollama(model="qwen3:4b")  # For faster responses
<!-- or any model you prefer -->


If you want to adjust Performance
Chunk size (larger = more context, slower)
chunk_size=800  # Default: fast responses
chunk_size=1500  # More context per chunk

Retrieved chunks (more = better context, slower)
search_kwargs={"k": 4}  # Default
search_kwargs={"k": 6}  # More comprehensive answers


<!-- Other Features -->

- Transcript Cleaning: Removes formatting artifacts and improves readability
Run the Chat:
python rag_app.py

<!-- Acknowledgments -->

- Will and Rusty for creating entertaining podcast content
- The Ollama team for making local AI accessible
- LangChain community for the excellent RAG framework
- YouTube Transcript API for easy transcript access

---

<!-- Star this repo if you found it helpful! -->

*Built By Charlie Hristov*