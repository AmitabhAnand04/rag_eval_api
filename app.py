import uvicorn
from fastapi import FastAPI
from apis.file_process import file_router


app = FastAPI()
app.include_router(router=file_router, prefix="/v1")


if __name__ == "__main__":
    try:
        uvicorn.run("app:app", host = "127.0.0.1", port = 8080, reload=True)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")