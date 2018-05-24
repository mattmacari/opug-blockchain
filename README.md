# opug-blockchain
Omaha Python User Group Lightning Talk - Blockchain Building Blocks

The original presentation can be found [here](http://bit.ly/2GGm0co)

## Quickstart

#### Install dev environment
```sh
    git clone git@github.com:mattmacari/opug-blockchain.git
    pyenv virtualenv blockchain
    pyenv activate blockchain
    pip install pipenv
    pipenv install --dev
```

#### Running unit tests
```sh
    pyenv activate blockchain
    python -m unittest -v
```

#### Running local server
```sh
    pyenv activate blockchain
    python ./blockchain/server.py
```

#### Running server example (while local server is running)
```sh
    pyenv activate blockchain
    python ./example/server_example.py
```

## Code Example

Suppose that Alice and Bob are planning a run, and  they want to keep a public record of their conversation since Bob's
friend Charles has a habit of hacking their cell phones and changing text message conversations.

```python
from blockchain import BlockChain
from blockchain import new_wallet

# Wallet generation and generate transaction.

bc = BlockChain()

# Alice's wallet to send messages.
alice_wallet = new_wallet()

# Bob's wallet to send messages.
bob_wallet = new_wallet()

alice_msg = alice_wallet.generate_transaction(message='Hello, Bob!  What time shall we meet for our run?',
                                              sender='Alice',
                                              recipient='Bob')

bc.append(alice_msg)

bob_msg = bob_wallet.generate_transaction(message='Hello, Alice!',
                                          sender='Bob',
                                          recipient='Alice')

bc.append(bob_msg)

bob_msg2 = bob_wallet.generate_transaction(message='I am planning a run tomorrow at 9:00.  Are you free?',
                                          sender='Bob',
                                          recipient='Alice')
                                          
bc.append(bob_msg2)

# Charles attempts to modify the message block chain.
blk = bc.chain[hash]
message = blk.transaction['transaction']['message']

blk.transaction['transaction'].update({'message': message.replace('9:00', '11:00')})

bc.chain[hash] = blk

bc.validate_chain()

```

## Background

* Blockchains are defined as a "continuously growing list of records called blocks, which are linked and secured
 using cryptography." [1]
 
## References
     [1]: https://en.wikipedia.org/wiki/Blockchain
     
## Resources
    [1]: http://adilmoujahid.com/posts/2018/03/intro-blockchain-bitcoin-python/
