import base64
import os
from hashlib import sha256


alphanumeric = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ -"

enc_dict = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=}{[]|':;<>.?"

alphanumeric_list = [i for i in alphanumeric]

def checkEncryption(username,password):
    newStr = "{}{}".format(username,password)
    h = sha256()
    h.update(bytes(newStr,'utf-8'))
    hash = h.hexdigest()
    with open("data.csai",'r')as fp:
        data = fp.read()
    data = data.split("\n")[0]
    if data == hash:
        return True
    else:
        return False

def decrypt(ciphertext, key):
    plaintext = ""
    list_ciphertext = [i for i in ciphertext]
    list_key = [i for i in key]
    j=0
    for i in range(len(list_ciphertext)):
        e = alphanumeric_list.index(list_ciphertext[i])-alphanumeric_list.index(list_key[j])
        e = e%len(alphanumeric_list)
        e = alphanumeric_list[e]
        plaintext+=e
        j+=1
        if j>=len(list_key):
            j=0
    return plaintext

def encrypt(plaintext, key):
    ciphertext = ""
    list_plaintext = [i for i in plaintext]
    try:
        list_plaintext.remove('\r')
        list_plaintext.remove('\r')
    except:
        pass
    list_key = [i for i in key]
    j=0
    for i in range(len(list_plaintext)):
        e = alphanumeric_list.index(list_plaintext[i])+alphanumeric_list.index(list_key[j])
        e = e%len(alphanumeric_list)
        e = alphanumeric_list[e]
        ciphertext+=e
        j+=1
        if j>=len(list_key):
            j=0
    return ciphertext

