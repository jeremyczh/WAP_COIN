import hashlib
import json
from textwrap import dedent
from uuid import uuid4
# import jsonpickle
# from flask import Flask
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from time import time
from datetime import datetime
import requests


class Blockchain (object):
    def __init__(self):
        self.chain = [self.addGenesisBlock()]
        self.pendingTransactions = []
        self.difficulty = 4
        self.minerRewards = 50
        self.blockSize = 10

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        if len(self.chain) > 0:
            block.prev = self.getLastBlock().hash
        else:
            block.prev = "GENSIS"
        self.chain.append(block)

    def addGenesisBlock(self):
        tArr = []
        tArr.append(Transaction('me', 'you', 1))
        genBlock = Block(0, tArr)
        genBlock.prev = 'GENESIS'

        return genBlock

    def addTransaction(self, sender, receiver, amt, keyString, senderKey):
        keyByte = keyString.encode('ASCII')
        senderKeyByte = senderKey.encode('ASCII')

        key = RSA.import_key(keyByte)
        senderKey = RSA.import_key(senderKeyByte)

        if not sender or not receiver or not amt:
            return False
        
        transaction = Transaction(sender, receiver, amt)

        transaction.signTransaction(key, senderKey)

        if not transaction.isValidTransaction():
            print("transaction error: not signed")
            return False
        self.pendingTransactions.append(transaction)
        return len(self.chain)+1

    def minePendingTransactions(self):
        
        lenPending = len(self.pendingTransactions)
        for i in range(0, lenPending, self.blockSize):


    def generateKeys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open("private.pem", "wb")
        file_out.write(private_key)

        public_key = key.publickey().export_key()
        file_out = open("receiver.pem", "wb")
        file_out.write(public_key)
        
        return key.publickey().export_key().decode('ASCII')

    def chainJSONencode(self):
        blockArrJSON = []
        for block in self.chain:
            blockJSON = {}
            blockJSON['hash'] = block.hash
            blockJSON['blockid'] = block.block_id
            blockJSON['prev'] = block.prev
            blockJSON['time'] = block.time

            transactionsJSON = []
            tJSON = {}
            for transaction in block.transactions:
                tJSON['time'] = transaction.time
                tJSON['sender'] = transaction.sender
                tJSON['receiver'] = transaction.receiver
                tJSON['amt'] = transaction.amt
                tJSON['hash'] = transaction.hash
                transactionsJSON.append(tJSON)
            blockJSON['transactions'] = transactionsJSON

            blockArrJSON.append(blockJSON)

        return blockArrJSON


class Block (object):

    def __init__(self, block_id, transactions):
        self.block_id = block_id
        self.transactions = transactions
        self.time = time()
        self.prev = ''
        self.nonse = 0
        self.hash = self.calculateHash()
        

    def __str__(self):
        return 'hash: ' + self.hash + '\nprevious block: ' + self.prev + '\n'

    def mineBlock(self, difficulty):
        arr = []
        for i in range(0, difficulty):
            arr.append(i+1)

        arrStr = map(str, arr)
        hashPuzzle = ''.join(arrStr)
        start_time = time()
        while self.hash[0:difficulty] != hashPuzzle:
            self.nonse += 1
            self.hash = self.calculateHash()
            # print("Nonse:", self.nonse);
            # print("Hash Attempt:", self.hash);
            # print("Hash We Want:", hashPuzzle, "...");
            # print("");
        print("BLOCK MINED! Nonse to Solve Proof of Work: ", self.nonse)
        print("Time taken: ", time()-start_time)
        return True

    def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash

        hashString = str(self.time) + hashTransactions + self.prev + str(self.block_id) + str(self.nonse)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()

        return hashlib.sha256(hashEncoded).hexdigest()


class Transaction (object):
    def __init__(self, sender, receiver, amt):
        self.sender = sender
        self.receiver = receiver
        self.amt = amt
        self.time = time()
        self.hash = self.calculateHash()
        self.signature = None

    def calculateHash(self):
        hashString = self.sender + self.receiver + \
            str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()

        return hashlib.sha256(hashEncoded).hexdigest()

    def signTransaction(self, key, senderKey):
        if self.hash != self.calculateHash():
            print("transaction error: could not be verified")
            return False

        if str(key.publickey().export_key()) != str(senderKey.publickey().export_key()):
            print("transaction error: attempt from another wallet")
            return False

        self.signature = "signed"
        return True

    def isValidTransaction(self):
        if self.hash != self.calculateHash():
            return False
        if self.sender == self.receiver:
            return False
        if self.sender == 'Miner Reward':
            return True
        if not self.signature == "signed":
            return False
        return True