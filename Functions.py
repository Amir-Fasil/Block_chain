import UTXO
import Block_Chain
import Block
import numpy as np 
import Transaction
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from queue import Queue
from fastapi import Request


####################################################################################################################################
##################################################### User Functions ###############################################################

def generate():
    """When creating account in the first place you will be asigned a public key and a private key and the amount of 
    UTXos you will buy."""

    keys = RSA.generate(256)
    private_key = keys.export_key()
    public_key = keys.public_key().export_key()

    return private_key, public_key

def create_signature(message, private_key):

    """ This function creates a signature from the transaction message(data) and the private key
    This will be used to make sure the transaction is valid. The idea behaind it is that only the person 
    that has the private key could create that signature and it differ from transaction to transaction making it more reliable.
    And it can be checked using the public key """

    priv_key = RSA.import_key(private_key) # Here I change the PEM format to a suitable object
    message_hash = SHA256.new(message.encode("UTF-8")) # Here I hashed the message using a cryptographic hash function
    signature = pkcs1_15.new(priv_key).sign(message_hash)

    return signature

def check_amount_in_utxo(request: Request, PubKey, needed_amount):

    """This function checks whether the sender has teh money or not to make the transaction
    Normally we check whether the sender has the money by checking the previous transactions
    and he has the money or not in those transactions, but what i did here is that I stored the utxos as in a dictionary where
    the key is the public key and the value is the UTXO this will make updateing and searching easier in the dictionary """

    spec_utxo = request.app.block_chain.return_specific_utxo(PubKey)
    boolean = spec_utxo.check_amount(needed_amount)

    return spec_utxo, boolean


# This can easily be done by the user
def create_transaction(request: Request, input_Privkey, input_PubKey, output_PubKey, needed_amount):

    """This function create transaction and this is done by the users. the only condition is 
    the user has  to have the money. if th user has the money the transaction will proceed and then added to the pending transactions Queue"""

    input_UTXO, boolean = check_amount_in_utxo(input_PubKey, needed_amount)
    if boolean:

        unspent_amount = input_UTXO.get_amount() - needed_amount
        spent_amount = needed_amount
        rng = np.default_rng()
        transaction_id = rng.random()
        output_utxo_1 = UTXO(input_PubKey, unspent_amount, transaction_id, 0)
        output_utxo_2 = UTXO(output_PubKey, spent_amount, transaction_id, 1)
        output_UTXO = [output_utxo_1, output_utxo_2]
        request.app.block_chain.add_UTXO({input_PubKey: output_utxo_1, output_PubKey: output_utxo_2})
        data = f"{input_PubKey} transfered {needed_amount} to {output_PubKey}"
    else:
        print("The transaction can't proceeed because you don't have enough money")
    

    signature = create_signature(data, input_Privkey)
    transaction = Transaction("Regular", output_UTXO, data, input_UTXO, signature)
    request.app.transaction_queue.put(transaction)

####################################################################################################################################
##################################################### Miner Functions #############################################################

def verification(message, signature, public_key):

    """This function is run by the miner, It verifies the signature is signed by the sender. 
    Note: this asymmetical property of crypography allows Encription and Digital signature.

    Encription: message encipted by a public key can only be decrepted by the cooresponding 
                private key making encription possible

    Digital Signature: message signed by the private key is gurateed that is is signed by the given public key owner 
                        making sure a unique sigature for every message, and it can be checked using the public key"""
    
    flag = True
    pub_key = RSA.import_key(public_key)

    try:
        pkcs1_15.new(pub_key).verify(message, signature)
    except(ValueError, TypeError):
        flag = False

    return flag

def verify_transaction():

    """This function verify the transaction that are in pending transaction queue and
    add them to a new verified transaction list where they will be added to the block"""
    # load the recent transaction from the pending queue
    # I have decided to include 2 transaction in a single block

    verified_transaction = []

    while len(verified_transaction) == 2:

        transaction = transaction_queue.get()
        message = transaction.get_message()
        signature = transaction.get_signature()
        PubKey = transaction.get_PubKey()
        verification(message, signature, PubKey)
        verified_transaction.append(transaction)

    return verified_transaction


def mine_block(request, miner_PubKey, amount): # amount because it changes over time

    """Here what I did is that when the miner verify the transaction and find the nonce value that will make 
    my first hexadecimal value 0 (This is my proof of work) the miner will be rewarded some utxo and this function will 
    add that into the UTXo set, However we must notice the miner first must verify teh transactions and find the nonce value"""

    miner_utxo = UTXO(miner_PubKey, amount)
    request.app.block_chain.add_UTXO({miner_PubKey: miner_utxo})


# Creating a block and mining one is closly related matter

def create_block(request: Request):
    """This function creates a block that is verified and add it to the block chain. 
    Here I uses a linked list for the block chain"""

    # This will create new block and append it to the block chain

    verified_transaction = verify_transaction()
    new_block = Block()
    new_block.add_transaction(verified_transaction)
    request.app.block_chain.append(new_block)
    new_block.create_hash()
    new_block.find_nonce()







    


    