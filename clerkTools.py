#!/usr/bin/env python3

import os

'''
Possible tools:
    - Folder Maker
    - Citation Mover
    - Citation Folder Checker (See if there are any non-existent names or folders that just do not belong)
        - Ability to 'exclude' folders from checker, similar to a gitignore file.
'''

def folderMaker():
    '''
    Make a set of folders based off of user input
    '''
    folders = []
    print("Please enter the folder names you wish to create. When finished press enter twice.")

    # Ask for names, append to folders list. If none given, break loop.
    while True:
        inp = input()

        if inp != "":
            folders.append(inp)
        else:
            break

    print(
        f"The current directory the folders will be created is: {os.getcwd()}\n If this is correct, press Enter. If it is not, type in the absolute path below:")
    inp = input()

    # Use current working directory if custom path not given.
    path = os.getcwd() if inp == "" else inp

    # Make folders
    for f in folders:
        os.mkdir(f"{path}/{f}")

    print("Folders created.")


if __name__ == "__main__":
    folderMaker()
