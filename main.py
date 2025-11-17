from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from book_gen import create_interior_pdf, create_simple_cover
from io import BytesIO
import zipfile, os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate(title: str = Form(...), author: str = Form(""), pages: int = Form(24), sample_text: str = Form("")):
    interior = create_interior_pdf(title, author, pages, sample_text)
    cover = create_simple_cover(title, author)

    mem = BytesIO()
    z = zipfile.ZipFile(mem, "w")
    safe_title = title.replace(" ", "_")
    z.writestr(f"{safe_title}-interior.pdf", interior)
    z.writestr(f"{safe_title}-cover.jpg", cover)
    z.close()
    mem.seek(0)

    return StreamingResponse(mem, media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={safe_title}.zip"}
    )
