from typing import List, TypedDict, Annotated
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage

class State(TypedDict):
    youtube_link : str
    youtube_content : str
    youtube_header : str
    youtube_summary_content : str
    keywords : List[str]
    search_results : List[str]                     
    response: str                              
    
    
class Sentence(BaseModel):
    texts: List[str] = Field(
        description="A list of sentences that collectively include all core information from the text."
    )