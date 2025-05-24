from utils.rag_utils import load_documents, split_documents, get_vectorstore
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Step 1: Load, split, and embed
documents = load_documents("data/food_knowledge.txt")
chunks = split_documents(documents)
vectorstore = get_vectorstore(chunks)
retriever = vectorstore.as_retriever()

# Step 2: Load FLAN-T5 model
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
llm = HuggingFacePipeline(pipeline=pipe)

# Step 3: Setup RAG chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Step 4: Run chatbot loop
print("🤖 FoodConnect Chatbot (type 'exit' to quit)")
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    answer = qa_chain.run(query)
    print("Bot:", answer)
