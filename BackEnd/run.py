# run_server.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
