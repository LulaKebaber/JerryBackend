from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DataFrameLoader
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import json
import pandas as pd

def ask_gpt(text):
    with open('documents.json', 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data["restaurants"])
    loader = DataFrameLoader(df, page_content_column='name')
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # задаем векторайзер
    embeddings = OpenAIEmbeddings(openai_api_key="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")

    # создаем хранилище    
    db = FAISS.from_documents(texts, embeddings)
    db.as_retriever()

    relevants = db.similarity_search("хочу суши")

    prompt_template = """Используй контекст для ответа на вопрос, пользуясь следующими правилами:
    Если тебя спрашивают о чемто не связанным с едой кафе или ресторанами, ответь что ты ничего не знаешь об этом.
    Используя полученные данные расскажи об этом месте, чтобы человеку было понятно что ожидать от этого места.
    Используй тексты которые находятся в кавычках.
    Информацию о ресторанах или кафе можешь взять отсюда, только в том случае если запрос совпадает с требованиями {documents}
    """

    PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["documents"]
    )

    chain = LLMChain(
    llm=OpenAI(temperature=0, openai_api_key="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", max_tokens=500),
    prompt=PROMPT)

    return chain.run(relevants[0])