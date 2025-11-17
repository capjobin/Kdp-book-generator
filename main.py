
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import shutil
from book_gen import generate_book

app = FastAPI()

@app.post("/generate")
async def generate(title: str = "My Book"):
    output_zip = "output.zip"
    generate_book(title, output_zip)
    return FileResponse(output_zip, filename=output_zip)
