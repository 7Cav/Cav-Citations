#!/usr/bin/env python3

import json
import textwrap

from PIL import Image, ImageDraw, ImageFont


def assembleCitation(citationName, nameText, dateText, dateNumber, citationText=False, saveFolder=False):
    '''
    Assemble a citation using given parameters.
    Inputs:
        citationName (str): Name of the citation in medals.json (Ex: "POW")
        nameText (str): Trooper name to appear on citation.
        dateText (str): Text of date given on citation.
        dateNumber (int): Date used when saving file (Ex: 200205)
        citationText (str) [OPTIONAL]: Text used for citation.
        saveFolder (str) [OPTIONAL]: What folder you want citaion saved in.
            If none given, saves to working directory.

    Because OOP doesn't play nice with PIL I'm forced to do this from a functional
     programming perspective. It's thrown together and may look like shit. But let's
     hope this trainwreck makes it to the station.
    '''

    # Open JSON and load config for that medal.
    with open("medals.json", "r") as file:
        global config
        config = json.load(file)[citationName]

    # Open file and initial config.
    img = Image.open(config["templateFile"])
    draw = ImageDraw.Draw(img)

    def writeText(confName, text):
        nonlocal img, draw
        c = config[confName]
        x, y = c["pos"]
        font = ImageFont.truetype(c["fontName"], c["fontSize"])
        
        cWrap = c["wrap"]
        if cWrap == False: # Single line.
            w, h = draw.textsize(text, font=font)
            draw.text(
                (x-(w/2), y-(h/2)), 
                text, 
                (0,0,0), 
                font=font
            )
        else: # Multi line.
            if cWrap["newline"] == True:
                lines = text.split("\n")
            else:
                lines = textwrap.TextWrapper(width=cWrap["charLimit"], break_on_hyphens=True).wrap(text)
                # lines = textwrap.wrap(text, width=cWrap["charLimit"])
            
            current_h, pad = y, 1
            for line in lines:
                w, h = draw.textsize(line, font=font)
                draw.text(((x-w/2), current_h), line,(0,0,0), font=font)
                current_h += h + pad

    # Name
    writeText("name", nameText)
    # Citation
    if citationText != False:
        writeText("citation", citationText)
    # Date
    writeText("date", dateText)


    # Save the file
    fileName = f"{citationName}-{str(dateNumber)}.jpeg"
    img.save(fileName)
    print(f"{fileName} saved.")

if __name__ == "__main__":
    assembleCitation(
        citationName="POW",
        nameText="Corporal Joshua Bell",
        dateText="Given under my hand on the \n 8th Day of November 2094",
        dateNumber=941108
    )