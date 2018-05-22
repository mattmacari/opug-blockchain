"""
Wallet is the client application that can be run from a local machine.

Would talk to the server.
"""
import json

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from cached_property import cached_property

from .base import Base


def generate_keypair(bits=2048):
    """
    Returns a keypair of the specificed bits.
    :param bits: bits length for RSA keypair.
    :return: keypair dictionary
    :rtype: dict
    """
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(bits, random_gen)
    public_key = private_key.publickey()
    return {
        'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    }


def new_wallet(private_key=None, bits=2048):
    """
    Returns a wallet object using the private key if provided, else generates a new private key pair.
    :param private_key: Private key string
    :return: Wallet for the user
    :rtype: Wallet
    """
    if not private_key:
        private_key = generate_keypair(bits=bits).get('private_key')
    return Wallet(private_key=private_key)


class Wallet(Base):
    """
    Base wallet implementation that exposes the ability for the client to sign a transaction (or message) using
    `sign_transaction()` and to generate a transaction using `generate_transaction()`
    """

    def __init__(self,
                 private_key):
        """
        :param private_key: RSA private key generated by the client.
        :ptype private_key: str
        """
        self.private_key = private_key
        self.rsa_private_key = RSA.importKey(binascii.unhexlify(private_key))

    def sign_transaction(self, **transaction):
        """
        Signs a transaction with the user's private key and returns a key for signing.
        :return: signature string based on transaction and private key
        :rtype: str
        """
        signer = PKCS1_v1_5.new(self.rsa_private_key)
        h = SHA.new(self._json_str(**transaction).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

    def generate_transaction(self, **transaction):
        """
        Generates a new transaction to add to the block chain.
        :param transaction: key-value pairs of transaction
        :return: transaction with signature
        :rtype: dict
        """
        return {'transaction': transaction,
                'signature': self.sign_transaction(**transaction),
                'public_key': self.public_key}

    @cached_property
    def public_key(self):
        """
        Returns the public key for the wallet's private key.
        :return: public key
        :rtype: str
        """
        return binascii.hexlify(self.rsa_private_key.publickey().exportKey(format='DER')).decode('ascii')
