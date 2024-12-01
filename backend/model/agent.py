from langchain_openai import ChatOpenAI
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

from langchain_teddynote.tools.tavily import TavilySearch
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
        self.graph = self.__graph_init()


    def youtube_download(self, state: State) -> State:

        print("---- this node is youtube_download ----")

        audio = download_audio(state["youtube_link"])

        text = transcribe_audio(audio)

        return State(youtube_content=text)

    def generation_question(self, state: State) -> State:
        
        print("---- this node is generation_question ----")

        prompt = PromptTemplate(
            template=prompts.generation_question_prompt,
            input_variables= ["content"],
        )

        chain = prompt | self.model.with_structured_output(Sentence)
        
        output = chain.invoke({"content" : state["youtube_content"]})
        
        print(output.text)
        
        #return {"keywords": output.text}
        return State(keywords=output.text)

    def search_naver_news(self, state: State) -> State:
        print("---- this node is search_naver_news ----")
        
        tasks = [fetch_news_content(keyword) for keyword in state["keywords"]]
     
        print(tasks)
     
        outputs = "\n".join(tasks)
        
        # return {"naver_news": outputs}
        return State(naver_news=outputs)
    
    def search_Tavily(self, state: State) -> State:
        print("---- this node is search_Tavily ----")
        
        tavily_tool = TavilySearch()
        
        tasks = []
        
        for keyword in state["keywords"]:
            search_result = tavily_tool.search(
                query=keyword,  # 검색 쿼리
                topic="news",  # 일반 주제
                days=100,
                max_results=1,  # 최대 검색 결과
                format_output=True,  # 결과 포맷팅
            )
            tasks.append("\n".join(search_result))
     
        #print(tasks)
     
        outputs = "\n".join(tasks)
        
        # return {"naver_news": outputs}
        return State(naver_news=outputs)    
    
    def fake_news_detection(self, state: State) -> State:
        
        print("---- this node is generation_question ----")

        prompt = PromptTemplate(
            template=prompts.fake_news_detection_prompt,
            input_variables=["content" , "news"],
        )

        chain = prompt | self.model | StrOutputParser()
        
        output = chain.invoke({"content" : state["youtube_content"] , "news" : state["naver_news"]})
        
        # return {"response" , output}
        return State(response=output)

    def __graph_init(self):

        graph_builder = StateGraph(State)
        graph_builder.add_node("youtube_download", self.youtube_download)
        graph_builder.add_node("generation_question", self.generation_question)
        #graph_builder.add_node("search_naver_news", self.search_naver_news)
        graph_builder.add_node("search_Tavily", self.search_Tavily)
        graph_builder.add_node("fake_news_detection", self.fake_news_detection)

        graph_builder.add_edge("youtube_download", "generation_question")
        #graph_builder.add_edge("generation_question", "search_naver_news")
        graph_builder.add_edge("generation_question", "search_Tavily") 
        #graph_builder.add_edge("search_naver_news", "fake_news_detection")
        graph_builder.add_edge("search_Tavily", "fake_news_detection")
        graph_builder.add_edge("fake_news_detection", END)

        graph_builder.set_entry_point("youtube_download")
        graph = graph_builder.compile()

        return graph