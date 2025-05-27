import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Debugging - Check if API Key is Loaded
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing! Check your .env file.")
    exit()

print("🚀 API Key Loaded Successfully!")

# Load FAISS index (Allow deserialization)
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")  

try:
    db = FAISS.load_local("D:\\solutyics.chatbot\\company-ai-chatbot\\embeddings\\faiss_index", embeddings, allow_dangerous_deserialization=True)
    print("FAISS Index Loaded Successfully!")
except Exception as e:
    print(f" ERROR: Failed to load FAISS index: {e}")
    exit()

# ✅ Increase Retrieval `k` for better accuracy
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# ✅ Improved Prompt for Clearer Responses
qa_prompt = """
You are an AI assistant for Solutyics. Answer questions **accurately and concisely** using the provided context.
- If the context **does not mention** the answer, **do not guess**. Instead, respond: "I don't know."
- If the user asks about **jobs or internships**, provide the **LinkedIn link** and **HR email**.
- Keep responses **short, professional, and clear**.

Context: {context}

User Query: {query}
Answer:
"""

# Initialize LLM (Groq LLaMA 70B)
try:
    llm = ChatGroq(temperature=0.3, model_name="llama3-70b-8192", api_key=GROQ_API_KEY)
    print("Groq LLM Initialized Successfully!")
except Exception as e:
    print(f" ERROR: Failed to initialize LLM: {e}")
    exit()

# Create Retrieval-QA Chain
try:
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, return_source_documents=True)
    print(" Retrieval-QA Chain Created!")
except Exception as e:
    print(f" ERROR: Failed to create QA Chain: {e}")
    exit()

# ✅ Function to Refine Answers
def refine_answer(query, answer):
    query_lower = query.lower()

    # 🔹 Handle Specific Queries
    if "products" in query_lower:
        return "Solutyics provides AI-powered chatbots, IVR systems, data analytics solutions, and AI consulting services."

    if "services" in query_lower:
        return """Solutyics offers:
        - AI & Machine Learning (Predictive Modeling, Anomaly Detection, Recommender Systems)
        - Data Engineering (ETL, Data Pipelines, Data Warehousing)
        - Data Analytics (Business Intelligence, Big Data)
        - AI Strategy & Training 
        - Web Development (Full stack)
        """

    if "how can apply" in query_lower or "how can apply for job?" in query_lower or "apply?" in query_lower:
        return """You can apply for jobs at Solutyics through:
         LinkedIn: [Solutyics Job Posts](https://www.linkedin.com/company/solutyics/posts/?feedView=all)
         Email: hrsolutyics@gmail.com
        """

    if "internship available?" in query_lower:
        return """Yes, Solutyics offers internships in AI research and software engineering.
         Apply here: [Solutyics Job Posts](https://www.linkedin.com/company/solutyics/posts/?feedView=all)
         Email: hrsolutyics@gmail.com
        """

    # 🔹 Ensure answer is concise
    if len(answer) > 300:
        return answer[:300] + "..."  # Truncate long responses

    return answer


# ✅ Chatbot Function
def chatbot():
    print("\n🤖 **Welcome to Solutyics AI Chatbot!** Ask anything about jobs or company info.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("🗣️ You: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting chatbot. Have a great day!")
            break

        try:
            # Invoke QA Chain
            response = qa_chain.invoke(query)
            
            # Extract answer
            answer = response.get('result', None)

            # 🔹 Handle cases where no relevant answer is found
            if not answer or answer.strip().lower() in ["i don't know", "not mentioned", "no context found"]:
                answer = "I don't know. Can I help with something else?"

            # 🔹 Refine Answer
            answer = refine_answer(query, answer)

            print(f"🤖 Bot: {answer}\n")

        except Exception as e:
            print("❌ Bot: Sorry, something went wrong. Please try again later.")

# ✅ Run Chatbot
if __name__ == "__main__":
    print("✅ Chatbot Script Started!")
    chatbot()
