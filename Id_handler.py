import random
import string

def get_new_id(lenght):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(lenght))