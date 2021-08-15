
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt(key,plaintext):
    ciphertext=""
    pt = list(plaintext)
    for i in range (len(plaintext)):
        for j in range (len(LETTERS)):
            if plaintext[i]==LETTERS[j]:
                keymod = key%26
                if j+keymod < 26:
                    pt[i] = LETTERS[j+keymod]  # need to handle end letter 
                else:
                    pt[i] = LETTERS[j+keymod-26]
    return ciphertext.join(pt)

def decrypt(key,ciphertext):
    plaintext=""
    ct = list(ciphertext)
    for i in range (len(ciphertext)):
        for j in range (len(LETTERS)):
            if ciphertext[i]==LETTERS[j]:
                keymod = key%26
                if j+keymod > 0:
                    ct[i] = LETTERS[j-keymod]  # need to handle end letter 
                else:
                    ct[i] = LETTERS[j-keymod+26]
    return plaintext.join(ct)


