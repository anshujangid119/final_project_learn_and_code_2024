import json
import os,time

def send_message(sock, command, data):
    message = json.dumps({'command': command, 'data': data})
    sock.send(message.encode())

    response = sock.recv(8096).decode()
    if not response:
        raise ValueError("Received empty response from server")

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON response: {response}")

def logout(obj):
    obj.close()
    time.sleep(2)
    os.system('cls')
    time.sleep(1)
    print("Logout Successfully")