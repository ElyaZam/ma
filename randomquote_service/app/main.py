import os
import uvicorn
from fastapi import FastAPI, status
import requests


app = FastAPI()



@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/")
async def get_random_quote():
    response = requests.get("https://api.quotable.io/random")
    if response.status_code == 200:
        quote_data = response.json()
        return f"{quote_data['content']} - {quote_data['author']}"
    else:
        return "Failed to retrieve quote"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
