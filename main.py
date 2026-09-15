# importing modules #

from cryptography import fernet
import hashlib
import csv
import re

# defining variables #

with open("config.txt", "r") as file:
    data = file.readlines()
    FirstTime = eval(data[0])
    if not FirstTime:
        master = data[1]
    file.close()

# defining functions #


def CreateMasterKey():
    Key = input("  [?] Please input a master key for the password manager : \n     ")
    if not ValidateKey(Key):
        CreateMasterKey()
    else:
        with open("config.txt", "w") as cnf:
            cnf.writelines(["False\n", ToSha256(Key)])
            cnf.close()


def ValidateKey(key):
    valid = True

    if len(key) < 12:
        print("  [-] The key has to be at least 12 characters")
        valid = False
    if not re.search(r'[a-z]', key):
        print("  [-] The key must contain lowercase characters")
        valid = False
    if not re.search(r'[A-Z]', key):
        print("  [-] The key must contain uppercase characters")
        valid = False
    if not re.search(r'[0-9]', key):
        print("  [-] The key must contain numerical characters")
        valid = False
    if not re.search(r'[!@#$%^&*()\-_=+{}:;,<>.]', key):
        print("  [-] The key must contain special characters")
        valid = False
    return valid


def ToSha256(key):
    key_bytes = key.encode("utf-8")
    sha256 = hashlib.sha256()
    sha256.update(key_bytes)
    hashed = sha256.hexdigest()
    return hashed


def Authenticate():
    key = input("  [?] Please enter the master key : \n     ")
    if ToSha256(key) == master:
        print("  [*] Login Success")
    else:
        print("  [-] Login Failure : Wrong Password")
        print("  [*] Quitting now")
        quit()


def LogOrReg():
    if FirstTime:
        CreateMasterKey()
    else:
        Authenticate()


def GetOption():
    choice = input("""
        * Welcome to my password manager *
            What do you need ?
            options:

            1. Store a password
            2. Retrieve a password

    \n  [#]  """)
    if choice != "1" and choice != "2":
        print("  [-] Please choose 1 or 2\n\n")
        GetOption()
    else:
        return choice


def StorePass():
    Domain = input("  [?] What is the domain name ? \n     ")
    User = input("  [?] What is the user name ? \n     ")
    Pass = input("  [?] What is the password ? \n     ")

    key = fernet.Fernet.generate_key()
    cipher = fernet.Fernet(key)
    encrypted = cipher.encrypt(Pass.encode())
    hashed = ToSha256(Pass)

    with open("Passwords.csv", "a") as PdFile:
        writer = csv.writer(PdFile, delimiter=":")
        writer.writerow([Domain, User, key, encrypted, hashed])
        PdFile.close()


def RetrievePass():
    found = False
    Domain = input("  [?] What is the domain name of the password ? \n     ")
    with open("Passwords.csv", "r") as PdFile:
        reader = csv.reader(PdFile, delimiter=":")
        for row in reader:
            if row[0] == Domain:
                found = True
                key = row[2]
                encrypted = row[3]
                cipher = fernet.Fernet(eval(key).decode())
                Pass = cipher.decrypt(eval(encrypted).decode())
                print(f"  [*] The password is :  {Pass.decode()}")
        if not found:
            print("  [-] Could not find the specified domain name")


# runtime #

LogOrReg()

option = GetOption()

if option == "1":
    StorePass()
elif option == "2":
    RetrievePass()
