
MINING_REWARD = 10

genesis_block = {
        'prev_hash': ' ', 
        'index': 0, 
        'transactions': []
    }
blockchain = [genesis_block]
open_txns = []
owner = 'Mo'
participants = {'Mo'}



def get_last():
    if len(blockchain) <  1:
        return None
    return blockchain[-1]


def add_txn(recipient, sender=owner, amt=1.0):
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amt': amt
    }

    if verify_txn(transaction):
        open_txns.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False



def mine_block():
    last_block= blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_txn = {
        'sender': 'MINING',
        'recipient': owner,
        'amt': MINING_REWARD
    }
    copied_txns = open_txns[:]
    copied_txns.append(reward_txn)
    block = {
        'prev_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_txns
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
    return True

def verify_txns():
    return all([verify_txn(tx) for tx in open_txns])

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


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
        amount_sent = 0
        amount_received = 0
        for tx in tx_sender:
            if len(tx) > 0:
                amount_sent += tx[0]
        for tx in tx_recipient:
            if len(tx) > 0:
                amount_received += tx[0]
        return amount_received - amount_sent
        

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
    print(get_balance('Mo'))
    

print('done')
