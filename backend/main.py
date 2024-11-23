from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# from langserve import add_routes

# from models * agent_executor


app = FastAPI()

origins = [
    "http://localhost:5173",
]

# app.include_router(user_router.router)

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)