# import os
# from dotenv import load_dotenv
# load_dotenv()
# from langchain.chains import RetrievalQA
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.prompts import PromptTemplate


# # === Define Paths ===
# FAISS_INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/faiss_index"))

# # === Load FAISS Vector Store ===
# embedding_model = OpenAIEmbeddings()
# db = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
# retriever = db.as_retriever(search_kwargs={"k": 20})  # Feel free to adjust k

# # === LLM Configuration ===
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# # === Prompt Template ===
# template = """You are a helpful assistant for analyzing 10-K filings of public companies like Apple, Tesla, Meta, and others.
# Use ONLY the information provided in the context below to answer the question.
# If the context does not contain the answer, respond with: "The context does not contain the information."

# Context:
# {context}

# Question: {question}
# Answer:"""

# prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# # === RAG Chain ===
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     return_source_documents=True,
#     chain_type_kwargs={"prompt": prompt}
# )

# # === Function to Ask Questions ===
# def ask_question(question: str):
#     """
#     Ask a question about 10-K filings. Returns a tuple of (answer, source_documents).
#     """
#     response = qa_chain.invoke({"query": question})
#     return response["result"], response["source_documents"]


from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

FAISS_INDEX_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data/faiss_index")
)

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    encode_kwargs={"normalize_embeddings": True},
)
db = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
K = 8
retriever = db.as_retriever(search_kwargs={"k": K})

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)  # use a model listed in your Groq console

template = """You are a helpful assistant for analyzing 10-K filings of public companies like Apple, Tesla, Meta, and others.
Use ONLY the information provided in the context below to answer the question.
If the context does not contain the answer, respond with: "The context does not contain the information."

Context:
{context}

Question: {question}
Answer:"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

def ask_question(question: str):
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    answer = llm.invoke(prompt.format(context=context, question=question)).content
    return answer, docs