from blockchain import BlockChain

bc = BlockChain()
bc.append({'t': 1, 'x': 2})
bc.append({'t': 1, 'x': 2, 'abc': 1})

hash = bc.last_block.hash

bc.append({'t': 1, 'x': 2, 'cbs': 2})

bc.validate_chain()

blk = bc.chain[hash]

blk.transaction.update({'abc': 4})

bc.chain[hash].transaction.update({'abc': 4})
