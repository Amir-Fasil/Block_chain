from Block import Block

class Block_chain():

    genesis = Block()
    # my Genesis block has no transaction
    genesis.create_hash()
    genesis.find_nonce()

    UTXO_set = {}

    def __init__(self):

        self.header = Block_chain.genesis
        self.current_block = self.header 
        self.previous_hash = None 

    # Appending a block to a block chain I first started with a Genesis block and 
    # everytime you want to append  you will take the current block hash and index and use it on the 
    # block you are using.

    def get_header(self):
        return self.header
    
    
    def append(self, block):

        """ for the first append what will happen is we take the previous_hash argument of the block and 
            assign it to the header and change the current_block, and it update the index variable to 1 plus
            of the previous block's """
        
        prev_hash = self.current_block.create_hash()
        index = self.current_block.get_index()
        block.assign_prev_hash(prev_hash)
        block.update(index + 1)
        self.current_block = block

        # I need to add a feature that confims or some how validate when a block is added
        # and it create a new block when a block is added #nope
    
    def create_block():

        """When miners validate a block and append it to the block chain 
            they get to create an new block where they could write the first transaction """
        

    def add_UTXO(self, **kwargs):
        Block_chain.UTXO_set.update(**kwargs)
        return True
    

    def return_specific_utxo(self, PubKey):
        spec_utxo = Block_chain.UTXO_set.get(PubKey)
        return spec_utxo
    
    def get_current_block(self):
        return self.current_block