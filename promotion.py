#!/usr/bin/env python3

import json
from PIL import Image, ImageDraw, ImageFont
import datetime
import os

# Promotion citaiton maker


'''
Date keys:
    %d: Date w/ ordinal indicator, lowercase (Ex: 17th).
    %D: Date w/ ordinal indicator, UPPERCASE (Ex: 17TH).
    %m: Full month, lowercase (Ex: January).
    %M: Full month, UPPERCASE (Ex: JANUARY).
    %y: Full year (Ex: 2020).

'''

def ordinalIndicator(num):
    '''
    Take number and output string w/ ordinal indicator attached
    Inputs:
        num (int): Number to be formatted
    Output (str): number with ordinal indicator (Ex: 17th)
    '''
    if int(num) in range(11, 20): # If a 'teen' number. (11, 12, 13, ...)
        return f"{int(num)}th"
    elif str(num)[-1] == "1": # If number ends in "1"
        return f"{int(num)}st"
    elif str(num)[-1] == "2": # If number ends in "2"
        return f"{int(num)}nd"
    elif str(num)[-1] == "3": # If number ends in "3"
        return f"{int(num)}rd"
    else:
        return f"{int(num)}th"
    

def rankCitation(rank, name, date, saveFolder=False):
    '''
    Assemble a citation using given parameters.
    Inputs:
        rank (str): Rank of citation (Ex: PFC).
        name (str): Name on citation (Ex: Kyle Bell).
        date (int): Date of citation in filename format. (Ex: 21 January 2019 would be 190121) 
        saveFolder (str) [OPTIONAL]: What folder you want the citation saved in.
            If none given, saves to working directory.
    '''
    assert isinstance(date, str), f"Date needs to be a string. Current {type(date)}"

    # Open JSON and load config for that medal.
    with open("ranks.json", "r") as file:
        config = [i for i in json.load(file) if i["short"] == rank][0]["citation"]

    # Open file and initial config.
    img = Image.open(config["templateFile"])
    draw = ImageDraw.Draw(img)

    def writeText(confName, text):
        nonlocal img, draw, config
        c = config[confName]
        x, y = c["pos"]
        font = ImageFont.truetype(c["fontName"], c["fontSize"])
        
        w, h = draw.textsize(text, font=font)
        draw.text(
            (x-(w/2), y-(h/2)), 
            text, 
            (0,0,0), 
            font=font
        )

    # Write name
    writeText("name", name if config["name"]["caps"] == False else name.upper())
    
    # Handle dateText formating
    dt = datetime.date(int(date[0:2]), int(date[2:4]), int(date[5:6]))
    dateReplace = [
        ["[d]", ordinalIndicator(dt.strftime("%d"))],
        ["[D]", ordinalIndicator(dt.strftime("%d")).upper()],
        ["[m]", dt.strftime("%B")],
        ["[M]", dt.strftime("%B").upper()],
        ["[y]", f"20{date[0:2]}"]
    ]
    dateText = config["date"]["dateText"]
    for r in dateReplace:
        dateText = dateText.replace(r[0], r[1])
    
    # Write date
    writeText("date", dateText)

    # Save the file
    os.makedirs(f"generatedCitations/{saveFolder}") if saveFolder is not False else None
    fileName = config["outFile"] + f"-{date}.jpeg"
    fileName = f"generatedCitations/{saveFolder}/{fileName}" if saveFolder is not False else fileName
    img.save(fileName)
    print(f"{fileName} saved.")


if __name__ == "__main__":
    cont = True
    while cont == True:
        name = input("Trooper Name: ")
        folderName = input("Trooper's Folder Name: ")
        rank = input("Rank: ").upper()
        date = str(input("Date (yymmdd): "))
        rankCitation(rank, name, date, folderName)
        if str(input("Again? (y/n): ")).lower() == "n":
            break
    print("Finished.")

