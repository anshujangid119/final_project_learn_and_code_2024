import socket
import json

def send_message(sock, command, data):
    message = json.dumps({'command': command, 'data': data})
    sock.send(message.encode())
    response = sock.recv(1024).decode()
    return json.loads(response)

def client_program(username, password):
    host = '127.0.0.1'
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    auth_prompt = client_socket.recv(1024).decode()
    print(json.loads(auth_prompt))

    auth_response = send_message(client_socket, 'AUTH', {'username': username, 'password': password})
    print(auth_response)

    if auth_response['command'] == 'AUTH_SUCCESS':
        role = auth_response['data']['role']
        print(f"Logged in as {role}")

        if role == 'admin':
            while True:
                action = input("Enter command (ADD_USER/LOGOUT): ")
                if action == 'ADD_USER':
                    new_username = input("New username: ")
                    new_password = input("New password: ")
                    new_role = input("New role (admin/chef/employee): ")
                    add_user_response = send_message(client_socket, 'ADD_USER', {'username': new_username, 'password': new_password, 'role': new_role})
                    print(add_user_response)
                elif action == 'LOGOUT':
                    send_message(client_socket, 'LOGOUT', {})
                    break
        elif role == 'chef':
            while True:
                action = input("Enter command (ADD_DISH/LOGOUT): ")
                if action == 'ADD_DISH':
                    dish_name = input("Dish name: ")
                    ingredients = input("Ingredients: ")
                    add_dish_response = send_message(client_socket, 'ADD_DISH', {'name': dish_name, 'ingredients': ingredients})
                    print(add_dish_response)
                elif action == 'LOGOUT':
                    send_message(client_socket, 'LOGOUT', {})
                    break
        elif role == 'employee':
            while True:
                action = input("Enter command (LOGOUT): ")
                if action == 'LOGOUT':
                    send_message(client_socket, 'LOGOUT', {})
                    break
    else:
        print("Authentication failed")

    client_socket.close()

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    client_program(username, password)
