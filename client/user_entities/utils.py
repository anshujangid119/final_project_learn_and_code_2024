import json


def send_message(sock, command, data):
    message = json.dumps({'command': command, 'data': data})
    sock.send(message.encode())

    response = sock.recv(1024).decode()
    if not response:
        raise ValueError("Received empty response from server")

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response: {response}")