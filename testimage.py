"""
Copyright Paul Drapeau (2020-2022)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os

fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
font = ImageFont.truetype(os.path.join(fonts_path, 'regular.ttf'), 30)

im = Image.new(mode = "RGB", size = (2550,3300), color = (255,255,255))
draw = ImageDraw.Draw(im)

ballotimg = Image.open("./blankballot2.png")
pubqr = Image.open("./pubImg.png")

draw.text((550, 50),"Ballot: 8D16A2666B971DE353542A1E520A9954A9259BB32CD08E5B534BC7AF14A788C7  -- Page 1",(255,0,0),font=font)
im.paste(ballotimg, (250,250))
im.paste(pubqr, (1100,850))
im.save("./testballotpage1.png")

im = Image.new(mode = "RGB", size = (2550,3300), color = (255,255,255))
draw = ImageDraw.Draw(im)


privqr = Image.open("./privImg.png")

draw.text((550, 50),"Ballot: 8D16A2666B971DE353542A1E520A9954A9259BB32CD08E5B534BC7AF14A788C7  -- Page 2",(255,0,0),font=font)
font = ImageFont.truetype(os.path.join(fonts_path, 'regular.ttf'), 45)
draw.text((550, 550),"This is your receipt. Please keep it private and in a safe place.",(255,0,0),font=font)

im.paste(privqr, (550,850))
im.save("./testballotpage2.png")