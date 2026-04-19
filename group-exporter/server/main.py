from fastapi import FastAPI, Response, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
import json

app = FastAPI()

origins = [
    "http://intra.epitech.eu",
    "https://intra.epitech.eu",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGES_FOLDER = "images"
JSON_FILE = ".groups.json"

class Module(BaseModel):
    code: str

class Project(BaseModel):
    name: str

class GroupPage(BaseModel):
    module: Module
    project: Project
    content: list

def get_json_file_contents() -> str:
    with open(JSON_FILE, "r") as f:
        return f.read()

def write_json(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.post("/group-page")
def group_page(group: GroupPage, response: Response):
    try:
        content = {}
        try:
            content = json.loads(get_json_file_contents())

            if group.module.code in content and group.project.name in content[group.module.code]:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"status": "Already exists"}
            content[group.module.code][group.project.name] = group.content
        except Exception as e:
            content[group.module.code] = {group.project.name: group.content}

        write_json(content)
        return {"status": "Success"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "Failure", "error": e}

@app.get("/groups")
def groups():
    return json.loads(get_json_file_contents())

@app.post("/image")
def upload_image(file: UploadFile, response: Response):
    Path(IMAGES_FOLDER).mkdir(parents=True, exist_ok=True)

    if file.filename in os.listdir(IMAGES_FOLDER):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "Already exists"}

    with open(f"{IMAGES_FOLDER}/{file.filename}", "wb+") as f:
        f.write(file.file.read())
        return {"status": "Success"}

@app.get("/images")
def list_images():
    if not os.path.exists(IMAGES_FOLDER):
        return []
    return os.listdir(IMAGES_FOLDER)
