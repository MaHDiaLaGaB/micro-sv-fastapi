import pathlib
import uuid
import io
from functools import lru_cache
from fastapi import FastAPI, Depends, Request, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings


# ---- config ------
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = ".env"


@lru_cache()
def get_sittings():
    return Settings()


DEBUG = get_sittings().debug

# ------ end config ------

# ------ tell fast api to search for templates and uploaded files ------
BASE_DIR = pathlib.Path(__file__).parent
PHOTO_DIR = BASE_DIR / "media"
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ------ end templates ---------


# ------ routs views --------
@app.get("/", response_class=HTMLResponse)
# settings here to import the settings from the config settings
async def root(request: Request, settings: Settings = Depends(get_sittings)):
    return templates.TemplateResponse("home.html", {'request': request, 'abc': 123})


@app.post("/")
def home_view():
    return {"hello": "My first fast API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# upload file bt http post
@app.post("/img-echo/", response_class=FileResponse)
async def img_echo(file: UploadFile = File(...), settings: Settings = Depends(get_sittings)):
    file_bytes_str = io.BytesIO(await file.read())
    file_name = pathlib.Path(file.filename)
    file_type = file_name.suffix  # jpg or .txt
    destination = PHOTO_DIR / f"{uuid.uuid1()}{file_type}"
    with open(str(destination), 'wb') as out:
        out.write(file_bytes_str.read())
    return file
