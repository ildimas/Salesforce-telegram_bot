from fastapi import FastAPI, Request
from services.async_dict import AsyncDict

app = FastAPI()

message_dict = AsyncDict()

# FastAPI route to receive data
@app.post("/message_recieve")
async def receive_data(request: Request):
    body = await request.json()
    user_id = body.get("id")
    message = body.get("message")
    await message_dict.set(user_id, message)
    # print(await message_dict.values())
    return {"status": "Data received"}
    
