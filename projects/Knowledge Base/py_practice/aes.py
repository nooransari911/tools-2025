import aes_cipher
from aes_cipher import DataEncrypter, DataDecrypter


data = "Hello world"
pwd  = ["test_pwd1"]
salt = ["test_salt1"]

data_encrypter = DataEncrypter(
)
data_encrypter.Encrypt(data, pwd, salt)
enc_data = data_encrypter.GetEncryptedData()

print ("Data: ", data)
print ("Passwords: ", pwd)
print ("Salts: ", salt)
print ("Encrypted data: ", enc_data)




data_decrypter = DataDecrypter (
)
data_decrypter.Decrypt (enc_data, pwd)
dec_data = data_decrypter.GetDecryptedData()


# print ("Data: ", data)
# print ("Passwords: ", pwd)
# print ("Salts: ", salt)
print ("\n\nDecrypted data: ", dec_data)

