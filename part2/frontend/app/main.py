from fastapi import FastAPI, Request, Form, APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import requests
import json
import os, time

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

API_HOST = os.environ.get('API_HOST', 'api')
API_PORT = os.environ.get('API_PORT', '8080')


# backend for courses
@app.get("/")
def index(request: Request):
    print("Index request from : ", request.client)
    try:
        r = requests.get(f'http://{API_HOST}:{API_PORT}/mct/courses')
        data = r.json()
        return templates.TemplateResponse('index.html', 
                        context={'title': 'Courses', 'request': request, 'courses': data})

    except requests.exceptions.ConnectionError as err:
        print('Did you fill in the correct API_HOST environment value?')
        print(err)
        error_message = f"Can not connect to API @ '{API_HOST}:{API_PORT}' Try some other Env variables for API_HOST and API_PORT?"
        return templates.TemplateResponse('index.html', 
                        context={'title': 'ERROR', 'request': request, 'error': error_message })