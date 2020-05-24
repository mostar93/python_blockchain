from collections import OrderedDict
from printable import Printable

class Transaction(Printable):
    def __init__(self, sender, recipient, amt):
        self.sender = sender
        self.recipient = recipient
        self.amt = amt
    
    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amt', self.amt)])

