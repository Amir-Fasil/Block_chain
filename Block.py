import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
class Block:

    def __init__(self, index = 0, previous_hash = 0):  # genesis block

        self.current_hash = None
        self.index = index  # This too
        self.transaction = [] # you need to add these transactions
        self.previous_hash = previous_hash # Add this using the block cahin current value
        self.nonce = 0   # I am going to implement this using the first 2 hexadigits since I have 16 possiblities


    def to_dict(self):

        return {

            "index" : self.index,
            "previous_hash" : self.previous_hash,
            "transactions" : self.transaction,
            "nonce": self.nonce
        }
    
    def add_transaction(self, valid_transaction):
        for transaction in valid_transaction:
            self.transaction.append(transaction)
        
    
    def create_hash(self):

        obj_data = json.dumps(self.to_dict(), sort_keys = True)    # This one create hash for the whole block
        obj_hash = SHA256.new(obj_data.encode("utf-8"))
        self.current_hash = obj_hash

        return obj_hash             
    
    # The way I defined the nonce is that what value would give 0 in the hash if the nonce value is hash together
    def find_nonce(self):

        obj_hash = self.create_hash()
        first_value = str(obj_hash.hexdigest())[0]

        while first_value != str(0):
            self.nonce += 1
            obj_hash = self.create_hash()
            first_value = str(obj_hash.hexdigest())[0]

        return self.nonce
    
    def assign_prev_hash(self, hash):
        self.previous_hash = hash

    def update_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    

            
            

