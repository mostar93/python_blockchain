from time import time
from printable import Printable

class Block(Printable):
    def __init__(self, index, prev_hash, txns, proof, time=time()):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = time
        self.txns = txns
        self.proof = proof

   
