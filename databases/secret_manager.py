import base64
import json

path = r"C:\Users\anshu.jangid\cred_file.txt"
def read_cred_file(path):
    key = ""
    with open(path, 'r') as file:
        for line in file:
            key += line
    return key

def decode_and_parse_json(encoded_str):
    decoded_json = base64.b64decode(encoded_str).decode('utf-8')
    secret = json.loads(decoded_json)
    return secret

key = read_cred_file(path)
secrets = decode_and_parse_json(key)
