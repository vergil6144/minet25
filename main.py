from fastapi import FastAPI,HTTPException,UploadFile,File,Form,Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database.dbops import *
from pathlib import Path
import hashlib
import os 

class AmendmentCreate(BaseModel):
    title: str
    description: str
    number: int
    date_proposed: str


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
@app.get("/tab")
async def read_x():
    return FileResponse("static/tab.html")

@app.get("/contact")
async def contact():
    return FileResponse("static/contact.html")

@app.get("/api/ammendments/all")
async def get_all():
    ammendments = await get_all_ammendments()
    if not ammendments:
        raise HTTPException(status_code=404, detail="No amendments found")
    return ammendments

@app.get("/api/documents/all")
async def get_all_docs():
    documents = await get_all_documents_for_user(1)
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return documents

@app.post("/api/ammendments/create")
async def create_amendment_endpoint(amendment: AmendmentCreate):
    try:
        await create_amendment(
            amendment.title, 
            amendment.description, 
            amendment.number, 
            amendment.date_proposed
        )
        return {"status": "success", "message": "Amendment created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
class FileUploadResponse(BaseModel):
    status: str
    message: str
    document_id: int
    filename: str

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/api/documents/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    user_id: int = Form(...),
):
    """
    Upload a file and store it in the database
    
    - **file**: The file to upload (sent in request body)
    - **title**: Document title
    - **document_type**: Type of document (constitution, amendment, law, memo, etc.)
    - **description**: Optional description
    """
    try:
       
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
       
        file_content = await file.read()
        file_size = len(file_content)
        
        
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 50MB")
        
        # Generate secure filename
        safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._-")
        file_hash = hashlib.md5(file_content).hexdigest()[:8]
        unique_filename = f"{file_hash}_{safe_filename}"
        
        # Save file to disk (optional - for backup/serving)
        file_path = UPLOAD_DIR / unique_filename
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        
        # Also store file path reference for backup
        await upload_document(
            user_id=user_id,
            file_path=str(file_path),
            filename=safe_filename,
            mime_type=file.content_type or "application/octet-stream"
        )


        
        return FileUploadResponse(
            status="success",
            message="File uploaded successfully",
            document_id="102",
            filename=safe_filename,
            file_size=file_size
        )
        
    except HTTPException:

        raise
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/stocks")
async def contact():
    return FileResponse("static/stocks.html")

@app.get("/locker")
async def locker():
    return FileResponse("static/locker.html")

@app.get("/login")
async def login():
    return FileResponse("static/login.html")

@app.get("/profile")
async def profile():
    return FileResponse("static/profile.html")

def strip_bearer_token(auth_header: str) -> str:
    """Strip 'Bearer ' prefix from authorization header"""
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " (7 characters)
    return auth_header

@app.get("/api/users/token-verify")
async def verify_user(request: Request):
    try:
        user = await get_user_by_token(strip_bearer_token(request.headers.get("authorization"))) # Example user ID
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@app.get("/api/users/create")
async def create():
    try:
        await create_user(
            username="Aditya Garg",
            email="sexmquee@sexmquee.com",
            age=12,
            gender="male",
            password_hash="demo2",
        )
        return {"status": "success", "message": "User created successfully"}
    except Exception as e:
        print(e)

@app.post("/api/users/verifyqr")
async def verify_qr(image: UploadFile = File(...)):
    try:
        img_content = await image.read()
        user_data = await parse_user_qr(img_content)
        
        if user_data and user_data.get('success'):
            return {"status": "success", "user_data": user_data}
        else:
            raise HTTPException(status_code=400, detail="Invalid QR code")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR code verification failed: {str(e)}")


@app.post("/api/transactions/attempt")
async def attemptTrans(
    reciever_id: int = Form(...),
    sender_id: int = Form(...),
    amount: float = Form(...),
    Type: str = Form(...)
):
    try:
        if not reciever_id or not sender_id or not amount or not Type:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        success = await attemptTransaction(reciever_id, sender_id, amount, Type)
        if success:
            return {"status": "success", "message": "Transaction successful"}
        else:
            raise HTTPException(status_code=500, detail="Transaction failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction error: {str(e)}")

@app.post("/api/users/login")
async def login_user(username: str = Form(...), password: str = Form(...)):
    try:
        token = await verify_login(username, password)
        if not token:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"status": "success", "message": "Login successful", "token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/api/transactions/all")
async def testtt(user_id:int):
    print(user_id)
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    id = user_id
    try:
        trans = await get_transactions_by_user(id)
        if not trans:
            raise HTTPException(status_code=404, detail="User not found")
        transProc = processTransactions(trans,id)
        return transProc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@app.get("/api/transaction")
async def get_transaction_by_idapi(transaction_id: int,user_id: int):
    if not transaction_id:
        raise HTTPException(status_code=400, detail="Transaction ID is required")
    
    try:

        transaction = await get_transaction_by_id(transaction_id)

        sender = await get_user_by_id(transaction['sender_id'])
        receiver = await get_user_by_id(transaction['receiver_id'])

       

        if not transaction or not sender or not receiver:
            raise HTTPException(status_code=404, detail="Transaction not found")

        trans_response = {
            "id": transaction['id'],
            "amount": transaction['amount'],
            "date": transaction['date'],
            "description": transaction['transaction_type'],
        }

        if transaction['sender_id'] == user_id:
            trans_response['target'] = receiver['username']
            trans_response['type'] = "credit"

        if transaction['receiver_id'] == user_id:
            trans_response['target'] = sender['username']
            trans_response['type'] = "debit"
        
        return trans_response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching transaction: {str(e)}")


def processTransactions(transactions,user_id):
    res = []
    for transaction in transactions:
        trans = {
            "id": transaction['id'],
            "date": transaction['date'],
            "desc": transaction['transaction_type'],
        }
        if transaction['sender_id'] == user_id:
            trans['target'] = transaction['receiver_id']
            trans['amount'] = -transaction['amount']
            trans['Type'] = "credit"
        
        if transaction['receiver_id'] == user_id:
            trans['target'] = transaction['sender_id']
            trans['amount'] = transaction['amount']
            trans['Type'] = "debit"
        res.append(trans)
    return res
       