import os, string, re, regex
import time

from dotenv import load_dotenv


from langchain_google_genai import GoogleGenerativeAI, ChatGoogleGenerativeAI
from langchain_google_community import GCSFileLoader
from langchain_community.document_loaders import PyPDFLoader


from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_community import BigQueryVectorStore
#from langchain_community.vectorstores import FAISS


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage



load_dotenv()
api_key = os.environ ["GOOGLE_API_KEY"]


def pypdf_loader (file_path):
    return PyPDFLoader(file_path)


def gcs_file_loader (project_id, bucket_name, blob_name):
    # loader = GCSDirectoryLoader(
    #     project_name="aist", bucket="testing-hwc", prefix="bucket prefix", continue_on_failure=True
    # )

    pdf_loader = GCSFileLoader(
        project_name=project_id,
        bucket=bucket_name,
        blob=blob_name,
        loader_func=pypdf_loader
    )


    loaded_file = pdf_loader.load()

    #loaded_file = " ".join([d.page_content for d in loaded_file])
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
    docs = text_splitter.split_documents(loaded_file)
    #print(loaded_file)
    return docs




def generate_vector_db ():
    docs = gcs_file_loader(
        project_id="optimum-task-411411",
        bucket_name="gcloud_pdf_intelligence",
        blob_name="Job Roadmap For Students.pdf"
    )
    #print(docs)


    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db_store = BigQueryVectorStore(
        project_id="optimum-task-411411",
        dataset_name="job_guide",
        table_name="langchain_vector_store",
        location="us-west1",
        embedding=embeddings,
    )
    db_store.add_documents(docs)


    docs = " ".join ([d.page_content for d in docs])
    return db_store, embeddings, docs




def vector_search (vector_db, embedding, query):
    """
    Search for documents
    query = "I'd like a fruit."
    docs = store.similarity_search(query)
    print(docs)

    Search for documents with metadata filter
    query_vector = embedding.embed_query(query)
    docs = store.similarity_search_by_vector(query_vector, k=2)
    docs = store.similarity_search_by_vector(query_vector, filter={"len": 6})

    Batch search
    results = store.batch_search(
        embeddings=None,  # can pass embeddings or
        queries=["search_query", "search_query"],  # can pass queries
    )
    """
    query_vector = embedding.embed_query(query)
    results = vector_db.similarity_search_by_vector(query_vector)

    results_string = " ".join ([d.page_content for d in results])
    #print(f"\n\nSimilarity Search Results for {query}:\n{results_string}")


    return results_string



def docs_chatbot (query, docs_string):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    prompt = PromptTemplate(
        input_variables=["query", "docs"],
        template="""
            Answer question based on given information. Use markdown formatting
            Question: {query};
            Information: {docs}
        """
    )

    chain = prompt | llm

    response = chain.invoke ({"query": query, "docs": docs_string})
    return response.content




def main_init ():
    query_string = "how can ai help me to become more productive"
    db_store, embedding, complete_docs = generate_vector_db()
    chatbot_response = docs_chatbot(query_string, complete_docs)
    print(f"\n\n\n\n# Extracted information:\n\n{complete_docs}")
    print(f"\n\n\n\n# Gemini response:\n\n{chatbot_response}")


def main_re ():
    query_string = "how can ai help me to become more productive"

    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db_store = BigQueryVectorStore(
        project_id="optimum-task-411411",
        dataset_name="job_guide",
        table_name="langchain_vector_store",
        location="us-west1",
        embedding=embedding,
    )
    query_results = vector_search(db_store, embedding, query_string)
    chatbot_response = docs_chatbot(query_string, query_results)
    print(f"\n\n\n\n# Gemini response:\n\n{chatbot_response}")






if __name__ == "__main__":
    pass
    query_string = "how can ai help me to become more productive"

    print(f"\n\n\n\n# main_init():\n")
    time_start = time.time_ns()
    main_init()

    time_end = time.time_ns()
    elapsed_time = (time_end - time_start) / (10 ** 9)
    print(f"\n\n\n\n# Elapsed time: {elapsed_time} seconds")




    print(f"\n\n\n\n# main_re():\n")
    time_start = time.time_ns()
    main_re()

    time_end = time.time_ns()
    elapsed_time = (time_end - time_start) / (10**9)
    print(f"\n\n\n\n# Elapsed time: {elapsed_time} seconds")
