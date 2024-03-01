from fastapi import FastAPI, Request, UploadFile
from fastapi.params import File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from tempfile import NamedTemporaryFile

from main import parce_file

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.file.read())
        filename = parce_file(file_name=tmp_file.name)
        return FileResponse(filename, filename=filename, media_type="application/octet-stream")

