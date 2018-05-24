from blockchain import Block

transaction = {
    'sender': 'Alice',
    'recipient': 'Bob',
    'message': 'Hello, Bob!'
}

blk = Block(transaction, previous_hash='previous-hash')

print(blk)

print(blk.to_json())