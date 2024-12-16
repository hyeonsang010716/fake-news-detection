from langchain_openai import ChatOpenAI , AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from operator import itemgetter
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import sqlite3
import json
import os
from langchain_core.tools import Tool
import gc

from model.tools.tavily_search import TavilySearch
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import RemoveMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import List, TypedDict, Annotated, Literal
from pydantic import BaseModel, Field
from langchain_core.documents import Document
import asyncio

from model.state import State , Sentence
from model.tools.News_keyword_crawling import fetch_news_content
from model.tools.youtube_download import download_audio, transcribe_audio
from model import prompts
from dotenv import load_dotenv

class Agent:

    def __init__(self):
        load_dotenv()
        self.model = ChatOpenAI(model="gpt-4o", temperature=0)
        # self.model = AzureChatOpenAI(model="gpt-4o", temperature=0)
        self.graph = self.__graph_init()


    def youtube_download(self, state: State) -> State:
        print("---- this node is youtube_download ----")

        audio , youtube_header = download_audio(state["youtube_link"])

        text = transcribe_audio(audio)

        return State(youtube_content=text , youtube_header=youtube_header)

    def summary_news(self, state: State) -> State:
        print("---- this node is summary_news ----")
        prompt = PromptTemplate(
            template=prompts.summary_news_prompt,
            input_variables= ["news"],
        )

        chain = prompt | self.model | StrOutputParser()
        
        output = chain.invoke({"news" : state["youtube_content"]})
        
        print(output)
        
        return State(youtube_summary_content=output)
    
    def generation_news_core_sentence(self, state: State) -> State:
        print("---- this node is generation_news_core_sentence ----")
        prompt = PromptTemplate(
            template=prompts.generation_news_core_sentence_prompt,
            input_variables= ["summary_news"],
        )

        chain = prompt | self.model.with_structured_output(Sentence)
        
        output = chain.invoke({"summary_news" : state["youtube_summary_content"] , "youtube_header" : state["youtube_header"]})
        
        print(output.texts)
        
        return State(keywords=output.texts)

    # def search_naver_news(self, state: State) -> State:
    #     print("---- this node is search_naver_news ----")
        
    #     tasks = [fetch_news_content(keyword) for keyword in state["keywords"]]
     
    #     print(tasks)
     
    #     outputs = "\n".join(tasks)
        
    #     # return {"naver_news": outputs}
    #     return State(naver_news=outputs)
    
    def search_Tavily(self, state: State) -> State:
        print("---- this node is search_Tavily ----")
        
        tavily_tool = TavilySearch()
        
        search_results = []
        
        for keyword in state["keywords"]:
            
            result = tavily_tool.search(
                query=keyword,  # 검색 쿼리
                topic="news",  # 뉴스 주제
                days=100,
                max_results=3,  # 최대 검색 결과
                format_output=True,  # 결과 포맷팅
            )
            
            search_results.append("\n".join(result))
        
        return State(search_results=search_results)    
    
    def fake_news_detection(self, state: State) -> State:
        print("---- this node is generation_question ----")

        prompt = PromptTemplate(
            template=prompts.fake_news_detection_prompt,
            input_variables=["context" , "query"],
        )

        chain = prompt | self.model | StrOutputParser()
        
        works = [
            {"context": context, "query": query}
            for context , query in zip(state["search_results"] , state["keywords"])
        ]

        results = chain.batch(works)
        
        return State(response=results)

    def __graph_init(self):

        graph_builder = StateGraph(State)
        graph_builder.add_node("youtube_download", self.youtube_download)
        graph_builder.add_node("summary_news", self.summary_news)
        graph_builder.add_node("generation_news_core_sentence", self.generation_news_core_sentence)
        #graph_builder.add_node("search_naver_news", self.search_naver_news)
        graph_builder.add_node("search_Tavily", self.search_Tavily)
        graph_builder.add_node("fake_news_detection", self.fake_news_detection)

        graph_builder.add_edge(START, "youtube_download")
        graph_builder.add_edge("youtube_download", "summary_news")
        graph_builder.add_edge("summary_news", "generation_news_core_sentence")
        graph_builder.add_edge("generation_news_core_sentence", "search_Tavily") 
        graph_builder.add_edge("search_Tavily", "fake_news_detection")
        graph_builder.add_edge("fake_news_detection", END)
        
        graph = graph_builder.compile()

        # def save_graph_image(graph, filename="graph.png"):
        #     try:
        #         # Get the image data as PNG
        #         image_data = graph.get_graph(xray=True).draw_mermaid_png()

        #         # Save to a file
        #         with open(filename, "wb") as f:
        #             f.write(image_data)

        #         print(f"Graph image saved as {filename}")
        #     except Exception as e:
        #         print(f"Error saving graph image: {e}")

        # save_graph_image(graph, "graph.png")

        return graph