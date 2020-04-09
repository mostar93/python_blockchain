from  functools import reduce
import hashlib
import json
import pickle
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

def load_data():
    try:
        with open('blockchain.p', mode='rb') as f:
            file_content = pickle.loads(f.read())
            global blockchain
            global open_txns
            blockchain = file_content['chain']
            open_txns = file_content['ot']

            ''' Below is an example of using JSON to convert data to a string, store to a file, and then reading from that file back to our blockchain
            However, it JSON doesnt distinguish between OrderedDict and normal dict so it messes up the proof for chain validation

            Pickling does keep the OrderedDict and because it is closer to machine language (it is binary) therefore the steps required to load data is 
            greatly reduced '''
        

            # blockchain = json.loads(file_content[0][:-1])
            # updated_blockchain = []
            # for block in blockchain:
            #     updated_block = {
            #         'prev_hash': block['prev_hash'],
            #         'index': block['index'],
            #         'proof':block['proof'],
            #         'transactions': [OrderedDict(
            #     [('sender', tx['sender']), ('recipient', tx['recipient']), ('amt', tx['amt'])]) for tx in block['transactions']]
            #     }
            #     updated_blockchain.append(updated_block)
            # blockchain = updated_blockchain
            # open_txns = json.loads(file_content[1])
            # updated_txns = []
            # for tx in open_txns:
            #     updated_txn = OrderedDict(
            #     [('sender', tx['sender']), ('recipient', tx['recipient']), ('amt', tx['amt'])]) 
            #     updated_txns.append(updated_txn)
            # open_txns = updated_txns
    except IOError:
        print('file not found')
    except ValueError:
        print('there is a value error')
    finally:
        print('Cleanup')
    



load_data()



def save_data():
    with open('blockchain.p', mode='wb') as f:
        # f.write(json.dumps(blockchain))
        # f.write('\n')
        # f.write(json.dumps(open_txns))
        save_data = {
            'chain': blockchain,
            'ot': open_txns
        }
        f.write(pickle.dumps(save_data))

def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
# This function uses a while loop to try numbers our until the hash algorithm (aka valid proof) results in a hash that begins with two 00's 

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
        save_data()
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
# Explain how enumerate works and how range selector works 

    for (index, block) in enumerate(blockchain): 
        if index == 0:
            continue
        if block['prev_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['prev_hash'], block['proof']):
            return False

    return all([verify_txn(tx) for tx in open_txns])




def get_balance(participant, user_choice= 'x'):
# explain how list comprehension works as well as lambda functions

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
            save_data()
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
