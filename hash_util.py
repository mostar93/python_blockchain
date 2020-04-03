import hashlib
import json

def hash_string(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    return hash_string(json.dumps(block, sort_keys=True).encode())