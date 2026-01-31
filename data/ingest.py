import os
import sys
from bs4 import BeautifulSoup
import re

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.retriever import Retriever

def clean_text(html_content):
    """
    Extracts cleaner text from SEC HTML filings.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove tables and noisy elements (optional, but good for RAG quality)
    for tag in soup(['script', 'style', 'table']):
        tag.decompose()
        
    text = soup.get_text(separator=' ', strip=True)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks for embedding.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        if len(chunk) > 50: # Skip tiny chunks
            chunks.append(chunk)
    return chunks

def ingest_filings(data_dir="data/filings", specific_files=None, retriever_instance=None):
    if retriever_instance:
        retriever = retriever_instance
    else:
        retriever = Retriever()
    
    docs_to_ingest = []
    all_metadatas = []
    
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist.")
        return

    # Determine files to process
    files_to_process = []
    if specific_files:
        files_to_process = specific_files # These should be full paths
        print(f"Ingesting {len(files_to_process)} specific files...")
    else:
        print(f"Scanning {data_dir} for filings...")
        for filename in os.listdir(data_dir):
             if filename.endswith(".htm") or filename.endswith(".html"):
                files_to_process.append(os.path.join(data_dir, filename))

    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        print(f"Processing {filename}...")
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        clean_content = clean_text(content)
        chunks = chunk_text(clean_content)
        
        # Add metadata context to chunks
        # Filename format: TICKER_TYPE_DATE.htm (e.g. AAPL_10-K_2025-10-31.htm)
        ticker = filename.split("_")[0]
        labeled_chunks = [f"Source: {filename} | {chunk}" for chunk in chunks]
        metadatas = [{"ticker": ticker, "source": filename} for _ in chunks]
        
        docs_to_ingest.extend(labeled_chunks)
        # We need to pass metadatas aligned with docs_to_ingest, but ingest_documents takes one list.
        # So we better collect them and pass them all at once.
        # However, the current structure collects all docs then ingests.
        # We need to collect metadatas too.
        all_metadatas.extend(metadatas)
        
        print(f"Extracted {len(labeled_chunks)} chunks for {ticker}.")

    if docs_to_ingest:
        print(f"Ingesting {len(docs_to_ingest)} total chunks into Vector Store...")
        retriever.ingest_documents(docs_to_ingest, metadatas=all_metadatas)
        print("Ingestion complete.")
    else:
        print("No documents found to ingest.")

if __name__ == "__main__":
    ingest_filings()
