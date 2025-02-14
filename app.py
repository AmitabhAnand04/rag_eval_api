import uvicorn
import multiprocessing as mp
from fastapi import FastAPI
from apis.file_process import file_router


app = FastAPI()
app.include_router(router=file_router)


if __name__ == "__main__":
    try:
        mp.set_start_method("spawn", force=True)
        uvicorn.run(app = app, host = "127.0.0.1", port = 8080)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")