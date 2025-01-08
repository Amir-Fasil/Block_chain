from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


# Just for insight I also implemented how RSA key Generation works

def generate():
    keys = RSA.generate(256)
    private_key = keys.export_key()
    public_key = keys.public_key().export_key()

    return private_key, public_key

def create_signature(message, private_key):

    priv_key = RSA.import_key(private_key) # Here I change the PEM format to a suitable object
    message_hash = SHA256.new(message.encode("UTF-8")) # Here I hashed the message using a cryptographic hash function
    signature = pkcs1_15.new(priv_key).sign(message_hash)

    return signature

def verification(message, signature, public_key):

    flag = True
    pub_key = RSA.import_key(public_key)

    try:
        pkcs1_15.new(pub_key).verify(message, signature)
    except(ValueError, TypeError):
        flag = False

    return flag

string = "My name amir"
hash_value = SHA256.new(string.encode("UTF-8"))
print(hash_value.digest())
string_hash = str(hash_value.hexdigest())
print(string_hash[0:5])