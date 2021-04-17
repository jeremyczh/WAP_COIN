from wap_coin import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

bc = Blockchain()

block_1 = Block(0, [])
bc.addBlock(block_1)

block_2 = Block(1, [])
bc.addBlock(block_2)

block_3 = Block(2, [])
bc.addBlock(block_3)
print(bc)


print(block_1.calculateHash())
block_1.mineBlock(4)
print(block_1.hash)
print(block_1.calculateHash())

# transaction = Transaction("Jeremy", "John", 1)
# bc.pendingTransactions.append(transaction)
# bc.pendingTransactions.append(transaction)

# bc.minePendingTransactions("Miner1")



pp.pprint(bc.chainJSONencode())