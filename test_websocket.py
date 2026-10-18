from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


with client.websocket_connect("/ws/chat") as websocket:

    websocket.send_text("What is the notice period policy?")

    response = websocket.receive_json()

    print("\n==============================")
    print("WEBSOCKET TEST RESULT")
    print("==============================")
    print(response)