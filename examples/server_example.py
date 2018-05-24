from blockchain import BlockChain
from blockchain import new_wallet

# Generate a local blok chain.

bc = BlockChain()

# Alice's wallet to send messages.
alice_wallet = new_wallet(node='http://localhost:5000')

# Bob's wallet to send messages.
bob_wallet = new_wallet(node='http://localhost:5000')

bob_wallet.submit_transaction(message='Hello, Alice!',
                              sender='Bob',
                              recipient='Alice')

alice_wallet.submit_transaction(message='Hello, Bob!  What time shall we meet for our run?',
                                              sender='Alice',
                                              recipient='Bob')