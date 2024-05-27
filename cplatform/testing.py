# 9. Testing with WebSocket Client
# As mentioned previously, you can use a simple WebSocket client to test:

# python
# Co/py code
import asyncio
import json
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws/chat/"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"message": "Hello, WebSocket!"}))
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(test_websocket())
# Run the script above to ensure your WebSocket is functioning correctly. If everything is configured correctly, you should see a response indicating the WebSocket connection is working.

# If you encounter any issues, make sure to check the Django server logs for any errors and ensure Redis is running properly.