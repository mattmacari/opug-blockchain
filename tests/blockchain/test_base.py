import unittest
import hashlib
import json
from datetime import datetime
from freezegun import freeze_time

from blockchain.base import (Block,
                             BlockChain,
                             DEFAULT_HASH,
                             BlockVerificationError)


@freeze_time('2006-12-03 19:25')
class BlockTestCase(unittest.TestCase):

    def setUp(self):
        self.tx = {'spam': 1, 'eggs': 2}
        self.previous_hash = hashlib.new(
            DEFAULT_HASH, 'previous_hash'.encode('utf-8')).hexdigest()
        self.timestamp = str(datetime.timestamp(datetime(year=2006,
                                                         day=3,
                                                         month=12,
                                                         hour=19, minute=25)
                                                ).as_integer_ratio()[0])

    def test_generate_hash(self):
        blk = Block(transaction=self.tx,
                    previous_hash=self.previous_hash)
        block_hash = hashlib.new(DEFAULT_HASH, b''.join([
            json.dumps(self.tx,
                       sort_keys=True).encode('utf-8'),
            self.previous_hash.encode('utf-8'),
            self.timestamp.encode('utf-8')
        ])).hexdigest()
        self.assertEqual(blk.hash_block(), block_hash)

    def test_verify_hash(self):
        blk = Block(transaction=self.tx,
                    previous_hash=self.previous_hash)
        self.assertIsNone(blk.verify_hash())
        with self.assertRaises(BlockVerificationError):
            blk.transaction.update({'test': '405'})
            blk.verify_hash()


@freeze_time('2006-12-03 19:25')
class BlockChainTestCase(unittest.TestCase):

    def setUp(self):
        self.tx = {'spam': 1, 'eggs': 2}
        self.bc = BlockChain()

    def test_block_factory(self):
        blk = self.bc.block_factory()
        self.assertIs(blk, Block)

    def test_append(self):
        self.bc.append(self.tx)
        self.assertEqual(len(self.bc.chain), 2)

    def test_last_block(self):
        self.bc.append(self.tx)
        self.assertEqual(self.bc.last_block.transaction,
                         self.tx)
