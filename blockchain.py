from  functools import reduce
import hashlib
import json
import pickle


from hash_util import hash_string, hash_block
from block import Block
from transaction import Transaction

MINING_REWARD = 10

blockchain = []

open_txns = []

owner = 'Mo'



def load_data():
# only handle errors that you can't predict or avoid. Only wrap code that will fail in runtime. Value errors dont need to be handled usually
    global blockchain
    global open_txns
    try:
        with open('blockchain.txt', mode='rb') as f:
            # file_content = pickle.loads(f.read())
       
            # blockchain = file_content['chain']
            # open_txns = file_content['ot']

            ''' Below is an example of using JSON to convert data to a string, store to a file, and then reading from that file back to our blockchain
            However, it JSON doesnt distinguish between OrderedDict and normal dict so it messes up the proof for chain validation

            Pickling does keep the OrderedDict and because it is closer to machine language (it is binary) therefore the steps required to load data is 
            greatly reduced '''
        
            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amt']) for tx in block['txns']]
                # converted_tx = [OrderedDict(
                # [('sender', tx['sender']), ('recipient', tx['recipient']), ('amt', tx['amt'])]) for tx in block['transactions']]
                updated_block = Block(block['index'],block['prev_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_txns = json.loads(file_content[1])
            updated_txns = []
            for tx in open_txns:
                updated_txn = Transaction(tx['sender'], tx['recipient'], tx['amt'])
                updated_txns.append(updated_txn)
            open_txns = updated_txns
    except (IOError, IndexError):
        genesis_block = Block(0, '', [], 100, 0)

        blockchain = [genesis_block]
        open_txns = []
    # except ValueError:
    #     print('there is a value error')
    finally:
        print('Cleanup')
    



load_data()



def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.prev_hash, [tx.__dict__ for tx in block_el.txns], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(savable_chain))
            f.write('\n')
            savable_txns = [tx.__dict__ for tx in open_txns]
            f.write(json.dumps(savable_txns))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_txns
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving Failed')

def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
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
    transaction = Transaction(sender, recipient, amt)

    if verify_txn(transaction):
        open_txns.append(transaction)
        # participants.add(sender)
        # participants.add(recipient)
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
    reward_txn = Transaction('MINING', owner, MINING_REWARD)
    copied_txns = open_txns[:]
    copied_txns.append(reward_txn)
    block = Block(len(blockchain), hashed_block, copied_txns, proof,)

    blockchain.append(block)
    return True

def get_txn_amt():
    tx_recipient = input('Enter recipient name: ')
    tx_amt =  float(input('input amount: '))
    return (tx_recipient, tx_amt)


def get_user_input():
    user_input = input("your choice: ")
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print('outputing block ')
        print(block)

def verify_txn(txn):
    sender_balance = get_balance(txn.sender)
    return sender_balance >= txn.amt


def validate_chain():
# enumerate takes every block in the chain and gives it an index allowingfor efficient for loop functionality
# and how range selector works 

    for (index, block) in enumerate(blockchain): 
        if index == 0:
            continue
        if block.prev_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.txns[:-1], block.prev_hash, block.proof):
            return False

    return all([verify_txn(tx) for tx in open_txns])




def get_balance(participant, user_choice= 'x'):
# using list comprehension to create a list IN PLACE of all transactions in a blockchain for that user as well as lambda functions

    tx_sender = [[tx.amt for tx in block.txns if tx.sender == participant] for block in blockchain]
    tx_recipient = [[tx.amt for tx in block.txns if tx.recipient == participant] for block in blockchain]
    open_txn_sender = [tx.amt for tx in open_txns if tx.sender == participant] 
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
   
    print('5: check txn validity')
    print('9: get sent amounts')
    print('10: get received amounts')
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
    elif user_choice == '5':
        if verify_txns():
            print('all txns are valid')
        else:
            print('there are invalid txns')
    elif user_choice == '9' or user_choice == '10':
        print(get_balance( 'Mo', user_choice))

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
