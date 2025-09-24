# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine


from openai import OpenAI
import os
from fastapi import FastAPI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
@app.get('/')
def root():
    return {'message': 'Semantic Engine API running'}
    
def _openai_llm(prompt: str) -> str:
    """
    Simple wrapper using gpt-4 or gpt-3.5
    """
    resp = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400
    )
    return resp.choices[0].message.content