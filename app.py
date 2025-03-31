from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Load FAISS index
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")
db = FAISS.load_local("D:\\solutyics.chatbot\\embeddings\\faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Initialize LLM
llm = ChatGroq(temperature=0.3, model_name="llama3-70b-8192", api_key=GROQ_API_KEY)

# Create Retrieval-QA Chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, return_source_documents=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"bot_response": "Please enter a message."})

    response = qa_chain.invoke(user_input)
    bot_response = response.get("result", "I don't know.")

    # Format the response properly
    formatted_response = format_response(bot_response)

    return jsonify({"bot_response": formatted_response})

def format_response(response_text):
    """Formats the response to look structured and professional."""
    
    # Convert numbered lists into bullet points with proper spacing
    response_text = response_text.replace("1.", "\n\n✅ ").replace("2.", "\n✅ ").replace("3.", "\n✅ ")
    response_text = response_text.replace("4.", "\n✅ ").replace("5.", "\n✅ ").replace("6.", "\n✅ ")
    
    # Capitalize first letter if missing
    response_text = response_text.strip()
    if response_text and response_text[0].islower():
        response_text = response_text[0].upper() + response_text[1:]

    return response_text


if __name__ == "__main__":
    app.run(debug=True)
