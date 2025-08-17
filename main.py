from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database.dbops import *
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

@app.get("/api/ammendments/all")
async def get_all():
    ammendments = await get_all_ammendments()
    print(ammendments)

@app.post("/api/ammendments/create")
async def create_amendment_endpoint(title: str, description: str, number: int, date_proposed: str):
    try:
        await create_amendment(title, description, number, date_proposed)
        return {"status": "success", "message": "Amendment created successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.get("/stocks")
async def contact():
    return FileResponse("/static/stocks.html")
