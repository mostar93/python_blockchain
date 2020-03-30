genesis_block = {
        'prev_hash': ' ', 
        'index': 0, 
        'transactions': []
    }
blockchain = [genesis_block]
open_txns = []
owner = 'Mo'


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
    open_txns.append(transaction)



def mine_block():
    last_block= blockchain[-1]
    hashed_block = '-'.join([str(last_block[key]) for key in last_block])
    print(hashed_block)

    block = {
        'prev_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': open_txns
    }
    blockchain.append(block)

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


def validate_chain():
    # block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index-1]:
            is_valid = True
        else:
            is_valid = False
            break
        # block_index += 1
    return is_valid


while True:
    print('Please Choose')
    print('1: Add a new txn value')
    print('2: Mine new block')
    print('3: output blockchain blocks')
    print('h: manipulate the chain')
    print('q: Quit')
    user_choice = get_user_input()
    if user_choice == '1':
        tx_data = get_txn_amt()
        recipient, amt = tx_data

        add_txn(recipient, amt=amt)
        print(open_txns)

    elif user_choice == '2':
        mine_block()
    elif user_choice == '3': 
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = 2
    elif user_choice == 'q':
        break
    else:
        print('not valid input')
    print('choice registered')
    # if not validate_chain():
    #     print_blockchain_elements()
    #     print('invalid blockchain')
    #     break
    

print('done')
