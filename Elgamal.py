import random
import os
def gcd(a,b):
    #Super fast super good
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

def egcd(a,b):
    #
    # Extended Euclidean Algorithm
    # returns x, y, gcd(a,b) such that ax + by = gcd(a,b)
    #

    #initialize our x vals
    u, u1 = 1, 0
    #initialize our y vals
    v, v1 = 0, 1

    #keep going until we get a remainder of 0
    while b:
        #get our integer quotient 
        q = a // b
        #update our x and y vals
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        #replace a with b and b with a%b
        a, b = b, a - q * b
    return u, v, a

def isprime(n):
    #check if n is prime
    #pick 'a' such that 'a' is an element of {2,..,n-1} 100 times
    # probably too much checking  ¯\_(ツ)_/¯
    for q in range(100):
        #slick lets pick a random a in our range
        a = random.randint(2,n-1)
        #even slicker is if this fn evaluates to 1
        if pow(a, n - 1, n) != 1:
            #awman tfw not prime
            return 0


    #good enough this is probably prime
    return 1

#I wanted threads and this is what I had to do
#    Deal
#Wi
#   th     i
#          t
def prime_maker(n_bits):
    padder = 1 << n_bits - 1
    p = random.getrandbits(n_bits)

    # p might not have n bits so we just want to make sure the most signigicant bit is a 1
    # bit-wiseOR p with (1 << n_bits - 1)
    # bit-wiseOR p with 1 to ensure oddness 
    p = p | padder
    p = p | 1

    #keep generating primes until we win
    while not isprime(p):
        p = random.getrandbits(n_bits)
        # p might not have n bits so we just want to make sure the most signigicant bit is a 1
        # bit-wiseOR p with (1 << n_bits - 1)
        # bit-wiseOR p with 1
        p = p | padder
        p = p | 1
    return p

#Assumptions p = 3 mod 4
# g^1 == 1 not generator
# g^2 == 1 not generator
# g^q == 1 not generator
def gen_check(g, p):
    #print(p)
    if pow(g, 1 ,p) == 1:
        return 0
    if pow(g,2,p) == 1:
        return 0

    q = (p-1)//2
    if pow(g, q, p) == 1:
        return 0
    #Generator
    return 1

def elgamal_generate_keys():
    #if os.path.isfile('Epub.keys'):
    #    return 1
    #generate p
    #p = 3 mod 4
    p = prime_maker(128)
    while p % 4 == 1:
        p = prime_maker(128)

    #find a g in p
    g = random.randint(1, p-1)
    while not gen_check(g,p):
        g = random.randint(1, p-1)
    #generate my secretf
    a = random.getrandbits(128)

    #generate my public half
    g_a = pow(g,a,p)
    '''
    #make pub key file (Epub.keys)
    nfile = open('Epub.keys', 'w')
    
    
    nfile.write("p = " + str(p) + '\n')

    line = ('g = ' + str(g)+ '\n')
    nfile.write(line)
    line = ('g^a = ' + str(g_a)+ '\n')
    nfile.write(line)
    line = ('a = ' + str(a)+ '\n')
    nfile.write(line)
    '''
    return (p,g,a,g_a)

def encrypt_with_keys():
    #parse file and get values 
    nfile = open('Epub.keys', 'r')
    # p, g, g^a, a
    vals = []
    for x in nfile:
        x = x.split('=')
        val = x[1]
        val.replace('\n','')
        val.replace(' ','')
        vals.append(int(val))
    print(vals)
    p = vals[0]
    g = vals[1]
    g_a = vals[2]
    #generate secret b value
    #generate my secretf
    b = random.getrandbits(128)

    #generate my public half
    g_b = pow(g,b,p)

    #generate the full mask
    f = pow(g_a,b,p)

    nfile = open('Assignment4_5.txt','r')
    wfile = open('SecretCipher.txt','w')
    for x in nfile:
        for y in x:
            val = ord(y)
            cipher = (f * val) % p
            #write cipher,half_mask
            wfile.write(str(cipher) + ',' + str(g_b) + '\n')
            #generate new b, half mask and full mask
            b = random.getrandbits(128)

            #generate my public half
            g_b = pow(g,b,p)

            #generate the full mask
            f = pow(g_a,b,p)

def decrypt_with_keys():
    #parse file and get values 
    nfile = open('Epub.keys', 'r')
    # p, g, g^a, a
    vals = []
    for x in nfile:
        x = x.split('=')
        val = x[1]
        val.replace('\n','')
        val.replace(' ','')
        vals.append(int(val))
    print(vals)
    p = vals[0]
    g = vals[1]
    g_a = vals[2]
    a = vals[3]
    b = a
    Prime = p
    res = ''
    encrypted = open('SecretCipher.txt','r')
    ciphers = []
    for x in encrypted:
        x.replace('\n','')
        x.replace(' ', '')
        x = x.split(',')
        ciphers.append((int(x[0]),int(x[1])))

    for x in ciphers:
        cipher = x[0]
        half_mask = x[1]
        full_mask = pow(half_mask, b, Prime)
        neg_full_mask = egcd(Prime, full_mask)[1]
        message = (cipher * neg_full_mask) % Prime
        res = res + chr(message)
    #print(res)
    meh = open('Decrypted.txt', 'w')
    meh.write(res)

if __name__ == '__main__':
    elgamal_generate_keys()
    encrypt_with_keys()
    decrypt_with_keys()