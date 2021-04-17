import hashlib
import json
from textwrap import dedent
from uuid import uuid4
# import jsonpickle
# from flask import Flask
from urllib.parse import urlparse
# from Crypto.PublicKey import RSA
# from Crypto.Signature import *
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

    def minePendingTransactions(self, miner):

        lenPT = len(self.pendingTransactions);
        if(lenPT <= 1):
            print("Not enough transactions to mine! (Must be > 1)")
            return False;
        else:
            for i in range(0, lenPT, self.blockSize):

                end = i + self.blockSize;
                if i >= lenPT:
                    end = lenPT;

                transactionSlice = self.pendingTransactions[i:end];

                newBlock = Block(len(self.chain), transactionSlice);
                # print(type(self.getLastBlock()));

                hashVal = self.getLastBlock().hash;
                newBlock.prev = hashVal;
                newBlock.mineBlock(self.difficulty);
                self.chain.append(newBlock);
            print("Mining Transactions Success!");

            payMiner = Transaction("Miner Rewards", miner, self.minerRewards);
            self.pendingTransactions = [payMiner];
        return True;

    def addTransaction(self, sender, receiver, amt, keyString, senderKey):
        keyByte = keyString.encode("ASCII")
        senderKeyByte = senderKey.encode("ASCII")

        key = RSA.import_key(keyByte)
        senderKey = RSA.import_ley(senderKeyByte)

        if not sender or not receiver or not amt:
            return False

        transaction = Transaction(sender, receiver, amt)

        transaction.signTransaction(key, senderKey);

        if not transaction.isValidTransaction():
            print("transaction error 2");
            return False;
        self.pendingTransactions.append(transaction);
        return len(self.chain) + 1;

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
        while self.hash[0:difficulty] != hashPuzzle:
            self.nonse += 1
            self.hash = self.calculateHash();
            print("Nonse:", self.nonse);
            print("Hash Attempt:", self.hash);
            print("Hash We Want:", hashPuzzle, "...");
            print("");
        print("BLOCK MINED! Nonse to Solve Proof of Work: ", self.nonse)
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

    def calculateHash(self):
        hashString = self.sender + self.receiver + \
            str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()

        return hashlib.sha256(hashEncoded).hexdigest()

    def signTransaction(self, key, senderKey):
        if(self.hash != self.calculateHash()):
            print("transaction tampered error");
            return False;
        #print(str(key.publickey().export_key()));
        #print(self.sender);
        if(str(key.publickey().export_key()) != str(senderKey.publickey().export_key())):
            print("Transaction attempt to be signed from another wallet");
            return False;

        #h = MD5.new(self.hash).digest();

        pkcs1_15.new(key);

        self.signature = "made";
        #print(key.sign(self.hash, ""));
        print("made signature!");
        return True;
