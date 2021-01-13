import random
import string
import json

def get_new_id():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(token_length))

f = open('config_file.JSON')
data = json.load(f)
token_length = data["postgresql"]["token_length"]