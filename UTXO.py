class UTXO:

    def __init__(self, scriptPubKey, amount, transaction_id = None, output_index = None):

        self.transaction_id = transaction_id
        self.output_index = output_index # in the regular type of transaction there will be two output UTXO the spent one and unspent one
        self.scriptPubKey = scriptPubKey  # This is just the public key this UTXo belongs to
        self.amount = amount

    def check_amount(self, needed_amount):
        if self.amount > needed_amount:
            return True
        else:
            return False

    def get_amount(self):
        return self.amount
    
    def get_PubKey(self):
        return self.scriptPubKey
    







