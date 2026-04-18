from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import json

app = FastAPI()

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
