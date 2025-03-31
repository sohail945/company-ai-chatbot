import os
from flask import Flask, request, jsonify
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Paths
FAISS_INDEX_PATH = "D:\\solutyics.chatbot\\embeddings\\faiss_index"

# Load Embeddings
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")

# Load FAISS Index (No Need to Rebuild)
vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings)

app = Flask(__name__, static_folder="static", static_url_path="")

# Serve Chat UI
@app.route("/")
def index():
    return app.send_static_file("index.html")

# Chatbot Response Endpoint
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "You have not entered a question. Please type your question."})

    # Search FAISS for answers
    docs = vector_store.similarity_search(user_message, k=3)  # Get top 3 results
    response_text = "\n".join([doc.page_content for doc in docs])

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
