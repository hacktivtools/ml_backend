from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
def greet(name: str = "Stranger"):
    return JSONResponse(content={"message": f"Hello, {name}"})