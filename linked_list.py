import hashlib
class Block:
    def __init__(self, index, timestamp, content, previous_hash):
      self.index = index
      self.timestamp = timestamp
      self.content = content
      self.previous_hash = previous_hash
      self.hash = self.calc_hash()
   
    def calc_hash(self):
      sha = hashlib.sha256()
      sha.update(str(self.index).encode('utf-8') + 
                 str(self.timestamp).encode('utf-8') + 
                 str(self.content).encode('utf-8') + 
                 str(self.previous_hash).encode('utf-8'))
      return sha.hexdigest()
      
M4BlockChain = []

from datetime import datetime

# create first block and start BlockChain
def create_genesis_block():
    return Block(0, datetime.now(), "Genesis Block", "0")
    
M4BlockChain.append(create_genesis_block())

# write a function `next_block` to generate a block
# based on last_block / keep tracking last_block

def next_block(last_block):
    
    # generate block
    content_i = "this is block "
    s_ind = str(last_block.index+1)
     
    next_node = Block(last_block.index+1, datetime.now(), content_i+ s_ind , last_block.hash)
    return next_node
    pass
    
# append 5 blocks to the blockchain
def app_five(block_list):
    
    last_block = M4BlockChain[len(M4BlockChain)-1]
    i = 0
    for i in range (0,5):
        next_node = next_block(last_block)
        block_list.append(next_node)
        last_block = next_node
        i += 1
    pass