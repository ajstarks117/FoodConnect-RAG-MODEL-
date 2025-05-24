from flask import Flask, request, jsonify, render_template
from utils.rag_utils import load_documents, split_documents, get_vectorstore
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Initialize Flask
app = Flask(__name__)

# Load and prepare RAG components at startup
documents = load_documents("data/food_knowledge.txt")
chunks = split_documents(documents)
vectorstore = get_vectorstore(chunks)
retriever = vectorstore.as_retriever()

# Load FLAN-T5
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
llm = HuggingFacePipeline(pipeline=pipe)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = qa_chain.run(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
