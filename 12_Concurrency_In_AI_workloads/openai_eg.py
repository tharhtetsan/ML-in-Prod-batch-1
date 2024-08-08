from openai import AsyncOpenAI,  OpenAI
from fastapi import FastAPI, Body
import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()

sync_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()

@app.post("/sync")
def sync_generate_text(prompt: str):

    completion = sync_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return completion.choices[0].message.content

@app.post("/async")
async def async_generate_text(prompt: str ):
    completion = await async_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return completion.choices[0].message.content


if __name__=="__main__":
    uvicorn.run("openai_eg:app",port = 8000,reload = True)