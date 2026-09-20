from fastapi import FastAPI , Request, Response , UploadFile, File , HTTPException
from fastapi.responses import Response

app = FastAPI()

@app.post("/highlight")
async def highlight(
    context_doc: UploadFile = File(..., description="The context document"),
    target_doc: UploadFile = File(..., description="The target document to be highlighted")
    ):
        if context_doc.content_type != "application/pdf" or target_doc.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Both files must be PDF files")
            
        return Response(content=target_bytes, media_type="application/pdf")

