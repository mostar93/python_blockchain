from  functools import reduce
import hashlib
from collections import OrderedDict

from hash_util import hash_string, hash_block

MINING_REWARD = 10

genesis_block = {
        'prev_hash': ' ', 
        'index': 0, 
        'transactions': [],
        'proof': 100
    }
blockchain = [genesis_block]
open_txns = []
owner = 'Mo'
participants = {'Mo'}



def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_txns, last_hash, proof):
        proof += 1
    return proof

def get_last():
    if len(blockchain) <  1:
        return None
    return blockchain[-1]


def add_txn(recipient, sender=owner, amt=1.0):
    # transaction = {
    #     'sender': sender, 
    #     'recipient': recipient, 
    #     'amt': amt
    # }

    transaction = OrderedDict(
        [
            ('sender', sender), 
            ('recipient', recipient), 
            ('amt', amt)
            ]
    )

    if verify_txn(transaction):
        open_txns.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False



def mine_block():
    last_block= blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    # reward_txn = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amt': MINING_REWARD
    # }

    reward_txn = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amt', MINING_REWARD)])
    copied_txns = open_txns[:]
    copied_txns.append(reward_txn)
    block = {
        'prev_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_txns,
        'proof': proof
    }
    blockchain.append(block)
    return True

def get_txn_amt():
    tx_recipient = input('Enter recipient name: ')
    tx_amt =  float(input('input amount: '))
    return (tx_recipient, tx_amt)


def  get_user_input():
    user_input = input("your choice: ")
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print('outputing block ')
        print(block)

def verify_txn(txn):
    sender_balance = get_balance(txn['sender'])
    return sender_balance >= txn['amt']


def validate_chain():
    for (index, block) in enumerate(blockchain): 
        if index == 0:
            continue
        if block['prev_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['prev_hash'], block['proof']):
            return False

    return all([verify_txn(tx) for tx in open_txns])




def get_balance(participant, user_choice= 'x'):
    tx_sender = [[tx['amt'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    tx_recipient = [[tx['amt'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    open_txn_sender = [tx['amt'] for tx in open_txns if tx['sender'] == participant] 
    tx_sender.append(open_txn_sender)
  
    if user_choice == '9':
        return tx_sender
    elif user_choice == '10':
        return tx_recipient
    else:
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    
        return amount_received - amount_sent

def verify_txns():
    """Verifies all open transactions."""
    return all([verify_txn(tx) for tx in open_txns])      

while True:
    print('Please Choose')
    print('1: Add a new txn value')
    print('2: Mine new block')
    print('3: output blockchain blocks')
    print('4: output participants')
    print('5: check txn validity')
    print('9: get sent amounts')
    print('10: get received amounts')
    print('h: manipulate the chain')
    print('q: Quit')
    user_choice = get_user_input()
    if user_choice == '1':
        tx_data = get_txn_amt()
        recipient, amt = tx_data

        if add_txn(recipient, amt=amt):
            print('txn success')
        else:
            print('txn failed')
        print(open_txns)

    elif user_choice == '2':
        if mine_block():
            open_txns = []
    elif user_choice == '3': 
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_txns():
            print('all txns are valid')
        else:
            print('there are invalid txns')
    elif user_choice == '9' or user_choice == '10':
        print(get_balance( 'Mo', user_choice))
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'prev_hash': ' ', 
                'index': 0, 
                'transactions': [{'sender': 'Chris', 'recipient': 'Mo', 'amt': 100.00}]
            }
    elif user_choice == 'q':
        break
    else:
        print('not valid input')
    print('choice registered')
    if not validate_chain():
        print_blockchain_elements()
        print('invalid blockchain')
        break
    print('Balance of {}: {:6.2f}'.format('Mo', get_balance('Mo')))
    

print('done')
