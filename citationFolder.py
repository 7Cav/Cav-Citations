#!/usr/bin/env python3

import json
import os

from milpacScraper import roster

class folderNameTools:
    def getAllFolders(self, fullPath=False):
        '''
        Get a list of all folders in the citation directory. FUNCTION MUST BE RUNNED USING A LINUX TERMINAL.

        Inputs:
            fullPath (bool) [OPTIONAL]: If true, show the full path to each folder, else just list folder names.
                Default: False
        Output (list): All folders within the citation directory.
        '''
        citationFolder = "/mnt/c/Users/Joshua/ownCloud/S1 Department/1 - Citations"
        if fullPath == True:
            [f"{citationFolder}/{name}" for name in os.listdir(citationFolder) if os.path.isdir(os.path.join(citationFolder, name))]
        else:
            return [name for name in os.listdir(citationFolder) if os.path.isdir(os.path.join(citationFolder, name))]

    def trooperFolderNames(self):
        '''
        Gets parsed folder names for all troopers in milpacs.

        Output (list): All trooper folder names parsed from Milpacs.
        '''
        with open("ranks.json", "r") as file:
            rankConfig = json.load(file)

        def parseFolderName(fullName, rankPicture):
            '''
            Takes a troopers name and rank picture and strips the rank from
            the name and generated approximate folder name. Folder name format is: last-first-middle

            Inputs:
                fullName (str): Trooper's full name with rank.
                rankPicture (str): URL for the trooper's rank image.
            Output (str): Folder name
            '''
            nonlocal rankConfig
            fullName = fullName.lower() # Make name all lowercase, because reasons.

            rankLength = len([r["long"] for r in rankConfig if r["milpacImage"] == rankPicture][0]) # Grab rank from pic and get string length of rank.
            name = fullName[rankLength+1:].split(" ") # Chop off the rank and following space, split name (without rank) into list.
            return "-".join([name[-1]] + name[:-1]) # Return folder name string using proper folder name format.

        return [parseFolderName(i[2], i[1]) for i in roster().scrapeAllRosters()]

    def checkFolders(self):
        '''
        Checks citations folder list for folders that don't belong.
        '''
        trooperFolders = self.trooperFolderNames()
        citationFolders = self.getAllFolders()

        errorFolders = [f for f in citationFolders if f not in trooperFolders] # Which folders do not have a coorelating trooper in milpacs.
        with open("errorFolders.txt", "w") as file:
            for f in errorFolders:
                file.write(f"{f}\n")

        print(f"{len(errorFolders)}/{len(citationFolders)} folders found in error!")

        troopersMissingFolder = [f for f in trooperFolders if f not in citationFolders] # Trooper's that do not have a citation folder.
        with open("troopersMissingFolder.txt", "w") as file:
            for f in troopersMissingFolder:
                file.write(f"{f}\n")

        print(f"{len(troopersMissingFolder)}/{len(trooperFolders)} troopers found without a folder!")


if __name__ == "__main__":
    folderNameTools().checkFolders()