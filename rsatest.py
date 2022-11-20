"""
Copyright Paul Drapeau (2020-2022)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from PIL import Image
import qrcode
import binascii
import base64

doQr = False
debug = False
signPublicKey = True
saveKeys = True

keyPair = RSA.generate(3072)

pubKey = keyPair.publickey()


if debug :
   print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")

pubKeyPEM = pubKey.exportKey()

if saveKeys :
   f = open('mypub.pem','wb')
   f.write(pubKeyPEM)
   f.close()

pubKeyAscii = pubKeyPEM.decode('ascii')
print(pubKeyAscii)

if doQr :
   pubQr = qrcode.QRCode (version=None,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
   pubQr.add_data(pubKeyAscii)
   pubQr.make(fit=True)
   pubImg = pubQr.make_image(fill_color="black", back_color="white")

   pubImg.save("./pubImg.png")

if debug :
   print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")

privKeyPEM = keyPair.exportKey()

if saveKeys :
   f = open('mypriv.pem','wb')
   f.write(privKeyPEM)
   f.close()

privKeyAscii = privKeyPEM.decode('ascii')
print(privKeyAscii)

if doQr :
   privQr = qrcode.QRCode (version=None,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
   privQr.add_data(privKeyAscii)
   privQr.make(fit=True)
   privImg = pubQr.make_image(fill_color="black", back_color="white")
   print(privImg)
   privImg.save("./privImg.png")


if signPublicKey :

#do signature	
   message = pubKeyAscii.encode('utf-8')
   messageHash = SHA256.new(message)
   signature = PKCS1_v1_5.new(keyPair).sign(messageHash)
   signatureBytes = base64.b64encode(signature)
   print(signatureBytes.decode('utf-8'))
#validate signature
   h = SHA256.new(message)
   try:
      PKCS1_v1_5.new(pubKey).verify(h, signature)
      print("The signature is valid.")
   except (ValueError, TypeError):
      print("The signature is not valid.")