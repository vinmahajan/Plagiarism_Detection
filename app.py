from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.plagiarism_checker import plagiarism_checker
from dotenv import load_dotenv
import os

load_dotenv()

# AUTH_KEYS = json.loads(os.getenv('AUTH_KEYS'))
AUTH_KEY1 = os.getenv('AUTH_KEY1')
AUTH_KEY2 = os.getenv('AUTH_KEY2')

app = FastAPI()

templates = Jinja2Templates(directory="templates")

max_text_len = 1000

def validate_api_key(api_key: str):
    if api_key != AUTH_KEY1 and api_key != AUTH_KEY2:
        raise HTTPException(status_code=403, detail="Invalid API key")
    else:
        return True

def validate_input_text(text: str):
    if len(text)>max_text_len:
        raise HTTPException(status_code=403, detail="Input Text limit exceeded.")
    else:
        return True

class TextInput(BaseModel):
    text: str
    api_key: str



@app.post("/api/check-plagiarism")
async def plagiarism_api(input_data: TextInput):

    validate_api_key(input_data.api_key)
    validate_input_text(input_data.text)
    result=plagiarism_checker(input_data.text)

    return result




@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, api_key: str = Form(...), text: str = Form(...)):
    # Check if API key is valid
    if api_key != AUTH_KEY1 and api_key != AUTH_KEY2:
        result = "Invalid API Key"
    else:
        # Process the text
        result=plagiarism_checker(text)
    
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

