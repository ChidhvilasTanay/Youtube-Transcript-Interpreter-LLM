from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()


def create_db(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(
    video_url, add_video_info=False
    )
    transcript = loader.load()
    textsplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = textsplitter.split_documents(transcript)

    db = FAISS.from_documents(docs, embeddings) # connection between the otained yt transcript data and the llm.
    return db


video_url = 'https://www.youtube.com/watch?v=lG7Uxts9SXs&t=18s'
print(create_db(video_url))


def get_query_response(db, query, k=4):
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n", "")
    return response, docs
