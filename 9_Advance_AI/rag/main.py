from fastapi import BackgroundTasks,File,UploadFile,Body
from fastapi import status,HTTPException 
from fastapi  import FastAPI
from extract import pdf_text_extractor
from typing import Annotated
import uvicorn
from upload import save_file

app = FastAPI()

@app.post("/upload")
async def file_upload_controller(
    file :  Annotated[UploadFile , File(description= "A file read as UploadFile")],
    bg_text_processor : BackgroundTasks,
):
    
    if file.content_type != "application/pdf":
          raise HTTPException(
            detail=f"Only uploading PDF documents are supported",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    

    try:
        filepath = await save_file(file)
        #bg_text_processor.add_task(pdf_text_extractor, filepath)
   
    except Exception as e:
        raise HTTPException(
            detail=f"An error occurred while saving file - Error: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    return {"filename" : file.filename, "message": "File uploaded successfully"}



if __name__ == "__main__":
    uvicorn.run("main:app",port=8000, reload=True)