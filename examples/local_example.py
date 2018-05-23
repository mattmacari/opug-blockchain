from blockchain import BlockChain
from blockchain import new_wallet

# Generate a local blok chain.

bc = BlockChain()

# Alice's wallet to send messages.
alice_wallet = new_wallet()

# Bob's wallet to send messages.
bob_wallet = new_wallet()

alice_msg = alice_wallet.generate_transaction(message='Hello, Bob!  What time shall we meet for our run?',
                                              sender='Alice',
                                              recipient='Bob')

print('appending {} to chain.'.format(alice_msg))

bc.append(alice_msg)

bob_msg = bob_wallet.generate_transaction(message='Hello, Alice!',
                                          sender='Bob',
                                          recipient='Alice')

print('appending {} to chain.'.format(bob_msg))

bc.append(bob_msg)

bob_msg2 = bob_wallet.generate_transaction(message='I am planning a run tomorrow at 9:00.  Are you free?',
                                           sender='Bob',
                                           recipient='Alice')

print('appending {} to chain.'.format(bob_msg2))

bc.append(bob_msg2)

# Charles attempts to modify the message block chain.
hash = bc.last_block.hash
blk = bc.chain[hash]
message = blk.transaction['transaction']['message']

blk.transaction['transaction'].update({'message': message.replace('9:00', '11:00')})

bc.chain[hash] = blk

bc.validate_chain()
