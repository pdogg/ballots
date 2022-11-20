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
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime 
import os
import qrcode
import binascii
import hashlib
import random
import base64

numBallots = 5

vote = False  # vote for these ballots
electionKeyFile = "./electionpriv.pem"

def renderBallot(ballotID) :

	fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
	font = ImageFont.truetype(os.path.join(fonts_path, 'regular.ttf'), 30)

	im = Image.new(mode = "RGB", size = (2550,3300), color = (255,255,255))
	draw = ImageDraw.Draw(im)

	ballotimg = Image.open("./blankballot2.png")
	pubqr = Image.open("./pubImg.png")

	draw.text((550, 50),"Ballot: " + ballotID + "  -- Page 1",(255,0,0),font=font)
	im.paste(ballotimg, (250,250))
	im.paste(pubqr, (1100,850))
	im.save("./ballots/" + ballotID + "page1.png")

	im = Image.new(mode = "RGB", size = (2550,3300), color = (255,255,255))
	draw = ImageDraw.Draw(im)


	privqr = Image.open("./privImg.png")

	draw.text((550, 50),"Ballot: " + ballotID + "  -- Page 2",(255,0,0),font=font)
	font = ImageFont.truetype(os.path.join(fonts_path, 'regular.ttf'), 45)
	draw.text((550, 550),"This is your receipt. Please keep it private and in a safe place.",(255,0,0),font=font)

	im.paste(privqr, (450,850))
	im.save("./ballots/" + ballotID + "page2.png")

def generateBallot(election, ballot) :
   
   ballotId = hashlib.sha256((election+str(ballot)).encode('utf-8')).hexdigest()
   print("-----------")
   print("Generating Ballot: " + ballotId.upper())
   
   keyPair = RSA.generate(3072)

   pubKey = keyPair.publickey()
#   print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
   pubKeyPEM = pubKey.exportKey()
   pubKeyAscii = pubKeyPEM.decode('ascii')
   print(pubKeyAscii)

   signPub = signPubKey(pubKeyAscii, electionKeyFile)
   signedPub = pubKeyAscii + signPub

   pubQr = qrcode.QRCode (version=None,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=8,border=4)
   pubQr.add_data(signedPub)
   pubQr.make(fit=True)
   pubImg = pubQr.make_image(fill_color="black", back_color="white")

   pubImg.save("./pubImg.png")

#   print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
   privKeyPEM = keyPair.exportKey()
   privKeyAscii = privKeyPEM.decode('ascii')
   print(privKeyAscii)

   privQr = qrcode.QRCode (version=None,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
   privQr.add_data(privKeyAscii)
   privQr.make(fit=True)
   privImg = privQr.make_image(fill_color="black", back_color="white")
  
   privImg.save("./privImg.png")
   return ballotId.upper(), [privKeyAscii, pubKeyAscii]

def storeVote(voteEnc, key, db) :

   sql = "INSERT INTO VOTES (vote,priv) VALUES ('" + voteEnc + "','" + key +"')"
   return sql

def signBlock(block, key) :
# sign a block of bytes and return base64 signature block
   message = block.encode('utf-8')
   messageHash = SHA256.new(message)
   signature = PKCS1_v1_5.new(key).sign(messageHash)
   signatureBytes = base64.b64encode(signature)
   return signatureBytes.decode('utf-8')

def signPubKey(block, filename) :
# load an election key and sign a ballot PubKey block
   f = open(filename, 'r')
   fileContents = f.read()
   print(fileContents)
   key = RSA.importKey(fileContents)
   return "\n-----BEGIN SIG BLOCK-----\n" + signBlock(block,key) + "\n-----END SIG BLOCK-----"

if __name__ == "__main__":

	election = ("MA_US_2024")

	for x in range(numBallots) :
	   ballotNumber = str(1000 + x) + str(datetime.now())
	   ballotID, ballotStructure = generateBallot(election, ballotNumber)
	   renderBallot(ballotID)
	   print(ballotID)
#	   print(ballotStructure)
	   if vote :
	   	print (storeVote('blahblahvote', ballotStructure[0], 0))


