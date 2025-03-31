import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define folder where text files are stored
DATA_FOLDER = "D:\\solutyics.chatbot\\data"

def process_text_files():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Chunk size to fit within LLM context
        chunk_overlap=100  # Overlap for better context
    )

    all_chunks = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):  # Process only .txt files
            file_path = os.path.join(DATA_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                chunks = text_splitter.split_text(text)
                all_chunks.extend(chunks)
    
    return all_chunks

if __name__ == "__main__":
    chunks = process_text_files()
    print(f"Processed {len(chunks)} text chunks.")
