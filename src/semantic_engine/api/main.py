from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def root():
    return {'message': 'Semantic Engine API running'}