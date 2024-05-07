from glob import glob
from typing import List, Any, Dict
import json
import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from schemas.Course import Course
from retry import retry


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@retry(delay=2)
def read_in_all_courses(limit: int = -1) -> List[Course]:
    """
    This function will read in all the data from the 'data' folder containing JSON files.
    Make sure to Parse them into Courses using Pydantic Schema's.
    Append them to the all_courses list and return that list."""

    all_courses = []
    for course in glob(f'data/*.{os.environ.get("file_format", "json")}')[:limit]:
        try:
            with open(course, 'r') as f:
                courseParsed = json.load(f)
                key = list(courseParsed.keys())[0]
                all_courses.append(Course(**courseParsed[key]))
        except Exception as e:
            print('Error with file', course)
    return all_courses

all_courses = read_in_all_courses(-1)

@app.get("/")
async def root():
    return {"message": "I am working correctly!"}

@app.get("/docker_test")
async def docker_test():
    return os.environ

@app.get('/mct/courses')
async def get_all_courses():
    return all_courses

def read_json_config(file_path: str) -> Dict[str, Any]:
    """Reads a JSON configuration file and returns its content."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Please make sure you are using the /mnt/src/config/config.json path!")
        raise HTTPException(status_code=404, detail="File not found. Read the logs for more info")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON")

@app.get("/config")
async def get_config():
    """Endpoint to return the content of the config file."""
    config_path = "/mnt/src/config/config.json"
    return read_json_config(config_path)