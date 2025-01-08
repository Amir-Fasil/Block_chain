import UTXO

class Transaction:

    def __init__(self, type, output_UTXOs, data, input_UTXO = None, signature = None):
        self.type = type
        self.signature = signature
        self.input = input_UTXO
        self.output = output_UTXOs
        self.data = data

    def get_message(self):
        return self.data
    
    def get_sigature(self):
        return self.signature
    
    def get_PubKey(self):
        return self.input.get_PubKey()
        