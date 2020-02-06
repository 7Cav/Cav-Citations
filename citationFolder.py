#!/usr/bin/env python3

# Tools for auditing the citation folder.
import os
import milpacScraper
from datetime import datetime
import csv


def getAllFolders():
    theDir = input("Feed me directory: ")
    folders = [name for name in os.listdir(theDir) if os.path.isdir(os.path.join(theDir, name))]
    fullPathFolders = [f"{theDir}\\{name}" for name in folders]
    lastMod = [datetime.utcfromtimestamp(os.path.getmtime(folder)).strftime('%Y-%m-%d %H:%M:%S') for folder in fullPathFolders]

    # print(zip(folders, lastMod))

    import csv

    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(list(zip(folders, lastMod)))
        
        # print(lastMod)

def getAllMilpacs():
    # Gets all milpac names. From all rosters
    pass

def getAllGhettopacks():
    # Gets all Ghettopacks names.
    pass

if __name__ == "__main__":
    getAllFolders()