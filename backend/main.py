from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# from langserve import add_routes
# from models * agent_executor

app = FastAPI()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)