This Elgamal.py is just EllipticalCurve.py with extra methods.

To use this program:
  First get a key file:
    run elgamal_generate_keys()
  Second to encrypt a file with the keys:
    run encrypt_with_keys()
  Third to decrypt with your key file:
    run decrypt_with_keys()

encrypt_with_keys outputs a cipher text file where each line
is formated as such:
   {Cipher},{Half_Mask}
	...
	...
   {Cipher},{Half_Mask}
   Note the Half_Mask is g^b
   The File is named SecretCipher.txt

Epub.keys is formatted as such:
	p = {prime}
	g = {generator}
	g^a = {half_mask}
	a = {Decryption secret}

