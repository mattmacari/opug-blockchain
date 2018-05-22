import hashlib
from datetime import datetime
import json
from collections import OrderedDict


DEFAULT_HASH = 'sha256'


class BlockVerificationError(Exception):
    pass


class BlockChainVerificationError(Exception):
    pass


class Block(object):
    _hash = DEFAULT_HASH

    def __init__(self,
                 transaction=None,
                 previous_hash=None):
        """

        :param transaction: transaction data that is stored in the block chain
        :param previous_hash: the hash of the previous block
        """
        super(Block, self).__init__()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.timestamp = str(datetime.timestamp(datetime.now()).as_integer_ratio()[0]).encode('utf-8')
        self.hash = self.hash_block()

    def hash_block(self):
        """
        Hashes the transaction, previous_hash, timestamp together.
        :return: block hash
        """
        transaction_str = json.dumps(self.transaction,
                                     sort_keys=True).encode('utf-8')
        return hashlib.new(self._hash, b''.join([transaction_str,
                                                self.previous_hash.encode('utf-8'),
                                                self.timestamp])).hexdigest()

    def __str__(self):
        return 'Block(hash={}, previous_hash={}, transaction={})'.format(
            self.hash,
            self.previous_hash,
            self.transaction
        )

    def __repr__(self):
        return self.__str__()

    def verify_hash(self):
        if self.hash != self.hash_block():
            raise BlockVerificationError('Unable to verify hash for {}'.format(self))


class BlockChain(object):
    """
    Class implementing the block chain.
    """

    def __init__(self,
                 hash=DEFAULT_HASH,
                 block_class=Block):
        super(BlockChain, self).__init__()
        self.hash = hash
        self.block_class = block_class
        self.chain = OrderedDict()
        self.timestamp = str(datetime.timestamp(datetime.now()).as_integer_ratio()[0]).encode('utf-8')
        self.chain_hash = hashlib.new(hash, self.timestamp).hexdigest()
        # Add first block
        b = self.block_factory()(transaction={}, previous_hash=self.chain_hash)
        self.chain[b.hash] = b

    def __len__(self):
        return len(self.chain)

    def __getitem__(self, item):
        return self.chain[item]

    def append(self, transaction):
        block = self.block_factory()
        new_block = block(transaction=transaction,
                          previous_hash=self.last_block.hash)
        self.chain.update({new_block.hash: new_block})

    def block_factory(self):
        bc = self.block_class
        bc._hash = self.hash
        return bc

    @property
    def last_block(self):
        return self.chain.get(next(reversed(self.chain)))

    def validate_chain(self):
        curr_indx = 1
        prev_block = self.last_block
        while curr_indx < len(self.chain):
            try:
                prev_block.verify_hash()
            except BlockVerificationError:
                raise BlockChainVerificationError()
            try:
                prev_block = self.chain[prev_block.previous_hash]
            except KeyError:
                raise BlockChainVerificationError('Unable to find previous hash: {}'.format(prev_block.hash))
            curr_indx += 1
        prev_block = self.chain[prev_block.hash]
        if prev_block.previous_hash != self.chain_hash:
            raise BlockChainVerificationError('Block chain hash: {}, previous hash: {}'.format(
                self.chain_hash,
                prev_block.previous_hash
            ))
