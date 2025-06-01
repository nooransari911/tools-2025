import aes_cipher
from aes_cipher import DataEncrypter, DataDecrypter, Pbkdf2Sha512Default, Pbkdf2Sha512


data = "Hello world"
pwd  = ["test_pwd1", "test_pwd2"]
salt = ["test_salt1", "test_salt2"]

data_encrypter = DataEncrypter(
    Pbkdf2Sha512(1024 * 1024)
)
data_encrypter.Encrypt(data, pwd, salt)
enc_data = data_encrypter.GetEncryptedData()

print ("Data: ", data)
print ("Passwords: ", pwd)
print ("Salts: ", salt)
print ("Encrypted data: ", enc_data)




data_decrypter = DataDecrypter (
    Pbkdf2Sha512 (1024 * 1024)
)
data_decrypter.Decrypt (enc_data, pwd)
dec_data = data_decrypter.GetDecryptedData()


# print ("Data: ", data)
# print ("Passwords: ", pwd)
# print ("Salts: ", salt)
print ("\n\nDecrypted data: ", dec_data)

