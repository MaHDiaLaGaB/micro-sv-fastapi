import pathlib
import uuid
import io
from PIL import Image
from functools import lru_cache
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings
from fastapi import (
    FastAPI, Depends,
    Request, File,
    UploadFile, HTTPException)


# ---- config ------
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


DEBUG = get_settings().debug

# ------ end config ------

# ------ tell fast api to search for templates and uploaded files ------
BASE_DIR = pathlib.Path(__file__).parent
PHOTO_DIR = BASE_DIR / "media"
PHOTO_DIR.mkdir(exist_ok=True)
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ------ end templates ---------


# ------ routs views --------
@app.get("/", response_class=HTMLResponse)
# settings here to import the settings from the config settings
async def root(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {'request': request, 'abc': 123})


@app.post("/")
def home_view():
    return {"hello": "My first fast API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# upload file bt http post
@app.post("/img-echo/", response_class=FileResponse)
async def img_echo(file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="invalid endpoint", status_code=400)
    file_bytes_str = io.BytesIO(await file.read())
    try:
        image = Image.open(file_bytes_str)
    except:
        raise HTTPException(detail="invalid image", status_code=400)
    file_name = pathlib.Path(file.filename)
    file_type = file_name.suffix  # jpg or .txt
    destination = PHOTO_DIR / f"{uuid.uuid1()}{file_type}"
    image.save(destination)
    return destination
