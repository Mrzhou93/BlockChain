# -*- encoding=utf-8 -*-
# -*- Author:Bill_zzq -*-
# -*- Environment: python 2.7 -*-
# -*- Sofeware: PyCharm -*-
# -*- Data: 2018/01/08

import hashlib
import uuid
import time


class Block(object):
    def __init__(self, timestamp=time.time(), data=None, previousHash=None, nonce=0):
        # 生成一个唯一的ID
        self.index = uuid.uuid4().hex
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculateHash()

    def calculateHash(self):
        return hashlib.sha256(str(self.index).encode('utf-8') + str(self.previousHash).encode('utf-8')
                              + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8')
                              + str(self.nonce).encode('utf-8')).hexdigest()

    def mineBlock(self, difficulty):
        """
        挖矿的结果是求出一个前difficulty位为0的hash
        """
        while str(self.hash)[0: difficulty] != str('0' * difficulty):
            self.nonce += 1
            self.hash = self.calculateHash()


class BlockChain(object):
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 4

    @staticmethod
    def createGenesisBlock():
        return Block("08/01/2018", "Genesis block", "0")

    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        # newBlock.hash = newBlock.calculateHash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            if currentBlock.hash != currentBlock.calculateHash():
                return False

            if currentBlock.previousHash != previousBlock.hash:
                return False

        return True


if __name__ == '__main__':
    blockchain = BlockChain()
    print "Mining Block 1..."
    blockchain.addBlock(newBlock=Block("1"))
    print blockchain.chain[1].hash

    print "Mining Block 2..."
    blockchain.addBlock(newBlock=Block("2"))
    print blockchain.chain[2].hash

    #print blockchain.isChainValid()
    #blockchain.chain[2].data = '100'
    #print blockchain.isChainValid()
