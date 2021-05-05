import os
import shutil
from zipfile import ZipFile
from pyfiglet import Figlet


def listMainDir(dir):
    folders = []
    files = os.listdir(dir)
    for file in files:
        if os.path.isdir(dir + "/" + file):
            folders.append(dir + "/" + file)
    return folders

def cleanJsonFromDir(dir):
    files = os.listdir(dir)
    for file in files:
        if file.endswith(".json") or file.endswith(".DS_Store"):
            print("Deleting: " + dir + "/" + file)
            os.remove(dir + "/" + file)
        else:
            files2 = os.listdir(dir + "/" + file)
            for file2 in files2:
                if file2.endswith(".json"):
                    print("Deleting: " + dir + "/" + file + "/" + file2)
                    os.remove(dir + "/" + file + "/" + file2)

def moveFilesToFinalDir(inputdir, outputdir):
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    else:
        print("Copying")
        files = os.listdir(inputdir)
        for file in files:
            if os.path.isdir(inputdir + "/" + file):
                if not os.path.exists(outputdir + "/" + file):
                    print("Create directory: " + outputdir + "/" + file)
                    os.mkdir(outputdir + "/" + file)
                images = os.listdir(inputdir + "/" + file)
                for image in images:
                    print("Moving " + inputdir + "/" + file + "/" + image + " to " + outputdir + "/" + file)
                    shutil.move(inputdir + "/" + file + "/" + image, outputdir + "/" + file+ "/" + image)
                    #shutil.copyfile(inputdir + "/" + file + "/" + image, outputdir + "/" + file+ "/" + image)

def extractAllFiles(inputdir, outputdir):
    dirNumber = 0
    print("Extracting")
    zipfiles = os.listdir(inputdir)
    for zipfile in zipfiles:
        if zipfile.endswith(".zip"):
            print("Extracting " + inputdir + "/" + zipfile + " to " + inputdir + "/" + str(dirNumber))
            with ZipFile(inputdir + "/" + zipfile, 'r') as zipObj:
                zipObj.extractall(inputdir + "/" + str(dirNumber))
            print("Moving " + inputdir + "/" + str(dirNumber) + "/Takeout/Google Photos/* to "+ inputdir + "/" + str(dirNumber))
            os.system("mv " + inputdir + "/" + str(dirNumber) + "/Takeout/Google\ Photos/* " + inputdir + "/" + str(dirNumber))
            os.system("rm -r " + inputdir + "/" + str(dirNumber) + "/Takeout")
            dirNumber += 1

def printBanner():
    banner = Figlet(font='bubble')
    print(banner.renderText('GooglePhotos Importer'))
    print("------")


if __name__ == "__main__":
    OUTPUTDIR = "./output"
    INPUTDIR = "./photos"

    printBanner()

    #Extract the original zipfiles
    extractAllFiles(INPUTDIR, INPUTDIR)

    #List the top directories
    folders = listMainDir(INPUTDIR)
    print(folders)

    #For each directory, clean the JSON files
    for folder in folders:
        cleanJsonFromDir(folder)

    #Move the directories and images to the final output directories
    for folder in folders:
        moveFilesToFinalDir(folder, OUTPUTDIR)
