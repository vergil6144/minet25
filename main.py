from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os 

app = FastAPI(title="ExMinet")

static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/ammendments")
async def read_x():
    return FileResponse("static/ammendments.html")

@app.get("/contact")
async def contact():
    return FileResponse("/static/contact.html")

@app.get("/stocks")
async def contact():
    return FileResponse("/static/stocks.html")