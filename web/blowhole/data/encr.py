from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)
cry = Fernet(key)
print(cry)
d = cry.encrypt("lovellllllllllllllllllllllllllllllllll".encode())
print(d)
l=cry.decrypt(d)
print(l)