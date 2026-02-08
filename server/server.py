from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

tools = {
    "add": add,
}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            tool_name = data.get("tool")
            params = data.get("params")

            if tool_name in tools:
                result = tools[tool_name](**params)
                await websocket.send_json({"result": result})
            else:
                await websocket.send_json({"error": "Tool not found"})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
