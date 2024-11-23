from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path
# from langserve import add_routes
# from models * agent_executor

app = FastAPI()

DOWNLOAD_DIR = Path("./downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True) # 디렉토리가 없으면 생성

class VideoDownloadRequest(BaseModel):
    url: str

@app.get("/")
def direct_root_path():
    return {"message": "안녕하세요"}

# 이후 agent_executor 생성하면 여기에 연결
# class Input(BaseModel):
#     chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
#         ...,
#         extra={"widget": {"type": "chat", "input": "input", "output": "output"}},
#     )
#
# class Output(BaseModel):
#     output: Any
#
# add_routes(
#     app,
#     agent_executor.with_types(input_type=Input, output_type=Output).with_config(
#         {"run_name": "agent"}
#     ),
# )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)