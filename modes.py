import sys
import aes as aes
import tool as tl
import time

def encryptionECB(key,plaintext):
	result = ""
	if (len(plaintext)%64 <> 0):
		sys.exit(0)
	#  AES
	for x in xrange(0, (len(plaintext)/64)):
		cipher = aes.encryption(key, plaintext[(x*64):(x*64+64)])
		result += cipher
	#  need to transformed to ASCII before write
	return result

def decryptionECB(key, ciphertext):
	cipher = tl.h2b(ciphertext[0])
	result = ""
	for x in xrange(0, (len(cipher)/64)):
		result += aes.decryption(key, cipher[(x*64):(x*64+64)])

	result = tl.unPadding(result, ciphertext[1])
	return result

def encryptionCBC(key,plaintext,iv):
	count = len(plaintext)/64
	cipher = ''
	for i in xrange(0,count,1):
		plain = tl.xor(plaintext[i*64:(i*64)+64],iv)

		c = aes.encryption(key,plain)
		cipher += c
		iv = tl.h2b(c)
	return cipher

def decryptionCBC(key,ciphertext,iv):
	hexCipher = tl.h2b(ciphertext[0])

	count = len(tl.h2b(ciphertext[0]))/64

	plain = ''
	for i in xrange(0,count,1):
		c = tl.h2b(aes.decryption(key,hexCipher[i*64:(i*64)+64]))

		p = tl.b2h(tl.xor(c,iv))
		iv = hexCipher[i*64:(i*64)+64]

		plain += p
	plain = tl.unPadding(plain, ciphertext[1])
	return plain

def encryptionOFB(iv, key, plaintext):
	biPlain = plaintext
	count = len(plaintext)/64
	cipher = []
	for i in xrange(0,count,1):
		iv = tl.h2b(aes.encryption(key, iv))
		biP = biPlain[i*64:(i*64)+64]
		cipher += tl.xor(iv, biP)
	cipherStr = tl.b2h(cipher)
	return cipherStr


def decryptionOFB(iv, key, ciphertext,padding_size):
	biCipher = ciphertext
	count = len(biCipher)/64
	plain = []
	for i in xrange(0,count,1):
		iv = tl.h2b(aes.encryption(key, iv))
		biC = ciphertext[i*64:(i*64)+64]
		plain += tl.xor(iv, biC)
	plainStr = tl.b2h(plain)
	plainStr = tl.unPadding(plainStr,padding_size)
	return plainStr

def encryptionCFB(key,plaintext,iv):
	count = len(plaintext)/64
	cipher = ''

	for i in xrange(0,count,1):
		key_plain = tl.h2b(aes.encryption(key,iv))
		c = tl.b2h(tl.xor(key_plain,plaintext[i*64:(i*64)+64]))
		cipher += c
		iv = tl.h2b(c)
	return cipher

def decryptionCFB(key,ciphertext,iv):
	hexCipher = tl.h2b(ciphertext[0])
	count = len(tl.h2b(ciphertext[0]))/64
	plain = ''
	for i in xrange(0,count,1):

		key_plain = tl.h2b(aes.encryption(key,iv))

		p = tl.b2h(tl.xor(key_plain,hexCipher[i*64:(i*64)+64]))
		iv = hexCipher[i*64:(i*64)+64]
		plain += p
	plain = tl.unPadding(plain, ciphertext[1])
	return plain

def readCounter(path):
    meta = tl.fileReader(path)
    binaryData = tl.h2b(meta)
    return binaryData

def getCounter(original_Counter,count,key):
    encryCounter_List =[]
    counter = int(original_Counter,16)
    for i in xrange(0,count,1):
        counter=counter + i
        counter_binary=bin(counter)[2:].zfill(len(original_Counter)*4)
        encryCounter = aes.encryption(key,tl.h2b(tl.b2h(counter_binary)))
        encryCounter_List.append(encryCounter)
    return encryCounter_List

def encryptionCTR(key,plaintext,original_Counter):
    count = len(plaintext)/64
    cipher = ''
    hexPlain = tl.b2h(plaintext)
    encryCounter_List = getCounter(tl.b2h(original_Counter),count,key)
    for i in xrange(0,count,1):
        cipher+= str(tl.b2h(tl.xor(tl.h2b(encryCounter_List[i]),tl.h2b(hexPlain[i*16:(i*16)+16]))))
    return cipher

def decryptionCTR(key,ciphertext,original_Counter,padding_size):
    count = len(ciphertext)/16
    plain=''
    encryCounter_List = getCounter(tl.b2h(original_Counter),count,key)
    for i in xrange(0,count,1):
        plain+= str(tl.b2h(tl.xor(tl.h2b(encryCounter_List[i]),tl.h2b(ciphertext[i*16:(i*16)+16]))))
    plain = tl.unPadding(plain,padding_size) 
    return plain

def main():
	print "1: ECB"
	print "2: CBC"
	print "3: OFB"
	print "4: CFB"
	print "5: CTR"
	tmp = raw_input('-->')

	[plaintext, padding_size] = tl.getPlaintext('./original.txt')
	roundKey = tl.getKey("./key.txt")
	iv = tl.getIV()

	userInput = int(tmp)
	ciphertext = ""
	resulttext = ""

	if userInput == 1:
		# Encryption process of ECB
		start1 = time.time()
		ciphertext = [encryptionECB(roundKey,plaintext), padding_size]
		end1 = time.time()
		print "encryption time: " + str(end1 - start1)

		start2 = time.time()
		resulttext = decryptionECB(roundKey,ciphertext)
		end2 = time.time()
		print "decryption time: " + str(end2 - start2)
	elif userInput == 2:
		# Encryption process of CBC
		start1 = time.time()
		ciphertext = [encryptionCBC(roundKey,plaintext,iv),padding_size]
		end1 = time.time()
		print "encryption time: " + str(end1 - start1)

		start2 = time.time()
		resulttext = decryptionCBC(roundKey,ciphertext,iv)
		end2 = time.time()
		print "decryption time: " + str(end2 - start2)
	elif userInput == 3:
		# Encryption process of OFB
		start1 = time.time()
		ciphertext = [encryptionOFB(iv, roundKey, plaintext), padding_size]
		end1 = time.time()
		print "encryption time: " + str(end1 - start1)

		start2 = time.time()
		resulttext = decryptionOFB(iv, roundKey, tl.h2b(ciphertext[0]), padding_size)
		end2 = time.time()
		print "decryption time: " + str(end2 - start2)
	elif userInput == 4:
		# Encryption process of CFB
		start1 = time.time()
		ciphertext = [encryptionCFB(roundKey,plaintext,iv),padding_size]
		end1 = time.time()
		print "encryption time: " + str(end1 - start1)

		start2 = time.time()
		resulttext = decryptionCFB(roundKey,ciphertext,iv)
		end2 = time.time()
		print "decryption time: " + str(end2 - start2)
	elif userInput == 5:
		# Encryption process of CTR
		Counter = readCounter("./counter.txt")
		start1 = time.time()
		ciphertext = [encryptionCTR(roundKey,plaintext,Counter), padding_size]
		end1 = time.time()
		print "encryption time: " + str(end1 - start1)

		start2 = time.time()
		resulttext = decryptionCTR(roundKey,ciphertext[0],Counter,padding_size)
		end2 = time.time()
		print "decryption time: " + str(end2 - start2)
	else:
		print "Wrong Input"
		sys.exit(0)

	tl.writeData('./cipher.txt', ciphertext[0], padding_size)
	print resulttext
	


if __name__ == '__main__':
	main()
