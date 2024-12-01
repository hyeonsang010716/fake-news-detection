from typing import List, TypedDict, Annotated
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage

class State(TypedDict):
    youtube_link : str
    youtube_content : str
    keywords : List[str]
    naver_news : str                     
    response: str                              
    
    
class Sentence(BaseModel):
    text: List[str] = Field(
        description="A list of core keyword extracted from the text."
    )