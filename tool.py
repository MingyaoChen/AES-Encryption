#  tool.py
#  Author: Xiaocong Yang
import random
import sys

#  read the hex format string from file, then padding it to make sure the length is multiple of 16
#  then transform it to binary
#  Params: path of file
#  Return: padded binary string
def getPlaintext(path):
    meta = fileReader(path)
    [padded, padding_size] = padding(meta)
    binaryData = h2b(padded)
    return [binaryData, padding_size]

def getKey(path):
    meta = fileReader(path)
    assert len(meta) == 16
    binaryData = h2b(meta)
    return binaryData

#  get the binary data and trasform it to hex string first, the unPadding it, then write it into file
#  Params: path: path of file
#          data: binary string data
#          padding_size: Integer
def writeData(path, data, padding_size):
    #  hexData = b2h(data)
    data = unPadding(data, padding_size)
    fileWriter(path, "0x" + data)

#  fileReader: read hex format string from file
#  Params: path: string
#  Return: hex format string without 0x
def fileReader(path):
    data = ""
    if path.endswith(".txt"):
        fo = open(path, "r")
        data = fo.read()
        fo.close()
    elif path.endswith(".docx") or path.endswith(".doc"):
        print ' Doc not supported yet'
        # data = ""
        # document = Document(path)
        # for p in document.paragraphs:
        #     data += p.text + "\n"
        # data = data[0:(len(data) - 1)]
    else:
        print "only .txt, .doc, .docx supported"
        sys.exit(0)
    if data.startswith("0x"):
        data = data[2:len(data)]
    return data


#  fileWriter: write data to file
#  Params: path: string,    data: hex format string
def fileWriter(path, data):
    if path.endswith(".txt"):
        fo = open(path, "w")
        fo.write(data)
        fo.close()
    elif path.endswith(".docx") or path.endswith(".doc"):
        print ' Doc not supported yet'
        # document = Documnet(path)
        # document.add_paragraph(data)

#  Padding: The length of encrypted data must be multiple of 8 bytes
#           PKCS5
#  Params: data: hex format string
#  Return: padded data: binary string
#          padding length: integer
def padding(data):
    #  Padding
    padding_size = 0
    if len(data) % 16 != 0:
        tail = len(data) % 16
        padding_size = 16-tail
        for x in xrange(0, padding_size):
            data += '0'
    return [data, padding_size]

#  unPadding: remove the padded element
#  Params: data: hex string
#          padding_len (length in hex): Integer
#  Return: unpadded data: binary string
def unPadding(data, padding_size):
    if padding_size != 0:
        data = data[0: (len(data) - padding_size)]
    return data

#  XOR: Calculate the xor value of two binary string
#  Params type: list of string type bits
#  Return: list of string type bits
def xor(b1, b2):
    #  Check the params 1. length of b1 must the same as b2
    #                   2. Make sure it is binary
    assert len(b1) == len(b2)

    length = len(b1)
    a = map(int, b1)
    b = map(int, b2)
    result = []
    for x in xrange(0, length):
        result.append(str(a[x] ^ b[x]))

    assert len(result) == length
    return result

#  hex to binary: hex to binary
#  Params: hex format string
#  Return: List of bits
def h2b(data):
    result = bin(int(data, 16))[2:].zfill(len(data)*4)
    return list(result)

#  binary to hex: binary to hex
#  Params: data: binary string
#  Return: hex format string
def b2h(data):
    result = "".join(data)
    result = hex(int(result, 2))[2:].zfill(len(data)/4)
    if result.endswith("L"):
        result = result[0:(len(result)-1)]
    return result

# find position in box
def get_Num_box(value):
    switcher ={
       '0':'1','1':'2','2':'3','3':'4','4':'5','5':'6','6':'7','7':'8','8':'9','9':'10','a':'11','b':'12','c':'13','d':'14','e':'15','f':'16'
       }
    return switcher.get(value)

#  Greatest common divisor
def gcd(a, b):
    if b > a:
        return gcd(b, a)

    if a % b == 0:
        return b

    return gcd(b, a % b)

#  IV Generator
def getIV():
    p = 11
    q = 19
    size = 64
    s0 = random.randint(2, 1000)
    while gcd(s0, p) <> 1 or gcd(s0, q) <> 1:
        s0 = random.randint(2, 1000)

    s = []
    iv = []
    s.append(s0)
    iv.append(s0 % 2)
    m = p*q
    for x in xrange(1,size):
        s.append((s[x-1] * s[x-1]) % m)
        iv.append(s[x] % 2)
    iv = map(str, iv)
    return iv
