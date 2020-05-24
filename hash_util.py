import hashlib
import json

def hash_string(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['txns'] = [tx.to_ordered_dict() for tx in hashable_block['txns']]
    return hash_string(json.dumps(hashable_block, sort_keys=True).encode())