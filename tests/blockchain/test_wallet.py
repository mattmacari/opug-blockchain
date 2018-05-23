import unittest

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii

from blockchain.wallet import generate_keypair, new_wallet, Wallet


class KeyPairTestCase(unittest.TestCase):

    def test_generate_keypair_ret_values(self):
        # Checks to make sure that `generate_keypair` returns a dict with `private_key` and `public_key`
        keypair = generate_keypair()
        self.assertIn('private_key', keypair)
        self.assertIn('public_key', keypair)
        self.assertIsInstance(keypair, dict)

    def test_generate_keypair_keys(self):
        message = 'Message that needs to be signed correctly.'.encode('utf-8')
        digest = SHA256.new()
        digest.update(message)

        keypair = generate_keypair()
        private_key = RSA.importKey(binascii.unhexlify(keypair['private_key']))

        signer = PKCS1_v1_5.new(private_key)
        sig = signer.sign(digest)

        verifier = PKCS1_v1_5.new(private_key.publickey())
        verified = verifier.verify(digest, sig)

        self.assertTrue(verified, 'Signature verification failed.  Public key and Private key not a pair.')


class WalletFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.kp = generate_keypair()

    def test_new_wallet(self):
        wallet = new_wallet(private_key=self.kp.get('private_key'))
        self.assertIsInstance(wallet, Wallet, 'new_wallet() should return Wallet instance.')
        self.assertEqual(self.kp.get('private_key'), wallet.private_key)
        self.assertEqual(self.kp.get('public_key'), wallet.public_key)


class WalletTestCase(unittest.TestCase):

    def setUp(self):
        self.kp = generate_keypair()

    def test_generate_transaction(self):
        wallet = new_wallet(private_key=self.kp.get('private_key'))
        transaction = {'a': 1, 'b': 2}
        signed_transaction = wallet.generate_transaction(**transaction)
        self.assertIsInstance(signed_transaction, dict, 'generate_transaction() should return dict')
        self.assertIn('transaction', signed_transaction, 'generate_transaction() should return dict with '
                                                         'transaction attribute')
        self.assertIn('signature', signed_transaction, 'generate_transaction() should return dict with '
                                                        'signature attribute')