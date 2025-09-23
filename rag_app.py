import os
import re
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

def clean_response(text):
    """Remove thinking tags and other unwanted formatting from model responses"""
    # Remove <think>...</think> blocks
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove extra whitespace and newlines
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)
    return cleaned.strip()

# Load documents with enhanced metadata
docs = []
transcript_folder = "transcripts"

print("Loading podcast transcripts...")

if not os.path.exists(transcript_folder):
    print(f"Creating {transcript_folder} folder...")
    os.makedirs(transcript_folder)

for file_name in os.listdir(transcript_folder):
    if file_name.endswith(".txt"):
        try:
            with open(os.path.join(transcript_folder, file_name), "r", encoding="utf-8") as f:
                text = f.read()
                
                if text.strip():  # Only process non-empty files
                    # Extract episode number from filename
                    episode_num = "Unknown"
                    if "playdate" in file_name.lower():
                        episode_match = re.search(r'playdate(\d+)', file_name.lower())
                        if episode_match:
                            episode_num = episode_match.group(1)
                    
                    # Add context to the document
                    context_text = f"This is from Will and Rusty's Playdate podcast, Episode {episode_num}.\n\n{text}"
                    
                    docs.append(Document(
                        page_content=context_text,
                        metadata={
                            "source": file_name,
                            "podcast": "Will and Rusty's Playdate",
                            "episode": episode_num,
                            "type": "podcast_transcript"
                        }
                    ))
                    
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

if not docs:
    print("No transcript files found! Add .txt files to the transcripts/ folder.")
    print("   Expected format: playdate139.txt, playdate140.txt, etc.")
    exit()

print(f"Loaded {len(docs)} podcast transcript files")

# Split documents into chunks
print("Processing documents...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,    # Smaller chunks for faster processing
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)
split_docs = splitter.split_documents(docs)
print(f"Created {len(split_docs)} document chunks")

# Create embeddings and vector database
print("Creating embeddings and vector database...")
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma.from_documents(split_docs, embeddings, persist_directory="chroma_db")

# Set up retriever
retriever = vectordb.as_retriever(
    search_type="mmr", # Maximal Marginal Relevance for diverse results
    search_kwargs={"k": 4, "fetch_k" : 20}  # proccessing speed
)

# Use a more reliable model (change this if you want to try others)
print("Initializing language model...")
chat_model = Ollama(
    model="qwen3:4b",
    temperature=0.1,
    num_ctx=2048,      # context window
    num_predict=256,   # response length
)

# Create custom prompt template
prompt_template = """
You are analyzing transcripts from "Will and Rusty's Playdate" podcast. This is a gaming/entertainment podcast hosted by Will and Rusty.

Context from podcast episodes:
{context}

Question: {question}

Instructions:
- Answer based only on the provided context
- If you don't know something based on the context, say "I don't have that information in the provided transcripts"
- Be conversational and natural in your responses
- Reference specific episodes when relevant
- Focus on being helpful and accurate
- Avoid making up information or hallucinating details
- If the user asks about a specific episode number, prioritize that episode's content.

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Create QA chain with custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=chat_model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

print("\n" + "="*50)
print("🎧 Will & Rusty's Playdate RAG Chat 🎧")
print("="*50)
print("Ask questions about the podcast episodes!")
print("Type 'exit' or 'quit' to end the conversation")
print("="*50)

# Main chat loop
while True:
    try:
        query = input("\nYour question: ")
        
        if query.lower().strip() in ["exit", "quit", "bye"]:
            print("\nThanks for using the Playdate RAG Chat!")
            break
        
        if not query.strip():
            continue
        
        print("\n Searching through episodes...")
        result = qa_chain.invoke({"query": query})
        
        # Clean the response
        clean_answer = clean_response(result["result"])
        
        # Display results
        print(f"\n Answer: {clean_answer}")
        
        # Show sources with episode info
        sources = result["source_documents"]
        if sources:
            print(f"\n Sources ({len(sources)} relevant chunks found):")
            episode_sources = set()
            for doc in sources:
                episode = doc.metadata.get("episode", "Unknown")
                filename = doc.metadata.get("source", "unknown")
                episode_sources.add(f"Episode {episode} ({filename})")
            
            for source in sorted(episode_sources):
                print(f"   • {source}")
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\nError: {e}")
        print("Please try asking your question again.")